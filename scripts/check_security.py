#!/usr/bin/env python3
"""Check compiled ACL first-match semantics and integration contracts, not IOS runtime."""
import csv
from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
import re

from build_lab import OUTPUT, SITES

ROOT = Path(__file__).resolve().parents[1]


def address(tokens):
    token = tokens.pop(0)
    if token == "any":
        return IPv4Network("0.0.0.0/0")
    if token == "host":
        return IPv4Network(tokens.pop(0) + "/32")
    wildcard = int(IPv4Address(tokens.pop(0)))
    return IPv4Network(f"{token}/{IPv4Address(wildcard ^ 0xffffffff)}", strict=False)


def port(tokens):
    if tokens and tokens[0] == "eq":
        tokens.pop(0)
        return int(tokens.pop(0))
    return None


def parse_rule(line):
    tokens = line.split()
    action, protocol = tokens.pop(0), tokens.pop(0)
    if action not in ("permit", "deny") or protocol not in ("ip", "tcp", "udp", "icmp"):
        raise ValueError(f"Unsupported ACL syntax: {line}")
    source = address(tokens)
    sport = port(tokens)
    destination = address(tokens)
    dport = port(tokens)
    flags = set(tokens) - {"log"}
    if flags - {"established", "echo", "echo-reply"}:
        raise ValueError(f"Unsupported ACL qualifiers: {line}")
    return action, protocol, source, sport, destination, dport, flags


def load_acls(text):
    acls, current = {}, None
    for raw in text.splitlines():
        if raw.startswith("ip access-list extended "):
            current = raw.split()[-1]
            assert current not in acls, f"Duplicate ACL {current}"
            acls[current] = []
        elif raw and not raw.startswith((" ", "!")):
            current = None
        elif current and raw.startswith(" ") and not raw.strip().startswith("remark "):
            acls[current].append(parse_rule(raw.strip()))
    return acls


def permitted(rules, case):
    src, dst = IPv4Address(case["src"]), IPv4Address(case["dst"])
    for action, proto, source, sport, destination, dport, flags in rules:
        if proto not in ("ip", case["proto"]) or src not in source or dst not in destination:
            continue
        if sport is not None and int(case["sport"] or 0) != sport:
            continue
        if dport is not None and int(case["dport"] or 0) != dport:
            continue
        if "established" in flags and not ({"ACK", "RST"} & set(case["flags"].split("|"))):
            continue
        if flags & {"echo", "echo-reply"} and case["flags"] not in flags:
            continue
        return action == "permit"
    return False


def main():
    configs = {path.stem: path.read_text(encoding="utf-8") for path in (OUTPUT / "configs").glob("*.cfg")}
    assert len(configs) == 9, "Build the lab first"
    acls = {name: load_acls(text) for name, text in configs.items()}
    with (ROOT / "test_results/static/security-cases.csv").open(encoding="utf-8", newline="") as stream:
        cases = list(csv.DictReader(stream))
    assert len({c['case'] for c in cases}) == len(cases), "Duplicate security case ID"
    for case in cases:
        actual = permitted(acls[case["node"]][case["acl"]], case)
        assert actual == (case["expected"] == "permit"), f"{case['case']}: unexpected {'permit' if actual else 'deny'}"
    with (OUTPUT / "dhcp-pools.csv").open(encoding="utf-8", newline="") as stream:
        pools = list(csv.DictReader(stream))
    assert len(pools) == 18
    for pool in pools:
        net = IPv4Network(pool["network"])
        start, end, gateway = map(IPv4Address, (pool["start"], pool["end"], pool["gateway"]))
        assert start in net and end in net and gateway in net
        assert net.network_address < start <= end < net.broadcast_address
        assert not start <= gateway <= end
        assert int(end) - int(start) + 1 == int(pool["max_users"])
        node = SITES[pool["site"]][1]
        pattern = rf"^interface GigabitEthernet0/0\.{pool['vlan']}\n ip helper-address {re.escape(pool['server'])}\n ip access-group (\S+) in$"
        binding = re.search(pattern, configs[node], re.M)
        assert binding and binding[1] in acls[node], pool["name"]
    for site, (_, node, _) in SITES.items():
        for vlan, suffix in ((70, 'SERVER'), (90, 'MGMT'), (110, 'CAMERA')):
            assert re.search(rf'^interface GigabitEthernet0/0\.{vlan}\n ip access-group {site.upper()}-{suffix}-IN in$', configs[node], re.M)
    fw = configs["Main-FW"]
    for interface, zone in ((0, "LAN"), (1, "OUTSIDE"), (2, "DMZ")):
        assert f"interface GigabitEthernet0/{interface}\n zone-member security {zone}" in fw
    for name, source, dest, policy in (("LAN-OUT", "LAN", "OUTSIDE", "INTERNET"),
                                       ("LAN-DMZ", "LAN", "DMZ", "LAN-DMZ"),
                                       ("OUT-DMZ", "OUTSIDE", "DMZ", "PUBLISHED-WEB"),
                                       ("DMZ-OUT", "DMZ", "OUTSIDE", "DMZ-UPDATE")):
        assert f"zone-pair security {name} source {source} destination {dest}\n service-policy type inspect PM-{policy}" in fw
        assert f"policy-map type inspect PM-{policy}\n class type inspect CM-{policy}\n  inspect\n class class-default\n  drop log" in fw
        assert f"class-map type inspect match-all CM-{policy}\n match access-group name FW-{policy}" in fw
    pairs = re.findall(r'^zone-pair security \S+ source (\S+) destination (\S+)', fw, re.M)
    assert ("OUTSIDE", "LAN") not in pairs and ("DMZ", "LAN") not in pairs
    assert "ip nat " not in fw, "No double NAT on Main-FW"
    edge = configs["Main-Edge"]
    static = re.findall(r'^ip nat inside source static .+$', edge, re.M)
    assert static == ["ip nat inside source static tcp 10.10.80.10 80 198.51.100.2 8080 extendable"]
    assert "access-list 102 permit ip 10.10.80.0 0.0.0.31 any" in edge
    assert "set ip next-hop verify-availability 198.51.100.1 1 track 2" in edge
    assert "ip nat inside" in edge and edge.count(" ip nat outside") == 2
    print(f"OK static security: {len(cases)} first-match flow cases, 18 DHCP pools, ingress bindings, ZBF/PAT contracts")
    print("NOT IOS runtime: no stateful sessions, DHCP leases, DNS/HTTP, VPN or IDS/IPS executed.")


if __name__ == "__main__":
    main()
