# Wi-Fi nhân viên /khách và quản trị AP

**TV2 chủ trì, TV3 ACL; cập nhật 02/11/2026. THIẾT KẾ GIẢ ĐỊNH; CHƯA RF SURVEY HOẶC RUNTIME.** Main phải phủ toàn site; Auxđược dự trù theo nhu cầu cần xác nhận. Giữ giả địnhTiendat3 AP/tầng, tăng và làm tròn lên4 AP/tầng để cấp cổng; không lấy số này làm kết quả khảo sát phủ sóng.

| Site | AP hiện tại→5 năm | Khách/ngày | Đồng thời | RF/channel/airtime |
| --- | --- | --- | --- | --- |
| Main |30→40 |Chưa biết |Chưa biết |Cần đo cả 10 tầng, hành lang/sảnh/vùng đông người |
| DBP |6→8 |Chưa biết |Chưa biết |2 tầng; xác nhận nhu cầu phủ |
| BHTQ |6→8 |Chưa biết |Chưa biết |2 tầng; xác nhận nhu cầu phủ |

Công thức chọn sau khảo sát: `N_AP >= max(N_phu_song, ceil(N_client_dong_thoi/client_target), ceil(traffic_peak/airtime_capacity))`. Client_target/airtime capacity phải đo/chọn theo workload và model, không dùng tốc độ quảng cáo PHY làm throughput ứng dụng. Khách/ngày dùng tính tải, khách đồng thời/lease dùng sizingAP/subnet, không đổi hai đại lượng.

## SSID /VLAN /gateway

| SSID | VLAN | IP/gateway tại site | Bảo mật /quyền |
| --- | --- | --- | --- |
| BenhVien_Staff |120 |10.10/20/30.120.0/24, gateway .1 |WPA2/WPA3-Enterprise+AAA khi hỗ trợ; HIS/CRM theo ma trận |
| BenhVien_Guest |100 |10.10/20/30.100.0/23, gateway .1 |Client isolation +ACL guest; chỉ DHCP/DNS/Web ngoài theo policy |
| AP management |90 |AP static dự trù .90.128–.191 Main, .90.128–.143 từng Aux |Không phát SSID quản trị, không cấp client thường vào VLAN90 |

VLAN ID lặp ở site không kéo dài L2 qua WAN. DHCP client dùng18 pool trong [server plan](server-dmz-plan.md); guest DNS ngoài192.0.2.100.244 staff/500 guest lease là số địa chỉ, chưa khẳng định đủ đồng thời. IPv6 chưa được kiểm; chỉ bật khi có ACL tương đương.

## Hai mô hình cần phân biệt

**Sản xuất dự trù:** C9115AXI +WLC, mỗi AP phát hai SSID và FlexConnect/local switching khi chọn. AP uplink native managementVLAN90, chỉ tagged100/120; cần xác nhận cấu hình AP/WLC. Main WLC .90.20/.21; mỗi controller hỗ trợ≥64 AP vì dự trù56 AP. AP→WLC CAPWAP và WLC→RADIUS/DNS/NTP phải được ACL cho đúng host/port trước triển khai; chưa có controller/AAA runtime. Đường Internet của Aux vẫn qua leased line/Main, local switching không phải local Internet breakout.

**AP-PT đơn giản của fileTiendat:** hai AP chỉ có SSID Guest và gửi frame untagged. CổngFa0/3 phải là **access VLAN100**, không phải trunk mặc địnhnativeVLAN1. Thêm AP Staff riêng trênFa0/4 accessVLAN120 nếu model không hỗ trợ haiSSID/802.1 Q; số AP đại diện này không thay số lượng AP sản xuất. Không gán WPA3/Enterprise/CAPWAP cho AP-PT khi chưa thấy hỗ trợ.

AP tham chiếu có uplink2,5 G nhưng baseline access48 P chỉ 1 G; đồng bộ [BOM](equipment-bom.md). Kiểm client thật nhận đúngVLAN/IP/DNS, guest→PC blocked với positiveInternet/DHCP/DNS, guest→guest isolation cùngSSID, staff có quyền và roaming nếu công cụ hỗ trợ. [TC05](../../test_results/TC05-guest-isolation/result.md)/[TC06](../../test_results/TC06-internet-web/result.md) chưa chạy; IPv4 ACL không tự chứng minh client isolationL2 hoặc RF coverage.
