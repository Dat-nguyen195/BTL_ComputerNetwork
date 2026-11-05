#!/usr/bin/env python3
"""Extract saved native lab evidence. This command does not execute the network."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/vendor/unpacket'))
from Decipher.pt_crypto import decrypt_pkt

STORES = {'hospital-spec.json', 'hospital-results.json', 'config-check.json',
          'services-check.json', 'addresses.json', 'hardware.json', 'probe-results.json',
          'wireless-associations.json', 'normalization.json', 'warmup-results.json',
          'pretest-snapshots.json', 'reopen-event-probe.json', 'manual-isp-results.json', 'final-label-fix.json'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def collect(source, output):
    payload = source.read_bytes()
    root = ET.fromstring(decrypt_pkt(payload))
    output.mkdir(parents=True, exist_ok=True)
    (output / 'lab.pkt').write_bytes(payload)
    written = ['lab.pkt']

    def write(name, value):
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                                   encoding='utf-8', newline='\n')
        written.append(name)

    data_stores = {}
    for store in root.findall('./SCRIPT_MODULE/SCRIPTS/SCRIPT_DATA_STORES/DATA_STORE'):
        name = store.findtext('ID')
        if name in STORES:
            if name in data_stores:
                raise ValueError('Duplicate data store ' + name)
            data_stores[name] = json.loads(base64.b64decode(store.findtext('CONTENT')))
            write(name, data_stores[name])
    inventory, pools, configs = [], [], {}
    for device in root.findall('./NETWORK/DEVICES/DEVICE'):
        engine = device.find('ENGINE')
        name = engine.findtext('NAME')
        kind = engine.findtext('TYPE')
        inventory.append({'name': name, 'type': kind, 'model': engine.find('TYPE').get('model')})
        for server in engine.findall('.//DHCP_SERVER'):
          for pool in server.findall('POOLS/POOL'):
            pools.append({'server': name, 'enabled': server.findtext('ENABLED') == '1', 'name': pool.findtext('NAME'),
                          'network': pool.findtext('NETWORK'), 'mask': pool.findtext('MASK'),
                          'gateway': pool.findtext('DEFAULT_ROUTER'), 'dns': pool.findtext('DNS_SERVER'),
                          'start': pool.findtext('START_IP'), 'end': pool.findtext('END_IP'),
                          'max_users': pool.findtext('MAX_USERS'),
                          'leases': [{c.tag: c.text for c in lease}
                                     for lease in pool.findall('./DHCP_POOL_LEASES/DHCP_POOL_LEASE')]})
        if kind in ('Router', 'Switch'):
            configs[name] = {tag: '\n'.join(n.text or '' for n in engine.findall(tag + '/LINE')) + '\n'
                             for tag in ('RUNNINGCONFIG', 'STARTUPCONFIG')}
    write('inventory.json', inventory)
    write('dhcp-pools-leases.json', pools)
    write('config-readback.json', configs)
    devices = {d.findtext('ENGINE/NAME'): d for d in root.findall('./NETWORK/DEVICES/DEVICE')}
    wireless = []
    for name, device in devices.items():
        if not name.endswith(('-Guest', '-Staff')) or name + '-AP' not in devices:
            continue
        engine = device.find('ENGINE')
        access_point = devices[name + '-AP'].find('ENGINE')
        profile = engine.find('WIRELESS_CLIENT/CURRENT_PROFILE/WIRELESS_PROFILE')
        ap_common = access_point.find('WIRELESS_SERVER/WIRELESS_COMMON')
        ports = [p for p in engine.findall('.//MODULE/PORT') if 'Wireless' in (p.findtext('TYPE') or '')]
        ap_ports = [p for p in access_point.findall('.//MODULE/PORT') if 'Wireless' in (p.findtext('TYPE') or '')]
        wireless.append({'node': name, 'scope': 'Saved configuration; live association is in wireless-associations.json',
                         'wireless_card_models': [m.findtext('MODEL') for m in engine.findall('.//MODULE')
                                                  if any('Wireless' in (p.findtext('TYPE') or '') for p in m.findall('PORT'))],
                         'port_ips': [p.findtext('IP') for p in ports],
                         'gateway': engine.findtext('GATEWAY'),
                         'dns': [p.findtext('PORT_DNS') for p in ports],
                         'profile_ssid': profile.findtext('SSID') if profile is not None else None,
                         'profile_auth': profile.findtext('AUTHEN_TYPE') if profile is not None else None,
                         'profile_encrypt': profile.findtext('ENCRYPT_TYPE') if profile is not None else None,
                         'ap_ssid': ap_common.findtext('SSID') if ap_common is not None else None,
                         'ap_auth': ap_common.findtext('AUTHEN_TYPE') if ap_common is not None else None,
                         'ap_encrypt': ap_common.findtext('ENCRYPT_TYPE') if ap_common is not None else None,
                         'ap_macs': [p.findtext('MACADDRESS') for p in ap_ports]})
    write('wireless-readback.json', wireless)
    embedded = {s.findtext('ID'): digest(base64.b64decode(s.findtext('CONTENT')))
                for s in root.findall('./SCRIPT_MODULE/SCRIPTS/SCRIPT')}
    network_devices = [d for d in inventory if d['type'] != 'Power Distribution Device']
    manifest = {'scope': 'Saved native application state and data stores; collector does not run tests',
                'collected_at_utc': datetime.now(timezone.utc).isoformat(),
                'clock_note': 'Collection time is host UTC. Raw record time is the application JavaScript clock; preserved without correction.',
                'version': root.findtext('VERSION'), 'native_sha256': digest(payload),
                'network_devices': len(network_devices), 'power_devices': len(inventory) - len(network_devices),
                'links': len(root.findall('./NETWORK/LINKS/LINK')),
                'dhcp_pools': sum(p['enabled'] for p in pools),
                'allocatable_dhcp_pools': sum(p['enabled'] and int(p['max_users'] or 0) > 0 for p in pools),
                'zero_capacity_dhcp_pools': sum(p['enabled'] and int(p['max_users'] or 0) == 0 for p in pools),
                'inactive_dhcp_pools': sum(not p['enabled'] for p in pools),
                'dhcp_leases': sum(len(p['leases']) for p in pools),
                'embedded_script_sha256': embedded,
                'sha256': {name: digest((output / name).read_bytes()) for name in written}}
    write('provenance.json', manifest)
    print(f"Collected {manifest['network_devices']} network devices, {manifest['links']} serialized links, "
          f"{manifest['allocatable_dhcp_pools']} allocatable DHCP pools "
          f"({manifest['zero_capacity_dhcp_pools']} zero-capacity) and {manifest['dhcp_leases']} saved leases; "
          "no tests executed by collector")
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    collect(args.input, args.output)
