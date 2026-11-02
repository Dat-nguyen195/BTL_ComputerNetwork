#!/usr/bin/env python3
"""Check physical cabling, server counts, host addresses and representative port map."""
import csv
from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from pathlib import Path
from check_wan import load_node
from build_lab import OUTPUT

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    nodes = {p.stem: load_node(p) for p in (OUTPUT / 'configs').glob('*.cfg')}
    assert len(nodes) == 9
    cables = read_csv(ROOT / 'simulation/lab/cabling.csv')
    assert len(cables) == 14 and len({c['link'] for c in cables}) == 14
    ports = set()
    for cable in cables:
        for suffix in ('a', 'b'):
            node, interface = cable[f'node_{suffix}'], cable[f'interface_{suffix}']
            assert (node, interface) not in ports, f"Duplicate cable port: {node}/{interface}"
            ports.add((node, interface))
            if node in nodes:
                assert f'interface {interface}' in nodes[node].blocks
                if cable['subnet']:
                    assert nodes[node].interfaces[interface].network == IPv4Network(cable['subnet'])
        if cable['node_b'] in nodes:
            a = nodes[cable['node_a']].interfaces[cable['interface_a']]
            b = nodes[cable['node_b']].interfaces[cable['interface_b']]
            assert a.network == b.network and a.ip != b.ip
    physical = {(node.name, key.split()[1]) for node in nodes.values() for key in node.blocks
                if key.startswith('interface ') and not key.startswith('interface Loopback')
                and '.' not in key.split()[1]}
    assert physical <= ports, f"Unmapped router ports: {physical - ports}"
    endpoints = read_csv(ROOT / 'simulation/lab/endpoints.csv')
    names, ips, servers = set(), {a.ip for node in nodes.values() for a in node.interfaces.values()}, {}
    for endpoint in endpoints:
        address = IPv4Interface(f"{endpoint['ip']}/{endpoint['prefix']}")
        gateway = IPv4Address(endpoint['gateway'])
        assert endpoint['node'] not in names and address.ip not in ips
        names.add(endpoint['node'])
        ips.add(address.ip)
        assert address.network.network_address < address.ip < address.network.broadcast_address
        assert gateway in address.network and gateway != address.ip
        assert any(a.ip == gateway and a.network == address.network for node in nodes.values() for a in node.interfaces.values())
        if endpoint['kind'] == 'server':
            servers[endpoint['site']] = servers.get(endpoint['site'], 0) + 1
    assert servers == {'Main': 10, 'DBP': 2, 'BHTQ': 2}, servers
    mapping = read_csv(OUTPUT / 'switch-ports.csv')
    assert {p['endpoint'] for p in mapping} == names and len(mapping) == len(names)
    assert len({(p['switch'], p['interface']) for p in mapping}) == len(mapping)
    for port in mapping:
        config = (OUTPUT / 'switches' / (port['switch'] + '.cfg')).read_text()
        assert f"interface {port['interface']}\n description {port['endpoint']}\n switchport mode access\n switchport access vlan {port['vlan']}" in config
    print(f"OK static inventory: 14 cables, {len(endpoints)} endpoints, 10/2/2 servers, unique addresses and switch ports")


if __name__ == '__main__':
    main()
