#!/usr/bin/env python3
"""Check the WAN reference configs and a small static forwarding model.

This is NOT an IOS emulator. It does not run OSPF, NAT sessions, HTTP or timers.
It reads the supplied interface/static-route/ACL/PBR/track declarations and checks
the shared Internet paths under link faults. Runtime test statuses stay NOT RUN.
"""
from collections import defaultdict
from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WEB = IPv4Address('192.0.2.100')


@dataclass
class Route:
    net: IPv4Network
    hop: str | None = None
    interface: str | None = None
    distance: int = 1
    track: str | None = None


@dataclass
class Node:
    name: str
    text: str
    interfaces: dict = field(default_factory=dict)
    blocks: dict = field(default_factory=dict)
    routes: list = field(default_factory=list)
    acls: dict = field(default_factory=lambda: defaultdict(list))


def network(address, mask):
    return IPv4Network(f'{address}/{mask}', strict=False)


def acl_address(tokens):
    token = tokens.pop(0)
    if token == 'any':
        return IPv4Network('0.0.0.0/0')
    if token == 'host':
        return IPv4Network(tokens.pop(0) + '/32')
    wildcard = IPv4Address(tokens.pop(0))
    mask = IPv4Address(int(wildcard) ^ 0xffffffff)
    return network(token, str(mask))


def load_node(path):
    text = path.read_text(encoding='utf-8')
    names = re.findall(r'^hostname (\S+)$', text, re.M)
    assert len(names) == 1, f'{path}: load exactly one node per file'
    node = Node(names[0], text)
    block = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('!'):
            continue
        if not raw.startswith(' '):
            block = line
            node.blocks[block] = []
        else:
            node.blocks[block].append(line)
        if raw.startswith(' ') and block.startswith('interface ') and line.startswith('ip address '):
            _, _, ip, mask = line.split()
            node.interfaces[block.split()[1]] = IPv4Interface(f'{ip}/{mask}')
        if line.startswith('ip route '):
            tokens = line.split()[2:]
            route = Route(network(tokens.pop(0), tokens.pop(0)))
            if not re.match(r'^\d+\.', tokens[0]):
                route.interface = tokens.pop(0)
            if tokens and re.match(r'^\d+\.', tokens[0]):
                route.hop = tokens.pop(0)
            if tokens and tokens[0].isdigit():
                route.distance = int(tokens.pop(0))
            if tokens:
                assert tokens.pop(0) == 'track' and len(tokens) == 1, line
                route.track = tokens.pop(0)
            node.routes.append(route)
        if line.startswith('access-list '):
            tokens = line.split()[1:]
            number, action, protocol = tokens.pop(0), tokens.pop(0), tokens.pop(0)
            assert protocol == 'ip', f'ACL protocol outside checker scope: {line}'
            source, dest = acl_address(tokens), acl_address(tokens)
            assert not tokens, line
            node.acls[number].append((action, source, dest))
    return node


def permitted(node, acl, source, dest):
    for action, srcnet, dstnet in node.acls[acl]:
        if source in srcnet and dest in dstnet:
            return action == 'permit'
    return False


def active_routes(node, tracks, disabled):
    result = []
    for name, addr in node.interfaces.items():
        if addr.network not in disabled:
            result.append(Route(addr.network, interface=name, distance=0))
    for route in node.routes:
        if route.track and not tracks.get((node.name, route.track), False):
            continue
        if route.interface and route.interface != 'Null0':
            if node.interfaces[route.interface].network in disabled:
                continue
        result.append(route)
    return result


def neighbors(node, hop, disabled):
    address = IPv4Address(hop)
    return [addr for addr in node.interfaces.values()
            if address in addr.network and addr.network not in disabled]


def pbr_hop(node, source, dest, tracks, disabled):
    entries = sorted((int(key.split()[-1]), lines)
                     for key, lines in node.blocks.items()
                     if key.startswith('route-map LOAD-BALANCE-PBR permit '))
    for _, lines in entries:
        acl = next(line.split()[-1] for line in lines if line.startswith('match ip address '))
        if not permitted(node, acl, source, dest):
            continue
        hops = []
        for line in lines:
            if line.startswith('set ip next-hop verify-availability '):
                tokens = line.split()
                hops.append((int(tokens[5]), tokens[4], tokens[7]))
        for _, hop, track in sorted(hops):
            if tracks.get((node.name, track), False) and neighbors(node, hop, disabled):
                return hop
        return None  # permit without set, or no usable next-hop: use the RIB
    return None


def paths(nodes, name, dest, tracks, disabled, source=None, seen=()):
    if name in seen:
        raise AssertionError(f'Forwarding loop to {dest}: {seen + (name,)}')
    seen = seen + (name,)
    node = nodes[name]
    for addr in node.interfaces.values():
        if addr.ip == dest and addr.network not in disabled:
            return [seen]
    hop = None
    if name == 'Main-Edge' and source is not None:
        hop = pbr_hop(node, source, dest, tracks, disabled)
    if hop:
        choices = [Route(IPv4Network('0.0.0.0/0'), hop=hop)]
    else:
        choices = [r for r in active_routes(node, tracks, disabled) if dest in r.net]
        if not choices:
            return []
        best = min((-r.net.prefixlen, r.distance) for r in choices)
        choices = [r for r in choices if (-r.net.prefixlen, r.distance) == best]
    result = []
    for route in choices:
        if route.interface == 'Null0':
            continue
        if route.hop:
            if not neighbors(node, route.hop, disabled):
                continue
            owners = [other.name for other in nodes.values()
                      if other.name != name and any(str(a.ip) == route.hop
                                                   for a in other.interfaces.values())]
            for owner in owners:
                result.extend(paths(nodes, owner, dest, tracks, disabled, source, seen))
        else:
            # Connected subnet: deliver to a modeled router or to the Web host.
            owners = [other.name for other in nodes.values() if other.name != name
                      and any(a.ip == dest for a in other.interfaces.values())]
            if owners:
                for owner in owners:
                    result.extend(paths(nodes, owner, dest, tracks, disabled, source, seen))
            elif dest == WEB:
                result.append(seen)
    return result


def has_default(node, tracks, disabled):
    return any(r.net.prefixlen == 0 for r in active_routes(node, tracks, disabled))


def check_scenario(nodes, label, off, expected, web_up=True):
    disabled = {IPv4Network(net) for net in off}
    tracks = {}
    edge = nodes['Main-Edge']
    for number, target, public in [('1', '192.0.2.11', '203.0.113.2'),
                                   ('2', '192.0.2.22', '198.51.100.2')]:
        tracks[('Main-Edge', number)] = bool(
            paths(nodes, 'Main-Edge', IPv4Address(target), tracks, disabled)
            and paths(nodes, 'INET-Core', IPv4Address(public), tracks, disabled))
    assert tuple(tracks[('Main-Edge', n)] for n in ('1', '2')) == expected, label
    assert has_default(edge, tracks, disabled) == any(expected), label
    for name in ('Main-Core', 'Main-GW'):
        source = nodes[name].interfaces['Loopback0'].ip
        outbound = paths(nodes, name, WEB, tracks, disabled, source)
        tracks[(name, '10')] = bool(outbound) and web_up
        assert tracks[(name, '10')] == (any(expected) and web_up), (label, name)
        assert has_default(nodes[name], tracks, disabled) == tracks[(name, '10')], label
        assert any(r.net == IPv4Network('192.0.2.100/32') and r.hop
                   for r in active_routes(nodes[name], tracks, disabled)), label
    for source_text, preferred in [('10.10.10.10', 1), ('10.10.20.10', 2),
                                   ('10.20.10.10', 1), ('10.30.10.10', 2),
                                   ('10.10.120.11', 2)]:
        source = IPv4Address(source_text)
        outbound = paths(nodes, 'Main-Edge', WEB, tracks, disabled, source)
        assert bool(outbound) == any(expected), (label, source_text)
        if any(expected):
            chosen = preferred if expected[preferred - 1] else 3 - preferred
            assert {path[1] for path in outbound} == {f'ISP{chosen}'}, (label, outbound)
            assert permitted(edge, '100', source, WEB), source_text
            public = IPv4Address('203.0.113.2' if chosen == 1 else '198.51.100.2')
            assert paths(nodes, 'INET-Core', public, tracks, disabled), (label, public)
    internal = IPv4Address('10.30.10.10')
    assert pbr_hop(edge, IPv4Address('10.20.10.10'), internal, tracks, disabled) is None
    assert not permitted(edge, '100', IPv4Address('10.20.10.10'), internal)
    for unused in ('10.10.200.1', '10.20.200.1', '10.30.200.1'):
        assert not paths(nodes, 'Main-Edge', IPv4Address(unused), tracks, disabled), (label, unused)
    print(f'OK static model: {label}; edge tracks={expected}; GW default={tracks[("Main-GW", "10")]}')


def main():
    nodes = {}
    for path in sorted((ROOT / 'configs').rglob('*.cfg')):
        node = load_node(path)
        assert node.name not in nodes, f'Duplicate hostname: {node.name}'
        nodes[node.name] = node
    assert set(nodes) == {'Main-Core', 'Main-GW', 'Main-FW', 'Main-Edge',
                          'DBP-GW', 'BHTQ-GW', 'ISP1', 'ISP2', 'INET-Core'}
    addresses = [(name, addr.ip) for name, node in nodes.items()
                 for addr in node.interfaces.values()]
    assert len({ip for _, ip in addresses}) == len(addresses), 'Duplicate interface IP'
    # Verify allocated VLAN/transit blocks individually, excluding /16 reserves.
    table = (ROOT / 'docs/02-design/ip-vlan-plan.md').read_text(encoding='utf-8')
    nets = [IPv4Network(cidr) for row in table.splitlines() if row.startswith('| **')
            for cidr in re.findall(r'`(10\.[\d.]+/\d+)`', row)]
    assert len(nets) == len(set(nets)), 'Duplicate allocated subnet'
    assert not any(a.overlaps(b) for i, a in enumerate(nets) for b in nets[i+1:]), 'Overlap'
    # OSPF checks are structural only: this checker does NOT execute SPF or LSAs.
    ospf = {'Main-Core', 'Main-GW', 'DBP-GW', 'BHTQ-GW'}
    ids = []
    for name in ospf:
        block = nodes[name].blocks['router ospf 1']
        assert 'passive-interface default' in block, name
        ids.extend(line.split()[1] for line in block if line.startswith('router-id '))
    assert len(ids) == len(set(ids)) == 4, 'Router IDs must be unique'
    gw = nodes['Main-GW']
    assert gw.blocks['router ospf 1'].count('default-information originate metric 10') == 1
    assert all('always' not in line for line in gw.blocks['router ospf 1'])
    assert all(r.track == '10' for r in gw.routes if r.net.prefixlen == 0)
    assert not any('default-information originate' in line
                   for line in nodes['Main-Core'].blocks['router ospf 1'])
    core = nodes['Main-Core']
    assert 'redistribute static subnets route-map DMZ-ONLY' in core.blocks['router ospf 1']
    assert core.blocks['route-map DMZ-ONLY permit 10'] == ['match ip address prefix-list DMZ-PREFIX']
    assert re.findall(r'^ip prefix-list DMZ-PREFIX (.+)$', core.text, re.M) == ['permit 10.10.80.0/27']
    assert 'GigabitEthernet0/0.80' not in core.interfaces
    assert nodes['Main-FW'].interfaces['GigabitEthernet0/2'].ip == IPv4Address('10.10.80.1')
    for number, iface in [('1', 'GigabitEthernet0/1'), ('2', 'GigabitEthernet0/2')]:
        edge = nodes['Main-Edge']
        target = '192.0.2.11' if number == '1' else '192.0.2.22'
        assert f'icmp-echo {target} source-interface {iface}' in edge.blocks[f'ip sla {number}']
        assert 'delay down 6 up 6' in edge.blocks[f'track {number} ip sla {number} reachability']
        assert any(r.net == IPv4Network(target + '/32') and r.interface == 'Null0'
                   and r.distance == 254 for r in edge.routes), target
        assert f'ip nat inside source route-map NAT-ISP{number} interface {iface} overload' in edge.text
        assert edge.blocks[f'route-map NAT-ISP{number} permit 10'] == ['match ip address 100', f'match interface {iface}']
    for name in ('Main-Core', 'Main-GW'):
        node = nodes[name]
        assert 'icmp-echo 192.0.2.100 source-interface Loopback0' in node.blocks['ip sla 10']
        assert 'delay down 6 up 6' in node.blocks['track 10 ip sla 10 reachability']
    active = {'Main-Core': {'GigabitEthernet0/1'},
              'Main-GW': {'GigabitEthernet0/0', 'Serial0/0/0', 'Serial0/0/1'},
              'DBP-GW': {'Serial0/0/0'}, 'BHTQ-GW': {'Serial0/0/0'}}
    for name, interfaces in active.items():
        actual = {line.split()[-1] for line in nodes[name].blocks['router ospf 1']
                  if line.startswith('no passive-interface ')}
        assert actual == interfaces, (name, actual)
    print(f'OK static declarations: {len(nodes)} nodes; {len(nets)} allocated VLAN/transit subnets; OSPF/NAT contracts')
    for args in [
        ('both ISP up', [], (True, True)),
        ('ISP1 local down', ['203.0.113.0/30'], (False, True)),
        ('ISP2 local down', ['198.51.100.0/30'], (True, False)),
        ('ISP1 upstream down', ['192.0.2.128/30'], (False, True)),
        ('ISP2 upstream down', ['192.0.2.132/30'], (True, False)),
        ('both upstream down', ['192.0.2.128/30', '192.0.2.132/30'], (False, False)),
        ('both local down', ['203.0.113.0/30', '198.51.100.0/30'], (False, False)),
        ('recovery', [], (True, True)),
    ]:
        check_scenario(nodes, *args)
    check_scenario(nodes, 'Web health target unavailable', [], (True, True), web_up=False)
    print('Static checks only. IOS parser, OSPF convergence, NAT sessions, HTTP/DNS and runtime test results are NOT verified.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (AssertionError, KeyError, ValueError) as exc:
        print(f'WAN static check FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
