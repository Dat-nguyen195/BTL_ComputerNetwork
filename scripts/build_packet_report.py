#!/usr/bin/env python3
"""Create a Packet Tracer supplement only after the saved runtime evidence checks pass."""
from collections import Counter
from html import escape
import json
from pathlib import Path
import shutil

from check_packet_runtime import check, ROOT


def main():
    run = ROOT / 'test_results/packet-tracer/after-reopen'
    project = ROOT / 'simulation/packet-tracer/hospital-3sites.pkt'
    assert (run / 'manual-isp-results.json').is_file(), 'Manual ISP evidence is required for this supplement'
    check(run, project)
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

    fonts = [(Path('C:/Windows/Fonts/arial.ttf'), Path('C:/Windows/Fonts/arialbd.ttf')),
             (Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
              Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))]
    regular, bold = next(pair for pair in fonts if all(path.is_file() for path in pair))
    pdfmetrics.registerFont(TTFont('Hospital', str(regular)))
    pdfmetrics.registerFont(TTFont('HospitalBold', str(bold)))
    navy, teal, gray = colors.HexColor('#16324B'), colors.HexColor('#087F83'), colors.HexColor('#526473')
    styles = {
        'title': ParagraphStyle('title', fontName='HospitalBold', fontSize=23, leading=29, textColor=navy, spaceAfter=10),
        'sub': ParagraphStyle('sub', fontName='Hospital', fontSize=12, leading=17, textColor=gray, spaceAfter=14),
        'h': ParagraphStyle('h', fontName='HospitalBold', fontSize=13, leading=18, textColor=teal, spaceBefore=12, spaceAfter=7),
        'body': ParagraphStyle('body', fontName='Hospital', fontSize=10, leading=15, textColor=navy, spaceAfter=8),
        'small': ParagraphStyle('small', fontName='Hospital', fontSize=8, leading=12, textColor=gray, spaceAfter=6),
        'cell': ParagraphStyle('cell', fontName='Hospital', fontSize=8.5, leading=12, textColor=navy),
        'head': ParagraphStyle('head', fontName='HospitalBold', fontSize=8.5, leading=12, textColor=colors.white),
    }
    def p(text, style='body'):
        return Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])

    def table(rows, widths):
        data = [[p(value, 'head' if i == 0 else 'cell') for value in row] for i, row in enumerate(rows)]
        result = Table(data, colWidths=[width * mm for width in widths], repeatRows=1, hAlign='LEFT')
        result.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), navy), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#EFF5F7'), colors.white]),
            ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor('#D5E2E8'))]))
        return result

    def read(name):
        return json.loads((run / name).read_text(encoding='utf-8'))
    provenance = read('provenance.json')
    records = read('hospital-results.json')['records']
    associations = read('wireless-associations.json')
    counts = Counter(record['group'] for record in records)
    descriptions = {'TC01': 'Cùng VLAN, hai chiều', 'TC02': 'Liên VLAN và HIS',
                    'TC03': 'Main - DBP/BHTQ, hai chiều', 'TC04': 'DMZ và PAT tĩnh từ bên ngoài',
                    'TC05': 'Guest bị chặn LAN/HIS, có đối chứng',
                    'TC06': 'Web/DNS tập trung cho PC/Guest', 'WIFI': 'Staff qua Wi-Fi đến HIS/Web'}
    limits = [
        'ISP2 là đường PAT chính. ISP1 dự phòng chuyển thủ công; chưa chứng minh tự động failover, IP SLA hoặc PBR trên Packet Tracer. Bằng chứng GNS3 cho các tính năng đó được lưu riêng.',
        'Main-FW dùng 2811/profile 2800_advip_12.4, module NM-1FE-TX và ba cổng vật lý LAN/OUTSIDE/DMZ. Tám router còn lại dùng 2911; không chuyển kết quả probe 2911 thành kết luận cho mọi profile.',
        'Sáu liên kết dùng card AC, WPA2-PSK/AES với khóa lab công khai HospitalLab2026Only. Chưa đo RF, roaming, AAA/Enterprise hoặc tải vô tuyến thực.',
        'Ethernet thay chức năng hai leased line và các đường ISP. Không đo tốc độ xDSL/GPON, tải HIS/PACS, VPN crypto hoặc HA thiết bị từ mô hình này.',
        'Mã responseType 7 của HTTP Guest được giữ nguyên, không suy đoán tên enum. Kết luận chặn dựa thêm vào trang rỗng, đối chứng truy cập thành công và bộ đếm ACL tăng trong lần chạy.',
    ]
    story = [p('Kiểm thử Packet Tracer', 'title'),
             p('Phụ lục bổ sung báo cáo mạng bệnh viện Main - DBP - BHTQ | 04/11/2026', 'sub'),
             p('Kết quả kỹ thuật sau lưu và mở lại', 'h'),
             p('32/32 quan sát phù hợp kỳ vọng trong bộ thử sau warmup. Tám lượt ping cho phép nhận đủ 4/4 phản hồi; ba ping Guest không nhận phản hồi. Các lượt HTTP cho phép trả đúng nội dung, còn Guest→HIS thất bại có đối chứng và ACL. Đây là phạm vi kiểm thử lab, không phải phê duyệt học phần hoặc SLA.'),
             table([['Nhóm', 'Phạm vi', 'Số lượt']] + [[key, descriptions[key], counts[key]]
                    for key in ['TC01', 'TC02', 'TC03', 'TC04', 'TC05', 'TC06', 'WIFI']], [22, 126, 26]),
             p('Trạng thái mô hình đã lưu', 'h'),
             p('Packet Tracer 9.0.1.0858; 58 thiết bị mạng, 53 cáp và sáu association Wi-Fi. Có 19 client DHCP, 18 pool thiết kế có sức chứa và ba serverPool mặc định giữ sức chứa 0 để tránh cấp phát ngoài thiết kế. PDU do ứng dụng tự thêm được tách khỏi số thiết bị mạng.'),
             p('Chọn ISP thủ công', 'h'),
             p('Ba lượt HTTP từ Main-PC10-A, DBP-Guest và BHTQ-Staff thành công qua ISP1/PAT 203.0.113.2. Sau khi trả về ISP2, một lượt HTTP thành công qua PAT 198.51.100.2. Cấu hình Edge được khôi phục đầy đủ; đây là chọn đường thủ công, không phải tự động failover.'),
             p('Lịch sử kiểm thử được giữ', 'h'),
             p('Giữ riêng 24 job có dây ban đầu và 32 job Wi-Fi đầu tiên, bao gồm đầu ra thiếu và mất gói. Lần sau mở lại lưu riêng warmup trước khi chạy bộ 32 job; không xóa lỗi cũ hoặc diễn giải mất gói đầu thành kết quả sạch.')]
    story += [PageBreak(), p('Wi-Fi, bằng chứng và giới hạn', 'title'),
              p('Sáu association được đối chiếu với MAC/SSID AP và địa chỉ DHCP thực nhận.', 'sub'),
              table([['Máy', 'IPv4', 'SSID', 'BSSID của AP']] +
                    [[r['node'], r['ip'], r['ssid'], r['ap_mac']] for r in associations], [34, 31, 42, 67]),
              p('Giới hạn cần giữ khi trình bày', 'h')]
    story += [p('- ' + item) for item in limits]
    native_hash = provenance['native_sha256']
    story += [p('Truy vết và tái kiểm', 'h'),
              p('Project: simulation/packet-tracer/hospital-3sites.pkt\nEvidence: test_results/packet-tracer/after-reopen/\nKiểm bằng: python scripts/check_packet_runtime.py', 'small'),
              p('SHA256 project: ' + native_hash[:32] + '\n' + native_hash[32:] +
                '\nGiờ thu thập UTC: ' + provenance['collected_at_utc'], 'small'),
              p('Lớp L08 - Nhóm 2. BTL2 do Nguyễn Thành Đạt (2410709, nhóm trưởng) và Phạm Tiến Đạt (2410723) thực hiện. Danh sách toàn nhóm và email có trong báo cáo chính; phê duyệt và biên nhận BKeL được ghi riêng.', 'small')]

    output = ROOT / 'output/pdf/packet-tracer-validation.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    def footer(canvas, doc):
        canvas.setStrokeColor(teal)
        canvas.line(18 * mm, 16 * mm, 192 * mm, 16 * mm)
        canvas.setFont('Hospital', 8)
        canvas.setFillColor(gray)
        canvas.drawString(18 * mm, 11 * mm, 'HOSPITAL NETWORK | Packet Tracer - bằng chứng kỹ thuật')
        canvas.drawRightString(192 * mm, 11 * mm, str(doc.page))
    SimpleDocTemplate(str(output), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=17 * mm, bottomMargin=23 * mm,
                      title='Phụ lục kiểm thử Packet Tracer - mạng bệnh viện', author='Nhóm dự án').build(
                          story, onFirstPage=footer, onLaterPages=footer)
    final = ROOT / 'docs/06-report/final/packet-tracer-validation.pdf'
    shutil.copy2(output, final)
    lines = ['# Phụ lục kiểm thử Packet Tracer', '', 'Cập nhật 04/11/2026; bằng chứng kỹ thuật, chưa thay phê duyệt nhóm.', '',
             '## Bộ thử sau mở lại', '', '| Nhóm | Phạm vi | Số lượt |', '| --- | --- | ---: |']
    lines += [f'| {key} | {descriptions[key]} | {counts[key]} |' for key in descriptions]
    lines += ['', 'Tám ping cho phép đều 4/4; ba ping Guest không phản hồi. HTTP cho phép đúng marker; HTTP Guest thất bại có đối chứng và ACL tăng.', '',
              '## Sáu kết nối Wi-Fi', '', '| Máy | IPv4 | SSID | BSSID AP |', '| --- | --- | --- | --- |']
    lines += [f"| {r['node']} | {r['ip']} | {r['ssid']} | {r['ap_mac']} |" for r in associations]
    lines += ['', '## Giới hạn', ''] + ['- ' + item for item in limits]
    lines += ['', '## Truy vết', '', 'Project: `simulation/packet-tracer/hospital-3sites.pkt`.',
              'SHA256: `' + native_hash + '`.', 'Evidence: `test_results/packet-tracer/after-reopen/`.',
              'Giờ thu thập UTC: `' + provenance['collected_at_utc'] + '`.', '',
              'Sinh bằng `python scripts/build_packet_report.py`; phải có ReportLab và font Arial hoặc DejaVu. Chỉ sinh sau khi checker evidence đạt. QA hình ảnh thực hiện riêng sau render.', '']
    (ROOT / 'docs/06-report/source/packet-tracer-validation.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print('Built ' + final.relative_to(ROOT).as_posix() + '; visual QA still required')


if __name__ == '__main__':
    main()
