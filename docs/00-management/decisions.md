# Sổ quyết định và giả định

**Cập nhật:** 02/11/2026. Phân biệt yêu cầu bắt buộc với baseline đề xuất; chưa có biên bản nhóm khóa thiết kế hoặc xác nhận tính năng mô phỏng.

| ID | Nội dung | Căn cứ | Trạng thái / phụ trách |
| --- | --- | --- | --- |
| D01 | 5 thành viên, 4 tuần 26/10–22/11, dự phòng tới 06/12/2026 | Kế hoạch nhóm | Kế hoạch; TV1 |
| D02 | TV5 biên tập, TV1 duyệt cuối PDF và mô phỏng | Phân công | Kế hoạch |
| D03 | Hai leased lines, Internet ba site qua Main, hai xDSL | [A] tr.2 theo README | Bắt buộc |
| D04 | Main/DBP/BHTQ dùng 10.10/16, 10.20/16, 10.30/16; transit 10.255.0.0/24; VPN 10.255.100.0/24 | IP plan đề xuất | Có bảng; chờ TV2/TV3 đọc chéo |
| D05 | Packet Tracer dự kiến; GNS3 nếu cần tính năng | Step4 | Chưa thử model/phiên bản; TV4 |
| D06 | Tải server theo từng máy là kịch bản bảo thủ; giữ kịch bản tổng | [A] ghi total theo hồ sơ | Chờ xác nhận; TV4 |
| D07 | Khách đồng thời/ngày, camera, PACS, AP/BOM chưa đủ dữ liệu | Khảo sát chưa có | TV2/TV3/TV4/TV5 phối hợp |
| D08 | OSPF area0; passive mặc định; WAN cost10, Core–GW cost1 | Kiến trúc TV1 | Cấu hình tham chiếu, chưa chạy |
| D09 | Main-GW default track10 qua Web chung; /32 riêng giúp phục hồi | Hiệu chỉnh review | Chưa chạy runtime; TV1/TV4 |
| D10 | PBR theo nguồn, probe phía sau từng ISP, PAT đúng egress | Hiệu chỉnh review | Chưa chạy runtime; TV1/TV3/TV4 |
| D11 | Leased Ethernet/Metro-E là phương án thiết kế; Serial2 Mbps chỉ mô hình chức năng | Hai leased lines bắt buộc | Cần sizing/báo giá; TV1/TV4 |
| D12 | FTTH/DIA là phương án thay thế/nâng cấp, không tự thay hai xDSL | Hiệu chỉnh bám yêu cầu | Chưa được chấp thuận thay yêu cầu |
| D13 | TCO hiện tại là giả định minh họa, chưa có nguồn giá/thuế/SLA | Review chi phí | TV1 thu báo giá, TV2 đối chiếu BOM |
| D14 | Lab Main-FW chỉ định tuyến; TV3 cần firewall/policy/VPN thật; DMZ80 tại FW | Hợp đồng tích hợp | Cần TV2/TV3 xác nhận gateway và policy |

Mỗi quyết định được phê duyệt thực tế phải thêm ngày/người xác nhận, lý do, PR/commit, sản phẩm và test bị ảnh hưởng. Hiện bảng này ghi phương án chuẩn bị; không thay thế chữ ký reviewer hoặc kết quả test.

## Bổ sung thiết kế02/11/2026 (chưa ký duyệt nhóm)

| ID | Nội dung | Căn cứ / trạng thái |
| --- | --- | --- |
| D15 | ACL in ở Core/Aux vì east-west không qua Main-FW; FW dùng IOS ZBF | Có cấu hình hợp nhất/61 flow tĩnh; chưa runtime |
| D16 | Chỉ publish DMZ qua ISP2:8080, PBR DMZ ưu tiên ISP2 | Tránh reply sai ISP trong baseline; chưa inbound HA/runtime |
| D17 | Server10/2/2, Infra local DHCP/DNS,18 pool; guest DNS ngoài | Đã có inventory/pool; chưa lease/dịch vụ |
| D18 | Capacity script giữ3 scope server và unknown guest upload | Đã tái lập số học, chưa khảo sát/nghiệm thu sizing |
| D19 | VTI10.255.1.0/29 chỉ dự trù; pool teleworker10.255.100/24 chưa bật | Chưa cấp interface/route/crypto vào bản lab |
| D20 | Chưa có executable Packet Tracer/GNS3/IOS image; giữ runtime NOT RUN | Có precheck, runbook và gói tham chiếu; TV4 dựng môi trường |
