# Tính thông lượng và băng thông ISP

**Chủ trì:** TV4; TV1 phối hợp WAN/ISP. **Cập nhật:** 02/11/2026. **Trạng thái:** TÍNH TOÁN TÁI LẬP ĐƯỢC / CHƯA NGHIỆM THU NĂNG LỰC THỰC.

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

- [x] Đã tái lập số học bằng script, tách ba cách hiểu server và tải chưa biết.
- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.

## Tái lập và phân tích độ nhạy

[capacity.py](../../scripts/capacity.py) đọc [capacity-inputs.csv](capacity-inputs.csv), dùng thư viện chuẩn Python. [Baseline CSV](calculated-baseline.csv) là đầu ra tính toán, không phải log thiết bị. Upload khách chưa biết hiện bằng `UNKNOWN`; tổng upload là **phần đã biết**, không khẳng định tải khách bằng 0. Biến overhead không có trong đề nên mặc định 0, cần chỉ định riêng khi phân tích.

```bash
python3 scripts/capacity.py
python3 scripts/capacity.py --server-scope global
python3 scripts/capacity.py --server-scope per-site
python3 scripts/capacity.py --guests 200 50 50 --overhead 0.10
python3 scripts/capacity.py --guest-scope global
python3 scripts/capacity.py --internet-down-share 0.4 --internet-up-share 0.6
python3 scripts/test_capacity.py
```

`global` không tự phân bổ số tổng cho site. `--guest-scope global` thay tổng download khách bằng 500 MB/ngày toàn hệ thống, không nhân số thiết bị. `--guest-upload-mb` là upload mỗi thiết bị/ngày nếu có khảo sát. Internet share down/up là tỷ lệ **giả định của phần tải đã biết**, không suy ra từ đếm thiết bị; phần còn lại chưa tự động trở thành WAN vì cần biết cặp nguồn/đích.

| Giả định server, khách | Design down/up Mbps, chưa overhead | Cách dùng |
| --- | --- | --- |
| Server tổng toàn hệ thống, N=0 | 569,90 / 115,81 | Giữ cách hiểu sát chữ total để so sánh |
| Server tổng mỗi site, N=0 | 571,94 / 119,87 | Chỉ dùng nếu xác nhận phạm vi từng site |
| Mỗi server, N=0 | 583,11 / 142,22 | Envelope bảo thủ của baseline |
| Mỗi server, N=300 | 735,49 / 142,22 + upload khách chưa biết | Số khách minh họa |
| Mỗi server, N=0, thêm overhead10% | 641,42 / 156,44 | 10% là giả định, không phải benchmark |
| Mỗi server, N=300, thêm overhead10% | 809,04 / 156,44 + upload khách chưa biết | Chưa thêm workload ngoài định mức |

`B_design = B_peak × (1 + growth) × (1 + overhead) / utilization`. Growth tổng 20%, overhead và utilization là ba yếu tố khác nhau; không gọi phần dự phòng utilization là tốc độ đường dây thực. PACS/camera/backup có thể đã góp vào định mức tổng; chỉ thêm **phần chưa được tính** sau khi xác định phạm vi để tránh đếm hai lần.

## Kịch bản ISP từng chiều và khi lỗi

Các gói dưới chỉ là **giả định số học**, chưa có nhà mạng/báo giá/SLA và không gọi 500/500 Mbps là gói xDSL đã tồn tại.

| Năng lực hiệu dụng giả định | Hai đường tốt down/up | Chỉ một đường tốt | Khoảng thiếu so baseline 583,11/142,22 khi còn một đường |
| --- | --- | --- | --- |
| 2×100/20 Mbps | 200/40; thiếu 383,11/102,22 | 100/20 | 483,11/122,22 Mbps |
| 2×500/500 Mbps | 1000/1000, đủ tổng phần đã biết | 500/500 | 83,11/0 Mbps down/up |
| 2×750/250 Mbps | 1500/500, đủ tổng phần đã biết | 750/250 | 0/0 với N=0; N=300 + overhead10% thiếu ít nhất59,04 Mbps down |

Không chọn gói chỉ bằng tổng down: phải đủ up, tải theo egress và tải ưu tiên khi một ISP mất. Chính sách giảm tải đề xuất: ưu tiên HIS/LIS và giao dịch; hạn chế guest, dời backup/cập nhật/PACS bulk. Chưa biết tỷ lệ tải thiết yếu nên chưa có số Mbps QoS hay cam kết duy trì đủ dịch vụ.

PBR tham chiếu chia Main VLAN10/30/50 + 8 server nội bộ + DBP vào ISP1; nhóm Main20/40/60 + 2 DMZ + BHTQ vào ISP2. Theo cùng giả định mỗi máy và chưa khách: nhóm1 khoảng 294,60/77,21 Mbps, nhóm2 288,51/65,02 Mbps. Khách Main/BHTQ dồn nhóm2, khách DBP nhóm1; vì vậy không được suy tỷ lệ50/50 hoặc kết luận đủ từ tổng hai ISP. Một phiên chỉ dùng một egress.

Với mỗi Aux, tải ISP envelope134,10/30,48 Mbps là phần phải qua leased line; chiều Main→Aux tương ứng download, Aux→Main tương ứng upload. Lưu lượng HIS/PACS liên site, backup và VPN bổ sung phải thống kê riêng. Mức150–200 Mbps đối xứng trong WAN plan là điểm bắt đầu lấy báo giá, chưa đủ cơ sở khẳng định đáp ứng camera/PACS. Serial2 Mbps của lab chỉ test chức năng, không nghiệm thu sizing.
