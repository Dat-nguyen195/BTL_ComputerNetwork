#!/usr/bin/env python3
"""Review saved Packet Tracer observations; never executes or accepts the lab."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def http_allowed(record):
    marker = record.get('marker')
    return (record.get('initiated') is True and bool(marker)
            and marker in record.get('page', '')
            and any(event.get('responseType') == 3
                    and event.get('url') == record.get('url')
                    and marker in event.get('content', '')
                    for event in record.get('events', [])))


def review(records):
    rows = []
    for index, record in enumerate(records):
        row = {'record_index': index, 'group': record.get('group'),
               'kind': record.get('kind'), 'source': record.get('source'),
               'target': record.get('target', record.get('url')),
               'expected': record.get('expected'), 'status': 'INCOMPLETE'}
        if record.get('kind') == 'ping':
            output = record.get('output', '')
            command = 'ping ' + str(record.get('target'))
            statistics = re.search(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)', output)
            correct_target = 'Ping statistics for ' + str(record.get('target')) + ':' in output
            if (record.get('command') == command and command in output and correct_target
                    and record.get('completion') == 'statistics' and statistics):
                sent, received, lost = map(int, statistics.groups())
                row.update(sent=sent, received=received, lost=lost)
                if sent == 4 and received + lost == sent:
                    if record.get('expected') == 'allow':
                        row['status'] = ('OBSERVED_ALLOW' if lost == 0 else
                                         'OBSERVED_ALLOW_WITH_LOSS' if received else 'UNEXPECTED_BLOCK')
                    elif record.get('expected') == 'deny':
                        row['status'] = 'OBSERVED_NO_REPLY' if received == 0 else 'UNEXPECTED_ALLOW'
            else:
                row['reason'] = 'Missing current command, matching target statistics, or complete output'
        elif record.get('kind') == 'http':
            if http_allowed(record):
                row['status'] = 'OBSERVED_ALLOW' if record.get('expected') == 'allow' else 'UNEXPECTED_ALLOW'
            elif (record.get('expected') == 'deny' and record.get('initiated') is True
                  and isinstance(record.get('events'), list) and record.get('page') == ''
                  and all(event.get('responseType') == 7 and event.get('content') == ''
                          and event.get('url') == record.get('url') for event in record['events'])):
                # A timeout alone does not prove the intended policy enforced it.
                # Require the same client to reach the external control, and a
                # same-site internal PC to reach this exact protected service.
                site = str(record.get('source', '')).split('-')[0] + '-'
                controls = [i for i, control in enumerate(records)
                            if control.get('expected') == 'allow' and http_allowed(control)
                            and ((control.get('source') == record.get('source')
                                  and control.get('marker') == 'HOSPITAL-LAB-Web-Lab')
                                 or (str(control.get('source', '')).startswith(site)
                                     and control.get('url') == record.get('url')))]
                same_client = any(records[i].get('source') == record.get('source') for i in controls)
                same_service = any(records[i].get('url') == record.get('url') for i in controls)
                row['control_record_indexes'] = controls
                if same_client and same_service:
                    row['status'] = ('OBSERVED_FAILURE_WITH_CONTROLS' if record['events']
                                     else 'OBSERVED_BLOCK_WITH_CONTROLS')
                if record['events']:
                    row['response_types'] = [event['responseType'] for event in record['events']]
                    row['reason'] = 'Native responseType 7 with empty content; enum meaning is not inferred. Check ACL counters separately.'
            elif record.get('expected') == 'allow':
                row['reason'] = 'Missing successful response event and expected page marker'
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    payload = args.input.read_bytes()
    data = json.loads(payload)
    rows = review(data['records'])
    result = {'scope': 'Offline review of saved observations; no new tests executed and no lab acceptance',
              'source_sha256': hashlib.sha256(payload).hexdigest(),
              'record_count': len(rows), 'counts': dict(Counter(row['status'] for row in rows)),
              'limitations': ['No-reply ICMP alone does not prove an ACL caused the block.',
                              'Successful pings with packet loss require a repeat after convergence.',
                              'This summary does not cover absent jobs, Wi-Fi association, failover, or reopen.'],
              'records': rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
