# Đầu vào và giả định tính tải

**Chủ trì:** TV4; TV1 duyệt. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

### 6.1. Dữ liệu gốc và giả định phải chốt

| Dữ liệu | Download | Upload | Cách sử dụng |
| --- | --- | --- | --- |
| Workstation | **500 MB/ngày/máy** | **100 MB/ngày/máy** | Nhân với 600/260/260 máy |
| Server | **1.000 MB/ngày** | **2.000 MB/ngày** | [A] tr.2 ghi “Servers ... total”; phải tính cả cách hiểu tổng và mỗi server |
| Thiết bị khách Wi-Fi | **500 MB/ngày/thiết bị** | Không được cung cấp | Giả định theo thiết bị; giữ biến số và kịch bản nếu 500 MB là tổng khách |
| Giờ cao điểm | Khoảng **80% tải**, **09:00-11:00 và 15:00-16:00** | Tổng cửa sổ **3 giờ/ngày** | Giả định 80% dung lượng ngày nằm trong hai cửa sổ này |
| Tăng trưởng | **20% trong 5 năm** | Cùng hệ số 1,2 | Không dùng lũy thừa 1,2⁵ |

Không có số lượng khách hoặc tỷ lệ đồng thời trong [A]. Đặt `N_M`, `N_D`, `N_B` là số thiết bị khách/ngày tại Main, DBP, BHTQ; `N = N_M + N_D + N_B`. Số thiết bị/ngày dùng tính dung lượng; số thiết bị **đồng thời** dùng tính AP/subnet, không hoán đổi hai đại lượng. Upload khách, camera, PACS và sao lưu chưa định lượng phải thành các hạng mục bổ sung, không gán bằng 0 trong thiết kế cuối.



## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
