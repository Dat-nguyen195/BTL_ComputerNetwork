# Kiểm thử bổ sung

TV4 điều phối, cập nhật 02/11/2026. Tất cả runtime NOT RUN; VPN/IDS/IPS chưa triển khai, giữ DESIGN ONLY.

- [SUPP-01 dual ISP](dual-isp-failover.md): PBR nhiều nguồn/phiên, lỗi local/upstream/both, default thu hồi/phục hồi và phiên cũ/mới.
- [SUPP-02 DHCP/DNS](dhcp-dns.md): DORA/renew,18 pool, DNS nhân viên/guest và positive control.
- [SUPP-03 VPN](vpn.md): SA/crypto/MTU/route/pool/quyền và thu hồi tài khoản.
- [SUPP-04 IDS/IPS](ids-ips.md): HTTP marker, alert/drop EVE và positive control.
- [SUPP-05 persistence](persistence.md): save/close/reopen, smoke6 nhóm và hash.

Các ca bổ sung không thay TC01–TC06. [Runbook](../../simulation/test-runbook.md) và [test matrix](../test-matrix.md) ghi nguồn/đích, expected và nguyên tắc evidence. Kiểm tĩnh ở thư mục `static/` là hồ sơ riêng.
