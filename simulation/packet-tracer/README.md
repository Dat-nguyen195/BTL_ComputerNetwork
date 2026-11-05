# Packet Tracer

**Bản kỹ thuật đã kiểm ngày04/11/2026:** [hospital-3sites.pkt](hospital-3sites.pkt), Packet Tracer9.0.1.0858,58 thiết bị mạng/53 cáp/sáu Wi-Fi. Bộ32 lượt sau lưu/mở lại phù hợp kỳ vọng, sáu BSSID/IP và19 client DHCP đã đối chiếu. Bốn HTTP chọn ISP thủ công và khôi phục ISP2 cũng đạt. [Bằng chứng, giới hạn và lịch sử](../../test_results/packet-tracer/README.md), [phụ lục PDF](../../docs/06-report/final/packet-tracer-validation.pdf) và [nguồn có thể sửa](../../docs/06-report/source/packet-tracer-validation.md) đi kèm. Chờ nhóm đọc chéo/phê duyệt học phần.

## Mở và trình diễn

1. Mở file chính trên Packet Tracer9.0.1. Người dùng tự đăng nhập Cisco nếu ứng dụng yêu cầu và tự xác nhận IPC khi mở file. File yêu cầu Get Network Info,Change Network Info,Change User Interface,Application; không chứa bộ cài hoặc tài khoản Cisco.
2. Đợi OSPF/DHCP/Wi-Fi hội tụ. Sáu Guest/Staff dùng card PT-HOST-NM-1W-AC, SSID theo tên máy thay dấu `-` bằng `_`, WPA2-PSK/AES và khóa ví dụ công khai `HospitalLab2026Only`. Cần kiểm BSSID/IP thực nhận; không dùng PC có dây làm bằng chứng Wi-Fi.
3. Main-FW dùng2811 với NM-1FE-TX, ba cổng Fa0/0 LAN,Fa0/1 OUTSIDE,Fa1/0 DMZ. DMZ-Access Gi0/1 vàGi0/2 ởVLAN999 nối Edge;Fa0/24 ởVLAN80 nối firewall. Không nối DMZ trực tiếp vào Core.
4. Main-Edge ưu tiên ISP2/PAT198.51.100.2; công bố WebDMZ tại198.51.100.2:8080. ISP1/PAT203.0.113.2 được thử bằng đổi route/NAT thủ công rồi khôi phục. Không gọi đây là tự động failover hoặc load balancing/PBR.
5. Có18 pool thiết kế, ba serverPool mặc định giữ sức chứa0 để tồn tại an toàn sau reopen,19 client DHCP. Không xóa ba pool rồi cho rằng Packet Tracer sẽ không tạo lại chúng. PDU ứng dụng tự thêm không tính vào58 node mạng.

## Chạy lại bằng controller nhúng

[controller.js](scripts/controller.js), [wireless.js](scripts/wireless.js), [repair-profile.js](scripts/repair-profile.js), [normalize-runtime.js](scripts/normalize-runtime.js) đã ghép trong file; hash bundle khớp nguồn ở [review persistence](../../test_results/packet-tracer/persistence-review.json). `main()` không tự ghi cấu hình. **Không gọi `hospital.configure()` hoặc `hospital.services()` khi chỉ cần kiểm thử:** hai hàm có thể tạo lại ACL/pool và renew DHCP.

Trong Extensions→Scripting→Edit File Script Module→Debug, ghi baseline rồi warmup/bộ32 job:

```javascript
var ps=[];
["Main-Core","DBP-GW","BHTQ-GW"].forEach(function(n){ps.push({node:n,command:"show access-lists",result:ipc.network().getDevice(n).enterCommand("show access-lists","enable")});});
$putData("pretest-snapshots.json",JSON.stringify(ps));
captureWireless();
warmupHospitalAndTest();
```

Đợi `HOSPITAL_TESTS_DONE 32`, gọi `captureWireless()` lần nữa và Ctrl+S. Dùng thư mục run mới để giữ lịch sử:

```powershell
python -X utf8 scripts/collect_packet_tracer.py --input simulation/packet-tracer/hospital-3sites.pkt --output tmp/pt-new-run
python -X utf8 scripts/check_packet_runtime.py --run tmp/pt-new-run --project simulation/packet-tracer/hospital-3sites.pkt
```

Collector/checker không chạy mạng. Nếu muốn thử ISP thủ công, nạp [manual-isp.js](scripts/manual-isp.js) qua Debug rồi gọi `testManualHospitalIsp()` sau khi lưu snapshot32 job; đợi `MANUAL_ISP_TEST_DONE 4`. Hàm trả route/NAT vềISP2, ghi startup-config và giữ bộ32 job chính; data bổ sung lưu riêng. Đây là helper đã chạy qua Debug, không nằm trong bundle nhúng. Cảnh báo console `EVENT_MANAGER` của9.0.1 đã được ghi; probe và bộ32 callback trực tiếp vẫn có đầu ra đầy đủ.

## Nguồn và giới hạn

[Module Main gốc](../modules/tv2-lan-wireless/tiendat-lan-original.pkt) giữ nguyên byte/hash; chỉ10 node Main, không thay bằng lab tổng. [Bản có dây lịch sử](../../test_results/packet-tracer/wired-runtime/lab.pkt) được giữ tại hồ sơ kiểm thử, không lưu thêm bản candidate trùng trong thư mục mô phỏng chính. [Assembly kit](assembly/manifest.json), sinh bằng `python scripts/build_packet_tracer.py`, là cấu hình tham chiếu58 node/52 cáp/6 WLAN; có lệnh nâng cao từ thiết kế cần thích nghi. Native đã sửa dùngFW2811, Ethernet WAN, thêm cáp DMZ và cấu hình theo profile đã thử.

Scaffold dựng native thử nghiệm phụ thuộc template tạm đã được dọn; file chính đã kiểm và các công cụ thu/kiểm bằng chứng vẫn được giữ. [Probe](scripts/probe.js) chỉ kiểm profile2911 cụ thể. Bản GNS3 có evidence riêng cho routing/failover nâng cao; Packet Tracer không đo RF/quang/DSL PHY, tải nghiệp vụ, VPN crypto hoặc HA thiết bị.
