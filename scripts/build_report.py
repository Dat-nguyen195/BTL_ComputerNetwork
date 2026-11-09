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
from integrate_report import integrate, NAMES

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/06-report/source/report.md'
LATEX_FILES = ('report.tex', 'header.tex', 'cover.tex', 'metadata.tex', 'README.md',
               'fonts.tex', '.latexmkrc', 'assets/logo-bach-khoa.png',
               'assets/topology.pdf', 'assets/physical-main.pdf', 'assets/physical-aux.pdf')
LATEX_FILES += tuple('assets/'+n+'.pdf' for n in NAMES)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime-run',default='after-firewall-restart-runtime');p.add_argument('--reopen-run',default='after-reopen-runtime')
    p.add_argument('--engine', choices=['xelatex', 'tectonic'], default='xelatex')
    p.add_argument('--reuse-diagrams', action='store_true', help='Reuse reviewed vector PDF diagrams when SVG sources have not changed')
    a=p.parse_args()
    runs=[]
    for name in [a.runtime_run,a.reopen_run]:
        path=ROOT/'test_results/runtime'/name/'results.json'
        if not path.is_file():p.error('Missing evidence: '+str(path))
        data=json.loads(path.read_text())
        if any(c['status']!='PASS' for c in data['cases']):p.error('Cannot publish passing summary from failed run '+name)
        runs.append(data)
    text=SOURCE.read_text()
    appendix=['\n\\clearpage\n\n# Phụ lục A - Kết quả chạy thực tế\n',
              'Bảng này được dựng từ JSON evidence; số lần kiểm bao gồm hai lượt smoke trong ca failover. Không quy đổi thành điểm môn học hoặc SLA.\n']
    for r in runs:
        counts=Counter(c['group'] for c in r['cases']);appendix+=['\n\\Needspace{22\\baselineskip}\n\n## Run '+r['run_id']+'\n',
            'Thời điểm UTC: '+r['timestamp_utc']+'. Nền tảng GNS3 '+r['platform']['version']+'.\n',
            '| Nhóm kiểm | Số kiểm tra | Kết quả |\n|:---|---:|:---|']
        appendix += [f'| {g} | {n} | PASS |' for g,n in sorted(counts.items())]
        appendix += ['\nTổng '+str(len(r['cases']))+' kiểm tra, không có FAIL trong lần chạy này.\n']
        timings=[c['convergence_seconds'] for c in r['cases'] if c['group']=='ISP-CONVERGENCE']
        if timings:appendix += ['Mất upstream ISP1/ISP2: phục hồi HTTP từ năm endpoint lần lượt '+', '.join(str(x)+' giây' for x in timings)+'. Có gián đoạn tạm thời trong các sample; không phải chuyển mạch không mất phiên.\n']
        appendix += ['Image ID của tag trong controller tại thời điểm test: `'+r['image_id']+'`.\n',
                     'Evidence: `test_results/runtime/'+r['run_id']+'/results.json`; SHA256 `'+hashlib.sha256((ROOT/'test_results/runtime'/r['run_id']/'results.json').read_bytes()).hexdigest()+'`.\n']
    persistence=json.loads((ROOT/'test_results/runtime/persistence/reopen.json').read_text())
    if persistence['status']!='PASS' or not persistence['loaded_committed_template']:p.error('Committed GNS3 project must pass reopen first')
    appendix += ['\n## Đối chiếu phiên bản và lỗi ban đầu\n',
                 'File GNS3 bàn giao được chép lại từ source, mở bằng chính GNS3 và chạy lại smoke. Có52 node (9 router/firewall,5 switch,38 endpoint),52 link. Hash project đã thử: `'+persistence['project_sha256']+'`.\n',
                 'Run initial-runtime giữ hai FAIL khi thử HTTP ở Aux ngay sau Edge chuyển trạng thái; OSPF/default chưa hội tụ. Bộ thử sau đó đo cả quá trình từ fault tới phục hồi đầu cuối, lưu các sample gián đoạn và kiểm lại sau hội tụ. Không xóa evidence lỗi ban đầu hoặc diễn giải thành zero-downtime.\n',
                 'Bản hiện tại sửa PID Suricata còn sót sau khi dừng container. Hai chu kỳ dừng/bật firewall đã xác nhận tiến trình Suricata sống và HTTP phục hồi; lần kiểm đầy đủ sau sửa đạt209/209. Source được cập nhật trong container hiện có, còn image mới được build/load cho lần tạo node sau. Base image ID của từng container và phép kiểm restart nằm tại `test_results/runtime/firewall-restart/restart.json`; hash file đang chạy được kiểm riêng trong `persistence/live-provenance.json`. Lần reopen137 kiểm ở trên là bằng chứng lịch sử trước bản sửa PID, không được diễn giải thành kiểm reopen lại source mới.\n',
                 '\n\\clearpage\n\n# Phụ lục B - Tái lập và danh mục sản phẩm\n',
                 'Các lệnh được chạy ở root repository trên Linux có Docker. Lần đầu dựng cần Internet để tải package/image, đủ RAM/disk; không cần IOS image có bản quyền.\n',
                 '```bash\npython3 scripts/verify.py\npython3 scripts/gns3_lab.py bootstrap\npython3 scripts/test_gns3_runtime.py --failover\npython3 scripts/gns3_lab.py status\n```\n',
                 'Trên máy đã có lab, dùng `start` hoặc `reopen`, không bootstrap lần hai đè môi trường. Xem `simulation/gns3/README.md` để mở GUI, xây image trên compute khác và dừng lab. Bản nộp kèm `submission/SHA256SUMS` và gói ZIP; việc đóng gói không thay phê duyệt hoặc biên nhận BKeL.\n']
    appendix.append((ROOT/'docs/06-report/source/design-appendices.md').read_text(encoding='utf-8'))
    proof_path=ROOT/'test_results/runtime/controller-restart/restart.json'
    if proof_path.is_file():
        proof=json.loads(proof_path.read_text(encoding='utf-8'))
        if proof['status']!='PASS':p.error('Current controller restart proof has not passed')
        appendix += ['\n\\clearpage\n\n# Phụ lục G - Kiểm tra trực tiếp trước nộp ngày 05/11/2026\n',
                     'Đã sửa lỗi controller GNS3 không lên sau stop/start do PID/socket Docker cũ. Entrypoint tạo exec-root mới mỗi lần bật, giữ dữ liệu image/project trong volume riêng. Lệnh start tự mở project đã lưu nếu server khởi động với project ở trạng thái closed. Hai lần bật controller đã xác nhận đủ52 node started, Docker/API hoạt động và hash entrypoint thực khớp source.\n',
                     '| Lần chạy | Phạm vi | Số kiểm tra | Kết quả |\n|:------------------------|:--------------------------------------|------:|:--------|']
        for index,name in enumerate(proof['runs']):
            current=json.loads((ROOT/name).read_text(encoding='utf-8'))
            if any(c['status']!='PASS' for c in current['cases']):p.error('Fresh runtime contains failures: '+name)
            appendix.append('| '+current['run_id']+' | '+('Sáu nhóm, DHCP/DNS, IDS/IPS, PBR và lỗi hai ISP' if index==0 else 'Sau restart controller: sáu nhóm, OSPF, DHCP/DNS, IDS/IPS')+' | '+str(len(current['cases']))+' | PASS |')
        fresh=json.loads((ROOT/proof['runs'][0]).read_text(encoding='utf-8'))
        timings=[str(c['convergence_seconds']) for c in fresh['cases'] if c['group']=='ISP-CONVERGENCE']
        appendix += ['\nThời gian phục hồi HTTP trong lượt mới khi mất upstream ISP1/ISP2 là '+', '.join(timings)+' giây. Đây là kết quả của lần chạy, không phải SLA hoặc chuyển mạch không mất phiên.\n',
                     'File code/config thực của52 node khớp nguồn. Các kết quả cũ ở phụ lục A được giữ nguyên để truy vết; lượt kiểm mới nằm tại `test_results/runtime/submission-20261105/` và `test_results/runtime/submission-reopen-20261105/`. Chứng cứ restart và hash ở `test_results/runtime/controller-restart/`. Kiểm offline bằng `scripts/check_gns3.py` xác nhận tính toàn vẹn, không tự chạy lại mạng.\n',
                     'Đã chốt Packet Tracer về đúng byte của bản native có evidence32+4; bản lưu lại chỉ khác đồng hồ/môi trường được bảo toàn trong backup local. Lượt05/11 không chạy lại Packet Tracer; không gán kết quả mới của GNS3 cho Cisco IOS.\n']
    assembled=text.replace('# Phạm vi, yêu cầu', r'\clearpage'+'\n\n# Phạm vi, yêu cầu',1)+'\n'.join(appendix)
    assembled=integrate(assembled)
    tmp=ROOT/'tmp/pdfs';tmp.mkdir(parents=True,exist_ok=True)
    latex=ROOT/'docs/06-report/latex';assets=latex/'assets'
    if not (assets/'logo-bach-khoa.png').is_file():p.error('Missing supplied Bach Khoa logo')
    if not a.reuse_diagrams:
        import cairosvg
    for name, source in [('topology', ROOT/'docs/06-report/source/topology.svg'),
                         ('physical-main', ROOT/'docs/02-design/diagrams/exports/physical-main.svg'),
                         ('physical-aux', ROOT/'docs/02-design/diagrams/exports/physical-aux.svg')]:
        if a.reuse_diagrams:
            if not (assets/(name+'.pdf')).is_file():
                p.error('Missing existing vector diagram: '+name)
        else:
            cairosvg.svg2pdf(url=str(source), write_to=str(assets/(name+'.pdf')))
    assembled=assembled.replace('\n## Packet Tracer - mô hình Cisco ba cơ sở', '\n!['+'Mô hình chức năng; cấu trúc vật lý và GPON có sơ đồ riêng trong bộ thiết kế.'+'](topology.svg){width=100%}\n\n## Packet Tracer - mô hình Cisco ba cơ sở')
    if '](topology.svg)' not in assembled and 'wan-cisco.pdf' not in assembled:
        assembled=assembled.replace('### Packet Tracer - mô hình Cisco ba cơ sở', '![Sơ đồ logic mô hình ba cơ sở và Internet tập trung.](topology.svg){width=100%}\n\n### Packet Tracer - mô hình Cisco ba cơ sở')
    (ROOT/'docs/06-report/source/report-with-evidence.md').write_text(assembled)
    build_input=tmp/'report-build.md'
    pdf_text=re.sub(r'\A---\n.*?\n---\n', '', assembled, count=1, flags=re.S)
    pdf_text=pdf_text.replace('(../latex/assets/', '(assets/')
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
