# So sánh WAN, định cỡ hai ISP và dự toán chi phí

**Chủ trì:** TV1; TV4 cung cấp tải, TV2 cung cấp BOM. **Cập nhật:** 26/10/2026. **Trạng thái:** THIẾT KẾ ĐỀ XUẤT / CHƯA CÓ BÁO GIÁ HOẶC KIỂM CHỨNG NĂNG LỰC.

## 1. Đầu vào định cỡ

Theo kịch bản bảo thủ trong [throughput.md](../03-capacity/throughput.md), giả sử các tải đã cho đi qua Internet, chưa tính khách và tải bổ sung:

| Phạm vi | Design down Mbps | Design up Mbps |
| --- | --- | --- |
| Main | 314,92 | 81,27 |
| DBP | 134,10 | 30,48 |
| BHTQ | 134,10 | 30,48 |
| Internet tập trung | 583,11 | 142,22 |

Các số là kết quả tính từ giả định, không phải tải đo; không suy ra toàn bộ nhu cầu PACS/HIS/camera từ chúng. TV4 cần tách LAN/WAN/Internet và tải giao dịch nội bộ để tránh cộng trùng.

- Leased line mỗi Aux: dự trù mức 150–200 Mbps đối xứng để khảo sát, chưa khẳng định đủ PACS/backup/VPN overhead.
- Hai ISP: tổng nhu cầu tối thiểu theo kịch bản hiện tại khoảng 583,11/142,22 Mbps; thêm khách, overhead và tải chưa biết trước lựa chọn gói.
- Ví dụ thiết kế **hai đường 500/500 Mbps**, là giả định năng lực để so sánh: bình thường tổng lý thuyết 1.000/1.000 Mbps nhưng một phiên không cộng hai đường. Khi chỉ một đường còn, thiếu ít nhất **83,11 Mbps down** so với baseline chưa có khách. Phải có ma trận ưu tiên/downgrade dịch vụ; chưa xác nhận tải thiết yếu đủ chạy trong 500 Mbps.
- Nếu cần giữ đầy đủ tải khi hỏng một đường, mỗi đường cần đáp ứng toàn bộ nhu cầu được chốt. Kiểm cả up/down, SLA, đường vật lý, thiết bị NAT/crypto, phiên đồng thời và tải từng nhóm PBR; tổng băng thông đủ không bảo đảm từng egress không nghẽn.

## 2. Bảo toàn yêu cầu hai xDSL

[A] tr.2 yêu cầu hai xDSL có load balancing, Internet ba site qua Main. Lab IOS dùng hai cổng Ethernet làm **mô hình chức năng hai ISP**, không mô phỏng đồng bộ DSL, tốc độ hoặc chất lượng đường đồng. Không tuyên bố mô hình Ethernet đã kiểm xDSL thực tế.

FTTH/DIA là phương án thay thế/nâng cấp đề xuất khi hồ sơ dịch vụ xDSL không đáp ứng tải. Cần ghi chấp thuận thay đổi yêu cầu trước khi dùng thay baseline. Chưa chọn VNPT/Viettel/gói thương mại cụ thể; ISP1/ISP2 là tên node lab, TEST-NET không phải địa chỉ public nhà mạng cấp thật.

## 3. So sánh công nghệ

| Phương án | Vai trò/ưu điểm | Điều kiện và giới hạn | Khoản cần báo giá |
| --- | --- | --- | --- |
| 2 Metro-E/leased Ethernet P2P | Bám hai kết nối Main–Aux; chạy routed OSPF nếu handoff hỗ trợ | Mỗi nhánh một tuyến, chưa có dự phòng; SLA/độ trễ theo hợp đồng | Hòa mạng, hai kênh, CPE/quang, SLA, bảo trì |
| MPLS L3VPN ba site | Nhà mạng cung cấp L3VPN và VRF, thuận tiện mở thêm site | Chốt PE/CE và handoff; không mặc định mã hóa payload; chưa triển khai trong lab | Ba access port/cước, QoS, CPE, hỗ trợ |
| SD-WAN trên leased/MPLS | Chính sách ứng dụng, quản lý overlay tập trung | Cần controller, edge, license và underlay; không gọi OSPF/PBR là triển khai SD-WAN | Thiết bị, license/controller, underlay và vận hành |
| IPsec trên hai leased lines | Đề xuất mã hóa lưu lượng liên site | TV3 chốt crypto, MTU/MSS, khóa và route; overhead/CPU phải kiểm, chưa có số đo | Crypto/license, hai kênh, bảo trì |

Không đặt số latency, jitter, uptime, MTTR hay overhead cố định khi chưa có nguồn/hợp đồng/benchmark cùng điều kiện. Giữ cùng phạm vi site, băng thông, SLA và thuế khi so chi phí. Hai ISP không dự phòng cho lỗi Edge/Core/FW hoặc leased line từng nhánh.

## 4. Bảng TCO minh họa bằng giả định

**Toàn bộ số tiền dưới đây là GIẢ ĐỊNH DỰ TOÁN để kiểm công thức, không phải giá thị trường hoặc báo giá của nhà mạng.** Nguồn giá: chưa có. VAT và khoản đã bao gồm: chưa xác nhận; không tự áp một mức thuế. Chưa dùng số này để phê duyệt mua hàng/chốt lựa chọn thương mại. Quy đổi và thay toàn bộ bảng khi có báo giá theo cùng cơ sở thuế.

`TCO 5 năm = CAPEX + 60 × OPEX tháng + bảo trì/định kỳ chưa nằm trong OPEX`.

| Hạng mục (VNĐ, giả định) | Metro-E | MPLS | SD-WAN + leased underlay | IPsec + leased |
| --- | --- | --- | --- | --- |
| Hòa mạng | 15.000.000 | 18.000.000 | 15.000.000 | 15.000.000 |
| Router/edge | 120.000.000 | 120.000.000 | 180.000.000 | 140.000.000 |
| Quang/SFP/ODF | 20.000.000 | 20.000.000 | 20.000.000 | 20.000.000 |
| Tổng CAPEX | 155.000.000 | 158.000.000 | 215.000.000 | 175.000.000 |
| Hai leased lines/tháng | 22.000.000 | 0 | 22.000.000 | 22.000.000 |
| MPLS ba site/tháng | 0 | 25.500.000 | 0 | 0 |
| Hai Internet/tháng | 3.500.000 | 3.500.000 | 3.500.000 | 3.500.000 |
| License/tháng | 0 | 0 | 4.500.000 | 0 |
| Tổng OPEX/tháng | 25.500.000 | 29.000.000 | 30.000.000 | 25.500.000 |
| OPEX 60 tháng | 1.530.000.000 | 1.740.000.000 | 1.800.000.000 | 1.530.000.000 |
| Bảo trì 5 năm | 60.000.000 | 50.000.000 | 90.000.000 | 70.000.000 |
| **TCO minh họa** | **1.745.000.000** | **1.948.000.000** | **2.105.000.000** | **1.775.000.000** |

Khoảng chênh IPsec–Metro-E là 30 triệu **trong mô hình giả định này**, gồm 20 triệu thiết bị và 10 triệu bảo trì, không phải chỉ phần cứng. BOM/router/module, thiết bị TV2/TV3 và phí quang có thể trùng giữa các bảng; phải đối soát trước tổng hợp TCO dự án. Chưa kết luận một phương án thực tế rẻ nhất.

Báo giá cần: địa chỉ ba site, tốc độ down/up nội địa/quốc tế và mức cam kết, SLA/MTTR, IP tĩnh, handoff, CPE/license, phí lắp đặt, thời hạn hợp đồng, VAT, hỗ trợ và điều kiện tăng giá; ghi tài liệu/link, ngày và hiệu lực. TV1 theo dõi thu nhận, TV2 đối chiếu BOM, TV4 xác nhận năng lực. Chưa có tài liệu báo giá trong workspace.

## 5. Cơ chế dual ISP được bàn giao

Chi tiết tại [architecture.md](architecture.md) và [module WAN](../../simulation/modules/tv1-wan/README.md). PBR phân nhóm nguồn, failover theo track, PAT theo egress; không bảo đảm 50/50. Probe dùng đích phía sau ISP và /32 ghim đường; Main-GW theo dõi Web chung để điều khiển default OSPF. Các timer là cấu hình dự kiến, thời gian hội tụ và hành vi phiên cũ phải đo trong [test dual ISP](../../test_results/supplemental/dual-isp-failover.md), hiện NOT RUN.

Baseline chức năng giữ hai leased lines và OSPF; MPLS/SD-WAN và VPN chỉ ở mức thiết kế đến khi có triển khai/bằng chứng tương ứng. Mã hóa là một biện pháp bảo vệ, không tự chứng minh tuân thủ toàn bộ yêu cầu pháp lý/vận hành bệnh viện.
