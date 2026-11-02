# Nhật ký tích hợp mô phỏng

**Điều phối:** TV4. **Trạng thái:** chưa có project hoặc lần tích hợp/kiểm mở lại được xác nhận.

| Ngày | Loại cập nhật | Nội dung | Kết quả / giới hạn |
| --- | --- | --- | --- |
| 02/11/2026 | Chuẩn bị tích hợp offline TV1/TV3/TV4 | Ghép9 router với ACL/relay/ZBF/static PAT,5 switch lab,18 pool,14 link/30 endpoint; thêm script capacity/checker/runbook/contributions | Kiểm tĩnh có log riêng; chưa nạp IOS, chưa nhận module project, không có test/persistence/runtime hash |
| 26/10/2026 | Chuẩn bị cấu hình tham chiếu TV1 | WAN/edge/branches, routing stand-in Core/FW, hai ISP và INET-Core chung | Có file text và hướng dẫn; chưa nạp IOS, chưa ghép project, chưa có hash mô phỏng |

## Mẫu ghi cho lần tích hợp thực tế

Ngày/người giữ file tổng; module/PR nhận; project/commit/hash trước và sau; node/port thay đổi; nền tảng/model/image/version; running/startup config; smoke test và log; lỗi/chủ trì/hạn; kết quả đóng/mở lại. TV4 điều phối để tránh ghi đè file nhị phân.

Lịch 06–08/11 trong kế hoạch là hạn dự kiến, không phải lần tích hợp đã thực hiện. Không dùng tag phiên bản tự đặt trong biên bản thay file project/hash thật.

Hồ sơ mới: [đối chiếu task](../docs/00-management/tv1-tv3-tv4-status.md), [kiểm tĩnh](../test_results/static/README.md), [manifest config](generated/manifest.json). Đây là lịch sử sửa file trong workspace, không phải biên bản bàn giao có chữ ký hoặc ghép `.pkt`.
