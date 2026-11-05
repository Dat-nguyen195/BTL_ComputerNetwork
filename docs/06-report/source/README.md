# Nguồn báo cáo có thể chỉnh sửa

[report.md](report.md) và [design-appendices.md](design-appendices.md) là nội dung gốc; [report-with-evidence.md](report-with-evidence.md) ghép tự động bảng từ hai run JSON và hash; [topology.svg](topology.svg) là hình nguồn. PDF ở [final/report.pdf](../final/report.pdf). Đã bổ sung [bộ LaTeX đầy đủ](../latex/README.md), có bìa/logo Bách Khoa, thông tin nhóm có thể sửa và [ZIP LaTeX](../final/report-latex.zip) để biên dịch độc lập.

Build từ Markdown cần Python+cairosvg, Pandoc, XeLaTeX, font Unicode tự chọn theo `fonts.tex` và evidence đã có. Cài dependency PDF trong venv riêng, rồi:

```bash
python3 scripts/build_report.py
```

Nếu Python hệ thống không có cairosvg, chạy bằng Python của venv. Script chỉ build khi hai run được chọn PASS và native template đã reopen. Mặc định lấy209 kiểm sau sửa firewall và137 kiểm reopen lịch sử; báo cáo phân biệt thời điểm của hai bằng chứng. Chỉnh `report.md`, không sửa riêng bản ghép; build lại và cập nhật checksum/package sau thay đổi. Có thể sửa và biên dịch LaTeX trực tiếp theo README của bộ LaTeX, nhưng build từ Markdown sẽ sinh lại `report.tex`. Nội dung/chữ ký học phần và việc nộp BKeL vẫn do nhóm xác nhận.


## Phụ lục Packet Tracer

[PDF2 trang](../final/packet-tracer-validation.pdf) bổ sung bằng chứng sau reopen và chọn ISP thủ công. [Bảng tóm tắt Markdown](packet-tracer-validation.md) sinh từ JSON; [nguồn sinh PDF](../../../scripts/build_packet_report.py) có toàn bộ nội dung/bố cục có thể sửa. Dùng `python scripts/build_packet_report.py` sau khi evidence checker đạt; chỉnh nội dung/bố cục trong generator, dữ liệu thực trong JSON run mới, rồi render và QA lại. Không sửa raw evidence để làm đẹp kết quả. [QA/hash](../../../test_results/packet-tracer/report-qa.json) riêng với báo cáo LaTeX13 trang.

## Biên dịch trên Windows

Có thể dùng Pandoc và Tectonic từ bản phát hành chính thức, thêm thư mục executable vào PATH rồi chạy `python -X utf8 scripts/build_report.py --engine tectonic`. `fonts.tex` ưu tiên TeX Gyre Termes/Heros và DejaVu Sans Mono (hoặc TeX Gyre Cursor) để dùng được trên Linux, Windows và Overleaf mà không cần font Microsoft. Script giữ hình vector đã QA; nếu sửa topology SVG cần xuất lại asset PDF trước build. Tectonic tự tải gói TeX lần đầu. Thông tin bìa ở `../latex/metadata.tex`; danh sách toàn nhóm/email nằm trong nội dung `report.md`. Hai người thực hiện BTL2: Nguyễn Thành Đạt và Phạm Tiến Đạt.
