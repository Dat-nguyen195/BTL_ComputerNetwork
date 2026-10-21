# Tính thông lượng và băng thông ISP

**Chủ trì:** TV4; TV1 phối hợp WAN/ISP. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

### 6.1. Dữ liệu gốc và giả định phải chốt

| Dữ liệu | Download | Upload | Cách sử dụng |
| --- | --- | --- | --- |
| Workstation | **500 MB/ngày/máy** | **100 MB/ngày/máy** | Nhân với 600/260/260 máy |
| Server | **1.000 MB/ngày** | **2.000 MB/ngày** | [A] tr.2 ghi “Servers ... total”; phải tính cả cách hiểu tổng và mỗi server |
| Thiết bị khách Wi-Fi | **500 MB/ngày/thiết bị** | Không được cung cấp | Giả định theo thiết bị; giữ biến số và kịch bản nếu 500 MB là tổng khách |
| Giờ cao điểm | Khoảng **80% tải**, **09:00-11:00 và 15:00-16:00** | Tổng cửa sổ **3 giờ/ngày** | Giả định 80% dung lượng ngày nằm trong hai cửa sổ này |
| Tăng trưởng | **20% trong 5 năm** | Cùng hệ số 1,2 | Không dùng lũy thừa 1,2⁵ |

Không có số lượng khách hoặc tỷ lệ đồng thời trong [A]. Đặt `N_M`, `N_D`, `N_B` là số thiết bị khách/ngày tại Main, DBP, BHTQ; `N = N_M + N_D + N_B`. Số thiết bị/ngày dùng tính dung lượng; số thiết bị **đồng thời** dùng tính AP/subnet, không hoán đổi hai đại lượng. Upload khách, camera, PACS và sao lưu chưa định lượng phải thành các hạng mục bổ sung, không gán bằng 0 trong thiết kế cuối.

### 6.2. Kịch bản tính toán bảo thủ theo từng server

Dùng MB thập phân: `1 MB = 10^6 byte`, `1 byte = 8 bit`. Các con số dưới đây là phép tính từ giả định, không phải kết quả đo. Giả sử lưu lượng download/upload đã cho đi qua ISP để có một envelope dự trù; cần khảo sát tỷ lệ LAN/WAN/Internet và đích server để tránh cộng trùng giao dịch nội bộ.

```text
D_down = 1120 × 500 + 14 × 1000 + 500N = 574000 + 500N MB/ngày
D_up   = 1120 × 100 + 14 × 2000        = 140000 MB/ngày + tải upload chưa biết
B_peak(D) = D × 8 × 0,8 / (3 × 3600) Mbps
B_design  = B_peak × 1,2 / 0,70
```

Hệ số sử dụng mục tiêu **70%** là giả định thiết kế tạo dư địa, không có trong đề. `B_peak` là **trung bình trong cửa sổ cao điểm**, chưa bao gồm đột biến tức thời, overhead giao thức/mã hóa, camera và workload bệnh viện chưa khảo sát.

| Phạm vi, chưa có khách | Download MB/ngày | Upload MB/ngày | Peak down/up Mbps | Design down/up Mbps |
| --- | --- | --- | --- | --- |
| Main: 600 PC + 10 server | 310.000 | 80.000 | 183,70 / 47,41 | 314,92 / 81,27 |
| DBP: 260 PC + 2 server | 132.000 | 30.000 | 78,22 / 17,78 | 134,10 / 30,48 |
| BHTQ: 260 PC + 2 server | 132.000 | 30.000 | 78,22 / 17,78 | 134,10 / 30,48 |
| Tổng ra Main Internet | **574.000** | **140.000** | **340,15 / 82,96** | **583,11 / 142,22** |

Mỗi thiết bị khách/ngày thêm khoảng **0,2963 Mbps peak down**, hoặc **0,5079 Mbps design down** theo cùng giả định. Ví dụ minh họa **N = 300**, không phải số đề bài: tổng nhu cầu thiết kế khoảng **735,49 Mbps down / 142,22 Mbps up**, chưa gồm upload khách và các tải bổ sung.

**Kịch bản server là tổng toàn hệ thống:** dùng `D_down = 561000 + 500N`, `D_up = 114000`, cho peak **332,44 / 67,56 Mbps** khi N = 0. Nếu số tổng là cho từng site thì dùng 3 lần định mức server: `D_down = 563000 + 500N`, `D_up = 118000`. Nếu 500 MB khách là tổng thay vì mỗi thiết bị, thay `500N` bằng `500` tại đúng phạm vi được xác nhận. TV4 phải lưu các kịch bản, lý do chọn baseline và người duyệt; không im lặng biến chữ “total” thành số liệu chắc chắn trên từng máy.

### 6.3. Điều kiện chọn ISP và WAN

- Hai xDSL tại Main cần tổng năng lực **hiệu dụng** down/up đáp ứng `B_design` theo kịch bản đã duyệt, có QoS cho ứng dụng bệnh viện. Không coi tốc độ download danh nghĩa là tốc độ upload. Chưa đủ dữ liệu để kết luận một gói xDSL cụ thể đáp ứng; nếu không đủ, ghi rõ khoảng thiếu và phương án nâng cấp quang ngoài baseline để xin xác nhận khi triển khai thực tế.
- WAN mỗi chi nhánh cần mang lưu lượng Internet của chi nhánh cộng giao dịch đến Main và lưu lượng liên site liên quan, xét **riêng từng chiều**. Mức **134,10 Mbps down / 30,48 Mbps up** mỗi Aux trước khách chỉ là envelope theo giả định trên, không phải định mức leased line đã chốt. Tránh cộng lại một giao dịch vừa tính ở client vừa tính ở server.
- Khi mất một xDSL, tuyến còn lại phải đạt tải dịch vụ thiết yếu đã ưu tiên; nếu yêu cầu đủ tải như bình thường thì **mỗi tuyến** phải đáp ứng tải đó. Ghi SLA, tải bị giảm và giới hạn failover, không tự ghi “HA đạt 100%”.

## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
