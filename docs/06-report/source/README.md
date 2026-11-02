# Nguồn báo cáo có thể chỉnh sửa

[report.md](report.md) là nội dung gốc; [report-with-evidence.md](report-with-evidence.md) ghép tự động bảng từ hai run JSON và hash; [topology.svg](topology.svg) là hình nguồn. PDF ở [final/report.pdf](../final/report.pdf).

Build cần Python+cairosvg, pandoc, XeLaTeX, font DejaVu Sans và evidence đã có. Cài dependency PDF trong venv riêng, rồi:

```bash
python3 scripts/build_report.py
```

Nếu Python hệ thống không có cairosvg, chạy bằng Python của venv. Script chỉ build khi hai run được chọn PASS và native template đã reopen. Chỉnh `report.md`, không sửa riêng bản ghép; build lại và cập nhật checksum/package sau thay đổi. Nội dung/chữ ký học phần và việc nộp BKeL vẫn do nhóm xác nhận.
