# Đề xuất IDS/IPS và chống phishing

Trạng thái: THIẾT KẾ / CHƯA NGHIỆM THU TRÊN NATIVE. Firewall ZBF/ACL/NAT đã có bằng chứng Cisco riêng; các bằng chứng đó không chứng minh IDS/IPS.

Đề xuất IDS thụ động nhận bản sao lưu lượng từ SPAN tại DMZ hoặc core, gửi cảnh báo về hệ thống quản lý. IPS inline tại biên FW–DMZ cần sizing throughput khi bật chữ ký, policy bypass/fail-closed, quản trị riêng và phương án lỗi. Chọn appliance/license sau khảo sát tải và khả năng hỗ trợ; không gán chức năng này cho firewall mô phỏng chỉ vì có biểu tượng.

Chống phishing cần kết hợp DNS/web filtering, bảo vệ email/endpoint, cập nhật feed, nhận thức người dùng và quy trình xử lý. Chưa có feed thật, test alert/drop hoặc failover sensor trong native.

Khi triển khai phải có lưu lượng kiểm an toàn, positive control, alert ID/log, counter drop, timestamp và thử dừng sensor. Nếu thuộc chương trình yêu cầu triển khai IDS/IPS, hạng mục này vẫn là khoảng trống cần hoàn thiện, không được ghi PASS.
