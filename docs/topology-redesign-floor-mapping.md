# Ánh xạ tầng trong bản redesign

**Trạng thái: đã đối chiếu native102/97, đăng ký14 camera và hồi quy/runtime sau mở lại.** Switch/PC/AP/camera là mẫu đại diện, không thay ngân sách sản xuất.

| Tầng | Switch → uplink | PC / VLAN | AP / VLAN | Camera / VLAN110 |
|---|---|---|---|---|
| MAIN-A-F1 | Main-A-F1-SW → Main-A-DIST FastEthernet0/1 | Main-PC10-A / 10 | Main-Guest-AP / 100 | Main-A-F1-CAM / 10.10.110.100 |
| MAIN-A-F2 | Main-A-F2-SW → Main-A-DIST FastEthernet0/2 | Main-PC10-B / 10 | Main-Staff-AP / 120 | Main-A-F2-CAM / 10.10.110.101 |
| MAIN-A-F3 | Main-A-F3-SW → Main-A-DIST FastEthernet0/3 | Main-PC20 / 20 | Main-A-F3-AP / 120 | Main-A-F3-CAM / 10.10.110.102 |
| MAIN-A-F4 | Main-A-F4-SW → Main-A-DIST FastEthernet0/4 | Main-PC30 / 30 | Main-A-F4-AP / 120 | Main-A-F4-CAM / 10.10.110.103 |
| MAIN-A-F5 | Main-A-F5-SW → Main-A-DIST FastEthernet0/5 | Main-PC40 / 40 | Main-A-F5-AP / 100 | Main-A-F5-CAM / 10.10.110.104 |
| MAIN-B-F1 | Main-B-F1-SW → Main-B-DIST FastEthernet0/1 | Main-PC50 / 50 | Main-B-F1-AP / 120 | Main-B-F1-CAM / 10.10.110.105 |
| MAIN-B-F2 | Main-B-F2-SW → Main-B-DIST FastEthernet0/2 | Main-PC60 / 60 | Main-B-F2-AP / 120 | Main-B-F2-CAM / 10.10.110.106 |
| MAIN-B-F3 | Main-B-F3-SW → Main-B-DIST FastEthernet0/3 | Main-B-F3-PC / 10 | Main-B-F3-AP / 100 | Main-B-F3-CAM / 10.10.110.107 |
| MAIN-B-F4 | Main-B-F4-SW → Main-B-DIST FastEthernet0/4 | Main-B-F4-PC / 20 | Main-B-F4-AP / 120 | Main-B-F4-CAM / 10.10.110.108 |
| MAIN-B-F5 | Main-B-F5-SW → Main-B-DIST FastEthernet0/5 | Main-B-F5-PC / 60 | Main-B-F5-AP / 120 | Main-B-F5-CAM / 10.10.110.109 |
| DBP-F1 | DBP-F1-SW → DBP-Access FastEthernet0/12 | DBP-PC10 / 10, DBP-PC20 / 20 | DBP-Guest-AP / 100 | DBP-F1-CAM / 10.20.110.100 |
| DBP-F2 | DBP-F2-SW → DBP-Access FastEthernet0/13 | DBP-PC30 / 30 | DBP-Staff-AP / 120 | DBP-F2-CAM / 10.20.110.101 |
| BHTQ-F1 | BHTQ-F1-SW → BHTQ-Access FastEthernet0/12 | BHTQ-PC10 / 10, BHTQ-PC20 / 20 | BHTQ-Guest-AP / 100 | BHTQ-F1-CAM / 10.30.110.100 |
| BHTQ-F2 | BHTQ-F2-SW → BHTQ-Access FastEthernet0/13 | BHTQ-PC30 / 30 | BHTQ-Staff-AP / 120 | BHTQ-F2-CAM / 10.30.110.101 |

Các appliance quản lý IoT nằm ngoài 14 application server trong đặc tả. Chúng không chứng minh ghi hình, lưu trữ video hoặc retention 30 ngày.
