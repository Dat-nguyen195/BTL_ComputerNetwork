# Mô phỏng 3 site

**Chủ trì tích hợp:** TV4. **Trạng thái:** CHƯA CÓ FILE MÔ PHỎNG. **Nền tảng:** Packet Tracer dự kiến; cần thử tính năng trước khi chốt phiên bản/model. Đã có [bộ cấu hình tham chiếu TV1](modules/tv1-wan/README.md), chưa có project hoặc runtime test.

| Thuộc tính | Giá trị |
| --- | --- |
| Nền tảng / phiên bản | Chờ thử và chốt tuần 1 |
| File chính | Chờ `packet-tracer/hospital-3sites.pkt` hoặc project trong `gns3/` |
| Node/model/OS/dependency | Chưa chọn |
| Phiên bản file / checksum | Chưa có |
| PC/server đại diện | Chưa tạo; cần mapping quy mô thật |
| Người kiểm mở lại / ngày | Chưa kiểm |

## Hướng dẫn khi có file

1. Dùng phiên bản công cụ/dependency được ghi nhận; mở bản làm việc từ release/commit đã duyệt.
2. Chờ DHCP/STP/OSPF ổn định; kiểm tên Main/DBP/BHTQ và hai tuyến WAN/hai xDSL mô hình hóa.
3. Chạy test theo [test matrix](../test_results/test-matrix.md), lưu bằng chứng gắn đúng phiên bản.
4. Lưu/đóng/mở lại file để xác nhận cấu hình persist.

TV1-TV3 giao module/config text; TV4 giữ lịch chỉnh file tổng trong [integration log](integration-log.md). Không merge `.pkt` theo dòng. Internet/Web trong lab là mô phỏng. Chức năng không hỗ trợ phải ghi rõ MODELED/DESIGN ONLY.
