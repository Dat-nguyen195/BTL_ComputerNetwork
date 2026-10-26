# Quy hoạch VLAN và địa chỉ IP toàn diện (VLSM Plan)

**Chủ trì:** TV1 (Trưởng nhóm, WAN & Routing Lead); TV2 (LAN) và TV3 (Security) đọc chéo.
**Trạng thái:** THIẾT KẾ ĐÃ HIỆU CHỈNH / CHỜ TV2–TV3 ĐỌC CHÉO VÀ MÔ PHỎNG.

---

## 1. Nguyên tắc thiết kế và phân bổ địa chỉ IP (VLSM)

1. **Khối địa chỉ tổng thể:** Sử dụng dải địa chỉ Private RFC 1918 lớp A `10.0.0.0/8`, phân chia phân cấp theo từng địa điểm (Site-based hierarchical addressing):
   - **Main Site (Trung tâm TP.HCM):** `10.10.0.0/16` (Vùng địa chỉ dự trữ quy mô lớn cho 600 máy trạm, 10 server, Wi-Fi, camera và quản trị).
   - **Auxiliary Site 1 - DBP (Điện Biên Phủ):** `10.20.0.0/16` (260 máy trạm, 2 server, Wi-Fi, camera và quản trị).
   - **Auxiliary Site 2 - BHTQ (Bà Huyện Thanh Quan):** `10.30.0.0/16` (260 máy trạm, 2 server, Wi-Fi, camera và quản trị).
   - **Mạng WAN Transit & Điểm-Điểm (P2P):** `10.255.0.0/24` (Dành riêng cho các kết nối L3 leased lines, core-to-firewall, firewall-to-edge).
   - **Dải cấp phát VPN Teleworker Pool:** `10.255.100.0/24` (Dành cho người dùng từ xa kết nối VPN Client-to-Site vào Main).
2. **Nguyên tắc phân rã VLSM (Variable Length Subnet Mask):**
   - Không cấu hình trực tiếp dải `/16` lên bất kỳ giao diện mạng nào. Chỉ cấu hình các subnet con cụ thể được cấp phát.
   - Các VLAN phòng ban máy trạm: Dùng prefix `/25` (128 IP, 126 usable hosts). Dự trữ `.1–.6` cho Default Gateway / HSRP / thiết bị mạng; dải DHCP pool từ `.7–.126` (đúng 120 IP). Đủ 120 PC sau tăng trưởng; không còn dư trong pool này nếu cần thêm host.
   - Phân vùng Server Farm: Dùng prefix `/27` (Main, 30 usable hosts) và `/28` (Aux, 14 usable hosts). Toàn bộ server dùng IP tĩnh, không nằm trong DHCP pool.
   - Phân vùng Quản trị (Management) & Camera: Dùng prefix `/24` (254 usable hosts).
   - Phân vùng Wi-Fi Khách (Guest Wi-Fi): Dùng prefix `/23` (510 usable hosts) dự trù 500 địa chỉ DHCP theo bảng; cần kiểm theo số khách đồng thời và lease, chưa kết luận đủ nhu cầu.
   - Các liên kết Transit WAN / L3: Dùng prefix `/30` (2 usable hosts) nhằm tối ưu không gian địa chỉ và bảo mật liên kết điểm-điểm.

---

## 2. Bảng quy hoạch IP chi tiết Main Site (`10.10.0.0/16`)

- **Quy mô hiện tại:** 600 máy trạm, 10 máy chủ (8 Server Farm, 2 DMZ).
- **Quy mô dự phòng 5 năm (+20%):** $600 \times 1{,}2 = 720$ máy trạm, $10 \times 1{,}2 = 12$ máy chủ.

| VLAN ID | Tên phân vùng / Nghiệp vụ | Hiện tại | 5 năm (+20%) | Network / CIDR | Subnet Mask | Default Gateway | Dải Reserved (Hạ tầng) | Dải DHCP Pool (.7–.126) | Dải IP Tĩnh | Broadcast | Usable Hosts |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | Tiếp nhận & Khám bệnh | 100 PC | 120 PC | `10.10.10.0/25` | `255.255.255.128` | `10.10.10.1` | `.2 – .6` | `10.10.10.7 – 10.10.10.126` (120 IP) | Không có | `10.10.10.127` | 126 |
| **20** | Điều trị & Nội trú | 100 PC | 120 PC | `10.10.20.0/25` | `255.255.255.128` | `10.10.20.1` | `.2 – .6` | `10.10.20.7 – 10.10.20.126` (120 IP) | Không có | `10.10.20.127` | 126 |
| **30** | Chẩn đoán hình ảnh (PACS) | 100 PC | 120 PC | `10.10.30.0/25` | `255.255.255.128` | `10.10.30.1` | `.2 – .6` | `10.10.30.7 – 10.10.30.126` (120 IP) | Không có | `10.10.30.127` | 126 |
| **40** | Xét nghiệm (LIS) | 100 PC | 120 PC | `10.10.40.0/25` | `255.255.255.128` | `10.10.40.1` | `.2 – .6` | `10.10.40.7 – 10.10.40.126` (120 IP) | Không có | `10.10.40.127` | 126 |
| **50** | Dược & Nghiệp vụ Y | 100 PC | 120 PC | `10.10.50.0/25` | `255.255.255.128` | `10.10.50.1` | `.2 – .6` | `10.10.50.7 – 10.10.50.126` (120 IP) | Không có | `10.10.50.127` | 126 |
| **60** | Hành chính & Quản trị | 100 PC | 120 PC | `10.10.60.0/25` | `255.255.255.128` | `10.10.60.1` | `.2 – .6` | `10.10.60.7 – 10.10.60.126` (120 IP) | Không có | `10.10.60.127` | 126 |
| **70** | Server Farm (Nội bộ) | 8 Svr | 10 Svr | `10.10.70.0/27` | `255.255.255.224` | `10.10.70.1` | `.2 – .9` | Không dùng DHCP | `.10 – .30` (Static) | `10.10.70.31` | 30 |
| **80** | DMZ (Công khai) | 2 Svr | 2 Svr | `10.10.80.0/27` | `255.255.255.224` | `10.10.80.1` | `.2 – .9` | Không dùng DHCP | `.10 – .30` (Static) | `10.10.80.31` | 30 |
| **90** | Network Management | Chờ BOM | Chờ BOM | `10.10.90.0/24` | `255.255.255.0` | `10.10.90.1` | `.2 – .10` | Không dùng DHCP | `.11 – .254` (Static) | `10.10.90.255` | 254 |
| **100** | Wi-Fi Khách (Guest) | Biến số | Dự phòng lớn | `10.10.100.0/23` | `255.255.254.0` | `10.10.100.1` | `.2 – .10` | `10.10.100.11 – 10.10.101.254` (500 IP) | Không có | `10.10.101.255` | 510 |
| **110** | Camera giám sát & NVR | Chờ khảo sát | Chờ khảo sát | `10.10.110.0/24` | `255.255.255.0` | `10.10.110.1` | `.2 – .10` | `10.10.110.100 – 10.10.110.254` | `.11 – .99` (NVR/Static) | `10.10.110.255` | 254 |
| **120** | Wi-Fi Nhân viên (Staff) | Biến số | Đồng bộ PC | `10.10.120.0/24` | `255.255.255.0` | `10.10.120.1` | `.2 – .10` | `10.10.120.11 – 10.10.120.254` (244 IP) | Không có | `10.10.120.255` | 254 |

---

## 3. Bảng quy hoạch IP chi tiết DBP Site (`10.20.0.0/16`)

- **Quy mô hiện tại:** 260 máy trạm, 2 máy chủ cục bộ.
- **Quy mô dự phòng 5 năm (+20%):** $\lceil 260 \times 1{,}2 \rceil = 312$ máy trạm, $\lceil 2 \times 1{,}2 \rceil = 3$ máy chủ.
- **Phân bổ máy trạm:** 3 nhóm (90, 90, 80 PC). Tăng trưởng 5 năm: 108, 108, 96 PC.

| VLAN ID | Tên phân vùng / Nghiệp vụ | Hiện tại | 5 năm (+20%) | Network / CIDR | Subnet Mask | Default Gateway | Dải Reserved (Hạ tầng) | Dải DHCP Pool (.7–.126) | Dải IP Tĩnh | Broadcast | Usable Hosts |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | Nghiệp vụ Khám bệnh 1 | 90 PC | 108 PC | `10.20.10.0/25` | `255.255.255.128` | `10.20.10.1` | `.2 – .6` | `10.20.10.7 – 10.20.10.126` (120 IP) | Không có | `10.20.10.127` | 126 |
| **20** | Nghiệp vụ Điều trị 2 | 90 PC | 108 PC | `10.20.20.0/25` | `255.255.255.128` | `10.20.20.1` | `.2 – .6` | `10.20.20.7 – 10.20.20.126` (120 IP) | Không có | `10.20.20.127` | 126 |
| **30** | Nghiệp vụ Hành chính 3 | 80 PC | 96 PC | `10.20.30.0/25` | `255.255.255.128` | `10.20.30.1` | `.2 – .6` | `10.20.30.7 – 10.20.30.126` (120 IP) | Không có | `10.20.30.127` | 126 |
| **70** | Server Farm cục bộ | 2 Svr | 3 Svr | `10.20.70.0/28` | `255.255.255.240` | `10.20.70.1` | `.2 – .5` | Không dùng DHCP | `.6 – .14` (Static) | `10.20.70.15` | 14 |
| **90** | Network Management | Chờ BOM | Chờ BOM | `10.20.90.0/24` | `255.255.255.0` | `10.20.90.1` | `.2 – .10` | Không dùng DHCP | `.11 – .254` (Static) | `10.20.90.255` | 254 |
| **100** | Wi-Fi Khách (Guest) | Biến số | Khảo sát | `10.20.100.0/23` | `255.255.254.0` | `10.20.100.1` | `.2 – .10` | `10.20.100.11 – 10.20.101.254` (500 IP) | Không có | `10.20.101.255` | 510 |
| **110** | Camera giám sát & NVR | Chờ khảo sát | Chờ khảo sát | `10.20.110.0/24` | `255.255.255.0` | `10.20.110.1` | `.2 – .10` | `10.20.110.100 – 10.20.110.254` | `.11 – .99` (NVR/Static) | `10.20.110.255` | 254 |
| **120** | Wi-Fi Nhân viên (Staff) | Biến số | Khảo sát | `10.20.120.0/24` | `255.255.255.0` | `10.20.120.1` | `.2 – .10` | `10.20.120.11 – 10.20.120.254` (244 IP) | Không có | `10.20.120.255` | 254 |

---

## 4. Bảng quy hoạch IP chi tiết BHTQ Site (`10.30.0.0/16`)

- **Quy mô hiện tại:** 260 máy trạm, 2 máy chủ cục bộ.
- **Quy mô dự phòng 5 năm (+20%):** $\lceil 260 \times 1{,}2 \rceil = 312$ máy trạm, $\lceil 2 \times 1{,}2 \rceil = 3$ máy chủ.
- **Phân bổ máy trạm:** 3 nhóm (90, 90, 80 PC). Tăng trưởng 5 năm: 108, 108, 96 PC.

| VLAN ID | Tên phân vùng / Nghiệp vụ | Hiện tại | 5 năm (+20%) | Network / CIDR | Subnet Mask | Default Gateway | Dải Reserved (Hạ tầng) | Dải DHCP Pool (.7–.126) | Dải IP Tĩnh | Broadcast | Usable Hosts |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | Nghiệp vụ Khám bệnh 1 | 90 PC | 108 PC | `10.30.10.0/25` | `255.255.255.128` | `10.30.10.1` | `.2 – .6` | `10.30.10.7 – 10.30.10.126` (120 IP) | Không có | `10.30.10.127` | 126 |
| **20** | Nghiệp vụ Điều trị 2 | 90 PC | 108 PC | `10.30.20.0/25` | `255.255.255.128` | `10.30.20.1` | `.2 – .6` | `10.30.20.7 – 10.30.20.126` (120 IP) | Không có | `10.30.20.127` | 126 |
| **30** | Nghiệp vụ Hành chính 3 | 80 PC | 96 PC | `10.30.30.0/25` | `255.255.255.128` | `10.30.30.1` | `.2 – .6` | `10.30.30.7 – 10.30.30.126` (120 IP) | Không có | `10.30.30.127` | 126 |
| **70** | Server Farm cục bộ | 2 Svr | 3 Svr | `10.30.70.0/28` | `255.255.255.240` | `10.30.70.1` | `.2 – .5` | Không dùng DHCP | `.6 – .14` (Static) | `10.30.70.15` | 14 |
| **90** | Network Management | Chờ BOM | Chờ BOM | `10.30.90.0/24` | `255.255.255.0` | `10.30.90.1` | `.2 – .10` | Không dùng DHCP | `.11 – .254` (Static) | `10.30.90.255` | 254 |
| **100** | Wi-Fi Khách (Guest) | Biến số | Khảo sát | `10.30.100.0/23` | `255.255.254.0` | `10.30.100.1` | `.2 – .10` | `10.30.100.11 – 10.30.101.254` (500 IP) | Không có | `10.30.101.255` | 510 |
| **110** | Camera giám sát & NVR | Chờ khảo sát | Chờ khảo sát | `10.30.110.0/24` | `255.255.255.0` | `10.30.110.1` | `.2 – .10` | `10.30.110.100 – 10.30.110.254` | `.11 – .99` (NVR/Static) | `10.30.110.255` | 254 |
| **120** | Wi-Fi Nhân viên (Staff) | Biến số | Khảo sát | `10.30.120.0/24` | `255.255.255.0` | `10.30.120.1` | `.2 – .10` | `10.30.120.11 – 10.30.120.254` (244 IP) | Không có | `10.30.120.255` | 254 |

---

## 5. Bảng quy hoạch liên kết Transit WAN & Point-to-Point (`10.255.0.0/24`)

Các liên kết mạng điểm-điểm được quy hoạch độc lập trong khối `10.255.0.0/24`, hoàn toàn cách ly khỏi dải mạng người dùng:

| Liên kết | Mục đích kết nối | Network / CIDR | Subnet Mask | IP Đầu A | Thiết bị / Cổng A | IP Đầu B | Thiết bị / Cổng B | Ghi chú OSPF |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :--- | :--- |
| **WAN Link 1** | Leased Line Main – DBP | `10.255.0.0/30` | `255.255.255.252` | `10.255.0.1` | Main-GW (Se0/0/0) | `10.255.0.2` | DBP-GW (Se0/0/0) | OSPF Area 0 (P2P, Cost 10) |
| **WAN Link 2** | Leased Line Main – BHTQ | `10.255.0.4/30` | `255.255.255.252` | `10.255.0.5` | Main-GW (Se0/0/1) | `10.255.0.6` | BHTQ-GW (Se0/0/0) | OSPF Area 0 (P2P, Cost 10) |
| **Transit L3 1** | Main Core – Main WAN GW | `10.255.0.8/30` | `255.255.255.252` | `10.255.0.9` | Main-Core (Gi0/1) | `10.255.0.10` | Main-GW (Gi0/0) | OSPF Area 0 (P2P, Cost 1) |
| **Transit L3 2** | Main Core – Main Firewall | `10.255.0.12/30` | `255.255.255.252` | `10.255.0.13` | Main-Core (Gi0/2) | `10.255.0.14` | Main-FW (Inside Gi0/0) | Static Route; không OSPF trên link FW |
| **Transit L3 3** | Main Firewall – Main Edge | `10.255.0.16/30` | `255.255.255.252` | `10.255.0.17` | Main-FW (Outside Gi0/1)| `10.255.0.18` | Main-Edge (Gi0/0) | Static Route (Outside FW) |

---

## 6. Dải địa chỉ VPN Pool & Mô phỏng Internet Public IP Lab

### 6.1. Dải cấp phát Teleworker VPN Pool

- **Subnet:** `10.255.100.0/24` (Subnet mask: `255.255.255.0`).
- **Dải cấp phát động cho bác sĩ/chuyên gia từ xa:** `10.255.100.2` đến `10.255.100.254` (253 địa chỉ dự trù; chưa triển khai VPN).
- **Default Gateway VPN Concentrator (Main-Edge/FW):** `10.255.100.1` dự trữ cho đầu VPN nếu công cụ cần gateway; không cấp trùng cho client. TV3 chốt cơ chế route-based/pool và route về trước triển khai.
- **Chính sách:** Cách ly hoàn toàn với các VLAN người dùng; chỉ được phép truy cập vào các server chỉ định tại VLAN 70 (HIS/PACS) thông qua tường lửa.

### 6.2. Dải Public IP mô phỏng Internet Lab (Edge – ISP)

- **ISP 1 (VNPT Telecom):**
  - Transit Edge – ISP1: `203.0.113.0/30` (Public Test Range RFC 5737).
  - Main-Edge (Gi0/1): `203.0.113.2/30`.
  - ISP1 Gateway: `203.0.113.1/30`.
- **ISP 2 (Viettel Telecom):**
  - Transit Edge – ISP2: `198.51.100.0/30` (Public Test Range RFC 5737).
  - Main-Edge (Gi0/2): `198.51.100.2/30`.
  - ISP2 Gateway: `198.51.100.1/30`.
- **Internet lab chung:** Web/DNS `192.0.2.100/26`, gateway `192.0.2.65` trên INET-Core; HTTP ON, DNS `web.hospital.test -> 192.0.2.100`.
- **Probe ISP1/ISP2:** `192.0.2.11/32` và `192.0.2.22/32` trên loopback INET-Core.
- **ISP1–INET:** `192.0.2.128/30`: ISP1 `.129`, INET-Core `.130`.
- **ISP2–INET:** `192.0.2.132/30`: ISP2 `.133`, INET-Core `.134`.
- **Loopback bệnh viện:** Main-Core `10.10.255.1/32`, Main-GW `10.10.255.2/32`, DBP `10.20.255.1/32`, BHTQ `10.30.255.1/32`; Edge `10.255.255.1/32` chỉ định danh lab.
- Chỉ dùng DNS lab đã dựng; không giả định `8.8.8.8`/`1.1.1.1` truy cập được trong topology mô phỏng.

---

## 7. Bảng kiểm tra xác thực không chồng lấn địa chỉ (Overlap Verification Matrix)

Để đảm bảo mạng hoạt động ổn định và không phát sinh lỗi định tuyến, bảng dưới tổng hợp vùng cấp phát. Kiểm riêng từng subnet đang dùng bằng script, không so khối /16 dự trữ như thể đó là interface:

| Thứ tự | Tên Subnet | Dải IP Network – Broadcast | Prefix | Dung lượng IP | Kiểm tra xung đột |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 1 | Main VLAN 10 | `10.10.10.0` – `10.10.10.127` | /25 | 128 | Độc lập, không trùng |
| 2 | Main VLAN 20 | `10.10.20.0` – `10.10.20.127` | /25 | 128 | Độc lập, không trùng |
| 3 | Main VLAN 30 | `10.10.30.0` – `10.10.30.127` | /25 | 128 | Độc lập, không trùng |
| 4 | Main VLAN 40 | `10.10.40.0` – `10.10.40.127` | /25 | 128 | Độc lập, không trùng |
| 5 | Main VLAN 50 | `10.10.50.0` – `10.10.50.127` | /25 | 128 | Độc lập, không trùng |
| 6 | Main VLAN 60 | `10.10.60.0` – `10.10.60.127` | /25 | 128 | Độc lập, không trùng |
| 7 | Main VLAN 70 (Server Farm) | `10.10.70.0` – `10.10.70.31` | /27 | 32 | Độc lập, không trùng |
| 8 | Main VLAN 80 (DMZ) | `10.10.80.0` – `10.10.80.31` | /27 | 32 | Độc lập, không trùng |
| 9 | Main VLAN 90 (Management) | `10.10.90.0` – `10.10.90.255` | /24 | 256 | Độc lập, không trùng |
| 10 | Main VLAN 100 (Guest Wi-Fi)| `10.10.100.0` – `10.10.101.255` | /23 | 512 | Chiếm dải .100.0 - .101.255, không chạm .110 |
| 11 | Main VLAN 110 (Camera) | `10.10.110.0` – `10.10.110.255` | /24 | 256 | Độc lập, không trùng |
| 12 | Main VLAN 120 (Staff Wi-Fi) | `10.10.120.0` – `10.10.120.255` | /24 | 256 | Độc lập, không trùng |
| 13 | DBP Tất cả VLAN (10–120) | `10.20.0.0` – `10.20.255.255` | /16 | Toàn dải DBP | Độc lập hoàn toàn với Main (10.10) và BHTQ (10.30) |
| 14 | BHTQ Tất cả VLAN (10–120) | `10.30.0.0` – `10.30.255.255` | /16 | Toàn dải BHTQ | Độc lập hoàn toàn với Main (10.10) và DBP (10.20) |
| 15 | WAN Transit Block | `10.255.0.0` – `10.255.0.31` | /27 sub-blocks | 32 | Các /30 nằm gọn từ .0 đến .19 |
| 16 | VPN Pool Block | `10.255.100.0` – `10.255.100.255`| /24 | 256 | Độc lập trong dải 10.255.x |

**Kiểm tra tĩnh:** chạy `python3 scripts/check_wan.py` để kiểm subnet cấp phát và các điều kiện WAN. Đây không phải kiểm chứng DHCP/OSPF hoặc cấu hình đang chạy. Tên nhóm nghiệp vụ, số AP/camera/thiết bị là mục cần TV2/TV3 xác nhận theo khảo sát và BOM.

---

## 8. Quy ước gán IP tĩnh, DHCP Scope và Gateway

1. **Default Gateway VLAN:** `.1` theo bảng; riêng DMZ80 kết thúc tại Main-FW, các VLAN Main khác tại Main-Core. Các link transit dùng địa chỉ trong bảng riêng.
2. **Hạ tầng dự phòng (Reserved):** Từ `.2` đến `.6` dùng cho HSRP/VRRP Virtual IP, standby router hoặc switch quản lý trực tiếp.
3. **DHCP Pool máy trạm:** Bắt đầu từ `.7` đến `.126` trên các dải `/25`. Gateway không bao giờ nằm trong DHCP Pool. DHCP Server sẽ cấu hình loại trừ (exclude) các địa chỉ `.1` đến `.6`.
4. **Server Farm:** Tuyệt đối không dùng DHCP. Toàn bộ server được gán IP tĩnh theo từng bảng: Main `.10–.30`, Aux `.6–.14`, được khai báo DNS phân giải tên miền rõ ràng (FQDN).
5. **Đọc chéo và phê duyệt:** TV1 chuẩn bị bảng; TV2/TV3 cần xác nhận dữ liệu trước khi khóa baseline. Khi đổi subnet, cập nhật config, sơ đồ, DHCP, ACL, OSPF, VPN và test liên quan.
