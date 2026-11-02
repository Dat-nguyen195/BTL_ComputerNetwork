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


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime-run',default='after-firewall-restart-runtime');p.add_argument('--reopen-run',default='after-reopen-runtime');a=p.parse_args()
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
    assembled=text.replace('# Phạm vi, yêu cầu', r'\clearpage'+'\n\n# Phạm vi, yêu cầu',1)+'\n'.join(appendix)
    tmp=ROOT/'tmp/pdfs';tmp.mkdir(parents=True,exist_ok=True)
    import cairosvg
    latex=ROOT/'docs/06-report/latex';assets=latex/'assets'
    if not (assets/'logo-bach-khoa.png').is_file():p.error('Missing supplied Bach Khoa logo')
    figure=assets/'topology.pdf'
    cairosvg.svg2pdf(url=str(ROOT/'docs/06-report/source/topology.svg'),write_to=str(figure))
    assembled=assembled.replace('# Chính sách bảo mật và kiểm thử - Step5', '!['+'Mô hình chức năng; cấu trúc vật lý và GPON có sơ đồ riêng trong bộ thiết kế.'+'](topology.svg){width=100%}\n\n# Chính sách bảo mật và kiểm thử - Step5')
    (ROOT/'docs/06-report/source/report-with-evidence.md').write_text(assembled)
    build_input=tmp/'report-build.md'
    pdf_text=re.sub(r'\A---\n.*?\n---\n', '', assembled, count=1, flags=re.S)
    pdf_text=pdf_text.replace('(topology.svg)', '(assets/topology.pdf)')
    pdf_text=re.sub(r'`((?:sha256:)?[0-9a-f]{64})`', lambda m:r'\nolinkurl{'+m[1]+'}', pdf_text)
    pdf_text=re.sub(r'`(\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?)`', lambda m:r'\nolinkurl{'+m[1]+'}', pdf_text)
    build_input.write_text(pdf_text)
    # Keep the complete .tex and its inputs in the handoff, rather than only
    # Pandoc's temporary LaTeX. The folder builds without Python or Pandoc.
    header=tmp/'header-ref.tex';header.write_text('\\input{header.tex}\n')
    cover=tmp/'cover-ref.tex';cover.write_text('\\input{cover.tex}\n')
    tex=latex/'report.tex'
    args=['pandoc',str(build_input),'-o',str(tex),'--standalone','--to=latex',
          '--toc','--number-sections','--include-in-header',str(header),'--include-before-body',str(cover),
          '-V','mainfont=DejaVu Serif','-V','sansfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono',
          '-V','fontsize=11pt','-V','geometry:a4paper,margin=22mm','-V','linestretch=1.08',
          '-V','colorlinks=true','-V','linkcolor=BKBlue','-V','urlcolor=BKBlue','-V','toccolor=BKBlue','-V','toc-depth=2']
    subprocess.run(args,cwd=latex,check=True)
    output=ROOT/'output/pdf';output.mkdir(parents=True,exist_ok=True)
    for run in range(1,4):
        result=subprocess.run(['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
                               '-output-directory='+str(output),'report.tex'],cwd=latex,text=True,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (tmp/f'xelatex-pass-{run}.txt').write_text(result.stdout)
        if result.returncode:raise RuntimeError('XeLaTeX failed:\n'+result.stdout[-5000:])
    final=ROOT/'docs/06-report/final/report.pdf';final.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(output/'report.pdf',final)
    bundle=final.with_name('report-latex.zip')
    files=[latex/n for n in ('report.tex','header.tex','cover.tex','metadata.tex','README.md','assets/logo-bach-khoa.png','assets/topology.pdf')]
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
