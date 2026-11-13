# Ma trận nghiệm thu Cisco Packet Tracer

Cập nhật13/11/2026; [phạm vi](cisco-scope.md). Evidence chính `test_results/packet-tracer/redesign-20261112-162237/`, runtime ngày12/11. Kiểm offline không tạo lượt chạy mạng mới.

| Yêu cầu | Mục báo cáo | Bằng chứng / trạng thái |
| --- | --- | --- |
| Step1 khảo sát/kiến trúc | 1 | Checklist; chưa khảo sát thực địa |
| Step1 tải cao/chọn thiết bị/LB | 1.2/3.4 | high-load-analysis, calculator; thiết kế, chưa đo nghẽn |
| Step2 cáp/BOM/VLAN/IP | 2 | CSV, sơ đồ, native và config; PHY/HA còn thiết kế |
| Camera | 2.8/5.7 | 14 mẫu10/2/2 đăng ký IoT/quyền truy cập; chưa ghi video |
| WAN/OSPF | 2.9/5.3 | Neighbor FULL, ping hai chiều; không provider overlay |
| Step3 throughput/ISP | 3 | Số học tái lập; chọn ISP thủ công đã có HTTP/PAT, chưa tự động |
| Step4 native | 4 | 102 node/97 cáp, saved/reopen proof |
| TC01 cùng VLAN | 5.2 | 2 ping đúng kỳ vọng |
| TC02 khác VLAN/HIS | 5.2 | 3 quan sát ping/HTTP |
| TC03 liên site | 5.3 | 4 ping và OSPF snapshots |
| TC04 DMZ | 5.4 | 2 HTTP, static PAT và ZBF |
| TC05 Guest deny | 5.5 | 9 quan sát, Web control, counter deny tăng |
| TC06 Internet | 5.6 | 6 HTTP/DNS observations |
| Wi-Fi | 5.6 | 6 association/BSSID/lease; chưa RF |
| SSH | 5.8 | 3 probes; Main-Core nguồn Admin, chưa toàn mạng |
| Step6 đánh giá | 6 | Rủi ro/giới hạn; IDS/IPS, VPN, HA chưa runtime |
| Step7 bàn giao | 7 | PDF/source/native/raw/ZIP/checksum; chưa biên nhận BKeL |
