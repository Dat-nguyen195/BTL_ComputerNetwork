# Kiểm trực tiếp trước nộp ngày 05/11/2026

**PASS: 209/209 kiểm tích hợp và137/137 sau restart controller GNS3.** Đây là kiểm gói tin trực tiếp trên Linux/FRR/GNS3 2.2.55, không phải dự đoán từ cấu hình hoặc bằng chứng Cisco IOS.

- [Lượt đầy đủ](../submission-20261105/results.json), [tổng hợp](../submission-20261105/summary.json): sáu nhóm bắt buộc, OSPF,19 DHCP client/18 pool, DNS, IDS/IPS, PBR, lỗi upstream từng ISP/cả hai và phục hồi.
- [Lượt sau restart controller](../submission-reopen-20261105/results.json), [tổng hợp](../submission-reopen-20261105/summary.json):137 kiểm sáu nhóm, OSPF, DHCP/DNS và IDS/IPS.
- [Hai lần bật controller và hash](restart.json), [live hashes lần đầu](live-provenance-boot1.json), [live hashes sau restart](live-provenance.json):52 node started; code/config khớp nguồn; Docker và API hoạt động.

Lỗi đã sửa: dockerd/containerd lưu PID/socket qua stop/start khiến daemon hiểu nhầm PID tái sử dụng là tiến trình cũ. Entrypoint dùng exec-root mới mỗi lần bật và giữ `/var/lib/docker` trong volume riêng. Lệnh `gns3_lab.py start` tự mở project đang closed sau server restart. Controller hiện có được nạp entrypoint mới; image controller đã rebuild từ source để dùng cho lần bootstrap sau. Native project và code/config node giữ nguyên byte.

Phục hồi HTTP trên năm endpoint khi mất upstream ISP1/ISP2 lần lượt8,344s và5,178s. Samples gián đoạn được giữ trong JSON; không suy giữ nguyên phiên NAT hoặc SLA. Kiểm hiện tại không chạy lại Packet Tracer, MPLS, RF, GPON, VPN crypto hoặc workload y tế.

`check_gns3.py` kiểm hash source/bằng chứng mới, hai lần boot và kết quả209+137. Các evidence ngày02/11 được giữ nguyên tại thư mục lịch sử tương ứng, không ghi đè để đổi trạng thái.
