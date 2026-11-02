# Hệ thống camera

**Chủ trì:** TV3 về quyền/lưu trữ; TV2 về cáp/PoE. **Trạng thái:** BẢN THẢO THIẾT KẾ (DRAFT) - CHỜ REVIEW.

Camera/NVR được quy hoạch tại **VLAN 110 (An ninh)** riêng biệt cho từng site. Chỉ NVR và máy tính của quản trị viên an ninh (Security Admin) được cấp quyền truy cập dải mạng này, thông qua Access Control List (ACL): tại Main đặt trên Core/Firewall, tại mỗi Aux đặt trên distribution/gateway của site (Aux không có firewall riêng). Do chưa khảo sát thực địa, toàn bộ số liệu bên dưới là **bản thiết kế giả định (Assumptions)** để làm cơ sở cấp phát tài nguyên hệ thống.

## 1. Thông số giả định ban đầu (Assumptions)

- **Số lượng camera:** 4 camera/tầng (hành lang, sảnh, thang máy). Không đặt trong phòng bệnh nhân hay phòng vệ sinh để đảm bảo quyền riêng tư.
  - Main Site: 40 camera (2 tòa × 5 tầng × 4).
  - Aux DBP: 8 camera (2 tầng × 4).
  - Aux BHTQ: 8 camera (2 tầng × 4).
- **Chất lượng video:** nén H.265, độ phân giải 4MP (2K), bitrate dự kiến **4 Mbps/camera** (giả định, chờ chốt theo model camera và mức độ chuyển động).
- **Thời gian lưu trữ tối thiểu:** **30 ngày** (giả định của nhóm, chưa có nguồn quy định; cần xác nhận nếu bệnh viện yêu cầu lưu lâu hơn).
- **Mô hình NVR:** NVR cục bộ tại mỗi site. Luồng video **chỉ chạy trong LAN** (từ access switch lên NVR ở MDF/phòng IT), không đi qua đường WAN (leased line) để tránh quá tải băng thông liên site. Chỉ xem lại (playback) từ xa mới dùng băng thông WAN.

## 2. Cổng, cáp và nguồn PoE (TV2)

- **Cổng và cáp:** mỗi camera dùng 1 cổng access 1GbE và 1 tuyến cáp đồng UTP Cat6 nối thẳng về tủ IDF của tầng tương ứng.
- **PoE budget:** tính theo mức cấp tối đa của PoE class 3 (802.3af) là **15,4 W/camera**, không dùng mức tiêu thụ thực để có dư địa.
  - Tải mỗi tầng: 4 camera × 15,4 W = **61,6 W**.
  - Kết luận TV2: switch access Catalyst 9200L-48P có ngân sách PoE 370 W. Dù dồn cả 4 camera vào một switch, vẫn còn 370 − 61,6 = **308,4 W** để cấp nguồn cho AP Wi-Fi (3 AP/tầng × 30 W = 90 W). Đáp ứng yêu cầu.

## 3. Băng thông và lưu trữ NVR (TV3)

Công thức:

`Storage_GB = B_total × 10^6 / 8 × 86400 × số_ngày_lưu / 10^9`

với `B_total` (Mbps) là tổng bitrate của các camera trong site. Dung lượng ổ cứng **dùng được** cần ≥ `Storage_GB` × 1,2 (dự phòng 20% cho định dạng ổ và dư địa).

| Site | Camera | `B_total` | `Storage_GB` (30 ngày) | Cần dùng được (×1,2) | Ví dụ cấu hình |
| --- | --- | --- | --- | --- | --- |
| Main | 40 | 160 Mbps | **51.840 GB (≈ 51,8 TB)** | **≥ 62,2 TB** | 10 ổ HDD 8 TB chạy RAID 6 = 64 TB dùng được |
| DBP | 8 | 32 Mbps | **10.368 GB (≈ 10,4 TB)** | **≥ 12,5 TB** | 3 ổ HDD 8 TB chạy RAID 5 = 16 TB dùng được |
| BHTQ | 8 | 32 Mbps | **10.368 GB (≈ 10,4 TB)** | **≥ 12,5 TB** | 3 ổ HDD 8 TB chạy RAID 5 = 16 TB dùng được |

Cách tính Main: 160 × 10^6 / 8 × 86.400 × 30 / 10^9 = 51.840 GB; × 1,2 = 62.208 GB. Aux: 32 × 10^6 / 8 × 86.400 × 30 / 10^9 = 10.368 GB; × 1,2 = 12.442 GB. Cấu hình ví dụ chỉ để minh họa dung lượng dùng được, model NVR và ổ cứng chờ TV3 chốt.

## Theo dõi cập nhật

- [ ] (TV2 & TV3) Thiết lập kịch bản giả định về băng thông, dung lượng và PoE (chờ reviewer xác nhận).
- [ ] (TV5) Xác nhận thông số khảo sát về độ che khuất (góc nhìn), vị trí thực, vùng riêng tư và loại cáp thực tế với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế sau khi có mô hình NVR chính thức.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.