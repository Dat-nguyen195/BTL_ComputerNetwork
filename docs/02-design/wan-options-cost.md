# So sánh WAN và chi phí

**Chủ trì:** TV1; TV2 phối hợp BOM. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

 Danh mục phương án và mô hình chi phí

| Phương án cần khảo sát | Điểm mạnh | Điểm yếu/điều kiện | Chi phí cần tính |
| --- | --- | --- | --- |
| **2 leased Ethernet/Metro-E**, routed OSPF tại handoff phù hợp | Đường riêng, mô hình dễ giải thích và mô phỏng | Khả dụng hạ tầng và SLA do nhà mạng; hai nhánh chưa có dự phòng tuyến | `C_E + 2L_E/tháng` |
| **MPLS L3VPN** đến 3 site | Tách mạng, hỗ trợ nhiều site theo dịch vụ nhà cung cấp | Phụ thuộc nhà mạng/PE-CE; MPLS không tự mã hóa payload | `C_M + (L_Main + L_DBP + L_BHTQ)/tháng` |
| **SD-WAN overlay** trên leased/MPLS | Chính sách ứng dụng, quản lý tập trung; có thể thêm underlay sau | License/controller, độ phức tạp; SD-WAN không thay đường truyền vật lý | `C_S + license + chi phí underlay` |
| **IPsec routed overlay** trên 2 leased lines | Mã hóa liên site, giữ baseline truyền dẫn | Overhead, CPU, MTU và quản lý khóa; không có đầy đủ tính năng SD-WAN | `C_V + phí 2 leased lines + license nếu có` |
| Internet business + IPsec/SD-WAN | Có thể phù hợp phương án tối ưu ngân sách | Chỉ là phương án thay thế cần phê duyệt vì đề yêu cầu 2 leased lines; vẫn backhaul qua Main | `C_I + cước 3 site + license` |
| 4G/5G hoặc radio/microwave dự phòng | Đa dạng đường truyền nếu khảo sát cho phép | Sóng/LOS, quota, IP và vận hành; chưa nằm trong hạ tầng đã cho | `C_backup + cước/thiết bị + dữ liệu phát sinh` |

`C_*` là CAPEX/khởi tạo; `L_*` là cước dịch vụ theo kỳ. **Các biến là ô chờ báo giá, không phải giá thị trường đã xác thực.** TV1 cùng TV2 lấy đơn giá, loại thuế, thời hạn hợp đồng, tốc độ đối xứng, SLA, IP tĩnh, phí lắp đặt/license, nguồn và ngày báo giá; dùng `TCO 5 năm = CAPEX + 60 × OPEX tháng + bảo trì/license chưa nằm trong OPEX`. Khi so sánh, giữ cùng băng thông/SLA và không tính trùng phí underlay. Không thể liệt kê tất cả gói nhà mạng nếu chưa biết địa chỉ khảo sát; bảng này là danh mục công nghệ để lấy phương án khả dụng và chi phí ở Step 2-3.

**Quyết định baseline:** giữ 2 leased lines và OSPF để triển khai chức năng; lựa chọn thương mại MPLS/SD-WAN được TV1 chốt sau so sánh kỹ thuật và chi phí. Phần chưa mô phỏng được phải có thiết kế, lý do và giới hạn công cụ.

## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
