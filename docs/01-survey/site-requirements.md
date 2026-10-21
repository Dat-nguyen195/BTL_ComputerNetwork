# Yêu cầu địa điểm và quy mô

**Chủ trì:** TV5. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

| Hạng mục | Yêu cầu gốc | Nguồn |
| --- | --- | --- |
| Vị trí | Main Site ở TP.HCM; 2 Auxiliary Sites ở đường DBP và BHTQ | [A] tr.1 |
| Tòa A và B | **Mỗi tòa 5 tầng, mỗi tầng 10 phòng**; tổng 10 tầng, 100 phòng | [A] tr.1 |
| Phòng trung tâm Main | Data center, IT và Cabling Central Local/patch panel ở phòng riêng, cách A/B **50 m** | [A] tr.1 |
| Main | **600 workstation, 10 server, 12 thiết bị mạng hoặc nhiều hơn** khi cần thiết bị bảo mật | [A] tr.1 |
| Mỗi Aux Site | **2 tầng**; tầng 1 có **1 phòng IT và 1 Cabling Central Local**; **260 workstation, 2 server, ít nhất 5 thiết bị mạng** | [A] tr.2 |
| Tổng hệ thống | **1.120 workstation, 14 server** theo cách hiểu quy mô trên là cho từng chi nhánh | Suy ra từ [A] tr.1-2 |
| Hạ tầng | Có dây và không dây; cáp quang **GPON**; Ethernet **1GbE/10GbE/40GbE**; VLAN theo phòng ban | [A] tr.1 |
| Wi-Fi | Phủ toàn Main Site; quy hoạch Wi-Fi chi nhánh theo khảo sát, tách khách khỏi nội bộ | [A] tr.1, 3-4 |
| WAN | **2 leased lines**, mỗi tuyến nối Main với một Aux Site; xem xét SD-WAN, MPLS và phương án thay thế theo chi phí | [A] tr.2-3 |
| Internet | **2 đường xDSL có load balancing**; Internet của cả 3 site **đều đi qua Main** | [A] tr.2 |
| Ứng dụng | Licensed + open source; HIS, RIS/PACS, LIS, CRM, văn phòng, client-server, multimedia, database | [A] tr.2 |
| Bảo mật và vận hành | Khả năng mở rộng, security, firewall, IDS/IPS, chống phishing, HA, chịu lỗi, dễ nâng cấp | [A] tr.2-4 |
| VPN và camera | Đề xuất **site-to-site VPN**, **teleworker VPN** và **hệ thống camera giám sát** | [A] tr.2 |
| Tăng trưởng | **20% trong 5 năm** về người dùng, tải mạng, mở rộng site; không phải 20% mỗi năm | [A] tr.3 |

Quy hoạch 5 năm: Main **720** workstation; DBP **312**; BHTQ **312**; tổng **1.344**. Với server, tính theo từng site và làm tròn lên cho kết quả **12 + 3 + 3 = 18 server**, thay vì làm tròn tổng 14 × 1,2 thành 17 rồi phân bổ thiếu ở chi nhánh. Đây là lượng dự trù, không tự thêm server vào quy mô ban đầu.

## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
