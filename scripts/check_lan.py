#!/usr/bin/env python3
"""Check TV2 budgets, adapter policies, saved-packet provenance and drawing source."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from build_campus import budget, rows
from check_security import load_acls, permitted

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'simulation/modules/tv2-lan-wireless'


def main():
    calculated = [budget(row) for row in rows()]
    assert len(calculated) == 3
    expected = {'Main': (960, 670, 810, 150, 40, 50, 88, 85050),
                'DBP': (384, 277, 334, 50, 8, 10, 37, 17010),
                'BHTQ': (384, 277, 334, 50, 8, 10, 37, 17010)}
    for row in calculated:
        actual = tuple(row[key] for key in ('access_ports','used_now','used_future','spare_future','aps_future','cameras_future','cat6_boxes_305m','nvr_usable_future_gb'))
        assert actual == expected[row['site']], (row['site'], actual)
        assert row['worst_floor_future'] <= row['floor_ports']
        assert row['floor_poe_future_w'] == 197 and row['floor_poe_future_w'] < row['floor_poe_budget_w']
    adapter = (MODULE / 'configs/Main-Core-3650.cfg').read_text()
    assert 'interface GigabitEthernet0/0' not in adapter
    assert 'encapsulation dot1Q' not in adapter and 'interface Vlan80' not in adapter
    for port, ip in ((23, '10.255.0.9'), (24, '10.255.0.13')):
        assert re.search(rf'interface GigabitEthernet1/0/{port}\n no switchport\n(?: .+\n)* ip address {re.escape(ip)} 255.255.255.252', adapter)
    acls = load_acls(adapter)
    assert 'interface Vlan100\n ip helper-address 10.10.70.10\n ip access-group MAIN-V100-IN in' in adapter
    with (ROOT / 'test_results/static/security-cases.csv').open() as stream:
        import csv
        cases = [c for c in csv.DictReader(stream) if c['node'] == 'Main-Core']
    for case in cases:
        assert permitted(acls[case['acl']], case) == (case['expected'] == 'permit'), case['case']
    for letter, group in (('A',1),('B',2)):
        text = (MODULE / f'configs/Main-Access-{letter}-2960.cfg').read_text()
        for port, vlan in ((1,10),(2,20),(3,100),(4,120)):
            assert re.search(rf'^interface FastEthernet0/{port}\n(?: description .+\n)? switchport mode access\n switchport access vlan {vlan}$', text, re.M)
        assert text.count(f' channel-group {group} mode passive') == 2
        for allowed in re.findall(r'^ switchport trunk allowed vlan (.+)$', text, re.M):
            assert '80' not in allowed.split(',')
    inventory = json.loads((MODULE / 'audit/inventory.json').read_text())
    packet = ROOT / inventory['artifact']
    assert hashlib.sha256(packet.read_bytes()).hexdigest() == inventory['sha256']
    assert len(inventory['devices']) == 10 and len(inventory['links']) == 10
    assert inventory['saved_packet_tracer_version'] == '9.0.0.0810'
    assert inventory['type_counts'] == {'AccessPoint':2,'MultiLayerSwitch':1,'Pc':4,'Power Distribution Device':1,'Switch':2}
    for name in ('physical-main','physical-aux'):
        drawing = ET.parse(ROOT / f'docs/02-design/diagrams/{name}.drawio')
        cells = drawing.findall('.//mxCell')
        ids = [c.get('id') for c in cells]
        assert len(ids) == len(set(ids))
        for cell in cells:
            for key in ('source','target'):
                if cell.get(key): assert cell.get(key) in ids
        ET.parse(ROOT / f'docs/02-design/diagrams/exports/{name}.svg')
    print(f'OK static TV2: 3 campus budgets/storage,72 uplinks,2 diagrams,3 adapters, {len(cases)} preserved Main ACL flows; original PKT hash verified')
    print('Original native file is a partial Main module. This static audit does not run it; integrated Packet Tracer evidence is validated separately.')


if __name__ == '__main__':
    main()
