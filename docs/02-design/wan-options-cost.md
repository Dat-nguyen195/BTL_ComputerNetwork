# So sánh WAN, định cỡ hai ISP và dự toán chi phí

**Chủ trì:** TV1; TV4 cung cấp tải, TV2 cung cấp BOM. **Cập nhật:** 02/11/2026. **Trạng thái:** THIẾT KẾ ĐỀ XUẤT / CHƯA CÓ BÁO GIÁ HOẶC KIỂM CHỨNG NĂNG LỰC.

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
| MPLS L3VPN ba site | Nhà mạng cung cấp L3VPN và VRF, thuận tiện mở thêm site | Chốt PE/CE và handoff; không mặc định mã hóa payload; đã có module MPLS Linux riêng | Ba access port/cước, QoS, CPE, hỗ trợ |
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

Baseline chức năng giữ hai leased lines và OSPF; MPLS đã có module/evidence thực thi riêng; SD-WAN và VPN crypto còn ở mức thiết kế. Mã hóa là một biện pháp bảo vệ, không tự chứng minh tuân thủ toàn bộ yêu cầu pháp lý/vận hành bệnh viện.

## 6. Bổ sung đối chiếu TV4 và dữ liệu chờ

Tính tải được tái lập bằng `python3 scripts/capacity.py`;3 scope server, tải khách, overhead và shares được giữ riêng. [Throughput](../03-capacity/throughput.md) có bảng2×100/20,2×500/500,2×750/250 Mbps giả định và khoảng thiếu khi còn một ISP. Tổng đủ chưa bảo đảm từng nhóm PBR đủ: chưa khách, nhóm1 khoảng 294,60/77,21, nhóm2 288,51/65,02 Mbps; khách Main/BHTQ dồn nhóm2. Không chốt gói dịch vụ từ các số ví dụ.

| Dữ liệu chờ | Chủ trì | Hạn đề xuất | Cần ghi nhận |
| --- | --- | --- | --- |
| Phạm vi total server/khách, số khách và tải thiết yếu | TV4/TV5 |05/11/2026 | Dữ liệu khảo sát, down/up, LAN/WAN/Internet, cách tránh đếm trùng |
| Báo giá/SLA hai leased lines và hai xDSL | TV1 |08/11/2026 | Địa chỉ, ngày/hiệu lực, down/up hiệu dụng, cước/thuế, IP public/handoff/CPE |
| BOM/CAPEX/license có bị tính trùng | TV2 + TV3 |08/11/2026 | Model, throughput khi inspect/crypto, support/license/PoE/quang |
| Tải khi chỉ một ISP, QoS/downgrade | TV1 + TV4 |08/11/2026 | Mức HIS/LIS tối thiểu, guest/backup giảm bao nhiêu; chưa gán tỷ lệ ưu tiên giả |

Các hạn là đề xuất xử lý, chưa phải cam kết của reviewer. Hai ISP không tạo dự phòng leased line/Core/FW/Edge. DMZ inbound hiện chỉ ISP2:8080 và gián đoạn khi ISP2 mất; tính sẵn sàng dịch vụ công bố phải đánh giá riêng outbound failover.

## 7. Nguồn dịch vụ đối chiếu và căn cứ chọn phương án

Đối chiếu ngày 04/11/2026: [VNPT - Kênh thuê riêng](https://vnpt.vn/doanh-nghiep/san-pham-dich-vu/kenh-thue-rieng/) mô tả dịch vụ kết nối các địa điểm cố định, hỗ trợ handoff Ethernet và hướng dẫn liên hệ đơn vị kinh doanh để có chi tiết. Trang này là nguồn xác nhận loại dịch vụ, không phải báo giá cho bệnh viện hoặc xác nhận khả dụng tại ba địa chỉ. Vì vậy các giá trong mục 4 vẫn là giả định minh họa có nhãn; chưa thể thay bằng giá thương mại được xác thực.

[VNPT - Dịch vụ Mạng riêng ảo](https://vnpt.vn/doanh-nghiep/san-pham-dich-vu/dich-vu-mang-rieng-ao-vpn/) phân biệt Metronet là MPLS VPN lớp 2 và Megawan là MPLS VPN lớp 3. Vì vậy Metro-E/leased Ethernet chỉ mô tả handoff của baseline; không tự suy ra underlay nhà mạng hoặc gọi mô hình OSPF là đã chạy MPLS. Nguồn đọc ngày 04/11/2026; báo giá ba điểm vẫn cần nhà cung cấp xác nhận.

## 8. Bảng cước công khai có nguồn và giới hạn sử dụng

Nguồn kiểm ngày 04/11/2026: [VNPT Hải Phòng - Báo giá TSL Metronet](https://vnpthaiphong.vn/SiteFolders/Root/2345/B%C3%A1o%20gi%C3%A1%20d%E1%BB%8Bch%20v%E1%BB%A5%20TSL%20Metronet.pdf), tài liệu một trang ghi năm **2020**, ngày/tháng để trống. Đây là tham khảo lịch sử tại Hải Phòng, không phải bảng giá hiện hành TP.HCM.

| Tốc độ | Nội hạt, VNĐ/điểm theo tài liệu | Phạm vi sử dụng trong bài |
| --- | ---: | --- |
| 20 Mbps | 10.557.000 | Tham chiếu lịch sử, thấp hơn nhu cầu Aux đã tính |
| 50 Mbps | 19.077.000 | Tham chiếu lịch sử, thấp hơn nhu cầu Aux đã tính |
| 100 Mbps | 31.343.000 | Tham chiếu lịch sử, vẫn thấp hơn envelope Aux 134,10 Mbps down |

Tài liệu ghi giá theo điểm kết nối, thời hạn tối thiểu 24 tháng và chưa gồm VAT 10% tại thời điểm tài liệu. Không tự áp mức thuế đó cho hợp đồng hiện tại. Không nội suy giá 150–200 Mbps hoặc coi phí một điểm là phí toàn bộ ba site. Bảng TCO mục 4 tiếp tục là kịch bản giả định, không lấy các con số cũ này để gắn nhãn báo giá mới.

Để chốt chi phí triển khai cần nhà cung cấp xác nhận ba địa chỉ, hai nhánh/ba điểm, băng thông và SLA, công nghệ/handoff, IP public, CPE/license, phí khởi tạo, thuế và hiệu lực. Dự án học thuật đã có phương án/công thức/phân tích chi phí có nguồn; giá hợp đồng theo địa chỉ là đầu việc thương mại bên ngoài mô phỏng.

## Trạng thái mô phỏng hiện tại

Hai leased line routed và OSPF được mô phỏng trên Cisco Packet Tracer. MPLS/SD-WAN là lựa chọn WAN so sánh và tính chi phí, chưa có provider overlay trong native. Hai ISP chỉ kiểm chọn/khôi phục thủ công; PBR/probe/failover tự động chưa nghiệm thu.
