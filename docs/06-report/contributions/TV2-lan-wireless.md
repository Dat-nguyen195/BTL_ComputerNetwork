# Nội dung TV2: LAN, Wi-Fi, cabling và thiết bị

**Chủ trì gốc: Phạm Tiến Đạt, nhánh `tiendat`, commit `3f52588`. Hiệu chỉnh tích hợp 02/11/2026. TV5 biên tập; TV1 duyệt cuối. Đã rà soát thiết kế/config tĩnh; chưa nghiệm thu runtime hoặc ký nhận chính thức.**

## Quy mô và kiến trúc

Main gồm hai tòa A/B, mỗi tòa 5 tầng ×10 phòng; MDF/IT/Data Center ở phòng riêng cách hai tòa 50 m theo đề. Mỗi Aux có 2 tầng với IT/CCL tại tầng1. Quy mô PC là 600/260/260, server 10/2/2; PC sau 5 năm là 720/312/312. VLAN theo nghiệp vụ, không đồng nhất một tầng/phòng với một VLAN.

Main có sáu VLAN PC10–60, mỗi VLAN100→120 máy; Aux có ba VLAN10/20/30, từ90/90/80 lên108/108/96. [IP plan](../../02-design/ip-vlan-plan.md) quy định gateway/pool. Thiết kế sản xuất dùng Cat6 1 G tới đầu cuối, OM3 10 G lên core/distribution và 40 G core-core dự trù. DMZ VLAN80 tách switch riêng sau firewall; campus không mang VLAN80.

## Cổng, PoE và quang

Main giữ 20 switch access48 cổng, mỗi tầng/tòa2 switch: dùng670 cổng hiện tại,810 sau 5 năm, dư150/960. Mỗi Aux giữ 8 switch48 cổng: dùng277 hiện tại,334 sau 5 năm, dư50/384; đã gồm 1 NVR và server2→3. AP giả định3/tầng tăng và làm tròn lên4, camera4/tầng lên5; tổng AP toàn hệ thống42→56, camera56→70. Đây là dự trù cổng, chưa phải khảo sát RF/camera.

[Port plan](../../02-design/lan-port-plan.md) phân bổ PC theo VLAN trên từng switch và dành cổng AP/camera. [Campus inputs](../../02-design/campus-inputs.csv) và [budget](../../02-design/campus-budget.csv) được tái lập bằng script. Mỗi tầng cần151,6 W PSE hiện tại và 197 W tương lai; C9200L-48P-4X với PSU1 kW có 740 W/switch theo nguồn Cisco trong BOM. Phải kiểm từng cổng/switch/UPS, không dùng tổng PoE để kết luận HA.

AP9115AXI hỗ trợ2,5 G nhưng switch baseline chỉ 1 G xuống AP, giới hạn này được ghi rõ. Mỗi WLC dự trù hỗ trợ≥64 AP vì56 AP có thể cần được một controller phục vụ khi lỗi. Model, compatibility, license và mức tiêu thụ điện vẫn cần báo giá/datasheet cuối.

Có72 link quang access:40 Main,16 DBP,16 BHTQ. Hai module/link cho80/32/32; thêm spare10% làm tròn thành 88/36/36 module, chưa gồm optics dịch vụ. Mỗi IDF Main có hai tuyến OM3 12 sợi độc lập, dùng4 sợi/tuyến; Aux tầng2 dùng8 sợi/tuyến. Cat6 giả định30 m/drop và 10% hao hụt cho88 thùng Main,37 thùng mỗi Aux; chưa đo chiều dài thực.

Core độc lập dùng trunk/RSTP; LACP xuyên hai chassis chỉ khi đã là một logical switch. File Tiendat ghép hai link1 G về cùng3650 nên LACP đúng phạm vi, nhưng không chứng minh dualcore HA. FastEthernet của2960-24TT chỉ 100 Mbps. [BOM](../../02-design/equipment-bom.md) và [cabling](../../02-design/physical-cabling.md) tách sản xuất với mô hình lab; giá/license/công suất chưa xác nhận giữ OPEN.

## Wireless, GPON và camera

[Wireless plan](../../02-design/wireless-plan.md) map Staff→VLAN120, Guest→100, quản trị AP→90. Cần khảo sát mật độ đồng thời, airtime, kênh, roaming; triển khai AAA và client isolation. AP-PT gốc chỉ Guest untagged nên adapter đổi cổng sang access100; thêm AP Staff riêng nếu model không hỗ trợ hai SSID. ACL IPv4 không chứng minh phủ sóng hoặc cách ly hai client cùng SSID.

GPON trong đề chưa triển khai. Phương án OLT/ODN/ONT dùng OS2 và optical budget riêng được mô tả; cần xác nhận phạm vi với giảng viên. Không gọi Ethernet OM3 là GPON hoặc tự duyệt bỏ yêu cầu này.

Camera giả định Main40→50, mỗi Aux8→10, VLAN110 và NVR ghi local. [Camera plan](../../02-design/camera-plan.md) thống nhất4 Mbps/camera,30 ngày,5% recording overhead và 80% fill: dung lượng usable5 năm cần85.050 GB Main,17.010 GB mỗi Aux. NVR/ổ/license phải chốt và thử thực tế; chỉ lưu lượng xem/backup từ xa mới cộng vào WAN.

## Module và kiểm chứng

[Module README](../../../simulation/modules/tv2-lan-wireless/README.md) giữ file `.pkt` gốc nguyên byte và audit. Metadata lưu version9.0.0.0810, chỉ 10 thiết bị/10 cáp Main:3650, hai2960, bốn PC, hai AP và PDU; chưa có Aux/WAN/FW/ISP/server. PC chưa lưu IP/gateway, startup-config trống. Không có evidence cho đoạn TC01 PASS/ngày 12/11 trong tài liệu quy trình nên đoạn đó đã gỡ; ngày hạn không được coi là ngày đã chạy.

Ba adapter text sửa SVI/ACL/relay/routing/OSPF/default trên3650 và hostname/port/LACP/guest trên hai2960. Chỉ nạp vào **bản sao**, thay ROAS Core; không để gateway .1 trùng nhau. Chưa sửa/repack binary hoặc chạy Packet Tracer. `check_lan.py` kiểm budget, diagram, hash, adapter và 37 flow ACL Main; `verify.py` kiểm toàn bộ gói tham chiếu. TC01/02/05/06 và persistence vẫn NOT RUN; [runbook](../../../simulation/test-runbook.md) là procedure/expected.

## Đánh giá và bàn giao

Thiết kế có MDF/IDF, dự trù đủ cổng5 năm và quyền VLAN rõ. Còn thiếu khảo sát RF/cáp/PoE, tải HIS/PACS/khách, runtime HA/GPON/AAA/isolation, báo giá và compatibility. Dư cổng không ngăn mất host khi access switch hỏng; module Main chưa đạt Step4 tổng 3 site.

TV5 có thể dùng phần này cho Step1/2/4/6 và bổ sung ảnh/log thật sau khi TV4 ghép. [Review TV2](../../00-management/tv2-review.md) ghi phát hiện và trạng thái xử lý. Người nhận/ngày/PR/chữ ký học phần chờ xác nhận thực, không tự điền thay thành viên.
