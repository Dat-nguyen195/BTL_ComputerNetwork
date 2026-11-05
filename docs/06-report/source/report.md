---
title: "THIẾT KẾ VÀ MÔ PHỎNG MẠNG BỆNH VIỆN BA CƠ SỞ"
subtitle: "Báo cáo kỹ thuật - Main, Điện Biên Phủ và Bà Huyện Thanh Quan"
author: "L08 - Nhóm 2 | Nguyễn Thành Đạt và Phạm Tiến Đạt"
date: "04/11/2026"
---

# Phạm vi, yêu cầu và nguyên tắc kiểm chứng

Báo cáo đối chiếu đề *Network Design and Simulation for a Critical Large Hospital* của Lai Nguyen, gồm bảy bước thiết kế, tính tải, mô phỏng, kiểm thử, đánh giá và bàn giao. Main có hai tòa A/B, mỗi tòa năm tầng và mười phòng mỗi tầng; phòng DC/IT/MDF riêng cách hai tòa khoảng 50m. Quy mô ban đầu là 600 máy trạm, 10 server tại Main và 260 máy trạm, 2 server tại mỗi cơ sở DBP/BHTQ. Hai cơ sở phụ có hai tầng, phòng IT/MDF ở tầng1.

Mức tăng trưởng của đề là **20% trong cả năm năm**, không phải 20% mỗi năm. Số PC tương lai là 720+312+312=1.344. Server dự trù theo từng cơ sở là 12+3+3=18. Số máy trong mô phỏng chỉ là đại diện chức năng; không dùng 38 endpoint để tuyên bố đã chạy tải của 1.120 PC hiện tại hoặc 1.344 PC tương lai.

Bằng chứng gồm thiết kế/phép tính, runtime GNS3 Linux/FRR và mô phỏng Cisco Packet Tracer 9.0.1.0858. GNS3 có 209 kiểm tích hợp đạt sau sửa firewall; 137 kiểm reopen là bằng chứng lịch sử trước sửa PID. Packet Tracer tổng ba cơ sở đã lưu/mở lại, có 58 thiết bị, 53 cáp và sáu association Wi-Fi; 32 quan sát phù hợp kỳ vọng và bốn HTTP chuyển ISP thủ công đạt. File Packet Tracer gốc của Tiendat vẫn được bảo toàn riêng. Khảo sát và đo triển khai thực chưa thực hiện. Lượt kiểm trực tiếp bổ sung ngày 05/11/2026 và kiểm sau restart controller được trình bày riêng ở phụ lục G; các kết quả lịch sử ở phụ lục A vẫn được giữ nguyên.

## Thành viên và phạm vi thực hiện BTL2

**Lớp L08 - Nhóm 2. Nhóm trưởng: Nguyễn Thành Đạt (2410709).**

| Họ và tên | MSSV | Email | Phân công |
|:-------------------------|:-------------|:-----------------------------------------|:-----------------|
| Nguyễn Thành Đạt | 2410709 | <dat.nguyen19052006@hcmut.edu.vn> | BTL2; nhóm trưởng |
| Nguyễn Phúc Bảo Đạt | 2410696 | <dat.nguyen662006@hcmut.edu.vn> | BTL1 |
| Bùi Công Danh | 2410448 | <danh.buicong@hcmut.edu.vn> | BTL1 |
| Nguyễn Minh Đạt | 2410694 | <dat.nguyen2410694@hcmut.edu.vn> | BTL1 |
| Phạm Tiến Đạt | 2410723 | <dat.pham123qwe@hcmut.edu.vn> | BTL2 |

Theo phân công lại của nhóm, BTL1 do Nguyễn Phúc Bảo Đạt, Bùi Công Danh và Nguyễn Minh Đạt thực hiện; **BTL2 do Nguyễn Thành Đạt và Phạm Tiến Đạt thực hiện**. Báo cáo này trình bày BTL2, đồng thời ghi đủ danh sách nhóm. Các nhãn TV1–TV5 trong kế hoạch là vai trò kỹ thuật, không phải năm người cùng thực hiện BTL2.

# Khảo sát và kiến trúc phù hợp công trình - Step1

## Checklist trước thi công

Khảo sát số người/thiết bị theo phòng, lượng khách đồng thời và lease Wi-Fi; ứng dụng HIS/RIS-PACS/LIS/CRM/DB, tải ảnh DICOM và thời điểm backup; SLA, tải thiết yếu khi lỗi và lịch bảo trì. Kiểm diện tích rack/MDF/IDF, nguồn và UPS, điều hòa, tiếp địa, phòng cháy, khóa cửa và kiểm soát người vào. Khảo sát ống/máng cáp, chiều dài, tuyến A/B độc lập, vị trí ODF/patch panel và nhãn; chiều dài Cat6 phải đáp ứng giới hạn thiết bị/cabling được chọn.

Khảo sát RF theo vật liệu tường, nhiễu, kênh, công suất, roaming và khả năng các thiết bị y tế; khảo sát góc camera, vùng riêng tư, ánh sáng, đường truyền và thời hạn lưu. Checklist không được đánh dấu đã khảo sát khi chưa có biên bản hoặc số đo. Số AP, camera và chiều dài cáp bên dưới là đầu vào thiết kế cần xác nhận.

## Phân tầng và vùng tải cao

Dùng cấu trúc core/distribution/access ở Main; hai cơ sở phụ dùng collapsed core/access. Mỗi IDF có patch panel, uplink quang và UPS. Server Farm, DMZ, người dùng, quản trị, khách, camera và Wi-Fi nhân viên thuộc các VLAN riêng. DMZ chỉ kết thúc trên firewall, không bridge vào core hoặc trunk campus.

Server Farm/PACS/backup và đường Main–Aux là các vùng cần kiểm tải. Thiết kế ưu tiên liên kết 10GbE ở access uplink/server và 40GbE liên core; không suy throughput ứng dụng từ tốc độ cổng. Hai ISP dùng PBR phân nhóm nguồn, PAT theo egress và probe độc lập. PBR không bảo đảm chia tải 50/50 hoặc cộng tốc độ cho một phiên. Cân bằng tải ứng dụng HIS/Web là hướng bổ sung khi có yêu cầu session, health check và HA ứng dụng cụ thể.

Wi-Fi dùng SSID Staff/VLAN120, Guest/VLAN100 và quản trị AP/VLAN90. AP/WLC sản xuất cần WPA2/WPA3 Enterprise tùy khả năng client, 802.1X/RADIUS, ACL và cách ly khách cùng lớp2. GNS3 kiểm host Staff/Guest đại diện qua VLAN có dây. Packet Tracer đã kiểm sáu client Wi-Fi thật trong lab với WPA2-PSK/AES, DHCP và HTTP; chưa kiểm RF thực, WLC, 802.1X hoặc roaming. AP-PT một SSID không được coi là WLC nhiều VLAN.

# Thiết bị, địa chỉ và hạ tầng cáp - Step2

## Quy hoạch VLAN và IP

Khối Main là 10.10.0.0/16, DBP là 10.20.0.0/16, BHTQ là 10.30.0.0/16. Đây là khối phân bổ; interface chỉ dùng subnet con. Gateway là .1. Sáu VLAN PC tại Main và ba VLAN PC mỗi Aux dùng /25 với pool .7–.126, đúng120 lease/pool. Main có 100→120 PC mỗi VLAN; Aux có 90/90/80→108/108/96 PC. VLAN server70 dùng /27 Main, /28 Aux; VLAN90 quản trị và110 camera dùng /24; Guest100 dùng /23, Staff120 dùng /24. VLAN80 DMZ chỉ có tại Main, /27.

Hai leased line Main–DBP và Main–BHTQ là 10.255.0.0/30 và 10.255.0.4/30. Core–Main-GW là .8/30, Core–FW là .12/30, FW–Edge là .16/30. OSPF area0 chạy giữa Main-Core/Main-GW/DBP-GW/BHTQ-GW; interface người dùng passive. Firewall/Edge dùng route cụ thể và default có điều kiện. Static discard của khối dự trữ tránh vòng lặp trên địa chỉ chưa phân bổ.

Địa chỉ Internet mô phỏng thuộc TEST-NET: ISP1 `203.0.113.0/30`, ISP2 `198.51.100.0/30` và Web-Lab `192.0.2.100`. Đây không phải Internet công cộng thật. Bảng IP đầy đủ, địa chỉ endpoint, cổng và cấu hình được bàn giao cùng project.

## Thiết bị và dự phòng cổng

| Hạng mục | Main | Mỗi Aux | Cơ sở thiết kế |
|:-----------------------------|:------------------|:------------------|:-----------------------------------|
| Access switch48 cổng | 20 | 8 | Main2/tầng; Aux4/tầng |
| Cổng dùng hiện tại / năm5 | 670 /810 | 277 /334 | Bao gồm PC, server tại access, AP, camera, NVR theo vị trí |
| Tổng cổng / dư năm5 | 960 /150 | 384 /50 | Chưa phải khả năng forwarding đã đo |
| AP hiện tại / năm5 | 30 /40 | 6 /8 | Ceil tăng trưởng theo tầng; tổng42→56 |
| Camera hiện tại / năm5 | 40 /50 | 8 /10 | Bốn→năm camera mỗi tầng |
| PoE mỗi tầng hiện tại / năm5 | 151,6 /197W | 151,6 /197W | Giả định AP30W, camera15,4W |

Thiết bị tham chiếu access C9200L-48P-4X với PSU PWR-C5-1KWAC có budget PoE740W; không nhầm với bản PSU600W/budget370W. AP C9115AXI hỗ trợ uplink2,5G nhưng cổng downlink1G của switch làm giới hạn thương lượng1G. Model, license, SFP, nhiệt độ, dự phòng nguồn và throughput khi bật inspect/crypto cần xác nhận trước mua. WLC mỗi thiết bị cần capacity ít nhất64 AP để chứa56 AP tương lai; HA WLC chưa triển khai.

Các core độc lập dùng hai trunk/RSTP. Chỉ dùng LACP xuyên hai chassis khi có stack/virtual chassis tương thích. Hai link LACP trong file TV2 gốc cùng nối một core nên không tạo dự phòng chassis.

## Cáp quang, đồng và GPON hybrid

Thiết kế Ethernet có72 uplink quang access:40 tại Main,16 tại mỗi Aux. Một link duplex cần hai sợi; không gọi hai sợi là hai đường độc lập. Main mỗi IDF có hai tuyến OM3 độc lập12 sợi; Aux tầng2 dự trù hai tuyến12 sợi. Tuyến khác ống/máng phải được khảo sát, không được suy từ hai nét trên sơ đồ. SFP có dự phòng10% làm tròn:88 Main và36 mỗi Aux. Ước lượng Cat6 là88 thùng Main,37 mỗi Aux, dựa trên30m/drop,10% hao hụt và305m/thùng; cần bóc khối lượng thực.

GPON phục vụ80 PC hành chính VLAN60 Main, tăng96 trong năm5. Hai cổng PON của một OLT tại MDF nối hai splitter1:16 tại A/B; mỗi tòa có10 ONT4GE, hai ONT mỗi tầng. Năm5 tăng tổng24 ONT, vẫn trong32 nhánh. Hai uplink OLT10GbE tới hai core bổ sung mỗi core một cổng:28→29 trên tối thiểu32. Những PC GPON đã nằm trong tổng600→720; budget Ethernet giữ chỗ để rollback, không cộng thêm PC.

Theo ITU-T G.984.2, GPON ví dụ dùng2,488Gbit/s down,1,244Gbit/s up chia sẻ theo PON. Ví dụ tuyến0,5km, sợi0,35dB/km, splitter13,5dB, bốn connector0,5dB và bốn mối hàn0,1dB cho16,075dB; thêm3dB dự phòng là19,075dB. Ví dụ nằm trong cửa sổ class B+13–28dB, nhưng phải thay Tx/Rx và suy hao theo vendor rồi đo OTDR/optical power. GPON chỉ nằm ở thiết kế vật lý; GNS3 không mô phỏng tín hiệu quang/DBA/OMCI. OLT đơn và nhánh PON là SPOF cần đánh giá riêng.

## Camera và máy chủ

Camera dùng4Mbps, lưu30 ngày, overhead5% và chỉ lấp80% usable storage. Main40 camera cần68.040GB usable hiện tại;50 camera cần85.050GB tương lai. Mỗi Aux8 camera cần13.608GB;10 camera cần17.010GB. Đây là phép tính đơn vị thập phân; RAID/format/hot-spare và throughput ingest phải kiểm với NVR thật. RAID6 10x8TB chỉ64TB lý thuyết, không đủ mức Main hiện tại. Ví dụ12x10TB RAID6 cho100TB lý thuyết và4x12TB RAID6 cho24TB tại Aux cần đối chiếu hệ thống file, ổ dự phòng và tiêu chí vendor.

Main có8 server nội bộ cho infra, HIS, PACS, LIS, CRM, DB, backup, monitor; hai server DMZ Web và proxy. Mỗi Aux có Infra và Local. HTTP trong mô phỏng là dịch vụ đại diện, không triển khai bệnh án, DICOM, DB hoặc sản phẩm y tế thương mại.

# Tính tải, lựa chọn WAN và ISP - Step3

Đề cho server1.000MB download và2.000MB upload mỗi ngày; mỗi workstation500MB download/100MB upload; thiết bị Wi-Fi khách500MB download. Khoảng80% tải tập trung9–11h và15–16h, tổng3 giờ. Dùng MB thập phân và hệ số sử dụng70% làm giả định dự phòng: `Mbps = MB/ngày ×8 ×0,8 /(3×3600) ×1,2 /0,7`.

Từ “total” ở server có thể chỉ toàn bộ hệ thống, từng site hoặc từng server. Công cụ bàn giao tính cả ba cách và các biến khách, upload khách, protocol overhead, tỷ lệ đi LAN/WAN/Internet. Baseline bảo thủ bên dưới chọn từng server, tất cả tải đã cho đi Internet, chưa có khách và tải ngoài đề; đây là envelope giả định, không phải số đo.

| Phạm vi | Design down Mbps | Design up Mbps |
|:---|---:|---:|
| Main | 314,92 |81,27 |
| DBP |134,10 |30,48 |
| BHTQ |134,10 |30,48 |
| Internet tập trung |583,11 |142,22 |

Mỗi Aux dự trù leased line150–200Mbps đối xứng để khảo sát; tải PACS/backup và VPN có thể làm thay đổi mức này. Đề yêu cầu hai xDSL có chia tải và mọi Internet qua Main; lab dùng hai handoff Ethernet để kiểm logic. Không dùng thông số Ethernet để khẳng định đường đồng xDSL đạt tốc độ tương ứng. Hai đường500/500Mbps chỉ là ví dụ tính toán: mất một đường thiếu ít nhất83,11Mbps down so với baseline chưa khách. Nếu phải giữ đủ tải khi lỗi, mỗi ISP phải đáp ứng toàn bộ tải được chốt và kiểm QoS/tải thiết yếu.

So sánh WAN giữ cùng phạm vi ba site, SLA, CPE, license và thuế: Metro-E/P2P đơn giản và phù hợp hai leased line; MPLS L3VPN thuận mở rộng nhưng không tự mã hóa; SD-WAN bổ sung overlay/controller/license; IPsec bổ sung mã hóa và overhead. Chọn Metro-E/P2P + OSPF làm baseline chức năng, MPLS L3VPN được triển khai thêm bằng module riêng; SD-WAN còn ở mức phương án. OSPF/PBR của baseline không được gọi là MPLS/SD-WAN.

TCO minh họa5 năm là CAPEX +60 tháng OPEX +bảo trì. Bảng giả định trong hồ sơ cho Metro-E1,745 tỷ, MPLS1,948 tỷ, SD-WAN+leased2,105 tỷ, IPsec+leased1,775 tỷ VNĐ. Đây là dự toán để so công thức, không phải báo giá thị trường, chưa có VAT/điều kiện hợp đồng. OLT/ONT/ODN bổ sung phải được đối soát riêng để tránh thiếu hoặc tính trùng CAPEX. Cần thu báo giá cùng SLA, băng thông nội địa/quốc tế cam kết, IP public, handoff, tuyến độc lập và hiệu lực trước quyết định thương mại. Nguồn VNPT Kênh thuê riêng (đối chiếu 04/11/2026) xác nhận loại dịch vụ và handoff Ethernet; trang hướng dẫn liên hệ đơn vị kinh doanh, không công bố báo giá áp dụng cho ba cơ sở này.

# Mô phỏng hai nền tảng - Step4

## GNS3 - nền tảng kiểm dual ISP và IDS/IPS

Mô hình thực thi có9 router/firewall Linux/FRR,5 switch VLAN và38 endpoint đại diện, bao gồm14 server nội bộ và Web-Lab. Cấu hình được sinh từ IP/cabling/endpoint/ACL đã review; phần dịch IOS sang Linux chỉ hỗ trợ cú pháp có trong repository và dừng khi gặp cú pháp ngoài phạm vi. Điều này không chứng minh CLI IOS được chấp nhận hoặc hành vi timer giống Cisco.

Switch Linux thực hiện bridge VLAN filtering; router-on-a-stick dùng802.1Q; FRR chạy OSPF thật. DHCP relay chuyển yêu cầu tới Infra từng site; dnsmasq phục vụ đủ18 pool và DNS. HTTP trả tên node và địa chỉ client để kiểm NAT. Firewall iptables conntrack tách LAN/OUTSIDE/DMZ; ACL ingress tại gateway kiểm east-west. NAT tập trung tại Edge, exempt traffic nội bộ. Static PAT chỉ ISP2:8080 tới10.10.80.10:80, giữ đường reply qua ISP2.

Controller GNS3 được đóng trong một container; Docker daemon con và các namespace mạng thuộc riêng lab, không mount Docker socket máy thật. API chỉ publish127.0.0.1:3080. Script bootstrap xây image, dựng node/link và chờ DHCP, OSPF, Web hoạt động. Tên image/version, package, source hash và output được ghi cùng lần chạy. Có lệnh dừng, mở lại và tái tạo; không đưa IOS image có bản quyền vào repository.

## Packet Tracer - mô hình Cisco ba cơ sở

File `simulation/packet-tracer/hospital-3sites.pkt` có 58 thiết bị, 53 cáp, sáu client kết nối Wi-Fi thực tới sáu AP. Có 19 client DHCP và 18 pool có sức chứa; ba serverPool mặc định đặt sức chứa 0. Main-FW dùng 2811 với module NM-1FE-TX và ba cổng LAN/OUTSIDE/DMZ; tám router còn lại dùng 2911. Mô hình đã được lưu và mở lại để đối chiếu cấu hình, địa chỉ, DHCP và association.

ISP2/PAT 198.51.100.2 là đường chính của Packet Tracer. ISP1/PAT 203.0.113.2 được kiểm bằng chọn đường thủ công rồi khôi phục ISP2. Phần chứng minh cân bằng tải theo nhóm nguồn, phát hiện lỗi upstream, failover tự động và IDS/IPS thuộc GNS3. Hai mô hình cùng mô tả kiến trúc logic; Ethernet đại diện leased line/xDSL, không đo tín hiệu hoặc tốc độ đường truyền vật lý.

## MPLS L3VPN - phần WAN mới đã thực thi

Module `simulation/mpls/` có 11 nút/10 liên kết: ba CE Main/DBP/BHTQ, ba PE, một P, ba PC và Web-Lab. Provider dùng OSPF area 0 và LDP; ba PE trao đổi VPNv4 bằng MP-BGP AS65000. VRF HOSPITAL/table1001 dùng RT65000:100, RD65000:1/2/3; CE dùng eBGP AS65101–65103. Ba LAN đại diện giữ 10.10.10.0/25, 10.20.10.0/25, 10.30.10.0/25. Internet hai Aux vẫn đi qua Main/PAT198.51.100.2.

Đã chạy thực trên Linux namespaces trong QEMU/WHPX, Alpine3.22.7, kernel6.12.114-lts và FRR10.2.2. Lượt validated đạt **28/28**, sau xóa/dựng lại đạt **28/28**: sáu ping hai chiều liên site, ba HTTP/PAT tại Main, MP-BGP/LDP/VRF, provider không truy cập LAN, tắt/khôi phục đường DBP và bắt gói MPLS. PCAP có EtherType0x8847 và hai nhãn transport/VPN trên ICMP DBP→Main, kèm gói trả lời; đây là bằng chứng chuyển tiếp nhãn thực trong môi trường ảo.

Khi đường DBP mất, DBP không liên lạc được; Main–BHTQ tiếp tục hoạt động và DBP phục hồi sau khi bật lại. Module vẫn có SPOF ở P và từng đường truy nhập, không công bố dự phòng MPLS. MPLS tách bảng định tuyến nhưng không mã hóa payload. Bộ thử đầu có lỗi HTTP/cú pháp show BGP được giữ riêng; không chuyển lỗi lịch sử thành PASS.

Project `simulation/mpls/hospital-mpls.gns3` được sinh từ cùng cấu hình và có Dockerfile/runbook. Project MPLS mới chưa được mở/chạy bằng GNS3; bằng chứng 28+28 thuộc Linux namespaces, không gắn nhãn GNS3 runtime. Mô hình GNS3 tổng và Packet Tracer tổng giữ bằng chứng riêng. Kiểm evidence bằng `python scripts/check_mpls.py`; raw CLI, PCAP, source hash nằm ở `test_results/mpls/`.

# Chính sách bảo mật và kiểm thử - Step5

Khách bị chặn tới mạng nội bộ, server/DMZ, quản trị và camera; vẫn được DHCP/DNS và Web Internet. Người dùng chỉ được truy cập ứng dụng theo vai trò; DB không công bố cho client. Camera không được tự truy cập LAN. Quản trị tập trung từ Main-Admin. Truy cập cùng VLAN cần host firewall/L2 isolation bổ sung, không được coi ACL gateway đã bảo vệ toàn bộ east-west.

VPN được đề xuất đủ hai trường hợp theo đề: site-to-site route-based IPsec/IKEv2 qua leased line; teleworker kết thúc trên firewall, tài khoản riêng/MFA, split tunnel chỉ tới HIS/CRM được duyệt. Chưa triển khai crypto, chứng thư, MFA hoặc kiểm MTU; không ghi VPN PASS. Trước triển khai phải tránh tuyến cleartext ưu tiên hơn tunnel và thêm route về pool, NAT exemption, ACL/VPN zone.

Suricata được đưa vào mô hình Linux để kiểm IDS/IPS bằng hai URI vô hại: một marker phát cảnh báo, một marker phải bị chặn. NFQUEUE repeat đánh dấu và đưa gói trở lại các luật firewall; verdict accept của IPS không được dùng để bỏ qua ACL/zone policy. DNS có miền thử `.invalid` bị trả0.0.0.0 để minh họa blocklist. Đây chỉ là bằng chứng rule mẫu, không chứng minh phát hiện mọi tấn công/phishing hoặc hiệu năng bảo vệ bệnh viện.

Sáu nhóm bắt buộc gồm: cùng VLAN; giữa VLAN; giữa Main và hai Aux; truy cập DMZ; chặn Guest tới LAN với đối chứng Internet; truy cập Internet Web theo IP/tên. Các ca bổ sung kiểm OSPF Full, DHCP ACK/route/DNS trên tất cả pool, counters DROP, phân nhóm NAT, mất từng ISP, mất cả hai, phục hồi và lưu/mở lại project. Kết quả chi tiết và hash được tổng hợp tự động ở phụ lục bằng chứng.

Khi lỗi ISP, có thời gian gián đoạn do probe, route default và OSPF hội tụ; không cam kết chuyển mạch tức thời. Bộ test đo phục hồi HTTP từ năm endpoint trong ngân sách thử45 giây, không coi45 giây là SLA. Phiên NAT cũ qua ISP hỏng có thể mất; thử HTTP phiên mới không chứng minh session preservation. Internet thật, TLS, RF, GPON PHY, dung lượng đường truyền và ứng dụng y tế không nằm trong phép thử này.

## Kết quả Packet Tracer sau mở lại

| Nhóm | Phạm vi kiểm | Số lượt |
|:---|:---|---:|
| TC01 | Cùng VLAN, hai chiều | 2 |
| TC02 | Liên VLAN và HIS | 3 |
| TC03 | Main với DBP/BHTQ, hai chiều | 4 |
| TC04 | DMZ và static PAT từ ngoài | 2 |
| TC05 | Guest bị chặn LAN/HIS, có đối chứng | 9 |
| TC06 | PC/Guest mỗi site tới Web/DNS | 6 |
| WIFI | Staff mỗi site tới HIS/Web qua Wi-Fi | 6 |

Tổng 32 quan sát phù hợp kỳ vọng sau warmup. Tám ping được phép đều nhận đủ 4/4; ba ping Guest không phản hồi. HTTP cho phép trả đúng URL/nội dung; HTTP Guest thất bại được đối chiếu với Guest ra Web thành công, PC nội bộ tới cùng HIS thành công và ACL deny tăng (Main 16, DBP 16, BHTQ 26). Lịch sử lần thử lỗi và warmup được giữ riêng.

Bốn lượt HTTP bổ sung gồm ba nguồn Main-PC10-A, DBP-Guest, BHTQ-Staff qua ISP1 và một lượt sau khôi phục ISP2; NAT public đúng egress, cấu hình Edge được khôi phục. Evidence ở `test_results/packet-tracer/after-reopen/`; chạy `python scripts/check_packet_runtime.py` để kiểm hash và kết quả đã lưu. Phụ lục `packet-tracer-validation.pdf` kèm bảng sáu BSSID, IP, SSID và hash native. Checker offline không chạy lại mạng.

# Đánh giá, hạn chế và hướng phát triển - Step6

## Tin cậy, mở rộng và phần mềm

Hai ISP giúp dự phòng kết nối Internet nhưng Core/FW/Edge, OLT và mỗi leased line Aux vẫn có SPOF. Mô hình không có firewall state sync hoặc bảo vệ PON; công bố DMZ phụ thuộc ISP2. Cần hai tuyến WAN độc lập, HA thiết bị, nguồn/UPS, backup cấu hình và thử khôi phục trước triển khai. Chọn RPO/RTO và tải thiết yếu cùng đơn vị y tế, không tự công bố một mức uptime từ ping.

Pool /25 Main còn đúng120 lease tại năm5; thêm thiết bị sẽ cần mở rộng subnet/pool. Guest500 lease/site và Staff244 lease/site cần xác nhận số truy cập đồng thời/lease/RF. Sizing cổng/PoE/quang/storage có dự phòng nhưng phải đo workload, throughput inspect/crypto, phiên NAT và radio contention.

| Nhóm phần mềm | Phương án | Phạm vi thực hiện |
|:---|:---|:---|
| Hệ điều hành/office | Windows/office có license hoặc Linux/phần mềm phù hợp | Đề xuất; cần ma trận tương thích và bản quyền |
| HIS/RIS-PACS/LIS/CRM | Sản phẩm được đơn vị y tế chọn | HTTP đại diện, chưa tích hợp nghiệp vụ |
| Định tuyến/bảo mật | Cisco tham chiếu; FRR/Linux/Suricata trong lab | Có kết quả GNS3, chưa benchmark sản phẩm thương mại |
| DNS/DHCP/giám sát/backup | dnsmasq trong lab; hệ thống quản trị/backup theo vận hành | DHCP/DNS đã thử; backup/restore dữ liệu thật chưa thử |

## An toàn và vận hành

Áp dụng tài khoản riêng, MFA cho truy cập từ xa, quản trị từ VLAN riêng, cập nhật/backup có kiểm tra restore, log tập trung, NTP, cảnh báo IDS và quy trình xử lý. Tắt dịch vụ/cổng không dùng, bảo vệ rack/IDF/ODF và UPS; đào tạo nhận diện phishing kết hợp DNS/mail filtering, không xem block một miền mẫu là giải pháp hoàn chỉnh. Thiết bị y tế cần cập nhật theo khả năng hỗ trợ của nhà cung cấp và lịch bảo trì được phê duyệt.

IPv6 chưa được thiết kế; không bật dual stack rồi để vượt chính sách IPv4. OSPF authentication, TLS/certificate ứng dụng, 802.1X/WLC, guest cùng VLAN, malware/signature feed, quản lý khóa VPN và HA cần triển khai/đo riêng. Kết quả GNS3 và Packet Tracer được đánh giá theo từng nền tảng; tính năng chưa thử trên Packet Tracer không được suy từ GNS3.

# Bàn giao và quy trình nộp - Step7

Bộ bàn giao gồm project `.gns3`, module MPLS L3VPN và evidence28+28, mô hình tổng `.pkt`, phụ lục kiểm thử Packet Tracer, Dockerfile/source cấu hình để dựng lại, bộ Cisco tham chiếu, file TV2 gốc, sơ đồ drawio/SVG, đầu vào CSV, công cụ tính tải/kiểm tra, báo cáo PDF cùng nguồn Markdown/LaTeX và evidence JSON/log kèm SHA256. Bộ LaTeX chứa nội dung đầy đủ, logo Bách Khoa do người dùng cung cấp trên bìa và hình topology; có thể biên dịch trực tiếp bằng XeLaTeX. Không cần IOS image cho mô hình GNS3 nguồn mở. Chạy lại lệnh hướng dẫn trên môi trường Linux có Docker trước buổi demo; người nhận cần dựng image trước khi mở project trên GNS3 khác.

Thông tin lớp L08, nhóm 2 và phân công BTL2 hai thành viên đã được cập nhật theo nhóm trưởng. Trước nộp, nhóm kiểm nhận xét và phê duyệt, file project/PDF đúng checksum, sau đó tự nộp BKeL và lưu biên nhận. Chưa thực hiện nộp BKeL, không tạo biên nhận hoặc chữ ký giả. Những việc ngoài workspace như khảo sát hiện trường, báo giá/SLA, đo RF/quang, license và triển khai thật vẫn phải có bằng chứng riêng.

# Tài liệu tham khảo

1. Lai Nguyen. *Network Design and Simulation for a Critical Large Hospital*. Đề gốc trong workspace, trang1–4; trang5 minh họa.
2. GNS3. *Docker support in GNS3* và *Controller API v2*. <https://docs.gns3.com/docs/emulators/docker-support-in-gns3> ; <https://api.gns3.net/en/stable/>.
3. FRRouting. *OSPFv2*. <https://docs.frrouting.org/en/stable-8.4/ospfd.html>.
4. OISF. *Suricata - IPS mode/NFQUEUE and configuration*. <https://docs.suricata.io/en/suricata-7.0.2/setting-up-ipsinline-for-linux.html>.
5. ITU-T. *G.984.2 (08/2019), GPON PMD, Annex A*. <https://www.itu.int/rec/T-REC-G.984.2/en>.
6. Cisco. *Catalyst9200 Series Switches Data Sheet*. <https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9200-series-switches/nb-06-cat9200-ser-data-sheet-cte-en.html>.

Nguồn tham khảo kỹ thuật được đối chiếu ngày02/11/2026. Các bảng chi phí là giả định dự toán đã ghi rõ, không được trích dẫn như báo giá nhà cung cấp.

Nguồn bổ sung đối chiếu dịch vụ WAN ngày 04/11/2026: VNPT, *Kênh thuê riêng*, <https://vnpt.vn/doanh-nghiep/san-pham-dich-vu/kenh-thue-rieng/>. Giá tại bảng TCO vẫn là giả định minh họa.

VNPT, *Dịch vụ Mạng riêng ảo*, <https://vnpt.vn/doanh-nghiep/san-pham-dich-vu/dich-vu-mang-rieng-ao-vpn/> (04/11/2026), phân biệt Metronet/MPLS VPN L2 và Megawan/MPLS VPN L3. Handoff Ethernet trong lab không chứng minh underlay MPLS của nhà mạng.

Nguồn MPLS: FRRouting, *LDP* và *Layer 3 VPN configuration*, <https://docs.frrouting.org/en/stable-10.4/ldpd.html>, <https://docs.frrouting.org/en/stable-10.4/bgp.html#layer-3-vpn-configuration>. Cú pháp đã kiểm bằng FRR10.2.2 trong module.

Tham khảo giá có nguồn: VNPT Hải Phòng, *Báo giá TSL Metronet*, tài liệu ghi năm2020 (ngày/tháng trống), 100Mbps nội hạt31.343.000VNĐ/điểm. Đây là dữ liệu lịch sử, không phải báo giá hiện hành TP.HCM hoặc gói đủ tải Aux134,10Mbps. Nguồn và các mức20/50Mbps nằm trong `docs/02-design/wan-options-cost.md`; không nội suy giá150–200Mbps từ bảng cũ.
