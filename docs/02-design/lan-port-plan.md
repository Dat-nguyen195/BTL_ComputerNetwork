# VLAN, access port và mapping phòng/tầng

**TV2;02/11/2026. BẢN THIẾT KẾ/CONFIG THAM CHIẾU, CHƯA CHỐT KHẢO SÁT.** VLAN là nghiệp vụ, không đồng nhất một tầng/phòng với một VLAN. Main600→720 PC chia6 VLAN10/20/30/40/50/60 (100→120 PC/VLAN). Mỗi Aux260→312 PC chia10/20/30 (90/90/80→108/108/96), theo [IP plan](ip-vlan-plan.md).

## Phân bổ cổng sản xuất để đủ tăng trưởng

Main20 switch, mỗi tầng2 switch48 port. Mỗi switch dành36 portPC:1–6 VLAN10,7–12 VLAN20,13–18 VLAN30,19–24 VLAN40,25–30 VLAN50,31–36 VLAN60. Hiện dùng5/6 port mỗi nhóm (=30 PC/switch), tăng lên6/6 (=36). Tổng20 switch tạo đúng 100→120 PC mỗi VLAN; vị trí phòng và patch panel phải khảo sát/ghi nhãn sau.

Main cổng37/38 dự trù2 AP/switch (uplink modelWLC native90, tagged100/120); cổng39–41 cameraVLAN110 trênS1,39–40 trênS2. Sau tăng trưởng41/48 và 40/48 cổng dùng; còn 7/8. Các cổng chưa dùng shutdown. AP/camera cùng tầng được phân phối PoE theo ngân sách từng switch, không chỉ tổng tầng.

Mỗi Aux4 switch/tầng, hiện33/33/32/32 PC,5 năm39 PC/switch. Phân bổ VLAN theo tầng: hiện45/45/40 PC,5 năm54/54/48. Ví dụ5 nămS1/S2 mỗi switch14/14/11 PC, S3/S4 mỗi switch13/13/13 PC. AP1/switch, camera5/tầng phân2/1/1/1. Tầng1 thêm3 server+1 NVR phân1 port/switch; tối đa43/48 trênS1,42/48 các switch còn lại, tổng 169/192. Địa chỉ server/NVR cố định theo TV3; không cấp chúng từ poolPC.

Uplink dùng2 cổng10 G/switch, ngoài48 cổngaccess; một tới mỗi core theo [campus-uplinks.csv](campus-uplinks.csv). Core độc lập dùng trunk/RSTP; không LACP xuyên hai core chưa là một logical switch. Trunk campus chỉ 10–70/90/100/110/120 theo site, **khôngVLAN80**. DMZ nối riêngMain-FW.

## Quản trị, gateway và IP

Switch quản trịMain đề xuất10.10.90.32–51 (20 switch), mỗi Aux10.20/30.90.32–39. AdminMain10.10.90.11, WLC .90.20/.21, AP management theo wireless plan để không đụng poolswitch. Core/gatewaylab .1; sản xuấtHA dự trùVIP .1, core .2/.3 trong reserved, phải chốt model/route/HSRP và ACL trên **cả hai** SVI trước triển khai. Chưa có HA runtime.

[Adapter3650](../../simulation/modules/tv2-lan-wireless/configs/Main-Core-3650.cfg) thay ROAS Main-Core bằng SVI, giữ ACL/DHCP relay/OSPF/default của TV1/TV3. G1/0/23→Main-GW .10 trên10.255.0.8/30; G1/0/24→Main-FW .14 trên10.255.0.12/30, phải `no switchport`. Không chạy đồng thời ROASgateway .1 và 3650 SVI .1. Aux hiện giữROAS bản hợp nhất; nếu đổi sangdistributionSVI phải remap tương tự và tránh gatewaytrùng.

## Native module Tiendat

Giữ nguyên `.pkt` gốc và hash trong [manifest module](../../simulation/modules/tv2-lan-wireless/reference-manifest.json). Core3650, accessA/B2960; LACP2 linkmỗiaccess về cùngcore có thể dùng làm functional module, không chứng minh10 GbE hoặc dualcoreHA. Patch accessA/B đặtPC ports1/2 VLAN10/20, APGuestport3 access100, APStaffbổ sungport4 access120; đóng cổng dư. Hostname khác nhau, quản trịswitchA .90.32/B .90.42.

[TC01](../../test_results/TC01-same-vlan/result.md): PC0↔PC2 VLAN10; [TC02](../../test_results/TC02-inter-vlan/result.md): PC0↔PC1 VLAN10/20 có quyền. IP/gateway trên4 PC gốc chưa lưu; phải cấpDHCP sau khi thêmInfra hoặc dùngIPtĩnh smoke tạm theo module, không ghiPASS từ file gốc. Lưu startup/project, mở lại, thu log/ảnh/hash thật trước nghiệm thu.
