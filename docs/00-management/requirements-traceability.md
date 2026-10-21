# Truy vết 7 bước yêu cầu

**Chủ trì:** TV5; TV1 duyệt. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

Các đường dẫn bên dưới là **sản phẩm dự kiến** sẽ được tạo khi triển khai; repository đã có scaffold; các sản phẩm kỹ thuật cuối vẫn đang chờ triển khai.

| Bước | Điểm | Nội dung và điều kiện nghiệm thu | Chủ trì / phối hợp | Sản phẩm dự kiến |
| --- | --- | --- | --- | --- |
| Step 1 | 1 | Phân tích 3 site; checklist khảo sát; vùng tải cao/load balancer; kiến trúc phù hợp tòa nhà/mỹ quan; wireless và phân vùng server/DMZ/firewall | TV5 / TV1, TV2, TV3, TV4 | `docs/01-survey/`, `docs/02-design/architecture.md` |
| Step 2 | 1 | BOM/spec; IP plan; sơ đồ vật lý/cabling; WAN và OSPF; phương án có chi phí và ưu/nhược | TV2 / TV1, TV3 | `docs/02-design/`, `configs/` |
| Step 3 | 1 | Tính down/up, 80% trong 3 giờ, kịch bản Wi-Fi/server, tăng trưởng; đề xuất ISP và cấu hình theo tải | TV4 / TV1, TV2 | `docs/03-capacity/throughput.md` |
| Step 4 | 2 | Mô phỏng tích hợp 3 site; file mở lại được, IP/VLAN/config khớp thiết kế, ghi rõ phần mô hình hóa | TV4 / TV1, TV2, TV3 | `simulation/packet-tracer/hospital-3sites.pkt` hoặc GNS3 |
| Step 5 | 2 | Chạy 6 nhóm test bắt buộc bên dưới; có expected/actual, ảnh/log, môi trường và liên hệ phiên bản | TV4 / TV1, TV2, TV3 | `test_results/test-matrix.md`, `test_results/TC01-*/` đến `TC06-*/` |
| Step 6 | 2 | Đánh giá tin cậy, dễ nâng cấp, đa dạng phần mềm, an toàn và bảo mật; vấn đề còn lại, hướng phát triển | TV5 / tất cả | `docs/05-evaluation/evaluation.md`, `docs/05-evaluation/risks.md` |
| Step 7 | 1 | Báo cáo PDF và mô phỏng được TV1 duyệt, đóng gói, nộp BKeL, lưu bằng chứng nộp | TV1 / TV5, TV4 | `docs/06-report/final/report.pdf`, `submission/` |
| **Tổng** | **10** | **Không bỏ bước đánh giá hoặc bước nộp bài** | | |

## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
