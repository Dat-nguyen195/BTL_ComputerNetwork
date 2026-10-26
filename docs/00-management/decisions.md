# Sổ quyết định và giả định

**Cập nhật:** 26/10/2026. Phân biệt yêu cầu bắt buộc với baseline đề xuất; chưa có biên bản nhóm khóa thiết kế hoặc xác nhận tính năng mô phỏng.

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
| D11 | Leased Ethernet/Metro-E là phương án thiết kế; Serial2Mbps chỉ mô hình chức năng | Hai leased lines bắt buộc | Cần sizing/báo giá; TV1/TV4 |
| D12 | FTTH/DIA là phương án thay thế/nâng cấp, không tự thay hai xDSL | Hiệu chỉnh bám yêu cầu | Chưa được chấp thuận thay yêu cầu |
| D13 | TCO hiện tại là giả định minh họa, chưa có nguồn giá/thuế/SLA | Review chi phí | TV1 thu báo giá, TV2 đối chiếu BOM |
| D14 | Lab Main-FW chỉ định tuyến; TV3 cần firewall/policy/VPN thật; DMZ80 tại FW | Hợp đồng tích hợp | Cần TV2/TV3 xác nhận gateway và policy |

Mỗi quyết định được phê duyệt thực tế phải thêm ngày/người xác nhận, lý do, PR/commit, sản phẩm và test bị ảnh hưởng. Hiện bảng này ghi phương án chuẩn bị; không thay thế chữ ký reviewer hoặc kết quả test.
