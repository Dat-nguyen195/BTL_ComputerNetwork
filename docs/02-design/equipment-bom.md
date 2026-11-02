# BOM và kiểm ngân sách cổng/PoE/quang

**TV2 Phạm Tiến Đạt chủ trì; hiệu chỉnh tích hợp 02/11/2026. THIẾT KẾ GIẢ ĐỊNH / CHƯA KHẢO SÁT, BÁO GIÁ HOẶC NGHIỆM THU.** Giữ phương án20 switch Main và 8 switch mỗi Aux của Tiendat; sửa sizing, vùng DMZ và thông số model. [Đầu vào CSV](campus-inputs.csv), [kết quả](campus-budget.csv) được tái lập bằng `python3 scripts/build_campus.py`.

## 1. Port budget hiện tại /5 năm

PC tăng tổng 20%. AP/camera là giả định3 AP+4 camera/tầng hiện tại; tăng và làm tròn **từng tầng** lên4 AP+5 camera, vì thiết bị không chia lẻ. Đây là dự trù cổng/PoE, không phải sizing RF đã được đo. NVR Main nối switch Server Farm; NVR Aux có 1 cổng access tại MDF tầng1, không bỏ sót trong budget.

| Site | Access /cổng | PC hiện tại→5 năm | AP | Camera | Server trên access | NVR trên access | Dùng hiện tại→5 năm | Dư5 năm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main |20 ×48=960 |600→720 |30→40 |40→50 |0 |0 |670→810 |150 |
| DBP, mỗi site |8 ×48=384 |260→312 |6→8 |8→10 |2→3 |1 |277→334 |50 |
| BHTQ, mỗi site |8 ×48=384 |260→312 |6→8 |8→10 |2→3 |1 |277→334 |50 |

Mỗi tầng Main có 2 switch,5 năm72 PC+4 AP+5 camera=81/96 cổng. Aux4 switch/tầng: tầng1 tối đa156 PC+4 AP+5 camera+3 server+1 NVR=169/192; tầng2 dùng165/192. Không đặt toàn bộ PC/server vào12 thiết bị mạng chỉ để khớp số minh họa của đề. Switch hỏng vẫn làm mất host nối vào nó; dư tổng cổng không tự tạo HA cho từng máy.

## 2. PoE, AP và uplink

C9200L-48P-4X với nguồn PWR-C5-1KWAC có **740 W PoE** theo [Cisco datasheet](https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9200-series-switches/nb-06-cat9200-ser-data-sheet-cte-en.html). Bản48 PL với nguồn600 W mới là 370 W; không nhầm hai SKU.48 P có 48 ×1 G và 4 ×10 G uplink; model thực, license, nguồn và khả năng cung cấp phải chốt theo báo giá.

PSE budget giả định30 W/AP và 15,4 W/camera. Mỗi tầng hiện tại 151,6 W,5 năm197 W. Main2 switch/tầng có 1480 W; Aux4 switch/tầng có 2960 W, đều dư trên giấy. Phải kiểm từng switch/cổng, phân phối thiết bị và điều kiện mất một PSU; không coi tổng hai PSU là công suất còn lại khi đã mất một PSU. Có thể đổi một phần sang switch không PoE sau thiết kế chi tiết và đối soát BOM.

AP tham chiếu9115AXI có uplink100 M/1 G/2,5 G theo [Cisco AP datasheet](https://www.cisco.com/c/en/us/products/collateral/wireless/catalyst-9100ax-access-points/datasheet-c78-741988.html). Baseline switch48 P chỉ cấp **1 GbE tới AP**, không cam kết2,5 GbE. Nếu đo RF/dung lượng yêu cầu hơn1 G/AP, thay switch có mGig và tính lại PoE/license/BOM.42 AP hiện tại và 56 AP dự trù theo từng tầng; mỗi WLC dự trù phải quản lý≥64 AP để không thiếu khi failover.

## 3. BOM Main (số lượng đề xuất, giá OPEN)

| Hạng mục | SL | Spec/cổng/uplink tối thiểu | PoE/quang/license/công suất | Nguồn giá /người chốt |
| --- | --- | --- | --- | --- |
| Core L3 |2 |≥32 cổng1/10 G và≥2 cổng40 G/core;20 access+2 Server Farm+2 FW+2 WAN+2 WLC=28/32 |10 G SR, core-core2 ×40 G; OSPF/SVI/ACL/HA license theo model; W chờ datasheet |OPEN; TV1/TV2 |
| Access |20 |48 ×1 G+4 ×10 G;2 uplink riêng tới2 core; C9200L-48P-4X tham chiếu |740 W PSE với PSU1 kW; Essentials/L2 theo chức năng, quang ở mục5; W thực phải cộng tải PoE |OPEN; TV2 |
| Switch Server Farm |2 |≥24 ×10 G/switch; mỗi switch10 NIC server+1 NVR+2 uplink core+2 inter-switch=15/24 sau tăng trưởng |VLAN70/90/110; không bridge DMZ; DAC/SFP+, công suất/license theo model |OPEN; TV2/TV3 |
| Switch DMZ tách riêng |2 |≥24 cổng1/10 G; chỉ DMZ server và cổng DMZ FW; không uplink L2 trực tiếp Core |VLAN80, quản trị OOB nếu cần; HA link/NIC theo model, chưa chạy |OPEN; TV2/TV3 |
| Server ứng dụng |10, dự trù12 |8 nội bộ+2 DMZ hiện tại; CPU/RAM/storage chờ khảo sát workload |NIC10 G dual nếu chọn; license OS/DB và W chờ chốt |OPEN; TV3 |
| Firewall |2 dự trùHA |≥4 cổng10 G; sizing theo throughput khi bật inspect/IPS/crypto/session, không chỉ tốc độ port |Security/VPN/IPS subscription, SFP+, W chờ model; lab1 FW |OPEN; TV1/TV3 |
| WAN gateway |2 dự trù |OSPF, handoff2 leased lines, IPsec nếu chọn;≥2 WAN+2 LAN10 G |License/crypto/CPE theo nhà mạng; lab1 gateway Main |OPEN; TV1 |
| Internet Edge /modem |2 Edge+2 modem |PBR/PAT/tracking và 2 xDSL; modem theo ISP; năng lực theo TV4 |Model/license/public IP/PSU chờ chốt; lab1 Edge |OPEN; TV1/TV3 |
| WLC |2 dự trù |Mỗi controller≥64 AP và 2 uplink10 G; controller compatibility phải kiểm |License cho56 AP dự trù, điều kiệnHA chờ báo giá; không cộng trùng license |OPEN; TV2 |
| AP |30→40 |Wi-Fi6, PoE+, uplink1 G trong baseline; RF chưa đo |30 W PSE giả định; controller/software compatibility chưa chốt |OPEN; TV2 |
| Camera |40→50 |4 MP/H.265/PoEaf giả định;1 access port/camera |15,4 W PSE; bitrate4 Mbps giả định, nguồn/vendor chưa chọn |OPEN; TV2/TV3 |
| NVR |1 hệ |≥64 kênh và ingest đáp ứng200 Mbps+headroom5 năm |≥85.050 GB usable sau RAID theo camera plan; model/ổ/license/W chưa chọn |OPEN; TV3 |

Hai switch Server Farm không tự tạo dual-homing: LACP qua hai chassis chỉ khi stack/MLAG được hỗ trợ/cấu hình; nếu không dùng NIC active/standby phù hợp. DMZ nằm sau FW, tuyệt đối không kéo VLAN80 vào trunk campus hoặc uplink DMZ thẳng Core.

## 4. BOM từng Aux

| Hạng mục | SL/site | Spec/cổng/uplink | PoE/license/công suất/giá |
| --- | --- | --- | --- |
| Distribution L3 |2 dự trù |≥16 cổng10 G;8 access+1 WAN+2 interconnect=11/16; SVI/ACL/OSPF/HSRP theo thiết kếHA riêng |SFP+/DAC, license/W/giá OPEN; TV1/TV2 |
| Access |8 |48 ×1 G+4 ×10 G,2 uplink độc lập;4 switch/tầng |C9200L-48P-4X tham chiếu740 W; giá OPEN; TV2 |
| WAN router |1 |1 leased line về Main, OSPF/IPsec nếu chọn; sizing theo TV4 |Một tuyến/site vẫn SPOF; license/W/giá OPEN; TV1 |
| Server cục bộ |2→3 |Infra .70.6, Local .70.7; thêm máy thứ3 khi cần |CPU/RAM/disk/NIC/license/W/giá OPEN; TV3 |
| AP |6→8 |Như Main, local switching VLAN100/120, Internet vẫn qua Main |PoE/RF/license/giá OPEN; TV2 |
| Camera |8→10 |Như Main; ghi local |15,4 W PSE; giá OPEN; TV3/TV2 |
| NVR |1 |≥16 kênh;5 năm40 Mbps video trước headroom |≥17.010 GB usable sau RAID,1 access port; giá OPEN; TV3 |

## 5. Quang, cáp, rack và thụ động

| Hạng mục | Main | Mỗi Aux | Cách tính /giới hạn |
| --- | --- | --- | --- |
| Link access10 G |40 |16 |Mỗi switch2 uplink; [72 link/port/tuyến A-B](campus-uplinks.csv) |
| SFP+ SR cho link access |80+8 spare=88 |32+4 spare=36 |2 module/link, spare10% làm tròn; chưa gồm uplink dịch vụ |
| Fiber trục |Mỗi IDF2 tuyến12 sợi OM3, tổng 20 tuyến giả định |2 tuyến12 sợi tới IDF tầng2, patch phù hợp tầng1 |Main mỗi tuyến dùng4 sợi; Aux tuyến tầng2 dùng8 sợi; tuyến A/B phải đi ống riêng sau khảo sát |
| Cat6,305 m/thùng |88 thùng |37 thùng |Main810/Aux334 drop×30 m×1,1 ÷305, làm tròn;30 m là giả định, chưa đo |
| Patch panel48 cổng |20 |8 |Khớp tổng cổng access; đầu nối/patch cord và nhãn phải bóc tách thêm |
| Rack/UPS/ODF/patch cord |OPEN |OPEN |Main10 IDF+MDF; AuxMDF tầng1+IDF tầng2; W/runtime UPS/chiều dài chờ khảo sát |
| GPON OLT/splitter/ONT |Phương án riêng |Chỉ chọn sau khảo sát |DESIGN ONLY, không cộng vào baseline Active Ethernet |

SR trên OM3 phải kiểm cự ly/connector theo optics được chọn; không lấy khoảng cách50 m giữa tòa làm chiều dài mọi tuyến.40 G/DAC/Server/FW/WLC optics chưa nằm trong 80/32 module access, cần dòng báo giá riêng. Toàn bộ giá tạm chưa có nguồn của bản Tiendat được chuyển OPEN; chưa tính tổng hoặc tuyên bố giá thị trường.

## 6. Việc còn mở

TV2/TV5 khảo sát cáp/RF/điện trước 05/11; TV3 xác nhận camera/NVR/RPO/RTO trước 06/11; TV1/TV2 thu báo giá/model/license/thuế trước 08/11/2026 (hạn đề xuất). Đối soát TCO WAN để không cộng trùng CPE/Edge/FW/license. HA/40 G/GPON/mGig, tốc độ sản xuất và RF vẫn DESIGN ONLY. [Review TV2](../00-management/tv2-review.md) ghi phát hiện, chỉnh sửa và hạn chế native `.pkt`.

## Bổ sung GPON trong phương án hybrid

[Thiết kế GPON](gpon-design.md) chọn 80→96 PC VLAN60 Main qua 20→24 ONT; các máy này đã nằm trong tổng PC. Hai uplink OLT bổ sung mỗi Core một cổng (28→29/32), hai splitter1:16 và ODN/OS2 có budget ví dụ, cần đo quang thực. Bảng cổng/cáp Ethernet giữ chỗ dự phòng để rollback. Đây là thiết kế, không phải GPON đã chạy trong GNS3.
