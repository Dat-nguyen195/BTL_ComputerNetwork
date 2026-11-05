#!/usr/bin/env python3
"""Validate saved Packet Tracer test evidence; does not execute the network."""
import argparse
from collections import Counter
import hashlib
from ipaddress import IPv4Address, IPv4Network
import json
from pathlib import Path
import re

from review_packet_results import http_allowed, review

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guest_deny_count(snapshots, node, acl):
    snapshot = next(s for s in snapshots if s['node'] == node and s['command'] == 'show access-lists')
    assert snapshot['result']['first'] == 0, 'ACL readback failed: ' + node
    block = re.search(r'Extended IP access list ' + re.escape(acl) + r'\n(.*?)(?=Extended IP access list|\Z)',
                      snapshot['result']['second'], re.S)
    assert block, 'Missing guest ACL ' + acl
    line = next(line for line in block[1].splitlines() if 'deny ip any 10.0.0.0 0.255.255.255' in line)
    count = re.search(r'\((\d+) match', line)
    return int(count[1]) if count else 0


def check(run, project):
    def read(name):
        return json.loads((run / name).read_text(encoding='utf-8'))

    provenance = read('provenance.json')
    for name, expected in provenance['sha256'].items():
        assert digest(run / name) == expected, 'Evidence changed: ' + name
    assert digest(project) == provenance['native_sha256'] == digest(run / 'lab.pkt'), 'Native lab hash mismatch'
    proof_path = run.parent / 'persistence-review.json'
    if proof_path.is_file():
        proof = json.loads(proof_path.read_text(encoding='utf-8'))
        assert proof['status'] == 'PASS' and proof['final_native_sha256'] == provenance['native_sha256']
        script_root = ROOT / 'simulation/packet-tracer/scripts'
        for name, expected in proof['embedded_sources_sha256'].items():
            assert digest(script_root / name) == expected, 'Embedded source changed: ' + name
        assert digest(script_root / 'manual-isp.js') == proof['manual_test_source_sha256']
    assert provenance['network_devices'] == 58 and provenance['links'] == 53
    assert provenance['allocatable_dhcp_pools'] == 18 and provenance['zero_capacity_dhcp_pools'] == 3
    assert read('config-check.json') == [], 'Recorded configuration errors'
    normalization = read('normalization.json')
    assert all(r['response']['first'] == 0 for r in normalization if 'command' in r)
    assert len([r for r in normalization if r.get('pool') == 'serverPool' and r['max_users'] == 0]) == 3

    results = read('hospital-results.json')
    records = results['records']
    rows = review(records)
    assert Counter(r['group'] for r in records) == {'TC01': 2, 'TC02': 3, 'TC03': 4, 'TC04': 2,
                                                  'TC05': 9, 'TC06': 6, 'WIFI': 6}, 'Missing/duplicate test jobs'
    allowed_statuses = {'OBSERVED_ALLOW', 'OBSERVED_NO_REPLY', 'OBSERVED_BLOCK_WITH_CONTROLS',
                        'OBSERVED_FAILURE_WITH_CONTROLS'}
    assert all(row['status'] in allowed_statuses for row in rows), 'Incomplete, lost-packet or unexpected result'
    assert len(records) == 32

    configs = read('config-readback.json')
    baseline = read('pretest-snapshots.json')
    deltas = {}
    for site, node in [('Main', 'Main-Core'), ('DBP', 'DBP-GW'), ('BHTQ', 'BHTQ-GW')]:
        acl = site.upper() + '-V100-IN'
        before = guest_deny_count(baseline, node, acl)
        after = guest_deny_count(results['snapshots'], node, acl)
        assert after > before, 'No new guest deny matches: ' + site
        deltas[site] = after - before
        interface = re.search(r'interface GigabitEthernet0/0\.100\n(.*?)(?=\ninterface|\n!)',
                              configs[node]['RUNNINGCONFIG'], re.S)
        assert interface and 'ip access-group ' + acl + ' in' in interface[1], 'Guest ACL binding missing'

    addresses = {r['node']: r['ip'] for r in read('addresses.json')}
    pools = read('dhcp-pools-leases.json')
    spec = read('hospital-spec.json')
    clients = [e for e in spec['endpoints'] if e['kind'] == 'client-dhcp-example']
    assert len(clients) == 19
    for client in clients:
        address = addresses[client['node']]
        pool = next(p for p in pools if p['enabled'] and p['gateway'] == client['gateway'])
        assert IPv4Address(address) in IPv4Network(pool['network'] + '/' + pool['mask'])
        assert any(lease['IP_ADDRESS'] == address for lease in pool['leases']), 'No lease for ' + client['node']
    for pool in pools:
        if pool['enabled'] and pool['name'] == 'serverPool':
            assert int(pool['max_users']) == 0 and not pool['leases']

    associations = read('wireless-associations.json')
    readback = {r['node']: r for r in read('wireless-readback.json')}
    expected_clients = {site + '-' + role for site in ['Main', 'DBP', 'BHTQ'] for role in ['Guest', 'Staff']}
    assert {r['node'] for r in associations} == expected_clients and len(associations) == 6
    for record in associations:
        saved = readback[record['node']]
        assert record['wireless_port'] and record['auth_type'] == record['encrypt_type'] == 4
        assert record['ssid'] == saved['profile_ssid'] == saved['ap_ssid'] == record['node'].replace('-', '_')
        assert record['ap_mac'].lower() in [mac.lower() for mac in saved['ap_macs']]
        assert record['ip'] == addresses[record['node']]
        assert saved['wireless_card_models'] == ['PT-HOST-NM-1W-AC']
        assert saved['profile_auth'] == saved['profile_encrypt'] == saved['ap_auth'] == saved['ap_encrypt'] == '4'
    if (run / 'manual-isp-results.json').is_file():
        manual = read('manual-isp-results.json')
        assert not manual.get('error'), 'Manual ISP test reported an error'
        assert all(r['response']['first'] == 0 for r in manual['commands']), 'Manual ISP CLI errors'
        assert Counter(r['group'] for r in manual['records']) == {'MANUAL-ISP1': 3, 'MANUAL-ISP2-RESTORED': 1}
        assert all(http_allowed(r) for r in manual['records']), 'Manual ISP HTTP failure'
        def response(stage, command):
            snapshot = next(s for s in manual['snapshots'] if s['stage'] == stage and s['command'] == command)
            assert snapshot['response']['first'] == 0
            return snapshot['response']['second']
        assert '203.0.113.1' in response('ISP1-selected', 'show ip route')
        assert '198.51.100.1' in response('ISP2-restored', 'show ip route')
        for record in manual['records']:
            isp1 = record['group'] == 'MANUAL-ISP1'
            nat = response('ISP1-selected' if isp1 else 'ISP2-restored', 'show ip nat translations')
            public = '203.0.113.2' if isp1 else '198.51.100.2'
            assert any(public + ':' in line and record['source_ip'] + ':' in line for line in nat.splitlines()), 'Missing expected public PAT mapping'
        assert response('before', 'show running-config') == response('ISP2-restored', 'show running-config'), 'Main-Edge config not restored exactly'
        print('OK recorded manual ISP selection: 3 HTTP via ISP1/PAT, 1 HTTP after ISP2 restoration; Main-Edge configuration restored exactly')
    print('OK recorded Packet Tracer evidence: 32 complete observations, 6 BSSIDs, 19 DHCP clients, '
          '18 allocatable pools, 3 zero-capacity defaults; guest deny counter deltas ' + str(deltas))
    print('Recorded evidence only; no network executed, automatic ISP failover or human approval claimed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, default=ROOT / 'test_results/packet-tracer/after-reopen')
    parser.add_argument('--project', type=Path, default=ROOT / 'simulation/packet-tracer/hospital-3sites.pkt')
    args = parser.parse_args()
    check(args.run, args.project)
