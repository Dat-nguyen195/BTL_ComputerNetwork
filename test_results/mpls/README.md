# Bằng chứng MPLS L3VPN thực thi

Ngày 04/11/2026: **28/28 PASS** trong [validated](validated/results.json), sau xóa/dựng lại **28/28 PASS** trong [recreated](recreated/results.json). Môi trường thực: Linux namespaces trong QEMU/WHPX trên Windows, Alpine3.22.7/kernel6.12.114-lts, FRR10.2.2. Đây là kiểm MPLS bổ sung, không phải chạy lại mạng GNS3 tổng hoặc Packet Tracer.

- Sáu ping hai chiều giữa ba LAN, ba HTTP từ Main/DBP/BHTQ qua PAT198.51.100.2 tại Main.
- MP-BGP hai peer mỗi PE, ba prefix VPN/VRF ở mỗi PE, LDP một peer mỗi PE và ba peer ở P.
- P không có route khách; ping từ provider vào LAN thất bại có sáu ca khách liên lạc thành công làm đối chứng.
- Tắt link DBP làm DBP mất kết nối; Main–BHTQ vẫn thông; bật lại DBP phục hồi. Đây là kiểm giới hạn một tuyến, không tuyên bố có dự phòng MPLS.
- [PCAP validated](validated/mpls.pcap) có7 frame MPLS, [PCAP recreated](recreated/mpls.pcap) có6 frame; có gói ICMP DBP→Main với hai nhãn transport/VPN và gói trả lời. Checker phân tích EtherType0x8847, stack nhãn và IP bên trong, không chỉ tìm chữ MPLS trong log.

[Mã/module/runbook](../../simulation/mpls/README.md), [provenance/hash](provenance.json). Chạy `python scripts/check_mpls.py` để kiểm evidence đã lưu; lệnh không chạy mạng.

[Lượt đầu](initial/initial.json) giữ19/25 đạt: HTTP server lỗi do tên hàm trùng tên module, ba lệnh show BGP chưa đủ cú pháp. [PCAP đầu](initial/mpls.pcap) đã có lưu lượng nhãn thật. Sau sửa, hai lượt28/28 đạt. [Lỗi quyền khởi tạo](history/initial-privilege-failure.txt) cũng được giữ. Không chuyển kết quả lỗi đầu thành PASS.

Project GNS3 riêng được sinh từ cùng specification, có11 nút/10 liên kết. Chưa mở/chạy project MPLS mới bằng GNS3; không dùng evidence namespace để ghi GNS3-runtime PASS. Mô hình GNS3 tổng cũ vẫn có hồ sơ runtime riêng. MPLS không mã hóa, không thay VPN IPsec, SD-WAN controller, SLA nhà mạng hoặc benchmark tải.
