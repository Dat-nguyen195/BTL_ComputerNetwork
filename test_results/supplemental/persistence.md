# SUPP-05 - Lưu, đóng/mở lại và hash

**Trạng thái: NOT RUN. Chuẩn bị: TV4; TV1 đọc kết quả. Cập nhật: 02/11/2026.** VPN/IDS/IPS hiện DESIGN ONLY; chưa có runtime evidence.

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích / VLAN / port | Ghi actual khi chạy |

## Điều kiện và thao tác

1. Trên bản ứng viên, ghi tên/version/model/image; lưu running-config thành startup-config ở mọi node; lưu project. Ghi SHA256 file `.pkt` hoặc gói GNS3 và dependency cần mở.
2. Đóng hoàn toàn project, mở lại cùng môi trường; kiểm không cần cấu hình tay bổ sung. GNS3 phải có image hợp pháp/cấu hình đường dẫn, không đóng gói image có license vào Git.
3. Kiểm interface/OSPF/default/ACL/zone/NAT/relay còn đúng; DHCP/DNS/HTTP server còn bật; switch VLAN/trunk/access còn nguyên.
4. Chạy smoke đủ TC01–TC06 trên bản mở lại; ghi actual và liên kết evidence. Nếu chỉnh/lưu lại project, tính hash mới và retest phần ảnh hưởng.
5. TV1 duyệt riêng PDF và mô phỏng theo đúng hash tại submission/approval.md; khi chưa có PDF/project thì không ký APPROVED.

## Expected

Mở lại được, cấu hình persist, sáu nhóm smoke đúng expected; hash/manifest/evidence cùng phiên bản. Chưa có project nên chưa thể kiểm persistence.

## Actual / evidence / retest

Chưa thực hiện. Khi có lần chạy, tạo thư mục theo run ID, giữ log/ảnh gốc, ghi version/hash và actual từng bước; không dùng log kiểm tĩnh làm evidence runtime. Lỗi: ghi bước tái hiện, người sửa, bản sau sửa, ca chạy lại và reviewer thực.
