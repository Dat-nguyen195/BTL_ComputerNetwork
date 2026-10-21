# Thiết bị và đặc tính tối thiểu

**Chủ trì:** TV2. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

### 7.1. Khảo sát và BOM

TV5 chủ trì checklist khảo sát: sơ đồ phòng/tầng, mật độ người dùng theo phòng ban, vị trí phòng trung tâm cách A/B 50 m, tuyến cáp thực tế, rack/patch panel/IDF, điện/UPS/tiếp địa/làm mát, chống cháy, đường ống và mỹ quan; nguồn điện PoE; nhiễu/suy hao RF, vật cản, vùng đông khách; camera, vùng riêng tư, thời gian lưu; SLA/băng thông/upload/public IP của ISP; yêu cầu HIS/RIS-PACS/LIS/CRM, backup, RTO/RPO và quyền truy cập. Chưa khảo sát thực địa thì ghi **giả định/chưa xác nhận**, không tạo kết quả đo giả.

TV2 lập BOM với cột **site, số lượng, model hoặc đặc tính tối thiểu, port/speed, PoE budget, uplink, quang/SFP, license, công suất, chi phí nguồn và ngày lấy giá**. Bao gồm router WAN, Internet edge/load balancer, firewall, core/distribution/access, OLT/splitter/ONT nếu dùng GPON, AP/controller, switch DMZ/server, patch panel, rack, cáp đồng/quang, UPS và camera/NVR. IDS/IPS là thiết bị hoặc chức năng có throughput khi bật kiểm tra, không chỉ tốc độ interface.

Các mốc **12 thiết bị Main và ≥5 thiết bị mỗi Aux** là quy mô tham chiếu của đề, không phải giới hạn trên. Chỉ xét port 48 cổng cho workstation, không tính uplink/AP/camera/server: Main cần tối thiểu **13 switch cho 600 PC**, **15 cho 720 PC**; mỗi Aux cần **6 cho 260 PC**, **7 cho 312 PC**. Vị trí theo tầng và dự phòng port có thể làm số switch cao hơn. Với GPON, phải tính lại port OLT, tỉ lệ chia, ONT và số cổng phía người dùng; không dùng phép chia 48 cổng để đại diện cho GPON.

Số AP phải dựa trên vùng phủ, dung lượng và khảo sát RF; số camera dựa trên góc nhìn, bitrate, PoE và lưu trữ. Không suy ra số AP/camera từ số phòng một cách máy móc. Kèm bảng port budget cho hiện tại và 5 năm; đối chiếu server Main tổng 10 và mỗi Aux tổng 2, không cộng thêm DMZ như server ngoài đề mà không ghi giả định.



## Bảng BOM cần hoàn thiện

| Site | Nhóm thiết bị | Số lượng | Model/spec | Port/uplink/PoE | License | Đơn giá/thuế | Nguồn/ngày | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main | Core/access/WAN/firewall/AP/quang | Chờ sizing | Chờ chọn | Chờ tính | Chờ xác nhận | Chưa báo giá | Chưa có | OPEN |
| DBP/BHTQ | LAN/WAN/AP/quang | Tính riêng từng site | Chờ chọn | Chờ tính | Chờ xác nhận | Chưa báo giá | Chưa có | OPEN |


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
