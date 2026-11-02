# SUPP-03 - Site-to-site và teleworker VPN

**Trạng thái: NOT RUN. Chuẩn bị: TV3 + TV1. Cập nhật: 02/11/2026.** VPN/IDS/IPS hiện DESIGN ONLY; chưa có runtime evidence.

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích / VLAN / port | Ghi actual khi chạy |

## Điều kiện và thao tác

1. Chỉ chạy sau khi triển khai phương án trong `docs/04-security/vpn-plan.md`; hiện chưa có crypto. Ghi image/client/certificate fingerprint đã che dữ liệu nhạy cảm.
2. Site-to-site: kiểm IKEv2 SA, IPsec SA và counter encrypt/decrypt hai chiều Main↔DBP, Main↔BHTQ; bắt gói underlay, bảo đảm không có đường cleartext ưu tiên. Kiểm Aux↔Aux nếu được duyệt.
3. Thử gói lớn/DF và ứng dụng TCP; ghi MTU/MSS đo được. Ngắt leased line, ghi đúng mất tunnel/site; chưa có underlay dự phòng.
4. Teleworker: IP pool không overlap; người có quyền mở HIS/CRM, bị chặn DB/admin/camera. Kiểm DNS, split routes và return route ở Core/Edge.
5. Sai account/certificate/MFA và account bị thu hồi phải bị từ chối; lưu log. Không lưu khóa riêng/mật khẩu thật trong evidence.

## Expected

Chỉ người/luồng có quyền truy cập; payload được bảo vệ khi nói đã có IPsec, không NAT nội bộ, không bypass cleartext. Thiếu SA/capture thì không kết luận VPN chỉ từ ping.

## Actual / evidence / retest

Chưa thực hiện. Khi có lần chạy, tạo thư mục theo run ID, giữ log/ảnh gốc, ghi version/hash và actual từng bước; không dùng log kiểm tĩnh làm evidence runtime. Lỗi: ghi bước tái hiện, người sửa, bản sau sửa, ca chạy lại và reviewer thực.
