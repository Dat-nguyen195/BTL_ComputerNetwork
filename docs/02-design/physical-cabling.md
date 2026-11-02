

# Sơ đồ đi dây và hạ tầng vật lý

**Chủ trì:** TV2. **Trạng thái:** BẢN THẢO THIẾT KẾ (DRAFT) - CHỜ REVIEW.

## 1. Kiến trúc phân bổ Tủ mạng (MDF/IDF)

Dựa trên yêu cầu kiến trúc của bệnh viện[cite: 1, 7], hệ thống tủ cáp được phân bổ như sau:
*   **Main Site (Tòa A & B):**
    *   **MDF (Main Distribution Frame):** Đặt tại phòng IT & Data Center trung tâm. Đặt Core Switch, Router WAN, Firewall và Server. Cách tòa A và B tối thiểu 50 mét[cite: 7].
    *   **IDF (Intermediate Distribution Frame):** Mỗi tòa A và B có 5 tầng. Đặt 1 tủ IDF tại phòng kỹ thuật của mỗi tầng (Tổng 10 tủ IDF cho Main Site) để thu hẹp khoảng cách kéo cáp đồng tới 100 phòng ban[cite: 7].
*   **Auxiliary Sites (DBP & BHTQ):**
    *   **MDF/CCL:** Đặt tại Tầng 1 theo yêu cầu[cite: 7]. Chứa Router, Switch tổng chi nhánh và 2 Server cục bộ.
    *   **IDF:** Đặt 1 tủ IDF tại Tầng 2.

## 2. Quyết định Công nghệ Cáp (Cabling Technology)

Để đảm bảo tính dự phòng, dễ dàng nâng cấp băng thông 20% trong 5 năm tới và phù hợp với giới hạn của công cụ Packet Tracer (giả lập GPON còn hạn chế), hạ tầng sử dụng công nghệ **Active Ethernet**:
*   **Trục chính (Backbone - MDF đến IDF):** Sử dụng **cáp quang Multi-mode (OM3/OM4)**. Cự ly 50m+ nằm trong phạm vi hiệu quả của cáp Multi-mode. Giao tiếp qua module SFP+ đạt tốc độ **10GbE**. Triển khai 2 sợi cáp quang chạy song song gộp luồng (LACP EtherChannel) để dự phòng chống đứt cáp (HA). *(Ghi chú: Hiệu năng 10GbE/40GbE là phần chỉ thiết kế - DESIGN ONLY, không đo đạc thực tế trên Packet Tracer)*.
*   **Lớp truy cập (Access - IDF đến Thiết bị):** Sử dụng **cáp đồng UTP CAT6**. Đảm bảo tốc độ **1GbE** tới các workstation. Cáp này đồng thời hỗ trợ truyền nguồn điện **PoE+ (802.3at)** cho các Access Point Wi-Fi và Camera IP.

## 3. Bảng kết nối đi dây chi tiết (Cabling Schedule)

Dưới đây là bảng trích xuất tiêu biểu các tuyến cáp trọng yếu (Sẽ đối chiếu với sơ đồ `physical-main.drawio`):

| Link ID | Đầu A / port | Đầu B / port | Tầng/phòng | Môi trường | Tốc độ | Chiều dài | Dự phòng |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LNK-M-A1-1 | MDF Main (Gig1/0/1) | IDF Tòa A Tầng 1 (Gig0/1) | Cáp trục ngoài trời | Cáp quang OM3 | 10GbE | ~60m | Có (LACP ghép cặp với LNK-M-A1-2) |
| LNK-M-A1-2 | MDF Main (Gig1/0/2) | IDF Tòa A Tầng 1 (Gig0/2) | Cáp trục ngoài trời | Cáp quang OM3 | 10GbE | ~60m | Có (LACP ghép cặp với LNK-M-A1-1) |
| LNK-M-B1-1 | MDF Main (Gig1/0/3) | IDF Tòa B Tầng 1 (Gig0/1) | Cáp trục ngoài trời | Cáp quang OM3 | 10GbE | ~75m | Có (LACP ghép cặp với LNK-M-B1-2) |
| LNK-A1-PC1 | IDF Tòa A Tầng 1 (Fa0/1)| Workstation (Tiếp nhận) | Tòa A - Tầng 1 | Cáp đồng CAT6 | 1GbE | ~15m | Không |
| LNK-A1-AP1 | IDF Tòa A Tầng 1 (Fa0/2)| Access Point 1 | Tòa A - Tầng 1 | Cáp đồng CAT6 | 1GbE | ~20m | Không (Có cấp nguồn PoE) |
| LNK-DBP-01 | MDF DBP Tầng 1 (Gig0/1) | IDF DBP Tầng 2 (Gig0/1) | Hộp kỹ thuật lõi | Cáp quang OM3 | 10GbE | ~10m | Có (LACP với port Gig0/2) |
| LNK-DBP-PC1| IDF DBP Tầng 2 (Fa0/1) | Workstation (Nghiệp vụ) | DBP - Tầng 2 | Cáp đồng CAT6 | 1GbE | ~25m | Không |

## 4. Tham chiếu Sơ đồ
* Bản vẽ sơ đồ đi dây vật lý Main Site: `diagrams/exports/physical-main.png`
* Bản vẽ sơ đồ đi dây vật lý 2 Chi nhánh: `diagrams/exports/physical-aux.png`

## Theo dõi cập nhật
- [x] Xác nhận kiến trúc Active Ethernet thay thế GPON nhằm thuận tiện cấu hình mô phỏng.
- [ ] TV2 hoàn thiện bản vẽ `.drawio` để khớp với số liệu trong Bảng đi dây chi tiết.
- [ ] Chờ TV1 và TV4 rà soát (Review) số lượng cổng quang trên Core Switch để đảm bảo đủ kết nối.