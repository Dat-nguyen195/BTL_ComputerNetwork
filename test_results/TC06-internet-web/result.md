# TC06 - Web Internet qua Main

**Trạng thái: NOT RUN. Chuẩn bị: TV4 + TV1 + TV3. Người chạy/lưu bằng chứng: TV4 phối hợp chủ trì. Cập nhật: 02/11/2026.**

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích mẫu | PC10 và Guest ở Main/DBP/BHTQ→192.0.2.100:80 / web.hospital.test |
| Giao thức / công cụ | HTTP theo IP/tên, NAT/route-map/track/session |
| Điều kiện trước | Web/DNS lab bật, route hai ISP và return public đúng, ZBF đã nạp |

## Bước chạy và expected

Thực hiện đúng mục tương ứng trong [runbook](../../simulation/test-runbook.md). Cả6 nguồn ra Web được; Aux qua Main; PAT đúng egress; không local breakout. IP client lấy từ lease thực, không khẳng định mẫu là IP đã được cấp.

## Actual và evidence

Chưa thực hiện. Lưu ảnh ở `screenshots/`, log văn bản `.txt` ở `logs/`, có run ID và liên kết từng bước. Mỗi hướng/nguồn phải có actual riêng. Output CLI/RTT/NAT port không tự soạn. Bộ kiểm tĩnh không thay runtime.

| Lần chạy / bước | Expected | Actual | Evidence / hash | Kết luận |
| --- | --- | --- | --- | --- |
| Chưa chạy | Theo runbook | Chưa có | Chưa có | NOT RUN |

## Lỗi và retest

- Lỗi/bước tái hiện/người sửa: chưa có kết quả để kết luận.
- Project sau sửa và hash: chưa có.
- Ca chạy lại / actual / reviewer: chưa thực hiện.
