# Ma trận kiểm thử - Step 5

**Điều phối và lưu ảnh/log:** TV4. **Trạng thái ban đầu:** mọi test NOT RUN; chưa có bằng chứng mô phỏng.

| ID | Kịch bản | Chuẩn bị kỹ thuật | Kết quả mong đợi | Trạng thái | Hồ sơ |
| --- | --- | --- | --- | --- | --- |
| TC01 | PC cùng VLAN | TV2 | Hai PC liên lạc được đúng VLAN. | NOT RUN | [result](TC01-same-vlan/result.md) |
| TC02 | PC khác VLAN | TV2 + TV3 | Liên lạc được theo quyền được duyệt. | NOT RUN | [result](TC02-inter-vlan/result.md) |
| TC03 | Main với DBP và BHTQ | TV1 | Cả hai chi nhánh liên thông theo chính sách. | NOT RUN | [result](TC03-inter-site/result.md) |
| TC04 | Truy cập dịch vụ DMZ | TV3 | Đúng dịch vụ/mapping được công bố. | NOT RUN | [result](TC04-dmz/result.md) |
| TC05 | Khách bị chặn vào LAN | TV3 + TV2 | LAN bị chặn có bằng chứng; DHCP/DNS/Internet khách vẫn dùng được. | NOT RUN | [result](TC05-guest-isolation/result.md) |
| TC06 | Web Internet qua Main | TV4 + TV1 + TV3 | Web thành công qua Main, không local breakout ở Aux. | NOT RUN | [result](TC06-internet-web/result.md) |

Test bổ sung lưu trong `supplemental/`. Trạng thái dùng NOT RUN/PASS/FAIL/BLOCKED; tính năng chỉ thiết kế ghi DESIGN ONLY/MODELED. Mỗi lần chạy phải ghi phiên bản mô phỏng và nguồn/đích, không tái dùng ảnh khi topology đã thay đổi kết quả.
