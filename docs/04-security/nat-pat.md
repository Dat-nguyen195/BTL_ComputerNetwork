# NAT/PAT và kiểm chứng địa chỉ

**Chủ trì:** TV3; TV1 phối hợp dual ISP. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

 và hiệu chỉnh tài liệu Multi-site

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

NAT Internet tại Main cho cả 3 site; không PAT liên LAN/WAN nội bộ/VPN. Hai egress phải có route/NAT nhất quán với chiều về. DMZ static PAT chỉ mở cổng công bố. Ghi inside/outside, ACL chọn nguồn NAT, rule firewall và địa chỉ/cổng trước/sau NAT. Chưa có mapping chạy thực tế.


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
