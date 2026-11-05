#!/usr/bin/env python3
"""Prepare a Packet Tracer assembly kit; never creates or claims to test a .pkt."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'simulation/packet-tracer/assembly'


def rows(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def csv_text(records):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(records)
    return stream.getvalue()


def artifacts():
    nodes, links, wireless = [], [], []
    output = {}
    for folder, model in [('configs', '2911'), ('switches', '2960-24TT')]:
        for path in sorted((ROOT / 'simulation/generated' / folder).glob('*.cfg')):
            serial = path.stem in ('Main-GW', 'DBP-GW', 'BHTQ-GW')
            nodes.append(dict(node=path.stem, model=model,
                              module='HWIC-2T in slot 0; power off before inserting' if serial else '',
                              config='configs/' + path.name))
            output['configs/' + path.name] = path.read_text(encoding='utf-8')
    for row in rows('simulation/lab/cabling.csv'):
        links.append(dict(node_a=row['node_a'], port_a=row['interface_a'],
                          node_b=row['node_b'], port_b=row['interface_b'],
                          medium='Serial DCE at Main-GW' if row['mode'].startswith('Serial') else 'Copper; choose Auto if needed',
                          vlan_or_network=row['subnet'] or row['mode']))
    endpoints = rows('simulation/lab/endpoints.csv')
    ports = {row['endpoint']: row for row in rows('simulation/generated/switch-ports.csv')}
    for row in endpoints:
        wlan = row['node'].endswith(('-Guest', '-Staff'))
        model = 'Laptop-PT' if wlan else 'Server-PT' if row['kind'] in ('server', 'external-server') else 'PC-PT'
        nodes.append(dict(node=row['node'], model=model,
                          module='Install WPC300N while powered off; verify adapter in target version' if wlan else '', config='GUI endpoints.csv'))
        port = ports[row['node']]
        attached = row['node']
        if wlan:
            attached += '-AP'
            nodes.append(dict(node=attached, model='AccessPoint-PT', module='', config='GUI wireless.csv'))
            ssid = row['site'] + ('_Guest' if row['vlan'] == '100' else '_Staff')
            wireless.append(dict(ap=attached, client=row['node'], ssid=ssid, vlan=row['vlan'],
                                 switch=port['switch'], port=port['interface'],
                                 addressing='DHCP; compare with site pool, not a fixed reserved client IP',
                                 security='Configure WPA2-PSK if available; supply a lab key locally; no AAA/RF claim'))
        links.append(dict(node_a=port['switch'], port_a=port['interface'], node_b=attached,
                          port_b='Port 0' if wlan else 'FastEthernet0', medium='Copper straight-through', vlan_or_network=row['vlan']))
    assert len(nodes) == 58 and len(links) == 52 and len(wireless) == 6
    assert len({n['node'] for n in nodes}) == len(nodes)
    used = set()
    for link in links:
        for side in ('a', 'b'):
            port = (link['node_' + side], link['port_' + side])
            assert port not in used, port
            used.add(port)
    output['devices.csv'] = csv_text(nodes)
    output['cabling.csv'] = csv_text(links)
    output['endpoints.csv'] = csv_text(endpoints)
    output['wireless.csv'] = csv_text(wireless)
    output['dhcp-pools.csv'] = (ROOT / 'simulation/generated/dhcp-pools.csv').read_text(encoding='utf-8')
    dns = [dict(server=server['ip'], name='web.hospital.test', address='192.0.2.100', type='A')
           for server in endpoints if server['node'].endswith('-Infra') or server['node'] == 'Web-Lab']
    for server in endpoints:
        if server['node'].endswith('-Infra'):
            dns.extend([dict(server=server['ip'], name='his.hospital.test', address='10.10.70.11', type='A'),
                        dict(server=server['ip'], name='dmz.hospital.test', address='10.10.80.10', type='A')])
    output['dns-records.csv'] = csv_text(dns)
    test_cases = [
        ('TC01', 'Main-PC10-A', 'Main-PC10-B', 'ping; verify same subnet and VLAN', 'ICMP replies'),
        ('TC02', 'Main-PC10-A', '10.10.20.10; http://10.10.70.11', 'ping; Web Browser', 'Allowed routing and HIS HTTP'),
        ('TC03', 'Main-PC10-A; DBP-PC10; BHTQ-PC10', '10.20.10.10; 10.30.10.10; 10.10.10.10', 'ping both directions; tracert; show ip ospf neighbor', 'Both branches via Main'),
        ('TC04', 'Main-PC10-A; Web-Lab', 'http://10.10.80.10; http://198.51.100.2:8080', 'Web Browser; show ip nat translations', 'HTTP through policy; inbound static PAT on ISP2'),
        ('TC05', 'Main-Guest; DBP-Guest; BHTQ-Guest', 'local PC10; http://10.10.70.11; http://web.hospital.test', 'Blocked ICMP/HTTP to LAN with internal positive control; ACL counters; guest Web/DNS', 'LAN denied; Internet and DNS allowed'),
        ('TC06', 'PC10 and Guest at each of 3 sites', 'http://web.hospital.test', 'Web Browser; tracert 192.0.2.100; show ip nat translations at Main', 'All 6 sources through Main with PAT'),
    ]
    output['test-results.csv'] = csv_text([dict(id=tc, source=src, destination=dst, steps=steps,
                                               expected=expected, actual='', status='NOT RUN',
                                               evidence='', tester='', timestamp='', project_sha256='')
                                          for tc, src, dst, steps, expected in test_cases])
    output['feature-probes.csv'] = csv_text([dict(feature=feature, node=node, probe=probe,
                                                 status='NOT RUN', actual='', fallback=remedy)
                                            for feature, node, probe, remedy in [
        ('OSPF and serial', 'Main-GW', 'show controllers serial 0/0/0; show ip ospf neighbor', 'Check DCE clock and HWIC slot'),
        ('802.1Q and relay', 'Main-Core', 'show ip interface brief; show interfaces gigabitEthernet 0/0.10', 'Verify subinterface support'),
        ('IP SLA and track', 'Main-GW; Main-Edge', 'ip sla ?; track ?', 'Record unsupported CLI; keep advanced tests NOT RUN'),
        ('PBR verify-availability', 'Main-Edge', 'route-map capability; show route-map', 'Do not silently replace monitored dual ISP with static ECMP'),
        ('NAT route-map and interface match', 'Main-Edge', 'ip nat inside source ?; show ip nat statistics', 'Record support before loading both PAT rules'),
        ('ZBF inspection', 'Main-FW', 'class-map type inspect ?; show zone-pair security', 'Keep explicit ACL/ZBF scope and test positive/negative flows'),
        ('WLAN client', 'Each Guest/Staff laptop', 'Wireless adapter; PC Wireless; SSID; DHCP', 'A wired VLAN test does not prove wireless association'),
    ]])
    output['manifest.json'] = json.dumps(dict(
        status='ASSEMBLY KIT ONLY; NATIVE PKT AND PACKET TRACER RUNTIME NOT RUN',
        nodes=58, wired_links=52, wireless_associations=6,
        sha256={name: hashlib.sha256(text.encode('utf-8')).hexdigest() for name, text in sorted(output.items())}), indent=2) + '\n'
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name, text in artifacts().items():
        path = OUT / name
        data = text.encode('utf-8')
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if stale:
        parser.exit(1, 'Stale Packet Tracer assembly kit: ' + ', '.join(stale) + '\n')
    print('OK static Packet Tracer assembly: 58 planned nodes, 52 cables, 6 WLAN associations, 18 DHCP pools; this check does not execute the native lab; see separate runtime evidence')


if __name__ == '__main__':
    main()
