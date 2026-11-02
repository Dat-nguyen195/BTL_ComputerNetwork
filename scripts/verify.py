#!/usr/bin/env python3
"""Run all offline checks; never marks simulation test cases PASS."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    checks = [
        ['check_docs.py'], ['build_lab.py', '--check'], ['test_capacity.py'],
        ['check_wan.py'], ['check_wan.py', '--config-dir', 'simulation/generated/configs'],
        ['check_security.py'], ['check_inventory.py'],
    ]
    for script, *args in checks:
        print(f"\n$ python3 scripts/{script} {' '.join(args)}".rstrip(), flush=True)
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *args], cwd=ROOT)
        if result.returncode:
            return result.returncode
    print('\nALL OFFLINE CHECKS OK. TC01-TC06 / VPN / IDS-IPS runtime remain NOT RUN.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
