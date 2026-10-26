# TC06 — Web Internet qua Main

**Trạng thái:** NOT RUN. **Chuẩn bị:** TV4 + TV1 + TV3. **Cập nhật mẫu:** 26/10/2026.

| Thuộc tính | Giá trị thực tế |
| --- | --- |
| Ngày/người chạy | Chưa chạy |
| Platform/model/phiên bản | Chưa chọn/kiểm |
| Project/commit/SHA256 | Chưa có project |
| Đích Web chung dự kiến | `http://192.0.2.100` và `http://web.hospital.test` |
| Web/DNS lab | Web `192.0.2.100/26`, gateway `192.0.2.65`, DNS record `web.hospital.test -> 192.0.2.100` |
| Điều kiện trước | HTTP/DNS và ICMP health probe hoạt động; gateway/route đúng; chính sách TV3 đã cho phép guest ra Internet, DHCP/DNS phù hợp |

## Các ca cần chạy

| Nguồn | Bước kiểm | Expected | Actual / evidence |
| --- | --- | --- | --- |
| Main nội bộ | HTTP tới IP rồi hostname; xem đường đi và NAT | HTTP thành công qua Main-Edge, PAT đúng egress | Chưa chạy |
| DBP nội bộ | Tương tự, ghi source IP/VLAN thật | Đi leased line về Main, không local breakout | Chưa chạy |
| BHTQ nội bộ | Tương tự | Đi leased line về Main, không local breakout | Chưa chạy |
| Guest mỗi site được triển khai | Tương tự sau khi TV3 bật policy | Internet/DNS được phép, test cô lập LAN ở TC05 vẫn đúng | Chưa chạy |

Thu route/default nguồn, traceroute/PDU đường đi, NAT translation/counter và HTTP thực. Lưu ảnh `screenshots/`, log `logs/`, gắn đúng project/hash. Ping không thay HTTP; IP truy cập được nhưng hostname không được thì kiểm DNS riêng. Không suy PASS từ routing-only stand-in chưa có guest isolation.

Test failover cùng đích và từng egress ở [dual ISP](../supplemental/dual-isp-failover.md). Kết luận, reviewer và bug/retest: chưa có; giữ NOT RUN đến khi có actual.
