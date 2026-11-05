#!/usr/bin/env python3
"""Guard against accepting stale ping output or uncorroborated HTTP timeouts."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from review_packet_results import review

ROOT = Path(__file__).resolve().parents[1]


class SavedObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = json.loads((ROOT / 'test_results/packet-tracer/wired-runtime/hospital-results.json')
                                 .read_text(encoding='utf-8'))['records']

    def test_known_harness_failure_stays_incomplete(self):
        record = self.records[1]
        self.assertEqual(record['group'], 'TC02')
        self.assertEqual(review([record])[0]['status'], 'INCOMPLETE')

    def test_previous_target_statistics_cannot_complete_new_ping(self):
        record = deepcopy(self.records[0])
        record.update(target='10.10.20.7', command='ping 10.10.20.7')
        self.assertEqual(review([record])[0]['status'], 'INCOMPLETE')

    def test_packet_loss_is_reported(self):
        record = next(r for r in self.records if r.get('kind') == 'ping'
                      and 'Lost = 2' in r.get('output', ''))
        self.assertEqual(review([record])[0]['status'], 'OBSERVED_ALLOW_WITH_LOSS')

    def test_http_timeout_requires_both_controls(self):
        record = next(r for r in self.records if r.get('kind') == 'http' and r['expected'] == 'deny')
        self.assertEqual(review([record])[0]['status'], 'INCOMPLETE')
        same_site_pc = next(r for r in self.records if r.get('kind') == 'http'
                            and r.get('url') == record['url'] and r['expected'] == 'allow'
                            and r['source'].split('-')[0] == record['source'].split('-')[0])
        self.assertEqual(review([record, same_site_pc])[0]['status'], 'INCOMPLETE')
        own_web = next(r for r in self.records if r.get('kind') == 'http'
                       and r['source'] == record['source'] and r.get('marker') == 'HOSPITAL-LAB-Web-Lab')
        self.assertEqual(review([record, same_site_pc, own_web])[0]['status'], 'OBSERVED_BLOCK_WITH_CONTROLS')

    def test_cached_page_without_success_event_is_not_allowed(self):
        record = deepcopy(next(r for r in self.records if r.get('kind') == 'http' and r['expected'] == 'allow'))
        record['events'] = []
        self.assertEqual(review([record])[0]['status'], 'INCOMPLETE')

    def test_native_failure_event_still_requires_controls(self):
        records = deepcopy(self.records)
        index = next(i for i, r in enumerate(records) if r.get('kind') == 'http' and r['expected'] == 'deny')
        record = records[index]
        record['events'] = [{'responseType': 7, 'content': '', 'url': record['url']}]
        self.assertEqual(review([record])[0]['status'], 'INCOMPLETE')
        self.assertEqual(review(records)[index]['status'], 'OBSERVED_FAILURE_WITH_CONTROLS')
        record['events'][0]['responseType'] = 999
        self.assertEqual(review(records)[index]['status'], 'INCOMPLETE')

    def test_success_event_for_other_url_is_not_allowed(self):
        record = deepcopy(next(r for r in self.records if r.get('kind') == 'http' and r['expected'] == 'allow'))
        record['events'][0]['url'] = 'http://wrong-target.test'
        self.assertEqual(review([record])[0]['status'], 'INCOMPLETE')


if __name__ == '__main__':
    unittest.main()
