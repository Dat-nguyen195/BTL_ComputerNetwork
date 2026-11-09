#!/usr/bin/env python3
"""Verify the exact report files covered by recorded visual QA and standalone compilation."""
import hashlib
import json
from pathlib import Path
import zipfile
from build_report import LATEX_FILES

ROOT = Path(__file__).resolve().parents[1]


def main():
    qa = json.loads((ROOT / 'test_results/report-latex/qa.json').read_text(encoding='utf-8'))
    assert qa['status'] == 'PASS' and qa['all_seven_steps_present']
    assert qa['standalone_text_matches_delivered_pdf']
    assert qa['visual_review']['status'] == 'PASS'
    assert qa['visual_review']['pages_rendered_and_inspected'] == list(range(1, qa['pages'] + 1))
    for name, expected in qa['sha256'].items():
        data = (ROOT / name).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != expected and hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() == expected:
            digest = expected
        assert digest == expected, 'Report changed since recorded QA: ' + name
    pdf = ROOT / 'docs/06-report/final/report.pdf'
    assert pdf.read_bytes().startswith(b'%PDF-')
    latex = ROOT / 'docs/06-report/latex'
    expected_names = set(LATEX_FILES)
    with zipfile.ZipFile(ROOT / 'docs/06-report/final/report-latex.zip') as archive:
        assert set(archive.namelist()) == expected_names, 'Unexpected standalone LaTeX bundle contents'
        for name in expected_names:
            assert archive.read(name) == (latex / name).read_bytes(), 'Standalone bundle differs: ' + name
    tex = (latex / 'report.tex').read_text(encoding='utf-8')
    assert tex.startswith('% !TeX program = xelatex'), 'Missing editor engine hint'
    assert 'requires XeLaTeX' in tex, 'Missing readable pdfLaTeX diagnostic'
    assert all(name in tex for name in ('main-cisco.pdf', 'aux-cisco.pdf','wan-cisco.pdf','gpon-cisco.pdf','security-cisco.pdf','wifi-cisco.pdf','mpls-cisco.pdf','vpn-cisco.pdf'))
    assert '$pdf_mode = 5' in (latex / '.latexmkrc').read_text(encoding='utf-8')
    print(f"OK: report/PDF/source hashes match recorded {qa['pages']}-page visual QA; standalone LaTeX bundle matches source")
    print('This check validates existing QA evidence; it does not render or recompile the PDF.')
    supplement = json.loads((ROOT / 'test_results/packet-tracer/report-qa.json').read_text(encoding='utf-8'))
    assert supplement['status'] == 'PASS' and supplement['pages'] == 2
    assert supplement['visual_review']['status'] == 'PASS'
    assert supplement['visual_review']['pages_rendered_and_inspected'] == [1, 2]
    for name, expected in supplement['sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, 'Supplement changed since visual QA: ' + name
    assert hashlib.sha256((ROOT / 'simulation/packet-tracer/hospital-3sites.pkt').read_bytes()).hexdigest() == supplement['runtime_native_sha256']
    print('OK: 2-page Packet Tracer supplement/source/generator hashes match visual QA and the tested native lab')


if __name__ == '__main__':
    main()
