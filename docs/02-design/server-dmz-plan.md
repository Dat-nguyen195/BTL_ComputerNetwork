# Server Farm và DMZ

**Chủ trì:** TV3. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

Quy mô nguồn: Main 10 server; DBP 2; BHTQ 2. Dự kiến Main 8 server nội bộ và 2 DMZ, là phân bổ đề xuất có thể thay đổi; DMZ không cộng thêm ngoài tổng 10.

Vai trò cần phân bổ: HIS, RIS/PACS, LIS, CRM, database, DHCP/DNS, cập nhật, backup và Web DMZ. Một server đại diện có thể gom dịch vụ trong mô phỏng; không coi điều này là sizing triển khai thật.

| Node | Site/vùng | IP tĩnh | Vai trò | Nguồn được phép | Backup/HA | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| Chưa tạo | Main/Server Farm | Theo IP plan | Dịch vụ nội bộ | Theo ma trận quyền | Chờ thiết kế | PLANNED |
| Chưa tạo | Main/DMZ | Theo IP plan | Web công bố | Cổng được duyệt | Chờ thiết kế | PLANNED |

Database/hồ sơ bệnh án không công khai. DHCP/relay đúng subnet, server không nhận IP ngẫu nhiên từ pool máy trạm. Dự trù 5 năm 12/3/3 server theo làm tròn từng site.


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
