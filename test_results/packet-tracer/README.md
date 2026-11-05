# Kiểm thử Packet Tracer

**Kết quả kỹ thuật ngày04/11/2026: đạt bộ32 quan sát sau mở lại, sáu Wi-Fi và bốn lượt chọn ISP thủ công.** [File native chính](../../simulation/packet-tracer/hospital-3sites.pkt) được lưu bằng Packet Tracer9.0.1.0858. [Log kiểm bằng chứng](verification.txt), [review persistence](persistence-review.json), [provenance/hash](after-reopen/provenance.json) và [phụ lục PDF](../../docs/06-report/final/packet-tracer-validation.pdf) truy vết đúng file. Đây là kiểm kỹ thuật theo yêu cầu chủ repo; chưa thay phê duyệt nhóm hoặc biên nhận BKeL.

## Lần chạy sau mở lại

58 thiết bị mạng,53 cáp và sáu association Wi-Fi;1 PDU do ứng dụng thêm được tách khỏi số node mạng.19 client DHCP có IP/lease đúng pool;18 pool thiết kế có sức chứa. Ba serverPool mặc định do Packet Tracer thêm khi reopen giữ `max_users=0` và không có lease;12 pool Default khác nằm trên dịch vụ DHCP tắt.

| Nhóm | Số lượt | Đối chiếu |
| --- | ---: | --- |
| TC01 cùng VLAN |2| Hai chiều, mỗi ping4/4 |
| TC02 liên VLAN/HIS |3| Hai ping4/4 và HTTP đúng marker |
| TC03 Main - hai Aux |4| Hai chiều, mỗi ping4/4; có route/OSPF snapshot |
| TC04 DMZ/PAT tĩnh |2| HTTP nội bộ và Web-Lab→198.51.100.2:8080 đúng marker |
| TC05 Guest/LAN/HIS |9| Ba ping không phản hồi; ba HTTP Guest thất bại/trang rỗng; ba PC cùng site→HIS thành công |
| TC06 Web/DNS tập trung |6| PC/Guest tại cả ba site trả đúng trang Web-Lab |
| Wi-Fi Staff bổ sung |6| Staff tại cả ba site→HIS/Web thành công |

[Raw32 lượt](after-reopen/hospital-results.json) và [đối chiếu](after-reopen-review.json) có26 OBSERVED_ALLOW,3 OBSERVED_NO_REPLY,2 OBSERVED_FAILURE_WITH_CONTROLS và1 OBSERVED_BLOCK_WITH_CONTROLS. Hai HTTP Guest có responseType7/nội dung rỗng, một HTTP chưa có event trong cửa sổ12 giây; không suy đoán tên enum7. Chính Guest truy cập Web được và PC cùng site truy cập HIS được. Bộ đếm dòng deny10.0.0.0/8 trên ACL V100 tăng Main16,DBP16,BHTQ26 so với [snapshot trước thử](after-reopen/pretest-snapshots.json). ACL được gắn ingress vào đúng subinterface100. Không dùng timeout riêng lẻ để kết luận chặn.

[Sáu BSSID/IP thực nhận](after-reopen/wireless-associations.json) khớp [MAC/SSID AP đã lưu](after-reopen/wireless-readback.json), card PT-HOST-NM-1W-AC, WPA2-PSK/AES. Sáu máy nhận lại IP sau reopen. Profile được hoàn tất qua Config→Wireless0 vì API ghi profile9.0.1 phát sinh `invalid vector subscript`; quyền Application do người dùng bật cho phép đặt các client gần AP.

## Chọn ISP thủ công và persistence

[Bốn HTTP bổ sung](after-reopen/manual-isp-results.json) gồm Main-PC10-A, DBP-Guest, BHTQ-Staff qua ISP1/PAT203.0.113.2 và Main-PC10-A sau trả về ISP2/PAT198.51.100.2. Route, NAT translations và cấu hình Edge trước/sau được đọc trực tiếp. Cấu hình được khôi phục đúng; sau đó chỉ sửa mô tả cổng inside bị lưu nhầm, ghi [bốn phản hồi CLI](after-reopen/final-label-fix.json).14 running/startup-config được đối chiếu với bản trước reopen: chỉ dòng description này khác. Script [manual-isp.js](../../simulation/packet-tracer/scripts/manual-isp.js) chạy qua Debug; hash nguồn ghi trong review, không giả định nó nằm trong script nhúng.

[Snapshot trước reopen](pre-reopen/provenance.json) giữ bản sau sửa16 lệnh loopback dư và khóa ba pool mặc định, mọi lệnh trả0. [Baseline sau reopen](after-reopen-baseline/provenance.json) giữ32 lượt trước phép thử ISP. Bản cuối và data store nằm ở [after-reopen](after-reopen/provenance.json). Tám [warmup](after-reopen/warmup-results.json) được lưu riêng; không xóa lần mất gói trước đó. Một [probe callback](after-reopen/reopen-event-probe.json) thu4/4 phản hồi sau reopen. Console9.0.1 có cảnh báo nội bộ `EVENT_MANAGER`; callback trực tiếp vẫn thu đủ bằng chứng trong bộ thử, không diễn giải là đã sửa framework của Cisco.

Main-FW dùng2811/profile2800_advip_12.4, NM-1FE-TX và ba cổng LAN/OUTSIDE/DMZ. Main-Edge dùng ISP2 chính, ISP1 chọn thủ công. **Không có bằng chứng tự động failover/IP SLA/PBR trên Packet Tracer**; không áp kết quả GNS3 sang nền tảng này. Chưa đo RF/roaming/AAA, DSL/GPON PHY, VPN crypto, HA chassis hay workload y tế thật.

## Lịch sử được giữ

- [Capability preflight](capability-preflight.json) giữ lỗi quyền ban đầu. Người dùng tự cấp quyền IPC, xác nhận hộp thoại và đăng nhập Cisco.
- [Probe2911](capability-results.json), [lab native](probe-2911.pkt):11 phản hồi CLI thực; profile2900_universal_base_15.1/ipbasek9 từ chối IP SLA,track,route-map/PBR,NAT route-map,class-map ZBF. Không suy diễn cho mọi model/profile; các lệnh con PBR chưa ở context route-map hợp lệ.
- [24 job có dây](wired-runtime/provenance.json), [review](wired-review.json), [lab có dây lịch sử](wired-runtime/lab.pkt):1 job thiếu echo/đầu ra do harness chuyển lệnh quá sớm và2 ping mất gói đầu. Đã sửa chờ500ms và kiểm đúng echo/statistics; không gọi24 job là24 PASS. Bản candidate trùng trong thư mục mô phỏng chính đã được dọn.
- [32 job Wi-Fi đầu](wireless-runtime/provenance.json), [review](wireless-review.json):23 allow đầy đủ,3 ping allow mất gói đầu,3 ping Guest không phản hồi và3 HTTP Guest thất bại có đối chứng. Giữ nguyên để truy vết hội tụ/ARP.
- Module Main gốc được khôi phục đúng hash `918a884a10e7dd759ad5ae6518e42270dc8a81aa5a7fc01f394cf38b70db922c`; không ghi đè bằng lab tổng.

Thời gian raw giữ nguyên đồng hồ JavaScript của ứng dụng; collector ghi riêng giờ UTC thu thập. `collect_packet_tracer.py` chỉ trích file đã lưu; `check_packet_runtime.py` chỉ kiểm bằng chứng, không chạy mạng. [QA hai trang phụ lục](report-qa.json) độc lập với QA báo cáo chính LaTeX.
