# Nguồn cấu hình security TV3

`main-fw-policy.inc`: IOS ZBF trên Main-FW sau routing reference, không phải ASA config. `main-edge-dmz.inc`: static PAT ISP2 và tắt dịch vụ Web quản trị. ACL nguồn/DHCP relay tại Core/Aux được tạo từ `scripts/build_lab.py` để đồng bộ prefix/pool ba site.

Chạy `python3 scripts/build_lab.py` từ repo root; nạp file hợp nhất tại [simulation/generated/configs](../../simulation/generated/configs/) và đọc [module TV3](../../simulation/modules/tv3-security/README.md). Mỗi file cuối có một hostname và một `end`. Không nạp overlay vào node khác, không nạp lại base WAN sau cùng.

Đây là config tham chiếu chưa qua IOS parser/runtime. [Security policy](../../docs/04-security/security-policy.md) ghi quyền, hướng ACL, giới hạn established/self-zone/L2/IPv6. [NAT plan](../../docs/04-security/nat-pat.md) ghi tính đối xứng ISP2 và giới hạn inbound HA. Không chứa account/key vận hành; VPN/IDS/IPS chưa cấu hình.
