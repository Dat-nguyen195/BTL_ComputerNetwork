# TC05 - Guest isolation ba site

**Trạng thái: NOT RUN. Chuẩn bị: TV3 + TV2. Người chạy/lưu bằng chứng: TV4 phối hợp chủ trì. Cập nhật: 02/11/2026.**

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích mẫu | Guest10.10/20/30.100.x→PC10 cả 3 site và HIS10.10.70.11:80 |
| Giao thức / công cụ | ICMP/TCP negative; DHCP/DNS/HTTP ngoài positive |
| Điều kiện trước | Chứng minh PC đang up/HIS80 đang chạy bằng nguồn có quyền; guest có lease |

## Bước chạy và expected

Thực hiện đúng mục tương ứng trong [runbook](../../simulation/test-runbook.md). Guest không tới PC/server/DMZ/admin; DNS/DHCP/Web ngoài vẫn được; có deny counter. IP client lấy từ lease thực, không khẳng định mẫu là IP đã được cấp.

## Actual và evidence

Chưa thực hiện. Lưu ảnh ở `screenshots/`, log văn bản `.txt` ở `logs/`, có run ID và liên kết từng bước. Mỗi hướng/nguồn phải có actual riêng. Output CLI/RTT/NAT port không tự soạn. Bộ kiểm tĩnh không thay runtime.

| Lần chạy / bước | Expected | Actual | Evidence / hash | Kết luận |
| --- | --- | --- | --- | --- |
| Chưa chạy | Theo runbook | Chưa có | Chưa có | NOT RUN |

## Lỗi và retest

- Lỗi/bước tái hiện/người sửa: chưa có kết quả để kết luận.
- Project sau sửa và hash: chưa có.
- Ca chạy lại / actual / reviewer: chưa thực hiện.
