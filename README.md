# Thiết kế và mô phỏng mạng bệnh viện ba cơ sở

Dự án chọn **Cisco Packet Tracer** làm nền tảng mô phỏng duy nhất. Native hiện tại có 102 thiết bị mạng, 97 cáp, 14 webcam Ethernet VLAN110 và ba cơ sở Main/DBP/BHTQ. File mô phỏng được giữ nguyên cấu hình đã kiểm.

- [Mô hình chính](simulation/packet-tracer/hospital-3sites.pkt), [hướng dẫn demo](docs/final-demo.md).
- [Báo cáo PDF](docs/06-report/final/report.pdf), [nguồn LaTeX](docs/06-report/latex/report.tex), [ZIP LaTeX](docs/06-report/final/report-latex.zip).
- [Ma trận yêu cầu](docs/final-acceptance-matrix.md), [bộ test](docs/final-test-matrix.md), [phạm vi và giới hạn](docs/cisco-scope.md).
- [Thiết kế/IP/VLAN](docs/02-design/ip-vlan-plan.md), [camera](docs/02-design/camera-plan.md), [phân tích tải cao](docs/03-capacity/high-load-analysis.md).

## Kết quả và giới hạn

Evidence Cisco ngày 12/11/2026: 32 quan sát P0/WIFI, 21 HTTP bổ sung, 3 SSH; sau lưu/mở lại có 12 HTTP và 3 SSH. Camera đăng ký 10/2/2; sáu client Wi-Fi có BSSID/lease. Đây là bằng chứng đã lưu, không phải lượt chạy mới khi sửa tài liệu.

Đã kiểm kết nối cùng/khác VLAN, liên site, OSPF, DHCP/DNS, NAT/PAT/DMZ, ACL Guest, Wi-Fi, SSH và quản lý camera IoT. Chuyển ISP trong native là thao tác thủ công. PBR/failover tự động, IDS/IPS, VPN crypto, GPON PHY, RF, HA, ghi video/NVR và throughput sản xuất chưa nghiệm thu. HIS/PACS/LIS chỉ là dịch vụ đại diện.

## Công cụ local

Thư mục `scripts/` chỉ giữ trên máy làm việc, được loại khỏi Git. Các lệnh dưới đây dùng khi có đủ công cụ local:

```bash
./project doctor
./project check
./project report
```

`check` kiểm offline, không phát gói hay tự mở Packet Tracer. `report` dùng XeLaTeX nhiều lượt và đồng bộ PDF xem trước/bản cuối. Bản tải từ GitHub có thể mở trực tiếp mô hình và PDF; nguồn LaTeX biên dịch bằng XeLaTeX/latexmk mà không cần `scripts/`.

Nguồn báo cáo nằm tại `docs/06-report/latex/`. Khi dùng Overleaf, tải ZIP LaTeX, chọn Main document `report.tex` và Compiler **XeLaTeX**. Khi dùng VS Code, chọn recipe **XeLaTeX (Vietnamese report)** để cập nhật đủ mục lục.

`configs/` và `simulation/generated/` là cấu hình tham chiếu; mô hình demo chính là file `.pkt` ở trên. `test_results/` giữ bằng chứng kiểm thử và QA báo cáo. Báo cáo PDF và ZIP nguồn LaTeX nằm tại `docs/06-report/final/`.

Xem [cài đặt Ubuntu](docs/07-operations/ubuntu.md) và [thông tin nhóm](docs/00-management/team-members.md). Không kèm bộ cài hoặc image có bản quyền trong repo.
