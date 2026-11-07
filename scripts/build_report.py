#!/usr/bin/env python3
"""Build the editable technical report and PDF with actual GNS3 evidence tables."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/06-report/source/report.md'
LATEX_FILES = ('report.tex', 'header.tex', 'cover.tex', 'metadata.tex', 'README.md',
               'fonts.tex', '.latexmkrc', 'assets/logo-bach-khoa.png',
               'assets/topology.pdf', 'assets/physical-main.pdf', 'assets/physical-aux.pdf')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime-run',default='after-firewall-restart-runtime');p.add_argument('--reopen-run',default='after-reopen-runtime')
    p.add_argument('--engine', choices=['xelatex', 'tectonic'], default='xelatex')
    a=p.parse_args()
    runs=[]
    for name in [a.runtime_run,a.reopen_run]:
        path=ROOT/'test_results/runtime'/name/'results.json'
        if not path.is_file():p.error('Missing evidence: '+str(path))
        data=json.loads(path.read_text())
        if any(c['status']!='PASS' for c in data['cases']):p.error('Cannot publish passing summary from failed run '+name)
        runs.append(data)
    persistence=json.loads((ROOT/'test_results/runtime/persistence/reopen.json').read_text())
    if persistence['status']!='PASS' or not persistence['loaded_committed_template']:p.error('Committed GNS3 project must pass reopen first')
    proof_path=ROOT/'test_results/runtime/controller-restart/restart.json'
    if proof_path.is_file():
        proof=json.loads(proof_path.read_text(encoding='utf-8'))
        if proof['status']!='PASS':p.error('Current controller restart proof has not passed')
        for index,name in enumerate(proof['runs']):
            current=json.loads((ROOT/name).read_text(encoding='utf-8'))
            if any(c['status']!='PASS' for c in current['cases']):p.error('Fresh runtime contains failures: '+name)
    text=SOURCE.read_text(encoding='utf-8')
    assembled=text.replace('# Giới thiệu', r'\clearpage'+'\n\n# Giới thiệu',1)
    tmp=ROOT/'tmp/pdfs';tmp.mkdir(parents=True,exist_ok=True)
    latex=ROOT/'docs/06-report/latex';assets=latex/'assets'
    if not (assets/'logo-bach-khoa.png').is_file():p.error('Missing supplied Bach Khoa logo')
    import cairosvg
    for name, source in [('topology', ROOT/'docs/06-report/source/topology.svg'),
                         ('physical-main', ROOT/'docs/02-design/diagrams/exports/physical-main.svg'),
                         ('physical-aux', ROOT/'docs/02-design/diagrams/exports/physical-aux.svg')]:
        cairosvg.svg2pdf(url=str(source), write_to=str(assets/(name+'.pdf')))
    assembled=assembled.replace('## Packet Tracer - mô hình Cisco ba cơ sở', '!['+'Mô hình chức năng; cấu trúc vật lý và GPON có sơ đồ riêng trong bộ thiết kế.'+'](topology.svg){width=100%}\n\n## Packet Tracer - mô hình Cisco ba cơ sở')
    (ROOT/'docs/06-report/source/report-with-evidence.md').write_text(assembled)
    build_input=tmp/'report-build.md'
    pdf_text=re.sub(r'\A---\n.*?\n---\n', '', assembled, count=1, flags=re.S)
    for name in ('topology', 'physical-main', 'physical-aux'):
        pdf_text=pdf_text.replace('('+name+'.svg)', '(assets/'+name+'.pdf)')
        pdf_text=pdf_text.replace('(../../02-design/diagrams/exports/'+name+'.svg)', '(assets/'+name+'.pdf)')
    pdf_text=re.sub(r'`((?:sha256:)?[0-9a-f]{64})`', lambda m:r'\nolinkurl{'+m[1]+'}', pdf_text)
    pdf_text=re.sub(r'`(\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?)`', lambda m:r'\nolinkurl{'+m[1]+'}', pdf_text)
    pdf_text=re.sub(r'`([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+/?)`', lambda m:r'\nolinkurl{'+m[1]+'}', pdf_text)
    build_input.write_text(pdf_text)
    # Keep the complete .tex and its inputs in the handoff, rather than only
    # Pandoc's temporary LaTeX. The folder builds without Python or Pandoc.
    header=tmp/'header-ref.tex';header.write_text('\\input{header.tex}\n')
    cover=tmp/'cover-ref.tex';cover.write_text('\\input{cover.tex}\n')
    tex=latex/'report.tex'
    args=['pandoc',str(build_input),'-o',str(tex),'--standalone','--to=latex',
          '--toc','--number-sections','--include-in-header',str(header),'--include-before-body',str(cover),
          '-V','fontsize=11pt','-V','geometry:a4paper,margin=22mm','-V','linestretch=1.08',
          '-V','colorlinks=true','-V','linkcolor=BKBlue','-V','urlcolor=BKBlue','-V','toccolor=BKBlue','-V','toc-depth=2']
    subprocess.run(args,cwd=latex,check=True)
    # Honour editor engine hints and fail early with a useful message under pdfTeX.
    generated=tex.read_text(encoding='utf-8')
    guard=('% !TeX program = xelatex\n% !TeX encoding = UTF-8\n'
           '\\RequirePackage{iftex}\n\\ifPDFTeX\n'
           '\\errmessage{This Vietnamese report requires XeLaTeX. Select the XeLaTeX recipe or run latexmk -xelatex report.tex}\n'
           '\\expandafter\\endinput\n\\fi\n')
    tex.write_text(guard+generated, encoding='utf-8', newline='\n')
    output=ROOT/'output/pdf';output.mkdir(parents=True,exist_ok=True)
    for run in range(1, 2 if a.engine=='tectonic' else 4):
        command = (['tectonic', '--keep-logs', '--outdir', str(output), 'report.tex'] if a.engine=='tectonic' else
                   ['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
                    '-output-directory='+str(output),'report.tex'])
        result=subprocess.run(command,cwd=latex,text=True,encoding='utf-8',errors='replace',
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (tmp/f'xelatex-pass-{run}.txt').write_text(result.stdout)
        if result.returncode:raise RuntimeError(a.engine+' failed:\n'+result.stdout[-5000:])
    final=ROOT/'docs/06-report/final/report.pdf';final.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(output/'report.pdf',final)
    bundle=final.with_name('report-latex.zip')
    files=[latex/n for n in LATEX_FILES]
    with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info=zipfile.ZipInfo(path.relative_to(latex).as_posix(),date_time=(2026,11,2,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            archive.writestr(info,path.read_bytes())
    build_input.unlink()
    print('Built editable source',tex.relative_to(ROOT))
    print('Built',final.relative_to(ROOT),hashlib.sha256(final.read_bytes()).hexdigest())
    print('Built standalone XeLaTeX bundle',bundle.relative_to(ROOT))

if __name__=='__main__':main()
