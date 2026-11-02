# Hồ sơ kiểm tra tĩnh TV1/TV3/TV4

**Ngày 02/11/2026. Đây là kết quả kiểm file/số học/mô hình tĩnh, không phải evidence Packet Tracer/GNS3/IOS.** TC01–TC06 và các ca runtime bổ sung giữ NOT RUN. Không có RTT, hội tụ OSPF thực, NAT session, HTTP response, DHCP lease, VPN SA hoặc EVE alert/drop trong bộ kiểm này.

Chạy từ repo root bằng Python3.10 trở lên:

```bash
python3 scripts/build_lab.py
python3 scripts/verify.py
```

Log của lần kiểm cuối: [verification.txt](verification.txt). Các thử cố tình đưa lỗi chỉ thực hiện trên bản sao tạm: [mutation-checks.txt](mutation-checks.txt); không sửa cấu hình làm việc để tạo kết quả.

| Kiểm tra | Phạm vi |
| --- | --- |
| check_docs.py | UTF-8, link local, code fence, task ID |
| build_lab.py --check | File sinh ra khớp source;9 router +5 switch lab,18 pool, port map/manifest |
| test_capacity.py |6 nhóm số học: MB/3 h,20%, scope server, khách/unknown upload, overhead/shares, tổng site và input lỗi |
| check_wan.py |9 node,33 subnet, khai báo OSPF/PBR/NAT/track và 9 tình huống trong mô hình routing tĩnh |
| check_wan.py --config-dir simulation/generated/configs | Cùng hợp đồng WAN sau ghép security; không kiểm session ZBF |
| check_security.py | [61 flow](security-cases.csv), first-match ACL, binding/hướng,18 pool, zone/policy/PAT contracts |
| build_campus.py --check / check_lan.py |3 sitebudget/PoE/storage,72 uplink,2 drawio/SVG,3 adapter3650/2960,37 flowMainACL vàhashbinary TV2; vẫnNOT RUN |
| check_inventory.py |14 link,30 endpoint, địa chỉ/gateway/port không trùng, server10/2/2 và mapping switch |

Nguồn authoritative của rule là [security policy](../../docs/04-security/security-policy.md); source cấu hình tại `configs/`, `scripts/build_lab.py`, `simulation/lab/`. Generated manifest chỉ hash cấu hình/bảng tham chiếu; không thay project hash. Sau sửa source, build lại rồi verify; chỉ runtime trên project có version/hash mới cho kết luận sáu nhóm test bắt buộc.

Sau tích hợp TV2: chạy `python3 scripts/build_campus.py` sau `build_lab.py`;`verify.py` kiểmcảbảnROAS vàadapterSVI. Filebinarygốccóthật nhưng chỉMain mộtphần; khônglấyhash/kiểmcấu trúc làmPASS runtime.
