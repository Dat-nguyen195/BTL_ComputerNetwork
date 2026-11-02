# Kế hoạch IDS/IPS và chống phishing

**TV3; 02/11/2026. DESIGN ONLY / runtime NOT RUN.** Yêu cầu nâng cao của chương trình kỹ sư tài năng phải xác nhận có áp dụng. ACL/ZBF không thay bằng chứng IDS/IPS; phát hiện phishing cũng chưa được triển khai chỉ từ lọc cổng.

## Vị trí và phạm vi quan sát

Đề xuất sensor Suricata trên mirror/SPAN của DMZ switch để thấy lưu lượng **sau DNAT** giữa FW và WebDMZ. HOME_NET của sensor DMZ là `10.10.80.0/27`; nếu muốn thấy LAN/WAN phải bổ sung điểm mirror phù hợp. Sensor thụ động không chặn gói. IPS cần thiết bị hai NIC inline trên đoạn FW–DMZ, đường quản trị riêng, chế độ AF_PACKET/NFQUEUE phù hợp và kiểm fail-open/fail-closed; không bật inline trên mạng dùng thật trong bài lab.

Nguồn [Suricata EVE](https://docs.suricata.io/en/suricata-8.0.3/output/eve/eve-json-output.html) mô tả log JSON; lưu `eve.json`, thời điểm, flow ID, SID và hành vi ứng dụng. Log alert không tự chứng minh packet bị drop; IPS cần kiểm verdict và client không nhận được nội dung bị chặn, đồng thời trang hợp lệ vẫn mở.

## Kịch bản lab có thể tái hiện

Dùng đường dẫn marker giả `/btl2-ids-probe`, không dùng mã khai thác hay dữ liệu bệnh nhân. Rule minh họa, cần `suricata -T` trên phiên bản được ghi nhận trước chạy:

```text
alert http any any -> 10.10.80.10 80 (msg:"BTL2 harmless HTTP marker"; flow:established,to_server; http.uri; content:"/btl2-ids-probe"; sid:1000001; rev:1;)
```

Chạy IDS trước: từ Web-Lab mở `http://198.51.100.2:8080/btl2-ids-probe`; expected SID1000001 xuất hiện nhưng HTTP không bị sensor chặn. Với IPS, thay action bằng `drop` trong bản rule riêng, chạy inline và kiểm marker bị chặn; `/` là positive control. Rule chỉ nhận biết marker, **không phải phát hiện phishing tổng quát**. Chưa có executable/rule syntax/runtime validation trong môi trường hiện tại.

HTTP mã hóa không cho sensor mạng đọc URI nếu không có điểm giải mã được cho phép; không khẳng định rule trên kiểm được HTTPS. Không thu payload bệnh án vào log bài tập. Theo dõi packet loss, CPU, độ trễ và thông lượng khi bật rule; chưa có benchmark sizing.

## Phòng chống phishing và HA

Thiết kế vận hành kết hợp lọc mail/link/DNS, xác thực mail ở hệ thống thư, MFA, trình duyệt/endpoint cập nhật, huấn luyện và kênh báo cáo email đáng ngờ. Chọn giải pháp sau khi biết hệ thống mail/license; không tự tạo email hoặc gửi thử tới người khác. Bài lab dùng trang giả và nhãn rõ để kiểm luồng, không thu mật khẩu.

Firewall/IDS/IPS lab đơn là SPOF. HA cần cặp firewall, đồng bộ state, nguồn/cáp độc lập và test chuyển thiết bị; hai ISP chưa chứng minh HA của security stack. [SUPP-04](../../test_results/supplemental/ids-ips.md) ghi ca chạy, expected/actual và bằng chứng; hiện NOT RUN, không có alert/drop log thật.
