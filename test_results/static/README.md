# Hồ sơ kiểm tra tĩnh TV1/TV3/TV4

**Bản chốt05/11/2026:** [log verify hiện tại](verification-2026-11-05.txt) kiểm đủ nguồn, bằng chứng controller restart209+137, Packet Tracer32+4 và QA báo cáo21 trang. Mạng GNS3 đã chạy trực tiếp riêng; checker offline không thay lần chạy mạng. Các log cũ bên dưới được giữ theo thời điểm.

**Lần kiểm Windows mới nhất04/11/2026:** toàn bộ `verify.py` đạt, gồm7 hồi quy đọc kết quả Packet Tracer và checker bằng chứng32 lượt sau reopen/bốn HTTP ISP thủ công. Đây là đối chiếu dữ liệu đã lưu, không chạy mạng trong checker. [Log](verification-windows.txt), [môi trường/hash](windows-review.json), [evidence Packet Tracer](../packet-tracer/README.md) và [QA phụ lục2 trang](../packet-tracer/report-qa.json) tách rõ từng phạm vi. Các ghi nhận02–03/11 bên dưới là lịch sử.

**Ngày 02/11/2026. Đây là kết quả kiểm file/số học/mô hình tĩnh, không phải evidence Packet Tracer/GNS3/IOS.** [Runtime GNS3](../runtime/README.md) đã có evidence riêng; checker này không tự sinh PASS runtime. Không có RTT, hội tụ OSPF thực, NAT session, HTTP response, DHCP lease, VPN SA hoặc EVE alert/drop trong bộ kiểm này.

Chạy từ repo root bằng Python3.10 trở lên:

```bash
python3 scripts/build_lab.py
python3 scripts/verify.py
```

Log của lần kiểm cuối: [verification.txt](verification.txt). Các thử cố tình đưa lỗi chỉ thực hiện trên bản sao tạm: [mutation-checks.txt](mutation-checks.txt); không sửa cấu hình làm việc để tạo kết quả.

## Kiểm trên Windows ngày03/11/2026

[Log Windows](verification-windows.txt) và [môi trường/hash đầu vào](windows-review.json) ghi lần kiểm offline mới. Đã sửa việc đọc tiếng Việt bằng code page ANSI, đường dẫn `\\` trong manifest GNS3 và ghi file LF/UTF-8. File runtime/GNS3 giữ nguyên byte so với bản đã có evidence. Các kiểm tra mới gồm đủ100 task ở checklist/bảng đối chiếu, assembly kit Packet Tracer, toàn vẹn PDF/ZIP LaTeX và6 ca hồi quy đóng gói. Không có mạng mô phỏng nào được chạy trong bộ kiểm này.

Từ root repo trên Windows:

```powershell
powershell -File scripts/check.ps1
# Khi muốn cập nhật ứng viên ZIP sau khi sửa source:
powershell -File scripts/check.ps1 -Package
```

Script tìm Python trong `.venv`, runtime Codex đã cài hoặc PATH; không tự cài Python. Python3.10+ là đủ cho bộ kiểm offline. CI đã cấu hình Windows/Linux; chưa có lần chạy GitHub của thay đổi này được xác nhận trong workspace.

`test_delivery.py` kiểm round-trip ZIP với văn bản UTF-8, từ chối checksum rỗng/thiếu và ZIP bị đổi dữ liệu, kiểm bản giải nén không có Git/ZIP gốc; đồng thời so từng hash sản phẩm sinh GNS3 với manifest runtime lịch sử. `check_report.py` kiểm hash và bản nguồn trong ZIP LaTeX khớp lần QA báo cáo chính đã lưu; không render hoặc compile PDF mới. `package_submission.py --check` yêu cầu danh sách checksum đầy đủ, không chỉ kiểm các dòng tình cờ có trong file. Sau giải nén, lệnh này kiểm các file bằng manifest và checksum nội bộ; `verify.py` cũng chạy được khi không có `.git`.

| Kiểm tra | Phạm vi |
| --- | --- |
| check_docs.py | UTF-8, link local, code fence, task ID |
| build_lab.py --check | File sinh ra khớp source;9 router +5 switch lab,18 pool, port map/manifest |
| test_capacity.py |6 nhóm số học: MB/3 h,20%, scope server, khách/unknown upload, overhead/shares, tổng site và input lỗi |
| check_wan.py |9 node,33 subnet, khai báo OSPF/PBR/NAT/track và 9 tình huống trong mô hình routing tĩnh |
| check_wan.py --config-dir simulation/generated/configs | Cùng hợp đồng WAN sau ghép security; không kiểm session ZBF |
| check_security.py | [61 flow](security-cases.csv), first-match ACL, binding/hướng,18 pool, zone/policy/PAT contracts |
| build_campus.py --check / check_lan.py |3 sitebudget/PoE/storage,72 uplink,2 drawio/SVG,3 adapter3650/2960,37 flowMainACL vàhashbinary TV2; vẫnNOT RUN |
| check_inventory.py |14 link,38 endpoint, địa chỉ/gateway/port không trùng, server10/2/2 và mapping switch |

Nguồn authoritative của rule là [security policy](../../docs/04-security/security-policy.md); source cấu hình tại `configs/`, `scripts/build_lab.py`, `simulation/lab/`. Generated manifest chỉ hash cấu hình/bảng tham chiếu; không thay project hash. Sau sửa source, build lại rồi verify; chỉ runtime trên project có version/hash mới cho kết luận sáu nhóm test bắt buộc.

Sau tích hợp TV2: chạy `python3 scripts/build_campus.py` sau `build_lab.py`;`verify.py` kiểmcảbảnROAS vàadapterSVI. Filebinarygốccóthật nhưng chỉMain mộtphần; khônglấyhash/kiểmcấu trúc làmPASS runtime.

`build_gns3.py --check` kiểm native project/config còn khớp nguồn; `check_gns3.py` đối chiếu52 node/52 link,18 pool, source/live hash, JSON evidence đã chạy và PCAP. `package_submission.py --check` kiểm ZIP/checksum riêng, không chạy mạng.

## MPLS bổ sung cuối04/11

Bộ verify hiện có `build_mpls.py --check`, bốn regression chống evidence sai/hỏng và `check_mpls.py`. Đã đối chiếu hai run28/28, source hash và PCAP có hai nhãn thật; đây là kiểm lại [evidence runtime](../mpls/README.md) đã chạy trong Linux/QEMU, không phải chạy mạng từ checker. PDF chính đã cập nhật MPLS; bản chốt05/11 bổ sung các phụ lục thiết kế và QA lại.
