# Server Farm, dịch vụ hạ tầng và DMZ

**TV3; cập nhật 02/11/2026. Trạng thái: thiết kế và dữ liệu cấu hình đã có; chưa dựng server trên mô phỏng.**

Phân bổ đúng **10 server Main (8 nội bộ + 2 DMZ), 2 DBP, 2 BHTQ**. Đây là vai trò đề xuất, không phải kết quả khảo sát ứng dụng. [Danh mục máy và địa chỉ](../../simulation/lab/endpoints.csv) là nguồn nạp cho lab; [IP plan](ip-vlan-plan.md) xác định subnet/gateway. NVR là appliance riêng trong BOM camera, không cộng vào 14 server ứng dụng.

| Server | IP / prefix | Vai trò thiết kế | Dịch vụ trong lab |
| --- | --- | --- | --- |
| Main-Infra | 10.10.70.10/27 | DHCP, DNS nội bộ | DHCP; DNS tĩnh |
| Main-HIS | 10.10.70.11/27 | HIS | HTTP trang `HIS LAB - NO PATIENT DATA` |
| Main-PACS | 10.10.70.12/27 | RIS/PACS | HTTP thay thế ứng dụng; chưa chạy DICOM |
| Main-LIS | 10.10.70.13/27 | LIS | HTTP thay thế ứng dụng |
| Main-CRM | 10.10.70.14/27 | CRM | HTTP thay thế ứng dụng |
| Main-DB | 10.10.70.15/27 | Database của ứng dụng | Không bật Web/công bố Internet |
| Main-Backup | 10.10.70.16/27 | Backup, repository cập nhật | Thiết kế; chưa có backup job |
| Main-Monitor | 10.10.70.17/27 | Syslog, NTP, giám sát | Bật dịch vụ nếu công cụ hỗ trợ |
| Main-WebDMZ | 10.10.80.10/27 | Web công bố | HTTP 80; static PAT ISP2:8080 |
| Main-ProxyDMZ | 10.10.80.11/27 | Reverse proxy/WAF dự trù | Không công bố; chưa chạy WAF/HA |
| DBP-Infra | 10.20.70.6/28 | DHCP, DNS cục bộ | DHCP; DNS tĩnh |
| DBP-Local | 10.20.70.7/28 | Cache/đệm tác vụ tại chi nhánh | Thiết kế; chưa đồng bộ dữ liệu |
| BHTQ-Infra | 10.30.70.6/28 | DHCP, DNS cục bộ | DHCP; DNS tĩnh |
| BHTQ-Local | 10.30.70.7/28 | Cache/đệm tác vụ tại chi nhánh | Thiết kế; chưa đồng bộ dữ liệu |

Gateway của server là `.70.1` tại site tương ứng; DMZ là `10.10.80.1` trên Main-FW. DNS nội bộ là Main-Infra hoặc Infra cục bộ; DMZ dùng DNS Web-Lab `192.0.2.100` trong lab cô lập. Tất cả server dùng IP tĩnh ngoài pool client. Sau tăng trưởng: Main 12, DBP 3, BHTQ 3; làm tròn từng site nên tổng dự trù là 18, không dùng 16,8 server vật lý.

## DHCP và DNS để TV4 dựng dịch vụ

Chạy `python3 scripts/build_lab.py`, lấy **18 pool** từ [dhcp-pools.csv](../../simulation/generated/dhcp-pools.csv). Mỗi dòng có DHCP server, start/end, mask, gateway, DNS và max users, có thể nhập vào Services > DHCP của Server-PT. Tắt pool mặc định không dùng. Main có 8 pool, mỗi Aux có 5. VLAN 70/80/90 dùng IP tĩnh; camera chưa bật DHCP trong baseline. Các pool /25 đúng 120 lease; không loại thêm địa chỉ client nếu chưa tính lại sức chứa 5 năm.

`ip helper-address` nằm trên từng subinterface client của Main-Core/DBP-GW/BHTQ-GW. DHCP ban đầu dùng UDP 68→67 broadcast, renew có thể unicast tới Infra cùng site. ACL chỉ mở đúng hai trường hợp; không mở toàn bộ Server Farm cho guest. DNS của guest là Web-Lab ngoài mạng, giúp tách guest khỏi DNS nội bộ. [Cisco DHCP relay](https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/27470-100.html) giải thích vai trò helper trong chuyển tiếp yêu cầu qua subnet; cần kiểm DORA và renew thực tế.

Tạo bản ghi trên ba DNS nội bộ: `his.hospital.test → 10.10.70.11`, `pacs.hospital.test → 10.10.70.12`, `lis.hospital.test → 10.10.70.13`, `crm.hospital.test → 10.10.70.14`, `portal.hospital.test → 10.10.80.10`, `web.hospital.test → 192.0.2.100`. Trên Web-Lab chỉ cần `web.hospital.test → 192.0.2.100`; không sao chép zone chứa tên/IP nội bộ cho guest. Nếu Server-PT không forward DNS, khai báo các bản ghi cần test trực tiếp, ghi rõ giới hạn này.

## Giới hạn và vận hành

HTTP 80 chỉ chứng minh kết nối dịch vụ trong lab dữ liệu giả; vận hành cần HTTPS và ứng dụng thật, xác thực, log truy cập. Chưa có TLS certificate, database hay DICOM thực; permit 443/11112 không chứng minh đã triển khai chúng. Server cùng VLAN 70 trao đổi tại L2 nên ACL trên gateway không kiểm soát được luồng app→DB cùng subnet; cần host firewall hoặc tách subnet/VRF khi triển khai thật.
