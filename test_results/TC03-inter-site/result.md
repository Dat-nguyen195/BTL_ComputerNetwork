# TC03 — Main với DBP và BHTQ

**Trạng thái:** NOT RUN. **Chuẩn bị:** TV1. **Chạy/lưu bằng chứng:** TV4 phối hợp TV1. **Cập nhật mẫu:** 26/10/2026.

## 1. Môi trường và điều kiện trước

| Thuộc tính | Giá trị thực tế |
| --- | --- |
| Ngày/người chạy | Chưa chạy |
| Công cụ/model/image/phiên bản | Chưa xác nhận |
| Project/commit/SHA256 | Chưa có project |
| Điều kiện trước | Link/trunk/gateway đúng IP plan; OSPF hội tụ; host đích hoạt động; ACL cho phép luồng test; xác định có/không VPN |

Các địa chỉ sau là host dự kiến trong lab tối thiểu, phải thay bằng địa chỉ thật nếu khác: Main-PC `10.10.10.10/25`; DBP-PC `10.20.10.10/25`; BHTQ-PC `10.30.10.10/25`; gateway `.1` cùng subnet. Server Aux tùy chọn `.70.10/28`.

## 2. Ca kiểm và expected

| Ca | Thao tác | Expected | Actual / evidence |
| --- | --- | --- | --- |
| TC03-A | Ping/traceroute Main-PC → DBP-PC, rồi chạy lại từ DBP-PC → Main-PC | Liên lạc được theo policy, qua Main-Core/Main-GW/DBP-GW | Chưa chạy |
| TC03-B | Ping/traceroute Main-PC → BHTQ-PC, rồi BHTQ-PC → Main-PC | Đủ hai chiều và đủ chi nhánh thứ hai | Chưa chạy |
| TC03-C bổ sung | DBP-PC ↔ BHTQ-PC | Qua Main-GW, không có cáp trực tiếp DBP–BHTQ | Chưa chạy |
| TC03-D bổ sung | Main-PC ↔ server Aux nếu có | Đúng IP, port/dịch vụ được phép; ghi ICMP/ứng dụng riêng | Chưa chạy |

Lưu `show ip ospf neighbor` trên Main-GW, route đến subnet đích và chiều về trên gateway; source/destination IP/VLAN, ping/traceroute từ hai đầu, phiên bản cấu hình và chính sách áp dụng. Không suy số metric/route tổng hợp /16 từ ví dụ tự soạn; ghi output thực. RTT mô phỏng không chứng minh hiệu năng HIS/PACS sản xuất.

## 3. Bằng chứng và kết luận

- Actual/ảnh trong `screenshots/`, log trong `logs/`: chưa có.
- Kết quả từng ca: chưa có; kết luận chung giữ NOT RUN.
- Ngày/người chạy và reviewer: chờ thực hiện.
- Issue/bước tái hiện, phiên bản sau sửa, ca retest và kết quả: điền khi phát sinh.

Các đoạn CLI/RTT trước review không có project/hash đi kèm đã được bỏ khỏi actual; không dùng làm bằng chứng nghiệm thu. Chỉ chuyển PASS sau khi đủ kết quả cho Main↔cả DBP và BHTQ trên đúng bản mô phỏng.
