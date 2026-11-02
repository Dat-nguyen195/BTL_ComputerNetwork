# TC04 - Truy cập DMZ và static PAT

**Trạng thái: NOT RUN. Chuẩn bị: TV3 + TV1. Người chạy/lưu bằng chứng: TV4 phối hợp chủ trì. Cập nhật: 02/11/2026.**

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích mẫu | PC10→10.10.80.10:80; Web-Lab192.0.2.100→198.51.100.2:8080 |
| Giao thức / công cụ | HTTP80, PAT8080; negative cổng/host không công bố |
| Điều kiện trước | DMZ HTTP bật, route .80/27 tới FW, ISP2 tốt, ZBF/EdgePAT đã nạp |

## Bước chạy và expected

Thực hiện đúng mục tương ứng trong [runbook](../../simulation/test-runbook.md). HTTP đúng trang; DNAT private80, reply ISP2; host/cổng khác bị chặn. IP client lấy từ lease thực, không khẳng định mẫu là IP đã được cấp.

## Actual và evidence

Chưa thực hiện. Lưu ảnh ở `screenshots/`, log văn bản `.txt` ở `logs/`, có run ID và liên kết từng bước. Mỗi hướng/nguồn phải có actual riêng. Output CLI/RTT/NAT port không tự soạn. Bộ kiểm tĩnh không thay runtime.

| Lần chạy / bước | Expected | Actual | Evidence / hash | Kết luận |
| --- | --- | --- | --- | --- |
| Chưa chạy | Theo runbook | Chưa có | Chưa có | NOT RUN |

## Lỗi và retest

- Lỗi/bước tái hiện/người sửa: chưa có kết quả để kết luận.
- Project sau sửa và hash: chưa có.
- Ca chạy lại / actual / reviewer: chưa thực hiện.
