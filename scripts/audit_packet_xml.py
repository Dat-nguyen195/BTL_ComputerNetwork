#!/usr/bin/env python3
"""Summarize a locally decoded Packet Tracer XML; never executes embedded scripts."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def audit(xml_path, packet_path):
    root = ET.parse(xml_path).getroot()
    assert root.tag == 'PACKETTRACER5'
    devices = []
    configs = {}
    refs = {}
    for device in root.findall('./NETWORK/DEVICES/DEVICE'):
        engine = device.find('ENGINE')
        name = engine.findtext('NAME')
        refs[engine.findtext('SAVE_REF_ID')] = name
        config = '\n'.join(n.text or '' for n in engine.findall('./RUNNINGCONFIG/LINE'))
        filename = re.sub(r'[^A-Za-z0-9_-]+', '-', name).strip('-') + '.txt'
        if config:
            # Do not export secret-bearing configuration lines or user profiles.
            safe = '\n'.join('[REDACTED SECRET LINE]' if re.search(r'\b(password|secret|community|key-string|pre-shared-key)\b', line, re.I) else line
                             for line in config.splitlines())
            configs[filename] = '! EXTRACTED SAVED RUNNING CONFIG; NOT RUNTIME ACCEPTANCE\n' + safe + '\n'
        devices.append(dict(name=name, type=engine.findtext('TYPE'),
                            command_set=engine.findtext('CURRENT_COMMAND_SET'),
                            vlans=[int(v.get('number')) for v in engine.findall('./VLANS/VLAN')],
                            ipv4_values=[n.text.strip() for n in engine.iter('IP') if n.text and n.text.strip()],
                            gateway=engine.findtext('GATEWAY') or None,
                            ssids=sorted({n.text for n in engine.iter('SSID') if n.text}),
                            running_config_lines=len(engine.findall('./RUNNINGCONFIG/LINE')),
                            startup_config_lines=len(engine.findall('./STARTUPCONFIG/LINE')),
                            exported_config=filename if config else None))
    links = []
    for cable in root.findall('./NETWORK/LINKS/LINK/CABLE'):
        ports = [p.text for p in cable.findall('PORT')]
        links.append(dict(source=refs[cable.findtext('FROM')], source_port=ports[0],
                          target=refs[cable.findtext('TO')], target_port=ports[1],
                          medium=cable.findtext('TYPE')))
    summary = dict(status='PARTIAL MAIN LAN MODULE; STATIC XML AUDIT ONLY; RUNTIME NOT RUN',
                   artifact=packet_path.as_posix(), sha256=hashlib.sha256(packet_path.read_bytes()).hexdigest(),
                   size_bytes=packet_path.stat().st_size, saved_packet_tracer_version=root.findtext('VERSION'),
                   decoder=dict(upstream='https://github.com/Punkcake21/Unpacket',
                                commit='54cb6d6a9b46c6b4973356258cb8df6ae58b2ec7'),
                   type_counts=dict(sorted(Counter(d['type'] for d in devices).items())),
                   devices=devices, links=links)
    return summary, configs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xml', type=Path, required=True)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    summary, configs = audit(args.xml, args.packet)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'inventory.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, text in configs.items():
        (args.output_dir / name).write_text(text, encoding='utf-8')
    print(f"Static audit saved: {len(summary['devices'])} devices, {len(summary['links'])} links; Packet Tracer runtime NOT RUN")


if __name__ == '__main__':
    main()
