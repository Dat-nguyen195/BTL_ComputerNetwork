# Kiểm khả năng nền tảng trước khi dựng

**TV4; 02/11/2026. PRECHECK môi trường đã thực hiện; feature support chưa thử.** Không tìm thấy PacketTracer/packettracer/gns3/dynamips qua PATH; chưa có model/image/version được khóa. Docker hiện có không chứng minh tương thích IOS hoặc tạo được `.pkt`.

| Tính năng | Điểm kiểm trên node/model được chọn | Nếu thiếu | Trạng thái |
| --- | --- | --- | --- |
| OSPF/point-to-point/passive | Core, Main-GW, Aux; neighbor/route | Đổi model hoặc GNS3 image hợp pháp | NOT CHECKED |
| IP SLA/track/delay | Edge SLA1/2; Core/GW SLA10 | Không thay bằng static default rồi gọi failover đạt | NOT CHECKED |
| PBR verify-availability | Edge; hai thứ tự next hop/track | Ghi BLOCKED nếu không hỗ trợ | NOT CHECKED |
| NAT route-map/match interface | Edge; PAT hai egress và session | Kiểm egress/translation thật, không chỉ CLI accept | NOT CHECKED |
| Static PAT + ZBF | Edge + FW; HTTP outside→DMZ và reply ISP2 | Không dùng ACL NAT thay firewall | NOT CHECKED |
| IOS ZBF inspect/drop log | Main-FW; class-map/policy-map/zone-pair | Dùng môi trường có stateful FW; ghi giới hạn bản PT | NOT CHECKED |
| DHCP relay/Services DNS | Core/Aux + Infra; DORA, renew, DNS UDP/TCP | Tách lỗi client/service/ACL | NOT CHECKED |
| Selective static redistribution | Core chỉ DMZ80 | Tránh redistribute default/static rộng | NOT CHECKED |
| VLAN trunk/access | 2960; Main exclude80, correct ports | TV2 merge và kiểm model thật | NOT CHECKED |
| VTI/IKEv2/remote access | Thiết bị và client có quyền dùng | Giữ DESIGN ONLY đến có crypto evidence | DESIGN ONLY |
| Suricata IDS/IPS | Sensor/inline riêng, rule -T, EVE | Không ghi ACL là IDS/IPS | DESIGN ONLY |

Mẫu ghi: ngày/người thử, tên công cụ, version, node/model/image (không commit image có license), lệnh nhận/bị từ chối, log/ảnh, cách xử lý và test bị ảnh hưởng. Chốt công cụ sau thử thực tế, không ký G1 chỉ từ bảng này.
