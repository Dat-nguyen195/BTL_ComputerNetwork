# Bộ kiểm Cisco

Nguồn: `test_results/packet-tracer/redesign-20261112-162237/`, chạy ngày12/11/2026. Script/checker chỉ đọc bằng chứng đã lưu.

| Nhóm | Số quan sát | Ý nghĩa |
| --- | --- | --- |
| TC01 | 2 | Ping cùng VLAN hai chiều |
| TC02 | 3 | Khác VLAN và HIS |
| TC03 | 4 | Main–Aux hai chiều, OSPF |
| TC04 | 2 | DMZ trong/ngoài, static PAT |
| TC05 | 9 | Guest deny và positive controls |
| TC06 | 6 | Web/DNS bên ngoài |
| WIFI | 6 | HTTP từ Staff/Guest; association kiểm riêng |
| Camera/PC bổ sung | 21 | Admin3, Guest3, Web3, nghiệp vụ3, Staff3, PC mới6 |
| SSH | 3 | Admin allow, Telnet closed, non-admin timeout |
| Reopen smoke | 12 HTTP +3 SSH | Kiểm sau save/close/reopen |

P0/WIFI tổng32; không cộng21 HTTP riêng thành cùng suite. Camera14 serial, sáu BSSID và22 IP/MAC sau reopen đối chiếu lease riêng. Lượt đầu có controls chưa trả đủ được giữ, chỉ lượt hoàn chỉnh được ghi đạt. ISP manual4 HTTP là dữ liệu lịch sử riêng, không phải failover tự động.

Kiểm: `python3 scripts/check_redesign_packet.py`; runbook: [demo](final-demo.md).
