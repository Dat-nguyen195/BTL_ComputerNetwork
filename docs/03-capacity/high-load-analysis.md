# Khu vực tải cao và nguy cơ nghẽn

Cập nhật 13/11/2026. Phân tích thiết kế phục vụ Step 1, kết hợp phép tính Step 3; chưa đo tải sản xuất và không có lượt runtime mới trong cập nhật tài liệu này.

## Yêu cầu trong đặc tả

Trang 3, Step 1 yêu cầu: “Define areas with high load (network load) to select the appropriate device configuration (load balancers are placed in necessary locations)”. Step 3 yêu cầu tính throughput, băng thông ISP và đề xuất cấu hình. Do đó cần chỉ ra vùng tập trung tải, căn cứ chọn năng lực và vị trí cân bằng tải khi cần; đề không quy định phải tạo nghẽn, đo throughput hoặc triển khai mọi loại load balancer trong demo.

Mục 1.2 báo cáo nhận diện vùng cần khảo sát; mục 3.4 tổng hợp phân tích; mục 2.2/2.8/3.2/3.3 trình bày lựa chọn thiết bị, video và WAN/ISP. Không dùng điểm lỗi đơn (SPOF) thay cho điểm nghẽn: sự cố thiết bị và thiếu năng lực có thể xảy ra độc lập.

## Phương pháp

1. Xác định nguồn–đích và đoạn mạng thực sự đi qua; tách LAN, WAN và Internet.
2. Tính từng chiều ở cùng điều kiện tải, có tăng trưởng/dư địa được ghi rõ; không cộng down+up để so với tốc độ full duplex một chiều.
3. So tải với năng lực **hiệu dụng** của link, CPU/IPS, phiên, airtime hoặc IOPS, xét cả lúc bình thường và lúc một tuyến lỗi.
4. Nếu tải chưa được khảo sát, ghi nguy cơ và phép đo cần làm; không gán “đã nghẽn” hoặc “đã đủ tải”.

## Vị trí, căn cứ và phương án

| Vùng | Căn cứ tính/đường đi | Nguy cơ và quyết định thiết kế | Điều kiện cần kiểm |
| --- | --- | --- | --- |
| Internet Edge và firewall Main | Internet ba site tập trung tại Main; envelope không khách `583,11/142,22 Mbps`, theo [baseline CSV](calculated-baseline.csv) | Một ISP 500 Mbps không đủ envelope down khi tuyến kia lỗi; dùng PBR/probe hai ISP, kiểm tải theo egress, QoS và Guest khi lỗi | Băng thông từng chiều, queue/drop, CPU, throughput khi bật IPS/NAT, phiên; xác nhận tỷ lệ tải thật ra ISP |
| WAN Aux–Main | Mỗi Aux `134,10/30,48 Mbps` theo envelope phần đã biết; HIS/PACS tới Main còn dùng WAN nhưng không ra ISP | 150–200 Mbps đối xứng là điểm bắt đầu lấy báo giá, không là cam kết đủ PACS/backup; dời bulk/backup, ưu tiên giao dịch | Main→Aux và Aux→Main, profile PACS, latency/loss, tải khi dịch vụ đồng thời; serial 2 Mbps trong lab chỉ thử định tuyến |
| Server Farm/PACS | Nhiều VLAN/site tới HIS/PACS/DB; chưa có số phiên, profile ảnh hoặc IOPS thực | Farm 10 GbE/core 40 GbE theo BOM; khả năng nghẽn có thể nằm ở ứng dụng/đĩa thay vì link; LB ứng dụng chỉ hợp lý khi có nhiều backend tương thích | Thời gian đáp ứng, CPU/RAM, NIC, IOPS, số phiên, session và khả năng chia sẻ dữ liệu |
| Uplink access tầng | 48×1 GbE chia sẻ **một uplink 10 GbE đang hoạt động**, tỷ lệ năng lực cổng danh nghĩa `48/10 = 4,8:1` | Đây là tỷ lệ oversubscription, không phải dự đoán tải; dùng 10G, phân bố tải và tuyến dự phòng; hai đường vật lý không tự có 20G usable | Utilization/queue/drop ở uplink; STP/LACP và năng lực khi mất một link. Chỉ khi ghép hai 10G thật sự hoạt động mới có tối đa 20G tổng, tỷ lệ 2,4:1; một flow vẫn chịu giới hạn một member |
| Wi-Fi sảnh/chờ khám | Vùng đông người là giả định cần khảo sát; AP 2,5G nhưng access baseline 1G | Ethernet 1G là trần cần xét, airtime/nhiễu/client đồng thời cũng có thể giới hạn; RF survey, thêm AP/kênh, nâng mGig/PoE khi cần | Client đồng thời, channel utilization, retry, RSSI/SNR, airtime và tải Ethernet; không suy từ số khách/ngày |
| Camera/NVR cùng site | Thiết kế Main 40→50 camera ×4 Mbps =160→200 Mbps; mỗi Aux 8→10 =32→40 Mbps | Ghi cục bộ nên không cộng toàn bộ video vào WAN; lựa chọn kênh/ingest/NIC/đĩa theo [camera-plan](../02-design/camera-plan.md) | Ghi đồng thời, phát lại/export, dung lượng usable và thời gian lưu; 14 webcam IoT không tạo bằng chứng lưu video |

## Vị trí cân bằng tải và phạm vi triển khai

## Phép tính và nguồn kiểm

- Tải/độ nhạy: công cụ local `scripts/capacity.py`, [đầu vào](capacity-inputs.csv), [throughput](throughput.md), [baseline](calculated-baseline.csv).
- Với baseline down `583,111111 Mbps`, tuyến còn 500 Mbps thiếu `83,111111 Mbps`; đây là kịch bản giả định tuyến, không là gói ISP đã xác thực.
- Với 300 khách và overhead 10%, design down `809,041270 Mbps`; tuyến 750 Mbps khi lỗi thiếu ít nhất `59,041270 Mbps`, chưa kể upload khách và workload chưa biết.
- Với số thiết bị đã làm tròn sau 5 năm (1.344 PC/18 server), `584,13/144,25 Mbps` được tính trực tiếp với U=70%; không nhân 1,2 thêm lần nữa. Kịch bản server tổng toàn viện/từng site giữ nguyên trong throughput.md.
- Phép tính tham khảo `187000 × 0,8 / 10800` cho `13,8518519 MB/s`; đổi sang Mbps và tăng 20% được `132,9777778 Mbps`. Calculator của nhóm dùng dữ liệu và giả định riêng từ đặc tả, không thay bằng số của bài tham khảo.

Các con số không thay đổi mô hình `.pkt`, cấu hình PBR hoặc log runtime. Nghiệm thu năng lực cần profile đồng thời đủ tải, đo ở đúng vùng và thử lỗi; ping/HTTP thành công không chứng minh không nghẽn.

PBR/probe chỉ là thiết kế; Packet Tracer giữ bằng chứng chọn ISP thủ công. LB ứng dụng chưa có cụm backend để kiểm.
