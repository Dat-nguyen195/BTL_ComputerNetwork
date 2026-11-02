# Nội dung TV4: tính tải, tích hợp và kiểm thử

**Cập nhật 02/11/2026. Đã có tính toán tái lập, gói cấu hình và hồ sơ test; chưa có project mô phỏng hoặc evidence runtime. TV5 biên tập; TV1 duyệt.**

## Đầu vào Step3 và các cách hiểu

1.120 workstation (600/260/260),14 server (10/2/2); PC500 MB down và 100 MB up/ngày; server1000/2000 MB với phạm vi total chưa xác nhận; khách 500 MB down nhưng chưa biết số thiết bị/ngày, đồng thời hay upload.80% dung lượng ngày trong 09–11 và 15–16, tổng 3 giờ; tăng trưởng **tổng 20% trong 5 năm**. Dùng MB thập phân. [Assumptions](../../03-capacity/assumptions.md) và [CSV đầu vào](../../03-capacity/capacity-inputs.csv) giữ nguồn/giả định.

Với kịch bản bảo thủ server mỗi máy, N khách/ngày:

```text
D_down = 574000 + 500N MB/day
D_up_known = 140000 MB/day
B_peak = D * 8 * 0.8 / 10800 Mbps
B_design = B_peak * 1.2 * (1 + overhead) / 0.70
```

70% utilization là giả định dư địa; overhead mặc định0 để tái lập baseline, không có nghĩa mạng thật không có overhead. Peak là trung bình cửa sổ3h, chưa bao gồm burst. Guest upload và camera/PACS/backup ngoài định mức vẫn chưa định lượng; không coi các phần này bằng 0.

| Phạm vi chưa có khách | Peak down/up Mbps | Design down/up Mbps |
| --- | --- | --- |
| Main | 183,70/47,41 | 314,92/81,27 |
| DBP | 78,22/17,78 | 134,10/30,48 |
| BHTQ | 78,22/17,78 | 134,10/30,48 |
| Tổng | 340,15/82,96 | 583,11/142,22 |

Nếu server là tổng hệ thống:569,90/115,81 Mbps design; tổng từng site571,94/119,87 Mbps. Mỗi khách/ngày thêm0,5079 Mbps design down; N=300 minh họa735,49 Mbps, thêm overhead10% thành 809,04 Mbps. Không tự phân bổ global total cho từng site nếu chưa có căn cứ. [throughput](../../03-capacity/throughput.md) có công thức, kịch bản ISP và hướng WAN.

## Phương án năng lực và Internet

Giả định toàn bộ định mức qua Internet để tạo envelope; cần đo tỷ lệ Internet riêng down/up, xác định giao dịch LAN/WAN và tránh cộng cùng giao dịch ở cả client/server. Mỗi Aux phải qua leased line để ra Main;134,10/30,48 Mbps chưa gồm workload riêng.150–200 Mbps leased line chỉ là điểm khảo sát, không nghiệm thu đủ PACS/backup.

Hai đường giả định500/500 Mbps đủ tổng phần đã biết khi cả hai tốt; chỉ một đường còn thiếu 83,11 Mbps down ở N=0, thiếu 235,49 Mbps nếu N=300 chưa overhead. Không khẳng định gói xDSL500/500 thực có sẵn. PBR theo nguồn tạo nhóm tải khác nhau, không bảo đảm50/50; một phiên không cộng tốc độ hai đường. Cần ưu tiên HIS/LIS/giao dịch và giảm guest/backup khi lỗi; chưa biết tải thiết yếu nên chưa chốt QoS Mbps hoặc SLA.

[capacity.py](../../../scripts/capacity.py) đọc CSV, hỗ trợ3 phạm vi server, guest per-device/global, upload khách, overhead, Internet shares. [calculated-baseline.csv](../../03-capacity/calculated-baseline.csv) là kết quả số học.6 nhóm unittest kiểm đơn vị/thời gian, phạm vi total, tăng trưởng, guest, overhead, shares và đầu vào lỗi. Đây không phải đo throughput thiết bị.

## Step4: gói tích hợp và giới hạn công cụ

Gói tham chiếu gồm 9 router IOS,5 switch lab,30 endpoint/mục đại diện,14 link cabling,18 DHCP pool và port map. Số server đúng 10/2/2; NVR appliance tách ứng dụng. Lab Main một switch không chứng minh đủ port/cáp/GPON cho600 PC; campus TV2 ghép riêng. Router/switch config đã có hash trong generated manifest; **đây chưa phải hash file mô phỏng**.

Môi trường hiện chưa có executable Packet Tracer/GNS3/Dynamips hoặc image IOS, nên chưa dựng/mở lại project, chưa xác nhận parser/feature. [Simulation README](../../../simulation/README.md) ghi thứ tự dựng/nạp, [capability matrix](../../../simulation/capability-matrix.md) liệt kê tính năng cần thử. Serial2 Mbps và Ethernet ISP chỉ mô hình chức năng; MPLS/SD-WAN/GPON/HA/VPN/IDS-IPS chưa triển khai. Không tạo `.pkt` hoặc `.gns3` giả.

## Step5: ma trận và bằng chứng

Đã soạn [TC01–TC06 + SUPP01–05](../../../test_results/test-matrix.md), [runbook](../../../simulation/test-runbook.md), expected cụ thể, nguồn/đích/cổng, positive/negative control, NAT PDU và cách ghi hash/actual. TC03 đủ Main↔cả hai Aux; TC05 lặp cả 3 guest và có DHCP/DNS/Web đối chứng; TC06 đủ PC/guest ở từng site. Tất cả runtime **NOT RUN**.

[verify.py](../../../scripts/verify.py) chạy kiểm Markdown, generated freshness,6 nhóm số học,9 tình huống WAN trên base và cấu hình hợp nhất,61 flow ACL, binding/zone/PAT, DHCP và inventory. [Log kiểm tĩnh](../../../test_results/static/README.md) không được dùng thay runtime evidence. Khi có mô phỏng, lưu actual từng nguồn, lỗi/retest, model/version và project hash; save/close/reopen trước bàn giao.

## Đánh giá và bàn giao

Rủi ro còn lại: chưa khảo sát khách/ứng dụng/PoE/RF; chưa có báo giá, image và feature support; single leased line từng Aux, thiết bị Core/FW/Edge đơn; ACL IPv4/stateless east-west; DMZ inbound chỉ ISP2. Các mốc nghiệm thu G1–G4, reviewer, PDF và mô phỏng cuối chưa ký. TV5 nhận phần tính tải/phương pháp triển khai/test và các bảng; ngày nhận/PR/reviewer chính thức chưa xác nhận.
