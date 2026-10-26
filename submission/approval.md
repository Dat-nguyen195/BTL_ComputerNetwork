# Hồ sơ TV1 duyệt sản phẩm cuối

**Trạng thái:** PENDING / CHƯA DUYỆT. **Cập nhật:** 26/10/2026. **Người duyệt cuối theo phân công:** TV1. Ngày G4 dự kiến 22/11/2026, không phải ngày đã ký.

## Sản phẩm và điều kiện duyệt

| Sản phẩm | Đường dẫn dự kiến | Phiên bản / SHA256 | Kết luận hiện tại |
| --- | --- | --- | --- |
| PDF | `docs/06-report/final/report.pdf` | Chưa có file/hash | PENDING |
| Mô phỏng | `simulation/packet-tracer/hospital-3sites.pkt` hoặc gói GNS3 | Chưa có file/hash | PENDING |
| Config | `configs/` | Cấu hình tham chiếu, chưa đối chiếu running-config | Chờ tích hợp và test |
| Evidence | `test_results/` | Mẫu/thủ tục; chưa có runtime evidence | NOT RUN |

## Bảng xác nhận để điền khi có sản phẩm thật

| Phần xác nhận | Người chủ trì | Trạng thái |
| --- | --- | --- |
| PDF đủ nội dung, font/hình/bảng/mục lục, nguồn và giới hạn | TV5 chuẩn bị, TV1 đọc | Chưa có PDF |
| Mô phỏng lưu/đóng/mở lại; đủ dependency; smoke test đúng bản | TV4 | Chưa kiểm |
| LAN/IP/security/DMZ/VPN được đọc chéo đúng phạm vi | TV2/TV3 với TV1 | Chưa xác nhận |
| TC01–TC06 và test bổ sung có actual, ngày/người chạy, evidence gắn phiên bản | TV4 và chủ trì chuyên môn | NOT RUN |
| Manifest và SHA256 khớp đúng PDF/mô phỏng | TV4/TV5 | Chưa lập hash |
| TV1 ký riêng hai sản phẩm cuối theo phiên bản/hash | TV1 | PENDING |

Ngày/người duyệt, nhận xét, lỗi cần sửa, kết luận từng sản phẩm: điền khi nghiệm thu thực tế. Chỉ ghi APPROVED sau khi kiểm đủ điều kiện. Mọi sửa đổi sau duyệt phải cập nhật manifest/hash, retest phần ảnh hưởng và tái duyệt. Chưa có xác nhận của TV2/TV3/TV4/TV5 hoặc xác nhận nộp BKeL trong hồ sơ hiện tại.
