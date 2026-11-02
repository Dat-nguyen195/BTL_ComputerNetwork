# TC03 - Main với cả hai Aux

**Trạng thái: NOT RUN. Chuẩn bị: TV1. Người chạy/lưu bằng chứng: TV4 phối hợp chủ trì. Cập nhật: 02/11/2026.**

| Thuộc tính | Giá trị |
| --- | --- |
| Ngày / người chạy | Chưa chạy |
| Công cụ / version / model | Chưa xác nhận |
| Project / commit / SHA256 | Chưa có |
| Nguồn / đích mẫu | PC10 Main/DBP/BHTQ; mẫu10.10.10.10/10.20.10.10/10.30.10.10 |
| Giao thức / công cụ | ICMP; tracert/traceroute; OSPF route/neighbor |
| Điều kiện trước | Hai Serial và 3 adjacency ổn định; ACL cho ICMP giữa subnetPC10 |

## Bước chạy và expected

Thực hiện đúng mục tương ứng trong [runbook](../../simulation/test-runbook.md). Đủ Main→DBP, DBP→Main, Main→BHTQ, BHTQ→Main; không NAT nội bộ. IP client lấy từ lease thực, không khẳng định mẫu là IP đã được cấp.

## Actual và evidence

Chưa thực hiện. Lưu ảnh ở `screenshots/`, log văn bản `.txt` ở `logs/`, có run ID và liên kết từng bước. Mỗi hướng/nguồn phải có actual riêng. Output CLI/RTT/NAT port không tự soạn. Bộ kiểm tĩnh không thay runtime.

| Lần chạy / bước | Expected | Actual | Evidence / hash | Kết luận |
| --- | --- | --- | --- | --- |
| Chưa chạy | Theo runbook | Chưa có | Chưa có | NOT RUN |

## Lỗi và retest

- Lỗi/bước tái hiện/người sửa: chưa có kết quả để kết luận.
- Project sau sửa và hash: chưa có.
- Ca chạy lại / actual / reviewer: chưa thực hiện.
