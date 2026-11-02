# NAT/PAT và kiểm chứng địa chỉ

**Chủ trì:** TV3; TV1 phối hợp dual ISP. **Cập nhật:** 02/11/2026. **Trạng thái:** CÓ CẤU HÌNH THAM CHIẾU / CHƯA KIỂM IOS RUNTIME.

## Tham khảo và hiệu chỉnh tài liệu Multi-site

[R] là nguồn tham khảo được mô tả trong README; file hiện không có trong workspace nên chưa kiểm lại trực tiếp nội dung/trang của [R]. Bảng dưới giữ ghi chú của dự án, không coi là bằng chứng đã đọc lại nguồn gốc.

[R] tr.2-7 minh họa DHCP, router inside/outside, PAT overload, static TCP port mapping và kiểm tra bằng `show ip nat statistics`, `show ip nat translations`, `show access-lists`. [R] tr.8-11 yêu cầu quan sát địa chỉ/cổng ở PC, gateway nguồn, router trung gian, gateway đích và server. TV3/TV4 áp dụng cách kiểm chứng này cho TC04/TC06 và viết chú thích ảnh trước/sau NAT.

| Nội dung trong [R] | Cách dùng trong dự án |
| --- | --- |
| LTK `192.168.110.0/24`, server `.5`, gateway `.1`; DiAn `192.168.120.0/24`, server `.5`, gateway `.1` | Ví dụ học tập; đổi sang bảng IP 3 site ở mục 5, không thay quy mô bệnh viện bằng 2 campus |
| DHCP start `.100`, max 100 user, mask `/24` ở mỗi site | Minh họa cách cấp DHCP; dự án dùng pool theo subnet và sức chứa đã tính, không giữ pool 100 cho site 260/600 máy |
| DHCP gateway DiAn ở bảng tr.3 ghi `192.168.110.1` | Không khớp subnet DiAn; khi tái hiện lab phải dùng `192.168.120.1`, khi triển khai dự án dùng gateway trong bảng IP tương ứng |
| Transit `172.28.16.0/30`, `172.28.18.0/30` được gọi “public” | Đây là địa chỉ private trong dải `172.16.0.0/12`; chỉ coi là WAN lab, không khẳng định là IP Internet công cộng |
| `172.28.16.1:1111 → 192.168.110.5:80`; `172.28.18.2:2222 → 192.168.120.5:80` | Là static PAT/port forwarding, không phải NAT 1:1 toàn bộ địa chỉ; chứng minh bằng HTTP và translation table |
| OSPF process `6000`, area `0` | Process ID cục bộ; bổ sung quảng bá route LAN/VLAN và default theo thiết kế, không chỉ chép hai network transit |
| Có cả `ip nat inside source static tcp` và `ip nat outside source static tcp` | Không sao chép cặp lệnh một cách mặc định; xác định loại NAT, nền tảng và chiều gói, kiểm tra bằng translation thực tế; ánh xạ DMZ thông thường được thiết kế từ rule inside-source static phù hợp |
| Gọi NAT tại gateway của mỗi campus | Dự án điều chỉnh thành NAT Internet tại Main, giữ route liên site; chỉ tái hiện hai NAT gateway trong lab tham khảo tách riêng nếu cần |

## Baseline bệnh viện

Main-Edge G0/0 `10.255.0.18` là **inside**; G0/1 `203.0.113.2` và G0/2 `198.51.100.2` là **outside**. Main-FW không NAT. ACL100 loại luồng 10/8→10/8 trước khi chọn nguồn ba site. Route-map NAT-ISP1/NAT-ISP2 chọn interface thực ra; PBR không áp sang mạng 10/8. Không bật NAT ở Aux.

| Luồng ví dụ | Trước Edge | Sau Edge / đường trả lời |
| --- | --- | --- |
| Main-PC10→Web | 10.10.10.10:p → 192.0.2.100:80 | 203.0.113.2:q → Web:80 nếu ISP1 tốt |
| BHTQ-PC10→Web | 10.30.10.10:p → Web:80 | 198.51.100.2:q → Web:80 nếu ISP2 tốt |
| Internet→WebDMZ | 192.0.2.100:p → 198.51.100.2:8080 | Web:p → 10.10.80.10:80; trả về ISP2 và đổi source thành public:8080 |
| Main↔Aux | IP riêng nguồn → IP riêng đích | Giữ nguyên source/destination; không NAT |

`p/q` là biến cổng, không phải cổng đo được. Lấy giá trị thật từ translation/PDU khi chạy. [Cisco NAT](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr3-fwd/nat/nat-configuration-guide/nat.html) mô tả mapping theo protocol, inside local IP/port và global IP/port. Cấu hình trong [overlay Edge](../../configs/security/main-edge-dmz.inc):

```ios
ip nat inside source static tcp 10.10.80.10 80 198.51.100.2 8080 extendable
```

**Chỉ công bố ISP2.** DMZ80 thuộc nhóm PBR ưu tiên ISP2 nên đường trả lời bình thường cùng egress. Nếu thêm mapping ISP1 mà vẫn PBR theo nguồn, phản hồi phiên vào ISP1 có thể đi sai ISP. Khi ISP2 hỏng, Web công bố bị gián đoạn; chưa có inbound HA. Outbound có thể failover; phiên cũ vẫn có thể đứt. HA inbound cần thêm thiết kế DNS/địa chỉ công bố và routing theo phiên, rồi kiểm riêng.

FW nhận packet **sau DNAT** từ Edge nên OUTSIDE→DMZ match `10.10.80.10:80`, không match public:8080. Static PAT tạo ánh xạ; firewall mới cho quyền qua vùng. Main-ProxyDMZ .11, DB .70.15 và SSH không được công bố. Nội bộ dùng `portal.hospital.test → 10.10.80.10`; không dựa vào NAT hairpin. Guest không được phép mở public:8080 theo ACL hiện tại.

VPN pool thuộc 10/8 nên được loại NAT khi đích cũng 10/8; điều đó chưa triển khai VPN. Route về pool, termination, crypto và quyền nằm ở [VPN plan](vpn-plan.md). Không thêm public mapping UDP500/4500 hoặc permit pool trong baseline chưa có VPN.

Kiểm runtime: Edge `show ip nat statistics`, `show ip nat translations`, `show route-map`, `show track`; FW `show policy-map type inspect zone-pair sessions`; route hai chiều và HTTP client. Kiểm cùng đích qua mỗi ISP, không NAT nội bộ và dịch vụ không công bố bị chặn. Bảng NAT không thay kết quả ứng dụng.


## Theo dõi cập nhật

- [x] Đã có mapping cụ thể và cấu hình hợp nhất cho baseline.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
