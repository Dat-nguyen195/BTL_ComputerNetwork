# SUPP-01 — Phân phối nguồn và failover hai ISP

**Trạng thái:** NOT RUN. **Chuẩn bị:** TV1 + TV3. **Chạy/lưu bằng chứng:** TV4. **Cập nhật:** 26/10/2026. Các hàng dưới là test procedure và expected; chưa có số đo hoặc actual CLI.

## 1. Metadata bắt buộc khi chạy

Ghi ngày/giờ/người chạy, platform/model/image/version, tên project/commit/SHA256, cấu hình đầu vào, host/IP/VLAN/dịch vụ, trạng thái ban đầu của link/track/route/NAT và reviewer. Chưa có project/hash trong workspace.

Đích HTTP cố định: **`192.0.2.100`** (Web-Lab, gateway `192.0.2.65`); DNS `web.hospital.test`. Không đổi đích sang server khác khi ISP bị ngắt. Source nhóm1: Main-PC10 `10.10.10.10`, DBP-PC10 `10.20.10.10`. Source nhóm2: Main-PC20 `10.10.20.10`, BHTQ-PC10 `10.30.10.10`; guest khi đã có policy TV3.

## 2. Chuỗi ca kiểm

Mỗi ca ghi actual và evidence riêng. Khôi phục link/track/route trước ca độc lập tiếp theo; ghi hiện trạng NAT và cách tạo phiên mới để phân biệt với mapping cũ. Không tự clear NAT rồi tuyên bố phiên cũ giữ được.

| Ca | Thao tác | Expected cần kiểm | Actual / thời gian / evidence |
| --- | --- | --- | --- |
| SUPP-01-A | Cả hai ISP up, tạo nhiều phiên HTTP từ cả hai nhóm nguồn tới cùng Web | Nhóm1 ưu tiên ISP1, nhóm2 ISP2; PAT dùng public đúng egress; ghi số phiên/byte thực, không áp 50/50 | Chưa chạy |
| SUPP-01-B | `shutdown` G0/1 Main-Edge (ISP1 local down) | Track1/default1 mất sau timer; phiên mới nhóm1 đi ISP2 và vẫn tới Web cũ; ghi số phận phiên cũ | Chưa chạy |
| SUPP-01-C | Khôi phục baseline rồi `shutdown` G0/2 Main-Edge | Track2/default2 mất; phiên mới nhóm2 đi ISP1, Web không đổi | Chưa chạy |
| SUPP-01-D | Khôi phục baseline rồi `shutdown` G0/1 **ISP1**, giữ G0/0 ISP1 và G0/1 Edge up | Probe `.11` mất qua upstream; probe không được chạy vòng qua ISP2; Track1 down, phiên mới ra ISP2 | Chưa chạy |
| SUPP-01-E | Khôi phục baseline rồi ngắt G0/1 **ISP2**, giữ link local Edge–ISP2 up | Kiểm độc lập upstream ISP2, probe `.22` mất; fallback ISP1 | Chưa chạy |
| SUPP-01-F | Ngắt cả hai ISP | Edge không default; GW track10 down và default bị gỡ; Aux mất O*E2 default sau hội tụ; ping liên site vẫn thông nếu leased lines còn | Chưa chạy |
| SUPP-01-G | Từ ca F bật ISP1, rồi ISP2 | Probe /32 hoạt động khi chưa có default; track/default phục hồi, Aux học lại; phiên mới tới cùng Web; ghi thời gian | Chưa chạy |
| SUPP-01-H | Giữ hai ISP tốt nhưng tắt Web/ICMP tại Web | Edge tracks có thể còn up nhưng Core/GW track10 down; ghi false negative của health target đơn và giới hạn thiết kế | Chưa chạy |
| SUPP-01-I bổ sung | Ngắt leased line Main–DBP rồi Main–BHTQ theo lượt | Chỉ nhánh mất tuyến bị mất đường về Main; không có dự phòng nhánh do hai ISP Main | Chưa chạy |

## 3. Điểm quan sát

- Edge: `show ip sla statistics`, `show track`, `show ip route`, `show route-map`, `show access-lists`, `show ip nat translations`, counter interface.
- Main-GW/Core: `show track 10`, `show ip route 0.0.0.0`, `show ip route 192.0.2.100`; `/32` Web giữ lại để phục hồi là chủ đích, không được nhầm với default còn sót.
- Aux: `show ip route ospf`, route LAN và kết quả ICMP nội bộ trong ca mất Internet.
- PC/Web: HTTP tới IP và hostname, source/đích/cổng, phiên TCP cũ và phiên mới. Nếu công cụ không quan sát được phiên cũ, ghi NOT RUN cho phần này.

`frequency 3`, `timeout 1000`, `delay down 6 up 6` là cấu hình dự kiến, không phải số đo 9s hoặc bộ đếm ba lần thất bại. Đo timestamp trước lỗi, lúc track đổi, route bị gỡ, lúc phiên mới HTTP thành công; ghi rõ đơn vị và số lần lặp thực tế. Không kết luận SLA sản xuất từ simulator.

## 4. Kết quả và retest

Ảnh/log: chưa có; lưu dưới `test_results/supplemental/` với tên ca, ngày và bản test. Kết luận từng ca và tổng thể: NOT RUN. Reviewer/issue/retest: chờ thực hiện. Thiếu tính năng nền tảng phải ghi BLOCKED/DESIGN ONLY, không chuyển PASS từ thiết kế hoặc kiểm tĩnh Python.
