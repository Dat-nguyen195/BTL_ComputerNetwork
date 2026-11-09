#!/usr/bin/env python3
"""Build the technical report PDF directly from editable LaTeX source."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LATEX_DIR = ROOT / 'docs/06-report/latex'
FINAL_DIR = ROOT / 'docs/06-report/final'

NAMES = ('wan-cisco', 'main-cisco', 'aux-cisco', 'gpon-cisco', 'security-cisco',
         'wifi-cisco', 'mpls-cisco', 'vpn-cisco', 'layers-cisco', 'camera-cisco')
LATEX_FILES = ('report.tex', 'header.tex', 'cover.tex', 'metadata.tex', 'README.md',
               'fonts.tex', '.latexmkrc', 'assets/logo-bach-khoa.png',
               'assets/topology.pdf', 'assets/physical-main.pdf', 'assets/physical-aux.pdf')
LATEX_FILES += tuple('assets/' + n + '.pdf' for n in NAMES)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine', choices=['xelatex', 'tectonic'], default='xelatex')
    p.add_argument('--reuse-diagrams', action='store_true', default=True,
                   help='Keep existing vector PDF diagrams in assets/')
    a = p.parse_args()

    tex = LATEX_DIR / 'report.tex'
    if not tex.is_file():
        p.error(f'Missing LaTeX source: {tex}')

    output = ROOT / 'output/pdf'
    output.mkdir(parents=True, exist_ok=True)

    print(f'Compiling {tex.relative_to(ROOT)} with {a.engine}...')
    if a.engine == 'tectonic':
        command = ['tectonic', '--keep-logs', '--outdir', str(output), 'report.tex']
        subprocess.run(command, cwd=LATEX_DIR, check=True)
    else:
        # Run XeLaTeX passes
        for run in range(1, 4):
            command = ['xelatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
                       '-output-directory=' + str(output), 'report.tex']
            result = subprocess.run(command, cwd=LATEX_DIR, text=True, encoding='utf-8',
                                    errors='replace', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f'XeLaTeX failed on pass {run}:\n' + result.stdout[-5000:])

    # Copy output to final and preview destinations
    final_pdf = FINAL_DIR / 'report.pdf'
    final_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output / 'report.pdf', final_pdf)
    shutil.copy2(output / 'report.pdf', LATEX_DIR / 'report.pdf')
    (LATEX_DIR / 'build').mkdir(parents=True, exist_ok=True)
    shutil.copy2(output / 'report.pdf', LATEX_DIR / 'build/report.pdf')

    # Create standalone ZIP bundle
    bundle = FINAL_DIR / 'report-latex.zip'
    files = [LATEX_DIR / n for n in LATEX_FILES]
    with zipfile.ZipFile(bundle, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(LATEX_DIR).as_posix(), date_time=(2026, 11, 2, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    print('Built editable source:', tex.relative_to(ROOT))
    print('Built PDF:', final_pdf.relative_to(ROOT), hashlib.sha256(final_pdf.read_bytes()).hexdigest())
    print('Built standalone XeLaTeX bundle:', bundle.relative_to(ROOT))


if __name__ == '__main__':
    main()
