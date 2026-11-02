> Hồ sơ lịch sử trước đợt hoàn thiện GNS3. Trạng thái hiện tại xem [review mới](project-review.md).

# Review toàn bộ dự án sau tích hợp TV2

**02/11/2026. Phạm vi: source, thiết kế, cấu hình, script, sơ đồ, module Packet Tracer, hồ sơ test và đóng gói.** Review theo yêu cầu chủ repo; không thay nghiệm thu học phần hoặc chữ ký TV1/TV5. Tiendat được giữ lịch sử commit`3f52588`; phần TV1/TV3/TV4 trước đó lưu riêng`39fab95`. File `.pkt` gốc giữ nguyên byte, audit/hash tại [module TV2](../../simulation/modules/tv2-lan-wireless/README.md).

**Kết luận:** có thể merge bản sửa source/thiết kế/module để nhóm tiếp tục tích hợp; **chưa sẵn sàng nộp bài hoặc xác nhận đạt Step4–5/7**. Tài liệu/code không có lỗi chặn kiểm tĩnh đã biết sau sửa, nhưng chưa có mô phỏng tổng 3 site, runtime evidence sáu nhóm và PDF cuối.

## Phát hiện và trạng thái

| ID /mức | Vấn đề | Đã xử lý /trạng thái | Phụ trách tiếp |
| --- | --- | --- | --- |
| F01/P1 | TC01 PASS/ngày tương lai, hình/log không có trong nhánh TV2 | Đã gỡ khỏi tài liệu quy trình; TC01 NOT RUN, không dùng ngày hạn làm actual | TV2/TV4 chạy thật |
| F02/P1 | Native `.pkt` là Main một phần:10 node, không Aux/WAN/FW/server,4 PC chưa IP/gateway, startup3 switch trống | Đã audit, giữ hash/byte gốc; thêm3 adapter sửa và hướng dẫn; bản binary chưa được sửa/runtime | TV4+TV1/TV2/TV3 |
| F03/P1 | AP-PT untagged trên trunk native1; PC port2 tại switchB saiVLAN | Adapter sửa APGuest access100/Staff access120, PC10/20; cần nạp bản sao | TV2/TV4 |
| F04/P1 | Lọc tại Main-FW không thấy east-west; native MLS không có guestACL | Có ACL gateway/SVI và ZBF đúng vị trí;37 flowMain giữ nguyên trênadapter; runtime NOT RUN | TV3/TV4 |
| F05/P1 | Sơ đồ WAN nốiFW lệch transitCore; switchDMZ có nguy cơ bridgeCore | Đã đồng bộ WAN→Core, VLAN80 chỉFW, switchDMZ riêng; diagram/adapter kiểm tĩnh | TV1/TV2 |
| F06/P1 | NAT công bố DMZ qua hai ISP có thể reply sai egress | Baseline chỉISP2:8080 và PBR DMZ ưu tiênISP2; inboundHA chưa có | TV1/TV3 |
| F07/P2 | Nhầm LACP với hai core độc lập/HA, sợi quang với sốlink | Đã tách RSTP độc lập và điều kiện logicalswitch;72 link có port/tuyến; diversity thực chưa khảo sát | TV2/TV5 |
| F08/P2 | PoE model sai, budget thiếu NVR/tăng trưởng AP-camera/WLC, bitrate NVR lệch | Đã sửa bằng nguồnCisco và script: Main810/960, Aux334/384;56 AP; usableNVR5 năm85.050/17.010 GB | TV2/TV3 xác nhận dữ liệu |
| F09/P2 | GPON trong đề chưa thực hiện, bị ghi như đã duyệt bỏ | Đã ghi gap rõ, thêm OLT/ODN/ONT/OS2/budget; vẫn DESIGN ONLY/chờ xác nhận giảng viên | TV1/TV2 |
| F10/P2 | 583,11/142,22 Mbps là envelope giả định, chưa biết server scope/guest/upload/Internet share | Script giữ 3 scope server, unknown và độ nhạy; chưa đủ chọn gói xDSL/leased line/throughput thật | TV4/TV5/TV1 |
| F11/P2 | HA, VPN, IDS/IPS, WLC/AAA, phishing, RF/roaming/L2 guest isolation chưa có runtime | Thiết kế/giới hạn đã nêu; requirement kỹ sư tài năng phải xác nhận; ACL không thay IDS/IPS | TV3/TV2/TV4 |
| F12/P2 | PDF/source báo cáo tổng, evidence và approval/hash cuối chưa có | Có4 contribution, runbook, evaluation thiết kế và manifest tham chiếu; final approval PENDING | TV5/TV4/TV1 |

## Đối chiếu bảy Step

| Step /điểm | Bằng chứng hiện có | Còn thiếu để nghiệm thu |
| --- | --- | --- |
| 1/1 | Yêu cầu3 site, checklist khảo sát, kiến trúc/phân vùng, wireless plan | Khảo sát thực/RF/workload và xác nhận phạm vi GPON |
| 2/1 | IP/VLSM33 subnet, BOM/campusbudget/cabling72 link, drawio/SVG, WAN/TCO giả định | Giá/model/license/handoff và review sizing trên dữ liệu thật |
| 3/1 | Script CSV,6 nhóm kiểm số học, down/up/growth/scopes/overhead/shares | Chốt phạm vi total/khách/tải thiết yếu; đo và báo giáISP |
| 4/2 | Module native Main có thật;9 router+5 switch tổng tham chiếu,3 adapter TV2, mapping | File tổng 3 site mở lại được, thử CLI/feature/version/model, ghép LAN/server/WAN/security |
| 5/2 | TC01–06/SUPP01–05 procedure,61 flowACL/9 WANfaultscenario tĩnh | Actual/ảnh/log/projecthash từng ca; sáu nhóm runtime đều NOT RUN |
| 6/2 | [Đánh giá thiết kế](../05-evaluation/evaluation.md), rủi ro/SPOF/5 năm và giới hạn | Kết luận từ runtime, đa dạng phần mềm/license, restore/HA thực |
| 7/1 | Cấu trúc submission, manifest config, tiêu chí duyệt | PDF+nguồn tổng, project cuối, evidence, checksum cặp cuối, ký duyệt và BKeL receipt |

Không tự quy đổi số lượng tài liệu/kiểm tĩnh thành điểm môn học. Module native gốc không chứng minh link chức năng, throughput hoặc packet-loss/RTT; SVG QA không phải ảnh chạy mô phỏng.

## Kiểm chứng bản sửa

`python3 scripts/build_lab.py`, `python3 scripts/build_campus.py`, `python3 scripts/verify.py`, `git diff --check`. Log tại [verification.txt](../../test_results/static/verification.txt);5 lỗi thử trên bản sao của security checker đã có [mutation log](../../test_results/static/mutation-checks.txt). PipelineCI thực hiện lại các kiểm tĩnh; kiểm branch/merge GitHub không thay G1–G4.

Review cấu hình: OSPF passive/ID/default/route về không đổi khi ghép TV2; adapter3650 chuyểnGi1/0/23/24 thànhroutedport và đặtACL trênSVI; không cóSVI80, không gatewaytrùngROAS nếu làm đúng hướng dẫn. Cấu hình tham chiếu không có secret vận hành; XMLuserprofile không được đưa vào repo. Original `.pkt` không repack; SHA256 khớp snapshotaudit và blobGit của commitTiendat. Native startup/reopen/compatibility vẫn cần công cụ thực.

## Ưu tiên xử lý sau merge

1. **TV4 trước 04/11:** mở bản sao module bằng môi trường tương thích metadata9.0.0.0810; thử feature, sửa IP/port/startup và ghép đủ 3 site. Không ghi đè bản gốc.
2. **TV1/TV2/TV3 phối hợp05–08/11:** chốt mapping/gateway, Infra/DHCP/DNS, ZBF/NAT, SSID; khảo sát/quote; GPON và chương trình nâng cao cần xác nhận rõ. Các hạn này là đề xuất, chưa phải cam kết của thành viên.
3. **TV4 và chủ trì trướcG3:** chạy6 nhóm cùng các ca failover/persistence, lưu actual/hash/ảnh/log, sửa rồi retest ca bị ảnh hưởng. Chỉ chuyển PASS khi có bằng chứng.
4. **TV5/TV1 trướcG4:** tổng hợp PDF/nguồn từ4 contribution và phần TV5, cập nhật evaluation theo runtime; duyệt riêng PDF/project đúng hash, đóng gói và nộp đúng bản.

Không có điều kiện nào ở trên được đánh dấu đạt chỉ vì đã merge `main`. [Review TV2](tv2-review.md) có chi tiết thay đổi của phầnTiendat; [trạng thái TV1/TV3/TV4](tv1-tv3-tv4-status.md) giữ các dependency đã có.
