#!/usr/bin/env python3
"""Build the editable technical report and PDF with actual GNS3 evidence tables."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/06-report/source/report.md'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime-run',default='validated-runtime');p.add_argument('--reopen-run',default='after-reopen-runtime');a=p.parse_args()
    runs=[]
    for name in [a.runtime_run,a.reopen_run]:
        path=ROOT/'test_results/runtime'/name/'results.json'
        if not path.is_file():p.error('Missing evidence: '+str(path))
        data=json.loads(path.read_text())
        if any(c['status']!='PASS' for c in data['cases']):p.error('Cannot publish passing summary from failed run '+name)
        runs.append(data)
    text=SOURCE.read_text()
    appendix=['\n# Phụ lục A - Kết quả chạy thực tế\n',
              'Bảng này được dựng từ JSON evidence; số lần kiểm bao gồm hai lượt smoke trong ca failover. Không quy đổi thành điểm môn học hoặc SLA.\n']
    for r in runs:
        counts=Counter(c['group'] for c in r['cases']);appendix+=['\n## Run '+r['run_id']+'\n',
            'Thời điểm UTC: '+r['timestamp_utc']+'. Nền tảng GNS3 '+r['platform']['version']+'.\n',
            '| Nhóm kiểm | Số kiểm tra | Kết quả |\n|:---|---:|:---|']
        appendix += [f'| {g} | {n} | PASS |' for g,n in sorted(counts.items())]
        appendix += ['\nTổng '+str(len(r['cases']))+' kiểm tra, không có FAIL trong lần chạy này.\n']
        timings=[c['convergence_seconds'] for c in r['cases'] if c['group']=='ISP-CONVERGENCE']
        if timings:appendix += ['Mất upstream ISP1/ISP2: phục hồi HTTP từ năm endpoint lần lượt '+', '.join(str(x)+' giây' for x in timings)+'. Có gián đoạn tạm thời trong các sample; không phải chuyển mạch không mất phiên.\n']
        appendix += ['Image ID: `'+r['image_id']+'`.\n',
                     'Evidence: `test_results/runtime/'+r['run_id']+'/results.json`; SHA256 `'+hashlib.sha256((ROOT/'test_results/runtime'/r['run_id']/'results.json').read_bytes()).hexdigest()+'`.\n']
    persistence=json.loads((ROOT/'test_results/runtime/persistence/reopen.json').read_text())
    if persistence['status']!='PASS' or not persistence['loaded_committed_template']:p.error('Committed GNS3 project must pass reopen first')
    appendix += ['\n## Đối chiếu phiên bản và lỗi ban đầu\n',
                 'File GNS3 bàn giao được chép lại từ source, mở bằng chính GNS3 và chạy lại smoke. Có52 node (9 router/firewall,5 switch,38 endpoint),52 link. Hash project đã thử: `'+persistence['project_sha256']+'`.\n',
                 'Run initial-runtime giữ hai FAIL khi thử HTTP ở Aux ngay sau Edge chuyển trạng thái; OSPF/default chưa hội tụ. Bộ thử sau đó đo cả quá trình từ fault tới phục hồi đầu cuối, lưu các sample gián đoạn và kiểm lại sau hội tụ. Không xóa evidence lỗi ban đầu hoặc diễn giải thành zero-downtime.\n',
                 '\n# Phụ lục B - Tái lập và danh mục sản phẩm\n',
                 'Các lệnh được chạy ở root repository trên Linux có Docker. Lần đầu dựng cần Internet để tải package/image, đủ RAM/disk; không cần IOS image có bản quyền.\n',
                 '```bash\npython3 scripts/verify.py\npython3 scripts/gns3_lab.py bootstrap\npython3 scripts/test_gns3_runtime.py --failover\npython3 scripts/gns3_lab.py status\n```\n',
                 'Trên máy đã có lab, dùng `start` hoặc `reopen`, không bootstrap lần hai đè môi trường. Xem `simulation/gns3/README.md` để mở GUI, xây image trên compute khác và dừng lab. Bản nộp kèm `submission/SHA256SUMS` và gói ZIP; việc đóng gói không thay phê duyệt hoặc biên nhận BKeL.\n']
    assembled=text.replace('# Phạm vi, yêu cầu', r'\clearpage'+'\n\n# Phạm vi, yêu cầu',1)+'\n'.join(appendix)
    tmp=ROOT/'tmp/pdfs';tmp.mkdir(parents=True,exist_ok=True)
    import cairosvg
    figure=tmp/'topology.png'
    cairosvg.svg2png(url=str(ROOT/'docs/06-report/source/topology.svg'),write_to=str(figure),output_width=2000,output_height=1280)
    assembled=assembled.replace('# Chính sách bảo mật và kiểm thử - Step5', '!['+'Mô hình chức năng; cấu trúc vật lý và GPON có sơ đồ riêng trong bộ thiết kế.'+'](topology.svg){width=100%}\n\n# Chính sách bảo mật và kiểm thử - Step5')
    (ROOT/'docs/06-report/source/report-with-evidence.md').write_text(assembled)
    build_input=tmp/'report-build.md'
    pdf_text=assembled.replace('(topology.svg)', '('+str(figure)+')')
    pdf_text=re.sub(r'`((?:sha256:)?[0-9a-f]{64})`', lambda m:r'\nolinkurl{'+m[1]+'}', pdf_text)
    build_input.write_text(pdf_text)
    header=tmp/'header.tex'
    header.write_text(r'''\usepackage{fancyhdr}
\usepackage{microtype}
\usepackage{xurl}
\renewcommand{\contentsname}{Mục lục}
\let\originaltableofcontents\tableofcontents
\renewcommand{\tableofcontents}{\clearpage\originaltableofcontents}
\renewcommand{\figurename}{Hình}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Hospital Network / Technical Report}
\fancyhead[R]{\small 02.11.2026}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{16pt}
\setlength{\emergencystretch}{3em}
\renewcommand{\arraystretch}{1.25}
''')
    final=ROOT/'docs/06-report/final/report.pdf';final.parent.mkdir(parents=True,exist_ok=True)
    args=['pandoc',str(build_input),'-o',str(final),
          '--pdf-engine=xelatex','--toc','--number-sections','--include-in-header',str(header),
          '-V','mainfont=DejaVu Sans','-V','sansfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono',
          '-V','fontsize=10pt','-V','geometry:a4paper,margin=22mm','-V','colorlinks=true',
          '-V','urlcolor=blue','-V','toc-depth=2']
    subprocess.run(args,cwd=ROOT,check=True)
    print('Built',final.relative_to(ROOT),hashlib.sha256(final.read_bytes()).hexdigest())

if __name__=='__main__':main()
