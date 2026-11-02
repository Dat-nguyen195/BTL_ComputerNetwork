# Nguồn báo cáo có thể chỉnh sửa

[report.md](report.md) là nội dung gốc; [report-with-evidence.md](report-with-evidence.md) ghép tự động bảng từ hai run JSON và hash; [topology.svg](topology.svg) là hình nguồn. PDF ở [final/report.pdf](../final/report.pdf). Đã bổ sung [bộ LaTeX đầy đủ](../latex/README.md), có bìa/logo Bách Khoa, thông tin nhóm có thể sửa và [ZIP LaTeX](../final/report-latex.zip) để biên dịch độc lập.

Build từ Markdown cần Python+cairosvg, Pandoc, XeLaTeX, font DejaVu Serif/Sans/Mono và evidence đã có. Cài dependency PDF trong venv riêng, rồi:

```bash
python3 scripts/build_report.py
```

Nếu Python hệ thống không có cairosvg, chạy bằng Python của venv. Script chỉ build khi hai run được chọn PASS và native template đã reopen. Mặc định lấy209 kiểm sau sửa firewall và137 kiểm reopen lịch sử; báo cáo phân biệt thời điểm của hai bằng chứng. Chỉnh `report.md`, không sửa riêng bản ghép; build lại và cập nhật checksum/package sau thay đổi. Có thể sửa và biên dịch LaTeX trực tiếp theo README của bộ LaTeX, nhưng build từ Markdown sẽ sinh lại `report.tex`. Nội dung/chữ ký học phần và việc nộp BKeL vẫn do nhóm xác nhận.
