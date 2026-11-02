#!/usr/bin/env python3
"""Numerical regression cases for units, ambiguous scopes and input bounds."""
import unittest
from capacity import ROOT, calculate, inputs


class CapacityTests(unittest.TestCase):
    def setUp(self):
        self.data = inputs(ROOT / "docs/03-capacity/capacity-inputs.csv")

    def test_baseline_decimal_mb_and_three_hour_peak(self):
        rows = calculate(self.data)
        self.assertEqual([r['down_mb_day'] for r in rows], [310000, 132000, 132000, 574000])
        self.assertAlmostEqual(rows[-1]['peak_down_mbps'], 340.148148148)
        self.assertAlmostEqual(rows[-1]['design_down_mbps'], 583.111111111)
        self.assertAlmostEqual(rows[-1]['design_up_mbps'], 142.222222222)
        self.assertEqual(rows[-1]['guest_upload'], 'UNKNOWN')

    def test_server_total_scopes_not_multiplied_by_devices(self):
        total = calculate(self.data, server_scope="global")
        self.assertEqual(len(total), 1)  # No arbitrary allocation of a global total to sites.
        self.assertEqual((total[0]['down_mb_day'], total[0]['up_mb_day']), (561000, 114000))
        per_site = calculate(self.data, server_scope="per-site")[-1]
        self.assertEqual((per_site['down_mb_day'], per_site['up_mb_day']), (563000, 118000))

    def test_guest_increment_and_unknown_upload(self):
        row = calculate(self.data, guests=(100, 100, 100))[-1]
        self.assertAlmostEqual(row['design_down_mbps'], 735.492063492)
        self.assertAlmostEqual(row['design_up_mbps'], 142.222222222)
        self.assertEqual(row['guest_upload'], 'UNKNOWN')
        self.assertEqual(calculate(self.data, guest_scope="global")[-1]['down_mb_day'], 574500)

    def test_overhead_shares_and_guest_upload_are_independent(self):
        row = calculate(self.data, guests=(10, 0, 0), guest_upload=100,
                        overhead=0.1, down_share=0.4, up_share=0.6)[-1]
        self.assertEqual(row['up_mb_day'], 141000)
        self.assertAlmostEqual(row['internet_up_mbps'], 141000 * 8 * 0.8 / 10800 * 1.2 * 1.1 / 0.7 * 0.6)
        self.assertAlmostEqual(row['internet_down_mbps'] / row['design_down_mbps'], 0.4)

    def test_site_sum_matches_total(self):
        rows = calculate(self.data, guests=(57, 13, 29), guest_upload=17, overhead=0.12)
        for key in ('down_mb_day', 'up_mb_day', 'design_down_mbps', 'design_up_mbps'):
            self.assertAlmostEqual(sum(r[key] for r in rows[:-1]), rows[-1][key])

    def test_reject_invalid_inputs(self):
        for args in ({'guests': (-1, 0, 0)}, {'guests': (0.5, 0, 0)}, {'overhead': -0.1},
                     {'down_share': 1.1}, {'up_share': -1}, {'guest_upload': -1},
                     {'overhead': float('nan')}, {'guest_upload': float('inf')}):
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate(self.data, **args)
        for key in ('target_utilization', 'peak_window', 'peak_fraction'):
            broken = self.data.copy()
            broken[key, 'all'] = 0
            with self.subTest(key=key), self.assertRaises(ValueError):
                calculate(broken)


if __name__ == '__main__':
    unittest.main()
