# Bộ nộp BTL2

**Lấy `hospital-network-delivery.zip` để bàn giao đầy đủ.** ZIP gồm PDF chính, LaTeX độc lập, cả hai mô hình, cấu hình/source Docker, sơ đồ và bằng chứng kiểm thử. Không chứa bộ cài Cisco, IOS image, dữ liệu bệnh nhân, cache hoặc môi trường Python local.

## Khi BKeL yêu cầu upload từng file

1. [Báo cáo chính](../docs/06-report/final/report.pdf).
2. [Packet Tracer tổng](../simulation/packet-tracer/hospital-3sites.pkt).
3. Gói đầy đủ `hospital-network-delivery.zip` để có GNS3, source dựng image và evidence; GNS3 chứng minh cân bằng tải/failover tự động và IDS/IPS.
4. [Nguồn LaTeX](../docs/06-report/final/report-latex.zip) nếu cần nộp source riêng.

[packet-tracer-validation.pdf](../docs/06-report/final/packet-tracer-validation.pdf) là phụ lục kiểm thử hai trang; có thể nộp kèm, không dùng thay báo cáo chính. PDF build local nằm ở `latex/build/` và `output/pdf/` không phải thêm một báo cáo khác.

## Kiểm gói sau giải nén

Trong thư mục vừa giải nén:

```bash
python3 scripts/verify.py
python3 scripts/package_submission.py --check
```

Windows có Python dùng `powershell -File scripts/check.ps1`. Các lệnh kiểm offline không cần GNS3/Packet Tracer đang chạy hoặc Git. Hướng dẫn dựng và demo thật ở `simulation/gns3/README.md`, `simulation/gns3/demo-guide.md`, `simulation/packet-tracer/README.md`.

## Sửa và đóng gói lại

Sửa Markdown, dùng `python3 scripts/build_report.py` với Python có CairoSVG/Pandoc/XeLaTeX; render và cập nhật QA, chạy verify rồi `python3 scripts/package_submission.py`. File `.pkt` chính được khóa đúng byte theo evidence; mở rồi Save có thể đổi hash dù chỉ đồng hồ thay đổi. Dùng bản sao để luyện demo và giữ nguyên bản nộp.

Nhóm tự upload BKeL, kiểm tải lại đúng file và lưu biên nhận thật trong `bkel-receipt/`. [SHA256SUMS](SHA256SUMS) và [manifest](manifest.md) giúp đối chiếu bản đã chọn.
