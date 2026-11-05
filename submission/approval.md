# Kiểm nhận kỹ thuật bản bàn giao

**Đã hoàn thiện theo yêu cầu chủ workspace ngày05/11/2026.** Lớp L08, nhóm2; hai người thực hiện BTL2: Nguyễn Thành Đạt (2410709) và Phạm Tiến Đạt (2410723).

| Điều kiện | Kết quả |
| --- | --- |
| Báo cáo và LaTeX |21 trang; XeLaTeX biên dịch thành công; ZIP độc lập và recipe editor cho text trùng PDF chính; render/kiểm đủ21 trang |
| Packet Tracer | Bản chính đúng hash đã thử32+4, sáu Wi-Fi và19 DHCP client; bản resave chỉ đổi đồng hồ được backup local |
| GNS3 trực tiếp |209/209 PASS;137/137 PASS sau restart controller; live code/config52 node khớp nguồn |
| Lỗi controller | Đã sửa PID/socket cũ và tự mở project closed; hai lần boot thành công |
| MPLS | Giữ28+28 quan sát Linux namespaces/QEMU; native GNS3 module chưa chạy |
| Thông tin nhóm | L08/nhóm2, tên/MSSV/email và phân công đã có; dòng giảng viên chưa cung cấp được ẩn |
| Upload BKeL | Chưa thực hiện; nhóm tự upload và lưu biên nhận thật |

Hash sản phẩm đã chọn:

| Sản phẩm | File | SHA256 |
| --- | --- | --- |
| Báo cáo chính | `docs/06-report/final/report.pdf` | `42daa947adfcc09ed721b304f45d5e36cfdaa56b05af73d3f82e58a8c664a03f` |
| Nguồn LaTeX | `docs/06-report/final/report-latex.zip` | `2c025b18dc95701abe65525855ae36730c1999e8ea96406cdd035e43660ad47e` |
| GNS3 tổng | `simulation/gns3/hospital-3sites.gns3` | `8047cff9ca418dc52a43cb1b546e3179e3962224136122f65fd00d35cff2d5bb` |
| Packet Tracer tổng | `simulation/packet-tracer/hospital-3sites.pkt` | `45ff85657fc08186f4863d541ac7b12de1bd09a72fbf305c445c01f3cf839289` |
| Phụ lục kiểm thử nhanh | `docs/06-report/final/packet-tracer-validation.pdf` | `5ff45d5df1746dd4cb54ddf3b1149135936bf246be73b92a31ee67fd66c53189` |

[QA báo cáo](../test_results/report-latex/README.md), [runtime mới](../test_results/runtime/controller-restart/README.md), [manifest](manifest.md) và [hướng dẫn nộp](README.md) là hồ sơ đối chiếu. Các kiểm nhận ở đây là kết quả kỹ thuật đã thực hiện, không gán chữ ký hoặc phê duyệt của giảng viên/thành viên khác. Sau khi đổi file cần cập nhật bằng chứng/hash và đóng gói lại.
