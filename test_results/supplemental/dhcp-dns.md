# SUPP02 - DHCP/DNS

**PASS trên GNS3 Linux/dnsmasq.** [Run sau reopen](../runtime/after-reopen-runtime/results.json) nhóm DHCP-DNS có76 kiểm:19 client x4 (IP/prefix, default gateway, DNS, DHCPACK). Có hai client cùng Main-V10 và một client trên mỗi pool còn lại, phủ đủ18 pool. Bảng cấp phát giữ100/120/500/244 giới hạn theo thiết kế, không trùng IP/gateway/server.

Actual lease/ACK do dhcrelay/dnsmasq/dhclient chạy thật, không điền tĩnh để gọi DHCP PASS. Captures cuối run lưu lease ba Infra. Chưa stress tối đa số client/lease hoặc mọi tình huống renew/expiry; IOS Services/relay cần kiểm riêng nếu chuyển nền tảng.
