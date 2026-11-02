# Thiết bị và đặc tính tối thiểu

**Chủ trì:** TV2. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU (chờ TV1 đọc chéo, chưa khảo sát thực địa).

## 1. Khảo sát và cơ sở sizing

TV5 chủ trì checklist khảo sát (phòng/tầng, tuyến cáp, rack/IDF, điện/UPS, RF, camera, ISP...). Vì chưa khảo sát thực địa, mọi số liệu về chiều dài cáp, RF, góc camera, số rack/UPS dưới đây là **giả định/chưa xác nhận**, không phải kết quả đo.

Quy ước: **OPEN** = chưa chọn/chưa báo giá; **Giả định** = số do TV2 tự đặt để tính, cần xác nhận. Đơn giá chỉ là **giá tạm của nhóm, chưa có nguồn báo giá và ngày lấy giá** (README: các biến chi phí là ô chờ báo giá). Chưa cộng tổng chi phí vì còn nhiều dòng OPEN.

Kiến trúc baseline: **Active Ethernet** (access Cat6 1GbE, uplink/backbone 10GbE quang OM3, 40GbE chỉ giữa hai core). **GPON không nằm trong BOM baseline** (OLT/splitter/ONT = DESIGN ONLY); nếu nhóm chọn GPON thì phải tính lại OLT, tỉ lệ chia, ONT và optical budget theo `physical-cabling.md`. File `.pkt` mô phỏng bằng model 3560/2960; model dưới đây là đề xuất thực tế, cần đối chiếu datasheet.

## 2. Port budget (hiện tại và 5 năm)

Chỉ tính cổng access 1G (không tính uplink). Tăng trưởng 20% trong 5 năm áp dụng cho PC; AP/camera giữ giả định.

| Site | Switch access | Cổng access | PC hiện tại → 5 năm | AP | Camera | Server nối access | Dùng hiện tại | Dùng 5 năm | Dư 5 năm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main | 20 × 48 | 960 | 600 → 720 | 30 | 40 | 0 (server vào switch server/DMZ) | 670 (69,8%) | 790 (82,3%) | 170 |
| DBP | 8 × 48 | 384 | 260 → 312 | 6 | 8 | 2 → 3 | 276 (71,9%) | 329 (85,7%) | 55 |
| BHTQ | 8 × 48 | 384 | 260 → 312 | 6 | 8 | 2 → 3 | 276 (71,9%) | 329 (85,7%) | 55 |

- Mốc tối thiểu của README (chỉ tính PC): Main 13/15 switch, Aux 6/7 switch. Thiết kế dùng **20 (Main) và 8 (mỗi Aux)** để còn chỗ cho AP, camera, server và dư địa.
- **Main:** 2 switch/tầng/tòa × 5 tầng × 2 tòa = 20. Mỗi tầng: 72 PC + 3 AP + 4 camera = 79 ≤ 96 cổng.
- **Aux:** 4 switch/tầng × 2 tầng = 8. Mỗi tầng 5 năm: 156 PC + 3 AP + 4 camera = 163 ≤ 192; tầng 1 thêm 3 server = 166 ≤ 192.
- Nếu đặt PC trong phòng khác (phòng trung tâm, IT/CCL) phải cộng thêm sau khảo sát.

## 3. PoE budget

Dùng mức cấp tối đa theo class để tính an toàn (không phải mức tiêu thụ thực): AP PoE+ 30 W, camera 802.3af 15,4 W. Switch 48 cổng PoE+ có ngân sách 370 W.

| Phạm vi | Tải PoE tối đa | Ngân sách PoE | Kết luận |
| --- | --- | --- | --- |
| 1 tầng Main/tòa A hoặc B (3 AP + 4 camera) | 151,6 W | 2 × 370 = 740 W | Đủ, dùng ~20% |
| 1 tầng Aux (3 AP + 4 camera) | 151,6 W | 4 × 370 = 1.480 W | Đủ, dùng ~10% |

PC không cần PoE, nên có thể thay phần lớn switch bằng bản không PoE để giảm chi phí; chỉ cần đủ cổng PoE gần AP/camera. Quyết định này chờ TV1/TV2 sau khi có báo giá.

## 4. BOM Main

| Site | Hạng mục | SL | Model / đặc tính tối thiểu | Port / speed / uplink | PoE | Quang/SFP | License | Công suất | Đơn giá tạm · nguồn/ngày | Chủ trì | TT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main | Core L3 | 2 | Switch L3 chassis/fixed ≥ 32 cổng 1/10G SFP+ và ≥ 2 cổng 40G QSFP, chạy HA. Ví dụ dòng Catalyst 9500 (kiểm datasheet) | Mỗi core: 20 cổng cho access, 2 cho server/DMZ, 2 cho firewall, 1 cho WLC = 25 ≤ 32; 2 × 40G nối core-core | Không | SFP+ SR ở link access (mục 6), DAC trong MDF | Network Advantage | Chờ datasheet | Chưa báo giá · chưa có | TV1, TV2 | OPEN |
| Main | Access switch | 20 | Catalyst 9200L-48P-4X (hoặc tương đương) | 48 × 1G, **4 × 10G SFP+**; dùng 2 uplink (mỗi core 1) | PoE+ 370 W | 10GBASE-SR (mục 6) | Network Essentials | Chờ datasheet | 65.000.000 (giá tạm, cần cập nhật theo model) · chưa có | TV2 | OPEN |
| Main | Switch server/DMZ | 2 | ≥ 24 cổng 10G (SFP+ hoặc 10GBASE-T), 2 uplink 10G lên hai core; tách VLAN 70 Server Farm / VLAN 80 DMZ | 8 server nội bộ + 2 DMZ, mỗi server 2 × 10G (1 cổng vào mỗi switch) = 20 cổng | Không | DAC/SFP+ | Theo model | Chờ datasheet | Chưa báo giá · chưa có | TV3, TV2 | OPEN |
| Main | Server (HIS/RIS-PACS/LIS/CRM/DB/DNS-DHCP/backup) | 10 | Cấu hình do TV3 chốt (mẫu giả định: 2 CPU, 128 GB RAM, 2 × 10G) | 2 × 10G/server | Không | DAC | Windows/DB | Chờ datasheet | Báo giá riêng | TV3 (phối hợp TV2) | OPEN |
| Main | Firewall NGFW (HA) | 2 | Firewall có IPS và VPN; throughput khi bật IPS/VPN ≥ `B_design` trong `throughput.md` (tạm ≥ 1 Gbps, giả định) | ≥ 4 × 10G (core, WAN, DMZ, Internet edge) | Không | SFP+ | Security/IPS/VPN | Chờ datasheet | Báo giá riêng | TV3 (Edge/Router: TV1) | OPEN |
| Main | Router WAN Main-DBP/BHTQ | 2 (HA) | Router L3, OSPF, 2 handoff leased line, IPsec nếu cần | ≥ 2 cổng WAN + 2 × 10G LAN | Không | SFP/SFP+ theo handoff nhà mạng | Theo model | Chờ datasheet | Báo giá riêng | TV1 | OPEN |
| Main | Internet edge/load balancer + 2 modem xDSL | 2 + 2 | Router/LB cân bằng theo luồng, PAT; modem xDSL do ISP cấp | 2 cổng xDSL + 2 × 10G | Không | — | Theo model | Chờ datasheet | Báo giá riêng / ISP | TV1, TV3 | OPEN |
| Main | WLAN controller (HA) | 2 | Controller phần cứng hoặc ảo, hỗ trợ ≥ 50 AP (42 AP + 20%), quản lý cả AP Aux qua WAN (FlexConnect/local switching) | ≥ 2 × 10G | Không | DAC | License AP | Chờ datasheet | Chưa báo giá · chưa có | TV2 | OPEN |
| Main | Access Point Wi-Fi 6 | 30 | Catalyst 9115AXI hoặc tương đương: 1 × 2,5G mGig, PoE+ (802.3at) | 3 AP/tầng × 10 tầng (giả định, chờ khảo sát RF) | PoE+ 30 W | — | DNA Essentials | Chờ datasheet | 15.000.000 · chưa có | TV2 | OPEN |
| Main | Camera IP | 40 | Dome 4 MP, H.265, PoE 802.3af, VLAN 110 (hãng/model chờ chọn) | 4 camera/tầng × 10 tầng (giả định) | 15,4 W | — | N/A | Chờ datasheet | 3.500.000 · chưa có | TV3, TV2 | OPEN |
| Main | NVR + lưu trữ camera | 1 hệ | Dung lượng = số camera × bitrate × ngày lưu × 1,2. Ví dụ minh họa (3 Mbps, 30 ngày, giả định): 40 camera ≈ 38,9 TB thô, chưa tính dư | ≥ 2 × 10G | Không | — | Theo hãng | Chờ datasheet | Chưa báo giá · chưa có | TV3, TV2 | OPEN |

## 5. BOM mỗi Aux (DBP và BHTQ, số lượng là cho **từng site**)

| Site | Hạng mục | SL | Model / đặc tính tối thiểu | Port / speed / uplink | PoE | Quang/SFP | License | Công suất | Đơn giá tạm · nguồn/ngày | Chủ trì | TT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBP, BHTQ | Core/distribution L3 (collapsed core, HA) | 2 | Switch L3 ≥ 16 cổng SFP+ 10G; kiểm license hỗ trợ OSPF và SVI/ACL cho VLAN 10-120 | Mỗi switch: 8 link access + 1 gateway + 1 firewall/WAN + 2 nối nhau = 12 cổng | Không | SFP+ SR hoặc DAC | Theo model | Chờ datasheet | Chưa báo giá · chưa có | TV1, TV2 | OPEN |
| DBP, BHTQ | Access switch | 8 | Catalyst 9200L-48P-4X (hoặc tương đương) | 48 × 1G, 4 × 10G SFP+; 2 uplink lên 2 distribution; 4 switch/tầng | PoE+ 370 W | 10GBASE-SR (mục 6) | Network Essentials | Chờ datasheet | 65.000.000 (giá tạm, cần cập nhật theo model) · chưa có | TV2 | OPEN |
| DBP, BHTQ | Router WAN gateway | 1 | Router L3, OSPF, 1 handoff leased line về Main, IPsec site-to-site (tạm ≥ 300 Mbps, giả định theo `B_design` Aux 134,10/30,48 Mbps) | 1 WAN + ≥ 1 × 10G LAN | Không | SFP theo handoff | Theo model | Chờ datasheet | Báo giá riêng | TV1 | OPEN |
| DBP, BHTQ | Access Point Wi-Fi 6 | 6 | Như AP Main; 3 AP/tầng × 2 tầng (giả định, chờ khảo sát RF) | 1 × 2,5G mGig | PoE+ 30 W | — | DNA Essentials | Chờ datasheet | 15.000.000 · chưa có | TV2 | OPEN |
| DBP, BHTQ | Camera IP | 8 | Như camera Main; 4 camera/tầng × 2 tầng | 1 × 10/100M | 15,4 W | — | N/A | Chờ datasheet | 3.500.000 · chưa có | TV3, TV2 | OPEN |
| DBP, BHTQ | NVR + lưu trữ | 1 hệ | Công thức như Main. Ví dụ minh họa (3 Mbps, 30 ngày, giả định): 8 camera ≈ 7,8 TB thô | ≥ 1 × 1G/10G | Không | — | Theo hãng | Chờ datasheet | Chưa báo giá · chưa có | TV3, TV2 | OPEN |
| DBP, BHTQ | Server cục bộ | 2 (dự trù 3) | Cấu hình tầm trung, TV3 chốt | 2 × 1G/10G, nối switch access tầng 1 | Không | — | Windows/DB | Chờ datasheet | Báo giá riêng | TV3 (phối hợp TV2) | OPEN |

Aux đạt mốc ≥ 5 thiết bị mạng của đề (2 distribution + 8 access + 1 router = 11). Aux không có firewall riêng trong baseline: chặn khách và ranh giới bảo mật dùng ACL tại distribution/gateway, firewall tập trung tại Main theo README.

## 6. Quang, cáp và thụ động

| Site | Hạng mục | SL | Đặc tính | Cách tính | Đơn giá tạm · nguồn/ngày | TT |
| --- | --- | --- | --- | --- | --- | --- |
| Main | Module 10GBASE-SR SFP+ (OM3, 850 nm, 300 m) | 80 | Cho link access | 20 switch × 2 uplink = 40 link, mỗi link cần module hai đầu = 80 (chưa tính dự phòng 10% và link server/firewall: dùng DAC trong MDF) | 8.000.000 · chưa có | OPEN |
| Main | Cáp quang OM3 trục MDF → IDF | 10 tuyến × 12 sợi | Mỗi IDF: 2 switch × 2 link × 2 sợi = 8 sợi, làm tròn lên 12 sợi, tuyến cuối cùng chờ khảo sát | Chiều dài mỗi tuyến ước ≤ 100 m (50 m khoảng cách tòa + đứng tầng + dư), tổng ≲ 1.000 m (giả định) | Bóc tách sau · chờ khảo sát | OPEN |
| Main | Cáp đồng UTP Cat6 (305 m/thùng) | 86 | Từ IDF tới PC, AP, camera | 790 đường × 30 m trung bình = 23.700 m ÷ 305 = 77,7 thùng, +10% hao hụt = 86 (30 m là giả định, cần đo theo từng tầng) | 3.200.000/thùng · chưa có | OPEN |
| Main | Patch panel Cat6 48 cổng | 20 | 1 panel/switch access | Khớp 20 switch | Chưa báo giá | OPEN |
| Main | Rack | OPEN | 10 rack IDF (1/tầng/tòa) + rack MDF (số lượng chờ khảo sát) | Chờ khảo sát | Chưa báo giá | OPEN |
| Main | UPS | OPEN | Tính theo công suất thiết bị trong cột Công suất + PoE + thời gian lưu điện | Chờ datasheet và khảo sát điện | Chưa báo giá | OPEN |
| DBP, BHTQ (mỗi site) | Module 10GBASE-SR SFP+ | 32 | Cho link access | 8 switch × 2 uplink = 16 link × 2 đầu; link cùng rack tầng 1 có thể thay bằng DAC | 8.000.000 · chưa có | OPEN |
| DBP, BHTQ (mỗi site) | Cáp quang OM3 tầng 1 ↔ tầng 2 | 1 lô | Chiều dài chờ khảo sát | Chờ khảo sát | Bóc tách sau | OPEN |
| DBP, BHTQ (mỗi site) | Cáp đồng UTP Cat6 (305 m/thùng) | 36 | Từ IDF tới PC, AP, camera, server | 329 đường × 30 m = 9.870 m ÷ 305 = 32,4 thùng, +10% = 36 (giả định) | 3.200.000/thùng · chưa có | OPEN |
| DBP, BHTQ (mỗi site) | Patch panel 48 cổng, rack, UPS | 8 / OPEN / OPEN | 1 panel/switch; rack tầng 1 (IT/CCL) và tầng 2 | Chờ khảo sát | Chưa báo giá | OPEN |
| Main, Aux | GPON (OLT, splitter, ONT) | 0 | Không dùng trong baseline | DESIGN ONLY, ghi rõ trong báo cáo | — | DESIGN ONLY |

## 7. Việc còn mở (cần chủ trì và hạn)

| Việc | Người xử lý | Ghi chú |
| --- | --- | --- |
| Chốt model core (≥ 32 cổng SFP+, ≥ 2 × 40G) và đối chiếu datasheet | TV1, TV2 | Thay đổi số cổng core nếu model khác |
| Chốt firewall, router WAN, Edge/LB, throughput khi bật IPS/VPN | TV1, TV3 | Dựa trên `throughput.md` của TV4 |
| Chốt cấu hình server và NVR/lưu trữ | TV3 | Bitrate và số ngày lưu trong `camera-plan.md` |
| Xác nhận có tách switch DMZ vật lý hay dùng VLAN | TV3, TV1 | README yêu cầu switch DMZ/server trong BOM |
| Khảo sát chiều dài cáp, số rack, UPS | TV5 (khảo sát), TV2 | Thay các giả định 30 m và 100 m |
| Báo giá, đơn vị tiền, thuế, ngày lấy giá | TV1, TV2 | Thay toàn bộ cột giá tạm |

## Theo dõi cập nhật

- [ ] TV1 đọc chéo và xác nhận port sizing, giả định và phân công (chưa đóng, vì chưa có reviewer).
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế (chờ khảo sát mặt bằng).
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.