# Wi-Fi nhân viên và khách

**Chủ trì:** TV2; TV3 bảo mật. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

Phủ toàn Main Site; xác nhận yêu cầu Aux trong khảo sát. Tách SSID nhân viên/khách và map VLAN 120/100 theo baseline IP; VLAN ID lặp giữa site không kéo dài Layer 2 qua WAN.

| Site/khu vực | Số khách/ngày | Số thiết bị đồng thời | AP/vùng phủ | PoE/uplink | Xác nhận RF |
| --- | --- | --- | --- | --- | --- |
| Main, DBP, BHTQ (tính riêng) | Chưa có | Chưa có | Chưa sizing | Chờ BOM | Chưa khảo sát |

Đề xuất WPA2/WPA3-Enterprise và AAA khi hỗ trợ; guest isolation và ACL/firewall ngăn truy cập LAN/quản trị/server, vẫn cấp DHCP/DNS và Internet qua Main. Không dựa vào VLAN riêng để tự kết luận đã cách ly. Không lấy số phòng làm số AP một cách mặc định.


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
