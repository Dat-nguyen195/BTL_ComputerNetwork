\clearpage

# Phụ lục C - Kịch bản trình bày và phạm vi bằng chứng {.unnumbered}

## Trình tự demo sáu nhóm bắt buộc {.unnumbered}

1. **Cùng VLAN:** Main-PC10-A ping `10.10.10.11` và chiều ngược lại.
2. **Giữa VLAN:** Main-PC10-A ping `10.10.20.10`, mở HTTP HIS `10.10.70.11`.
3. **Liên site:** Main-PC10-A ping `10.20.10.10`, `10.30.10.10`; Aux ping ngược Main và traceroute liên site.
4. **DMZ:** PC được phép mở `http://10.10.80.10`; Web-Lab mở `http://198.51.100.2:8080`.
5. **Cách ly khách:** Guest truy cập Web-Lab thành công nhưng ping PC/mở HIS thất bại; đối chiếu bộ đếm ACL deny tăng.
6. **Internet:** PC/Guest cả ba site mở `http://web.hospital.test`; kiểm DNS và NAT tại Main.

## Chứng minh phần mở rộng {.unnumbered}

GNS3 là nền tảng demo **PBR hai nhóm, lỗi upstream ISP1/ISP2, mất cả hai và phục hồi**, cùng **Suricata IDS alert/IPS drop**. Dùng runbook `simulation/gns3/demo-guide.md` và bộ thử `scripts/test_gns3_runtime.py --failover`. Khi mất cả hai ISP, Internet mất nhưng liên lạc nội bộ liên site vẫn phải hoạt động. Phiên NAT cũ có thể mất; phép thử HTTP mới không chứng minh giữ nguyên phiên.

Packet Tracer đã có Wi-Fi thật trong lab: sáu association, DHCP và HTTP. ISP2 là đường chính, chuyển ISP1 bằng thao tác thủ công rồi trả lại cấu hình. Không gọi thao tác này là load balancing hay failover tự động. Dùng Packet Tracer 9.0.1.0858 và file `simulation/packet-tracer/hospital-3sites.pkt` đã đối chiếu provenance.

MPLS riêng chứng minh LDP/MP-BGP/VRF và gói hai nhãn qua PCAP trong Linux namespaces/QEMU. Không gán 28+28 quan sát đó cho project native GNS3 chưa chạy. VPN site-to-site/teleworker, GPON PHY, RF thực, HA chassis và tải đủ 1.120 PC là phạm vi thiết kế/chưa đo; trình bày đúng giới hạn này khi được hỏi.

## Chọn file nộp {.unnumbered}

**Báo cáo chính:** `docs/06-report/final/report.pdf`. **Nguồn LaTeX:** `docs/06-report/final/report-latex.zip`. PDF `packet-tracer-validation.pdf` là phụ lục kiểm thử ngắn hai trang, có nội dung khác báo cáo chính. Các PDF trong thư mục `build/` hoặc `output/pdf/` là sản phẩm biên dịch local.

Nộp kèm cả mô hình Packet Tracer, GNS3, source dựng image và bằng chứng qua gói `submission/hospital-network-delivery.zip`. Giải nén gói và kiểm trước khi dùng:

```bash
python3 scripts/verify.py
python3 scripts/package_submission.py --check
```

Máy demo GNS3 phải có image được build/load trên compute. Việc nộp BKeL và biên nhận do nhóm thực hiện.
