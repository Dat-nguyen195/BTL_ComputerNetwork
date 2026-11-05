# Manifest bộ nộp kỹ thuật

**Chốt ngày05/11/2026.** Lớp L08, nhóm2; BTL2 do Nguyễn Thành Đạt (2410709) và Phạm Tiến Đạt (2410723) thực hiện. Xem [thông tin nhóm](../docs/00-management/team-members.md) và [hướng dẫn chọn file](README.md).

| Sản phẩm | Đường dẫn | Tình trạng kỹ thuật |
| --- | --- | --- |
| Báo cáo chính | [report.pdf](../docs/06-report/final/report.pdf) | Bảy Step, phụ lục A-G, IP/VLAN, BOM, sơ đồ vật lý, demo và kiểm trực tiếp mới |
| Nguồn LaTeX | [report-latex.zip](../docs/06-report/final/report-latex.zip), [hướng dẫn](../docs/06-report/latex/README.md) | XeLaTeX, font dự phòng, build độc lập; có recipe editor |
| Packet Tracer tổng | [hospital-3sites.pkt](../simulation/packet-tracer/hospital-3sites.pkt) | Khóa đúng byte của bản có32+4 quan sát,58 node/53 cáp/sáu Wi-Fi |
| GNS3 tổng | [hospital-3sites.gns3](../simulation/gns3/hospital-3sites.gns3) |52 node/52 link;209 kiểm và137 sau restart controller ngày05/11 |
| MPLS bổ sung | [module và runbook](../simulation/mpls/README.md) | Linux namespaces/QEMU28+28 và PCAP hai nhãn; native GNS3 module chưa chạy |
| Phụ lục kiểm thử nhanh | [packet-tracer-validation.pdf](../docs/06-report/final/packet-tracer-validation.pdf) | Hai trang, nội dung khác báo cáo chính |
| Cấu hình, source và sơ đồ | [configs](../configs/README.md), [simulation](../simulation/README.md), [source report](../docs/06-report/source/README.md) | Có Dockerfile, CSV, Markdown, LaTeX, drawio/SVG/PDF vector |
| Bằng chứng hiện tại | [controller-restart](../test_results/runtime/controller-restart/README.md), [Packet Tracer](../test_results/packet-tracer/README.md), [QA PDF](../test_results/report-latex/README.md) | Giữ cả bằng chứng cũ, không chuyển kết quả giữa các nền tảng |
| Gói nộp và hash | `hospital-network-delivery.zip`, [package-manifest.json](package-manifest.json), [SHA256SUMS](SHA256SUMS) | Bao gồm source/PDF/project/evidence; kiểm được sau giải nén không có Git |
| Upload BKeL | [bkel-receipt](bkel-receipt/README.md) | Nhóm tự upload và lưu biên nhận thật |

Đã sửa lỗi GNS3 controller không bật lại do PID/socket cũ; lệnh start tự mở project closed. Mã/config node và native project giữ nguyên byte. `.pkt` chính đã trả về bản được kiểm; bản Save lại chỉ khác thời gian/môi trường được giữ trong backup local. Lỗi LaTeX là pdfLaTeX không hỗ trợ Unicode tiếng Việt; bản chốt dùng XeLaTeX và các file cấu hình đi kèm.

Bản PDF trong `latex/build/` hoặc `output/pdf/` chỉ để xem trước; lấy PDF chính trong `final/` để nộp. Sau thay đổi source/PDF/project phải kiểm liên quan, cập nhật QA và đóng gói lại. Không đưa file đề local, bộ cài, IOS image, khóa hoặc cache vào ZIP. GPON/RF/DSL PHY, VPN crypto, HA chassis và workload y tế thật vẫn là giới hạn thiết kế đã ghi trong báo cáo.

```bash
python3 scripts/verify.py
python3 scripts/package_submission.py --check
```

Lệnh trên kiểm offline; kiểm trực tiếp mạng dùng runbook riêng. Đóng gói không thực hiện upload BKeL hoặc tạo phê duyệt học phần thay người khác.
