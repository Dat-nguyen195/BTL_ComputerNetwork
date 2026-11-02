# Kịch bản test và demo với giảng viên

Áp dụng cho [project GNS3 Linux/FRR](hospital-3sites.gns3) trên máy hiện tại. Thực hiện các lệnh trong **Terminal Ubuntu tại thư mục dự án**, không nhập vào ô tìm kiếm Web UI hoặc CLI Cisco. Sáu nhóm TC01–TC06 dưới đây là phần trình diễn chức năng bắt buộc; DHCP/DNS, OSPF, IDS/IPS và hai ISP là phần mở rộng.

## 1. Chuẩn bị trước buổi demo

```bash
cd '/media/nguyen-dat/New Volume/HK1_261/ComputerNetwork/BTL/BTL_2'
python3 scripts/gns3_lab.py start
python3 scripts/gns3_lab.py status
```

Chờ thông báo `Ready: DHCP lease and inter-site ICMP verified`; kiểm tra đủ 52 node có trạng thái `started`. Khởi động thành công chưa thay thế việc kiểm thử từng chức năng. Nếu project đã đóng nhưng controller vẫn chạy, dùng `python3 scripts/gns3_lab.py reopen` rồi kiểm lại. `bootstrap` chỉ dùng lần cài đầu theo [README](README.md), không chạy lại trước mỗi buổi demo.

Mở trình duyệt tại <http://127.0.0.1:3080/static/web-ui/bundled?webfix=2>, chọn **Hospital-3Sites-FRR**. Nếu còn trang lỗi cũ, nhấn Ctrl+Shift+R. Dùng **Pan workspace** và **Zoom out** để đưa sơ đồ vào vùng nhìn. Giữ hai cửa sổ: sơ đồ và Terminal. Console telnet trong controller chưa publish ra máy host; dùng lệnh `exec` dưới đây.

Tạo hai hàm viết tắt trong Terminal hiện tại:

```bash
lab() { python3 scripts/gns3_lab.py exec "$@"; }
web() { lab "$1" curl --noproxy '*' --connect-timeout 2 --max-time 3 -fsS -w '\n' "$2"; }
```

Đóng Terminal thì các hàm mất; cần tạo lại ở cửa sổ mới. `lab` thực thi trên node có tên ở tham số đầu, còn `web` gửi HTTP từ node đó. Không phải gửi từ máy Ubuntu host.

| Node | Địa chỉ / vai trò |
| --- | --- |
| Main-PC10-A / Main-PC10-B | 10.10.10.10 / 10.10.10.11, cùng VLAN10 |
| Main-PC20 | 10.10.20.10, khác VLAN tại Main |
| DBP-PC10 / BHTQ-PC10 | 10.20.10.10 / 10.30.10.10, hai cơ sở phụ |
| Main-HIS | 10.10.70.11, server nội bộ đại diện |
| Main-WebDMZ | 10.10.80.10, Web trong DMZ |
| Main-Guest / DBP-Guest / BHTQ-Guest | Máy khách VLAN100 tại ba cơ sở |
| Web-Lab | 192.0.2.100, tên web.hospital.test, Web/DNS Internet mô phỏng |
| Main-Edge | NAT/PBR, ISP1 203.0.113.2 và ISP2 198.51.100.2 |

Luyện trước bằng test tự động ở mục 5. Trước lúc trình bày nên giữ hai ISP ở trạng thái bình thường, không bấm Stop/Reload trong lúc đang kiểm chức năng.

## 2. Mở đầu khoảng 1 phút

Chỉ sơ đồ và nói: “Mô hình gồm Main và hai cơ sở phụ DBP/BHTQ. Hai nhánh nối về Main bằng leased line; Internet của cả ba đi qua firewall, NAT và hai ISP ở Main. VLAN tách người dùng, server, quản trị và khách; DMZ dành cho dịch vụ công bố.”

Mở [báo cáo PDF](../../docs/06-report/final/report.pdf) nếu cần trình bày khảo sát, chọn topology, dung lượng và thiết bị. Quy mô thiết kế là 600 + 260 + 260 PC và 10 + 2 + 2 server. Lab dùng 38 endpoint đại diện trong tổng 52 node, không phải chạy đủ 1.120 PC.

## 3. Sáu nhóm bắt buộc, khoảng 6–8 phút

### TC01 — Hai máy cùng VLAN liên lạc

```bash
lab Main-PC10-A ping -n -c 3 -W 1 10.10.10.11
lab Main-PC10-B ping -n -c 3 -W 1 10.10.10.10
```

**Đạt:** hai chiều có reply, sau hội tụ không mất gói. Giải thích: hai PC cùng VLAN10 và subnet, trao đổi qua switch; bài này kiểm kết nối lớp 2.

### TC02 — Liên VLAN và server nội bộ

```bash
lab Main-PC10-A ping -n -c 3 -W 1 10.10.20.10
lab Main-PC20 ping -n -c 3 -W 1 10.10.10.10
web Main-PC10-A http://10.10.70.11
```

**Đạt:** ping hai chiều thành công; HTTP có `"node": "Main-HIS"`. Giải thích: khác VLAN cần gateway định tuyến, chính sách cho phép luồng này. HIS ở đây là Web đại diện, không phải phần mềm bệnh viện thật.

### TC03 — Main và cả hai cơ sở phụ

```bash
lab Main-PC10-A ping -n -c 3 -W 1 10.20.10.10
lab DBP-PC10 ping -n -c 3 -W 1 10.10.10.10
lab Main-PC10-A ping -n -c 3 -W 1 10.30.10.10
lab BHTQ-PC10 ping -n -c 3 -W 1 10.10.10.10
lab DBP-PC10 traceroute -I -n -m 10 -w 1 10.30.10.10
lab Main-GW vtysh -c 'show ip ospf neighbor'
```

**Đạt:** bốn ping thành công, traceroute đến BHTQ qua mạng Main, Main-GW có ba láng giềng ở trạng thái `Full/`. Giải thích: OSPF trao đổi các subnet giữa ba cơ sở. Có thể chỉ bảng route bằng `lab DBP-GW vtysh -c 'show ip route ospf'`.

### TC04 — Truy cập server DMZ và công bố dịch vụ

```bash
web Main-PC10-A http://10.10.80.10
web DBP-PC10 http://10.10.80.10
web BHTQ-PC10 http://10.10.80.10
web Web-Lab http://198.51.100.2:8080
web Web-Lab http://198.51.100.2:8081
```

**Đạt:** bốn lệnh đầu trả về `Main-WebDMZ`; cổng 8081 thất bại là **đúng chính sách**. Giải thích: bên ngoài chỉ được công bố TCP 8080 qua static PAT tới HTTP 80 trong DMZ. Có thể xem bằng `lab Main-Edge iptables -t nat -S PREROUTING`. DMZ là vùng riêng, không phải mở toàn bộ LAN cho bên ngoài.

### TC05 — Guest không vào LAN nhưng vẫn ra Web

```bash
web Main-Guest http://web.hospital.test
web DBP-Guest http://web.hospital.test
web BHTQ-Guest http://web.hospital.test
lab Main-Core iptables -nvx -L MAIN-V100-IN
lab Main-Guest ping -n -c 2 -W 1 10.10.10.10
lab DBP-Guest ping -n -c 2 -W 1 10.30.10.10
lab BHTQ-Guest ping -n -c 2 -W 1 10.20.10.10
web Main-Guest http://10.10.70.11
lab Main-Core iptables -nvx -L MAIN-V100-IN
lab DBP-GW iptables -nvx -L DBP-V100-IN
lab BHTQ-GW iptables -nvx -L BHTQ-V100-IN
```

**Đạt:** ba Guest ra Web được; ba ping vào LAN và HTTP vào HIS bị chặn. Counter `DROP` tăng trên ACL tương ứng. Đọc cột `pkts` trước/sau, không chỉ nhìn quy tắc có tồn tại.

Nói: “Timeout ở đây là kết quả mong muốn của bài kiểm chính sách. Guest vẫn truy cập Web, máy nội bộ ở TC02/TC03 vẫn thông, và counter DROP tăng, nên có bằng chứng việc chặn do chính sách.” Test tự động kiểm đủ ba Guest tới PC cả ba site, HIS và DMZ; các lệnh trên là phần minh họa ngắn.

### TC06 — Web Internet từ cả ba cơ sở

```bash
web Main-PC10-A http://web.hospital.test
web DBP-PC10 http://web.hospital.test
web BHTQ-PC10 http://web.hospital.test
```

**Đạt:** cả ba trả JSON có `"node": "Web-Lab"`; trường `client` là địa chỉ sau NAT. Khi cả hai ISP hoạt động, Main-PC10-A và DBP-PC10 đi ISP1 (`203.0.113.2`), BHTQ-PC10 đi ISP2 (`198.51.100.2`). Giải thích: truy cập bằng tên đồng thời kiểm DNS, định tuyến, firewall và NAT. Đây là Internet mô phỏng trong lab.

## 4. Phần mở rộng, chọn theo thời gian

### DHCP/DNS và VLAN, khoảng 1 phút

```bash
lab Main-PC10-A ip -4 -br addr show eth0
lab Main-PC10-A ip route show default
lab Main-PC10-A cat /tmp/dhclient.log
lab Main-PC10-A dig +short @10.10.70.10 web.hospital.test
lab Main-Access bridge vlan show
```

Kỳ vọng IP `10.10.10.10/25`, default qua `10.10.10.1`, log có `DHCPACK`, DNS trả `192.0.2.100`. Bảng VLAN cho thấy các cổng access có PVID/untagged và trunk mang nhiều VLAN. Không xóa lease để demo; có thể làm mất kết nối không cần thiết.

### IDS khác IPS, khoảng 1 phút

```bash
web Main-PC10-A http://10.10.80.10/hospital-ids-test
web Main-PC10-A http://10.10.80.10/hospital-ips-test
web Main-PC10-A http://10.10.80.10/
lab Main-FW tail -n 6 /tmp/suricata/fast.log
lab Main-Guest dig +short @192.0.2.100 phishing-test.invalid
```

Kỳ vọng IDS vẫn trả HTTP và ghi alert SID `1000001`; IPS làm request timeout và ghi SID `1000002` với hành động Drop. Web bình thường sau đó vẫn thông. Đây là hai rule marker vô hại minh họa phát hiện/chặn, không chứng minh ngăn mọi cuộc tấn công. Lệnh DNS cuối trả `0.0.0.0` cho miền thử `.invalid` trong blocklist, minh họa chặn tên miền mẫu.

### Hai ISP: phân luồng và phục hồi, khoảng 2 phút

Kiểm tra trước khi gây lỗi:

```bash
lab Main-Edge cat /tmp/edge-health.json
web Main-PC10-A http://192.0.2.100
web Main-PC20 http://192.0.2.100
```

Kỳ vọng `[true, true]`, hai máy có `client` lần lượt `203.0.113.2` và `198.51.100.2`. Mô hình phân luồng theo nhóm nguồn, không cộng hai đường cho một phiên hoặc bảo đảm tỷ lệ tải 50/50.

Chạy trọn khối sau để gây lỗi **upstream eth1 của ISP1 trong lab**, kiểm rồi tự phục hồi khi khối kết thúc:

```bash
(
  trap 'lab ISP1 ip link set eth1 up' EXIT
  lab ISP1 ip link set eth1 down
  sleep 20
  lab Main-Edge cat /tmp/edge-health.json
  web Main-PC10-A http://192.0.2.100
  web Main-PC20 http://192.0.2.100
  lab DBP-PC10 ping -n -c 3 -W 1 10.30.10.10
)
```

Kỳ vọng `[false, true]`, cả hai máy ra bằng `198.51.100.2`, ping nội bộ vẫn thông. Sau khối trên chờ hội tụ rồi kiểm lại `[true, true]`. Nếu chưa hội tụ sau 20 giây, quan sát thêm và ghi thời gian thực tế; không đổi kết luận thành PASS khi chưa thấy kết quả. Muốn thử ISP2, dùng cùng cách nhưng ngắt **ISP2 eth1**, khi đó địa chỉ NAT còn lại phải là `203.0.113.2`.

Lệnh phục hồi thủ công nếu buổi demo bị ngắt:

```bash
lab ISP1 ip link set eth1 up
lab ISP2 ip link set eth1 up
```

Không ngắt interface mạng của máy Ubuntu. Luồng TCP cũ có thể gián đoạn khi đổi IP NAT; demo này chứng minh phiên mới phục hồi. Hai ISP chưa loại bỏ điểm lỗi đơn ở Core/Firewall/Edge.

## 5. Chạy bộ test đầy đủ và lưu bằng chứng

Chạy trước buổi demo, không đồng thời với thử ngắt ISP thủ công:

```bash
python3 scripts/verify.py
python3 scripts/test_gns3_runtime.py
```

`verify.py` kiểm tài liệu, cấu hình, tính toán và tính nhất quán; không tự gửi gói tin trong mạng. `test_gns3_runtime.py` mới chạy kiểm thực tế: bình thường có 137 kiểm tra. Kết quả mới nằm trong thư mục có timestamp ở `test_results/runtime/`, gồm `results.json` và `summary.json`; cần mọi nhóm có `fail: 0` và tiến trình kết thúc mã 0.

Muốn kiểm đủ mất từng ISP, mất cả hai, phục hồi và chạy lại sáu nhóm:

```bash
python3 scripts/test_gns3_runtime.py --failover
```

Bộ này bình thường có 209 kiểm tra; gây gián đoạn Internet **bên trong lab** trong khi thử. Không chạy giữa một demo HTTP khác. Script dùng `finally` để phục hồi interface; nếu bị cưỡng bức tắt tiến trình, dùng hai lệnh phục hồi ở mục 4. Giữ cả kết quả FAIL nếu có, sửa nguyên nhân rồi chạy lần mới; không ghi đè hoặc xóa lỗi để báo PASS.

Để luyện lưu/mở lại project trước buổi trình bày:

```bash
python3 scripts/gns3_lab.py reopen
python3 scripts/test_gns3_runtime.py
```

Các [bằng chứng đã lưu](../../test_results/runtime/README.md) và [ma trận kiểm thử](../../test_results/test-matrix.md) là tài liệu đối chiếu; không thay cho kết quả live trên máy mới. Chụp Terminal có tên node, lệnh và kết quả; riêng chặn Guest cần cả Web thành công lẫn DROP counter. PCAP có sẵn tại [hospital-demo.pcap](../../test_results/runtime/persistence/hospital-demo.pcap).

Sau khi quyết định đưa log mới vào bộ nộp, cập nhật archive và kiểm checksum:

```bash
python3 scripts/package_submission.py
python3 scripts/package_submission.py --check
```

## 6. Trả lời các phần đặc tả không thể chứng minh bằng ping

| Nội dung giảng viên hỏi | Tài liệu / cách trình bày |
| --- | --- |
| Khảo sát, quy mô, phân tầng, địa chỉ | [Báo cáo](../../docs/06-report/final/report.pdf), [IP/VLAN](../../docs/02-design/ip-vlan-plan.md), [sơ đồ Main](../../docs/02-design/diagrams/exports/physical-main.svg), [sơ đồ Aux](../../docs/02-design/diagrams/exports/physical-aux.svg) |
| Lưu lượng, giờ cao điểm, tăng trưởng 20% | [Tính dung lượng](../../docs/03-capacity/throughput.md), [giả định](../../docs/03-capacity/assumptions.md); giải thích đầu vào trước kết quả. RTT ping không chứng minh băng thông thiết kế. |
| GPON và 1/10/40GbE | [Thiết kế GPON](../../docs/02-design/gpon-design.md), [cáp vật lý](../../docs/02-design/physical-cabling.md); trình bày OLT/ONT, splitter, dự phòng và budget quang. GPON PHY/tốc độ vật lý chưa đo trong GNS3. |
| Thiết bị và chi phí | [BOM](../../docs/02-design/equipment-bom.md), [chi phí WAN](../../docs/02-design/wan-options-cost.md); số liệu dự trù/giả định cần được nêu rõ. |
| Wi-Fi, camera và VPN | [Wi-Fi](../../docs/02-design/wireless-plan.md), [camera](../../docs/02-design/camera-plan.md), [VPN](../../docs/04-security/vpn-plan.md). Có phương án thiết kế; RF/WLC/AAA và VPN crypto chưa chạy. Guest ở demo là endpoint đại diện cho VLAN khách, chưa phải kiểm sóng Wi-Fi. |
| An ninh và độ sẵn sàng | Chỉ bằng ACL counters, IDS/IPS, NAT và phép thử lỗi ISP; nêu giới hạn single Core/FW/Edge, chưa có HA chassis hoặc state sync. |
| Hồ sơ nộp | PDF + project `.gns3` + cấu hình + bằng chứng + archive/checksum. Có bộ đóng gói chưa đồng nghĩa đã nộp BKeL. |

## 7. Nếu gặp lỗi ngay trước buổi demo

| Hiện tượng | Kiểm tra / xử lý |
| --- | --- |
| `lab: command not found` | Chạy lại hai dòng định nghĩa hàm ở mục 1 trong Terminal hiện tại. |
| `Container ... is not running` | Kiểm `status`, chạy `start`, chờ Ready. Nếu vẫn lỗi, xem log node; không nhận định toàn mạng lỗi chỉ vì một node tắt. |
| Web UI còn `null.on` | Mở URL có `webfix=2`, Ctrl+Shift+R; bản controller hiện tại đã có patch Electron. |
| Toàn bộ localhost:3080 không mở | Kiểm `docker ps -a --filter name=btl2-gns3-controller`; controller dừng thì chạy `docker start btl2-gns3-controller`, chờ API rồi dùng `reopen`. Không bootstrap đè lab có sẵn. |
| Ping/HTTP Guest thất bại | So với đúng đích: vào LAN/DMZ phải bị chặn, ra Web phải thành công. Kiểm counter ACL. |
| Ping liên cơ sở được nhưng Web lỗi | Kiểm hai ISP đã được phục hồi, health tại Edge và Main-FW/Suricata. Chạy lại test sau hội tụ. |
| Lệnh `show vlan brief` không tồn tại | Đây là Linux/FRR: dùng `bridge vlan show`, `ip route`, `iptables`; chỉ lệnh định tuyến FRR chạy qua `vtysh`. |

Mỗi ca nên trình bày theo cùng thứ tự: **mục tiêu → máy nguồn/đích → lệnh → kết quả mong đợi → kết quả thực tế → giải thích**. Nếu có 10 phút: 1 phút sơ đồ, 6 phút sáu nhóm, 2 phút IDS/IPS hoặc lỗi ISP, 1 phút giới hạn và tài liệu.
