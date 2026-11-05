#!/usr/bin/env python3
"""Regression checks for portable generation and a complete, tamper-evident handoff."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import build_gns3
import package_submission as package


class DeliveryTests(unittest.TestCase):
    def test_runtime_bytes_still_match_tested_build(self):
        generated = build_gns3.artifacts()
        tested = json.loads((build_gns3.ROOT / 'test_results/runtime/persistence/runtime-manifest-tested.json').read_text(encoding='utf-8'))
        for name, expected in tested['sha256'].items():
            self.assertEqual(package.digest(generated[name].encode('utf-8')), expected, name)
        manifest = json.loads(generated['runtime-manifest.json'])
        self.assertTrue(all('\\' not in name for name in manifest['source_sha256']))

    def exercise_package(self, mutate=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'submission').mkdir()
            (root / '.git').mkdir()
            files = {name: b'test data' for name in (
                'docs/06-report/final/report.pdf',
                'simulation/gns3/hospital-3sites.gns3',
                'test_results/runtime/after-reopen-runtime/results.json')}
            files['docs/tieng-viet.md'] = 'Bệnh viện ba cơ sở\n'.encode('utf-8')
            for name, data in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            with patch.multiple(package, ROOT=root, ZIP=root/'submission/hospital-network-delivery.zip',
                                MANIFEST=root/'submission/package-manifest.json', SUMS=root/'submission/SHA256SUMS'), \
                 patch.object(package, 'selected', return_value=files), contextlib.redirect_stdout(io.StringIO()):
                with patch.object(sys, 'argv', ['package_submission.py']):
                    package.main()
                if mutate:
                    mutate(root)
                with patch.object(sys, 'argv', ['package_submission.py', '--check']):
                    package.main()

    def test_complete_package_roundtrip(self):
        self.exercise_package()

    def test_unpacked_delivery_without_git_is_verifiable(self):
        def unpack(root):
            archive_path = root / 'submission/hospital-network-delivery.zip'
            with zipfile.ZipFile(archive_path) as archive:
                internal_sums = archive.read('submission/SHA256SUMS')
            (root / 'submission/SHA256SUMS').write_bytes(internal_sums)
            archive_path.unlink()
            (root / '.git').rmdir()
        self.exercise_package(unpack)

    def test_empty_checksum_list_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'checksum list'):
            self.exercise_package(lambda root: (root/'submission/SHA256SUMS').write_bytes(b''))

    def test_missing_checksum_is_rejected(self):
        def truncate(root):
            path = root/'submission/SHA256SUMS'
            path.write_bytes(b'\n'.join(path.read_bytes().splitlines()[1:])+b'\n')
        with self.assertRaisesRegex(AssertionError, 'checksum list'):
            self.exercise_package(truncate)

    def test_tampered_zip_is_rejected(self):
        def tamper(root):
            path = root/'submission/hospital-network-delivery.zip'
            with zipfile.ZipFile(path) as archive:
                contents = {name: archive.read(name) for name in archive.namelist()}
            contents['docs/tieng-viet.md'] = b'changed'
            with zipfile.ZipFile(path, 'w') as archive:
                for name, data in contents.items():
                    archive.writestr(name, data)
        with self.assertRaisesRegex(AssertionError, 'tieng-viet'):
            self.exercise_package(tamper)


if __name__ == '__main__':
    unittest.main()
