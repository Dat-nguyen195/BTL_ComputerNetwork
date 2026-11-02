# SUPP-04 - IDS/IPS và positive control

**Trạng thái: NOT RUN. Chuẩn bị: TV3 + TV4. Cập nhật: 02/11/2026.** VPN/IDS/IPS hiện DESIGN ONLY; chưa có runtime evidence.

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích / VLAN / port | Ghi actual khi chạy |

## Điều kiện và thao tác

1. Xác nhận yêu cầu chương trình kỹ sư tài năng, chọn sensor vị trí DMZ theo IDS plan, ghi HOME_NET, mode/version/interfaces và rule SHA256.
2. Kiểm syntax bằng `suricata -T` trên cấu hình thực. IDS mode: mở marker `/btl2-ids-probe` trên public DMZ từ Web-Lab, lưu EVE SID1000001; xác nhận sensor chỉ alert.
3. IPS mode riêng: rule action drop và inline thực; marker bị chặn, trang `/` vẫn mở. Lưu verdict/drop, timestamp/flowID, client và server logs.
4. Không coi packet mất do ACL/route là IPS. Chạy positive control khi tắt rule/giữ topology tương ứng; ghi tải CPU/loss/latency nếu đánh giá hiệu năng.
5. HTTP URI marker không kiểm được HTTPS chưa giải mã, không phải phishing engine. Chưa có cài đặt/rule runtime nên giữ NOT RUN.

## Expected

IDS có alert đúng marker; IPS có drop đúng marker và trang hợp lệ vẫn mở; có đối chứng để tách lỗi routing/firewall. Không đánh dấu đạt từ ACL hit.

## Actual / evidence / retest

Chưa thực hiện. Khi có lần chạy, tạo thư mục theo run ID, giữ log/ảnh gốc, ghi version/hash và actual từng bước; không dùng log kiểm tĩnh làm evidence runtime. Lỗi: ghi bước tái hiện, người sửa, bản sau sửa, ca chạy lại và reviewer thực.
