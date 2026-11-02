# Hạ tầng vật lý, cabling và lựa chọn GPON

**TV2; review tích hợp02/11/2026. THIẾT KẾ GIẢ ĐỊNH, CHƯA ĐO TUYẾN CÁP.** Yêu cầu Main hai tòaA/B, mỗi tòa5 tầng×10 phòng; IT/Data Center/CCL ở phòng riêng cách hai tòa50 m. Đây không phải cự ly tối thiểu hoặc chiều dài cáp đo được. Mỗi Aux2 tầng, MDF/IT/CCL tầng1 vàIDF tầng2.

## MDF /IDF và cáp baseline

Main có 10 IDF,2 access48 port/IDF; mỗi Aux4 access/tầng,8/site. Active Ethernet dùng Cat6 từ access tới PC/AP/camera, dự trù1 GbE; cáp quang OM3 duplex10 GbE từ access tới core/distribution.40 GbE chỉ là liên kết core-core dự trù, không phải tốc độ của model3650/2960 trong `.pkt`. Cổng FastEthernet của2960-24TT chỉ 100 Mbps, không được ghi Fa0/1 là 1 GbE.

Mỗi access có 2 uplink: một tới Core1 qua tuyếnA, một tới Core2 qua tuyếnB. Với core độc lập, dùng trunk độc lập +RSTP, gatewayHA cần HSRP/VRRP được cấu hình riêng; không ghép một LACP xuyên hai core chưa stack/virtual hóa. [Cisco EtherChannel designs](https://www.cisco.com/c/en/us/support/docs/lan-switching/gigabit-etherchannel-gec/222012-etherchannel-designs.html) phân biệt một switch vật lý với một logical switch/stack. Bản `.pkt` Tiendat ghép2 link về **cùng một core** nên LACP đúng phạm vi nhưng không có chassisHA.

[Danh mục72 link](campus-uplinks.csv) ghi từng switch/cổng/core/tuyến, gồm 40 Main,16 DBP,16 BHTQ. Tên Te là tên cổng **đề xuất sản xuất**, phải remap theo model mua; không dùng chúng như output từ Packet Tracer. Main2 switch/IDF→4 link duplex=8 sợi, chia4 sợi/tuyếnA và 4/tuyếnB; dự trù hai cáp12 sợi **hai ống độc lập** mỗi IDF. Auxtầng2 có 4 switch→8 link duplex,8 sợi/tuyếnA và 8/tuyếnB, hai cáp12 sợi. Đi chung một ống không tạo dự phòng chống đứt cả tuyến.

Cat6 dự trù30 m/drop và 10% hao hụt để tính BOM, không phải khảo sát. Khi triển khai phải giới hạn permanent link/channel theo loại cáp/standard chọn, tính patch cord, đi dây/ống/tiếp địa/chống cháy/ODF, đo kiểm quang và đồng. Không kéo fiber multimode ra leased line Main–Aux rồi coi là mạng campus10 G: nhà mạng cung cấp handoff/SLA riêng.

## Bảng tham chiếu có thể sửa /xuất

- [Main drawio](diagrams/physical-main.drawio) và [SVG Main](diagrams/exports/physical-main.svg):20 switch access,10 IDF, server/DMZ tách riêng, cổng core28/32 và các vùng dự trù.
- [Aux drawio](diagrams/physical-aux.drawio) và [SVG Aux](diagrams/exports/physical-aux.svg): IT/CCL tầng1,4 switch/tầng, NVR/server tại site.
- [BOM](equipment-bom.md), [port plan](lan-port-plan.md), [logical diagram](diagrams/logical-3sites.mmd) và [mapping lab](../../simulation/lab/cabling.csv).

Nguồn drawio và SVG cùng geometry sinh từ `scripts/build_campus.py`; không trỏ tới PNG chưa được tạo. Bản vẽ là khối chức năng, không phải bản vẽ thi công hoặc chiều dài đã đo.

## GPON: phương án cần xác nhận theo yêu cầu đề

Đề nhắc GPON; hiện Active Ethernet là **baseline mô phỏng của nhóm, chưa có xác nhận được bỏ GPON**. GPON vẫn là khoảng trống triển khai, không đánh dấu hoàn thành chỉ từ tuyến quang Ethernet. TV1 xác nhận với giảng viên nếu cần GPON trong phần chạy; TV2 chuẩn bị thiết kế riêng:

| Thành phần | Đề xuất sơ bộ Main | Điều kiện |
| --- | --- | --- |
| OLT |1 OLT có≥2 PON port và uplink10 G tới core;2 nếu thực sự cần redundancy |Báo giá/HA/nguồn/license chưa có |
| ODN/splitter |Mỗi tòa1 splitter1:8, phục vụ5 ONT/tòa |Fiber single-mode OS2 +SC/APC theo thiết bị, **không dùng OM3 của10GBASE-SR** |
| ONT |10 ONT,1/tầng; Ethernet uplink/downlink theo số access/AP phục vụ |Không giả định ONT4 port thay được96 cổng của2 access switch |
| Dịch vụ |Chỉ chọn vùng office/guest sau khảo sát; tách VLAN và quản trị |PACS/video peak cần đánh giá shared medium và uplink ONT |

Theo [Cisco GPON](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-pon-series/216230-understand-gpon-technology.html), PON chia sẻ khoảng 2,488 Gbps down/1,244 Gbps up; không phải mỗi ONT được toàn bộ tốc độ. Tính optical loss riêng từng chiều từ Tx/Rx/budget model: `L=fiber+splitter+connector+splice+margin`, kiểm cả mất mát tối đa và công suất nhận quá cao. Chưa có model/đo OTDR nên không tự gán kết luận optical budget PASS. OLT/splitter/ONT/OS2 không được âm thầm cộng chung baseline OM3 hoặc gọi labEthernet là GPON.
