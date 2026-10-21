# VPN liên site và teleworker

**Chủ trì:** TV3; TV1 routing. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

- Site-to-site: đề xuất IPsec giữa Main và DBP/BHTQ trên hạ tầng IP WAN phù hợp, có subnet selector, route, NAT exemption và MTU được kiểm tra.
- Teleworker: kết thúc VPN tại Main, cấp pool riêng không overlap VLAN, xác thực và quyền truy cập theo vai trò.
- Không giả định chi nhánh có local Internet dự phòng; mọi Internet bình thường đi qua Main.
- Chưa chốt thuật toán, phiên bản phần mềm, pool và nền tảng. Mật khẩu/khóa thật không đưa vào Git.

| Luồng | Endpoint / pool | Xác thực | Quyền | Bằng chứng | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| Main↔DBP/BHTQ | Chờ thiết kế chi tiết | Chờ chọn | Theo ma trận | Chưa có | NOT RUN |
| Teleworker→Main | Chờ cấp pool riêng | Chờ chọn | Theo vai trò | Chưa có | NOT RUN |


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
