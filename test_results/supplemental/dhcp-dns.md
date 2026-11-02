# SUPP-02 - DHCP/DNS và renew

**Trạng thái: NOT RUN. Chuẩn bị: TV3 + TV2. Cập nhật: 02/11/2026.** VPN/IDS/IPS hiện DESIGN ONLY; chưa có runtime evidence.

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích / VLAN / port | Ghi actual khi chạy |

## Điều kiện và thao tác

1. Với mỗi site, tạo client đại diện mỗi pool cần dùng (nghiệp vụ, guest, staff). Từ trạng thái chưa có IP, thực hiện DHCP; xem DORA ở Simulation mode nếu công cụ hỗ trợ.
2. Đối chiếu lease với `simulation/generated/dhcp-pools.csv`: đúng mask/gateway/DNS/start/end; không cấp gateway/server/network/broadcast. Kiểm hai client không trùng IP.
3. Renew lease, gồm unicast tới Infra `.70.10` ở Main hoặc `.70.6` ở Aux; xem ACL permit UDP68→67 và phản hồi67→68/relay67→67. Tắt server/đổi helper là ca lỗi riêng, không dùng nó làm bằng chứng isolation.
4. Client nội bộ resolve HIS/CRM/portal/Web; guest chỉ cần resolve `web.hospital.test` trên192.0.2.100. Thử HTTP bằng IP rồi hostname. Kiểm TCP53 nếu nền tảng có công cụ; nếu không, ghi phần đó chưa chạy.
5. Kiểm đủ 18 pool theo cấu hình server, thêm nhiều lease khi cần chứng minh khả năng cấp phát; một lease thành công không chứng minh pool đạt 120/244/500 client đồng thời.

## Expected

Đúng pool, DNS và gateway; guest không được truy cập DNS nội bộ ngoài ngoại lệ DHCP; không có IP trùng. Cấu hình120 lease chỉ là dung lượng thiết kế đến khi có kiểm tải thực.

## Actual / evidence / retest

Chưa thực hiện. Khi có lần chạy, tạo thư mục theo run ID, giữ log/ảnh gốc, ghi version/hash và actual từng bước; không dùng log kiểm tĩnh làm evidence runtime. Lỗi: ghi bước tái hiện, người sửa, bản sau sửa, ca chạy lại và reviewer thực.
