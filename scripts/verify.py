#!/usr/bin/env python3
"""Run all offline checks; never marks simulation test cases PASS."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    # Windows otherwise decodes Vietnamese sources using the local ANSI code page.
    os.environ['PYTHONUTF8'] = '1'
    checks = [
        ['check_docs.py'], ['build_lab.py', '--check'], ['build_campus.py', '--check'], ['test_capacity.py'],
        ['check_wan.py'], ['check_wan.py', '--config-dir', 'simulation/generated/configs'],
        ['check_security.py'], ['check_inventory.py'], ['check_lan.py'], ['build_gns3.py', '--check'], ['check_gns3.py'],
        ['build_packet_tracer.py', '--check'], ['test_packet_results.py'], ['check_packet_runtime.py'],
        ['build_mpls.py', '--check'], ['test_mpls_evidence.py'], ['check_mpls.py'], ['test_delivery.py'], ['check_report.py'],
    ]
    for script, *args in checks:
        print(f"\n$ python3 scripts/{script} {' '.join(args)}".rstrip(), flush=True)
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *args], cwd=ROOT)
        if result.returncode:
            return result.returncode
    print('\nALL OFFLINE CHECKS OK. Runtime evidence is recorded separately under test_results/runtime/; these checks do not execute the network.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
