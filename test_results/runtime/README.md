# Bằng chứng chạy GNS3 thực tế

**02/11/2026.** Nền tảng GNS3 2.2.55, FRR8.4.4, Linux/iptables, dnsmasq và Suricata. Đây là gói tin thật giữa namespace/container của52 node, không phải checker dự đoán hoặc kết quả Cisco IOS.

| Lần chạy | Nội dung | Kết quả | Evidence |
| --- | --- | --- | --- |
| initial-runtime | Lần đầu; sáu nhóm bắt buộc đạt, thử HTTP Aux quá sớm sau thay đổi Edge | Có2 FAIL trong cửa sổ hội tụ; giữ lại nguyên trạng | [JSON](initial-runtime/results.json) |
| validated-runtime | Sáu nhóm trước/sau fault, OSPF,19 lease trên18 pool, DNS, IDS/IPS, NAT/PBR, lỗi upstream từng ISP/cả hai và phục hồi | 209 kiểm tra PASS,0 FAIL | [JSON](validated-runtime/results.json), [tổng hợp](validated-runtime/summary.json) |
| after-reopen-runtime | Chép lại đúng native project từ source, mở lại bằng GNS3, chạy sáu nhóm và dịch vụ/security | 137 kiểm tra PASS,0 FAIL | [JSON](after-reopen-runtime/results.json), [tổng hợp](after-reopen-runtime/summary.json) |
| persistence/provenance | Hash project mở lại; file code/config thực trong52 node khớp source | PASS | [reopen](persistence/reopen.json), [live hashes](persistence/live-provenance.json) |

Thời gian phục hồi HTTP trên năm endpoint khi mất upstream ISP1/ISP2 trong run đã duyệt lần lượt8,707s/6,521s. Samples gián đoạn được giữ trong `attempts`; không coi đây là zero-downtime hoặc SLA. Khi mất cả hai ISP, Web mất kết nối, default OSPF tại Aux được rút và ping Aux↔Aux vẫn đạt. Chưa kiểm lỗi local từng ISP, mọi timeout/MTU hoặc duy trì phiên NAT cũ.

Có [PCAP thật](persistence/hospital-demo.pcap) ở phía ngoài Main-FW cho HTTP DMZ/IDS/IPS và [bản đọc tcpdump](persistence/packet-capture.txt). Hai URI marker vô hại: IDS cho request đi qua và có alert1000001; IPS chặn request bằng drop1000002, HTTP bình thường vẫn đi qua. Rule mẫu và EVE nằm trong JSON captures; chỉ chứng minh rule mẫu. DNS blocklist `.invalid` là minh họa, không kết luận phát hiện mọi phishing.

JSON lưu lệnh, stdout, returncode, expected/actual, thời gian, source/project/image hash, package versions, OSPF, NAT, ACL counters và DHCP leases. Kiểm tra tĩnh dùng `check_gns3.py` để xác nhận evidence/phạm vi/hash, không tự chạy lại mạng. Muốn chạy mới dùng [hướng dẫn GNS3](../../simulation/gns3/README.md); đổi `--run-name` để giữ lịch sử, không ghi đè kết quả cũ.

VPN crypto, RF/WLC/AAA, GPON PHY, xDSL PHY/throughput, HA chassis/state sync và ứng dụng y tế thật chưa được thử. File `.pkt` gốc vẫn PARTIAL/NOT RUN trên Packet Tracer; không chuyển kết quả GNS3 thành bằng chứng IOS.

## Sau sửa lỗi Web UI Electron

[after-webui-fix-runtime](after-webui-fix-runtime/results.json) chạy lại137 kiểm chức năng sau khi sửa tương thích Web UI,0 FAIL. Native project, mã/config trong52 node không đổi; manifest cập nhật controller/patch. [Bài kiểm Chrome/Electron](../web-ui/README.md) là bằng chứng giao diện riêng, không lấy kết quả HTTP200 thay kết luận trang đã render.
