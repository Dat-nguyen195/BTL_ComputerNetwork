# Tình trạng TV1 sau hiệu chỉnh review

**Ngày:** 26/10/2026. **Trạng thái chung:** ĐÃ HIỆU CHỈNH THIẾT KẾ/CẤU HÌNH THAM CHIẾU, CHƯA NGHIỆM THU TRIỂN KHAI. Checklist task chính thức vẫn ở [tasks-assignment.md](../../tasks-assignment.md).

## Những điểm đã hiệu chỉnh

| Phát hiện review | Hiệu chỉnh bàn giao | Kiểm chứng còn cần |
| --- | --- | --- |
| PASS/APPROVED thiếu sản phẩm | Đưa test, hồ sơ duyệt, nhật ký và checklist về trạng thái thực; bỏ actual CLI/RTT chưa xác thực | Project/hash, ảnh/log runtime, xác nhận reviewer |
| Default OSPF không theo ISP | Main-GW có IP SLA10/track10, default có track; /32 Web độc lập giúp phục hồi | Tắt hai ISP, xem default ở GW/Aux và khôi phục |
| Probe chỉ tới gateway local | Đặt probe .11/.22 ở INET-Core, ghim /32 từng egress và Null0 fallback | Lỗi upstream khi cổng Edge vẫn up; chứng minh không probe vòng |
| Hai Web tách biệt | INET-Core chung, Web .100 duy nhất, route trả về public NAT qua hai ISP | HTTP cùng đích qua từng ISP; NAT và đường về |
| Kết luận 50/50/timer không có số đo | Mô tả đúng PBR theo nguồn, timer cấu hình và phiên PAT cũ/mới | Counter/số phiên/byte và timestamp thực |
| Giá/SLA không có nguồn | Ghi toàn bộ số tiền là giả định; bỏ cam kết giá/thuế/SLA không nguồn | Báo giá theo địa chỉ, SLA, model và ngày hiệu lực |
| FTTH thay yêu cầu xDSL | Tách mô hình chức năng hai ISP và phương án nâng cấp | Chấp thuận ngoại lệ nếu dùng thay yêu cầu gốc |
| Serial bị hiểu là 150Mbps | Serial2Mbps cho chức năng, explicit OSPF cost; sizing leased line riêng | Không dùng RTT/Serial chứng minh tải sản xuất |

Bổ sung thêm discard route cho các vùng site chưa cấp và route trả về Aux tại Core, nhằm ngăn vòng lặp default Core–FW/Core–GW. Chỉ static DMZ được redistribute vào OSPF. Đây là bảo vệ thiết kế; cần giữ khi TV2/TV3 tích hợp.

## Tiến độ theo nhóm task TV1

**Đã hoàn thành trọn vẹn 1/20 task chính:** W1-TV1-03 — thiết kế WAN/OSPF/default tập trung, sơ đồ, mapping, vai trò MPLS/SD-WAN và giới hạn mô phỏng đã có, đã rà soát logic/kiểm tĩnh. Đây là hoàn thành sản phẩm thiết kế, chưa phải nghiệm thu nhóm G1 hoặc PASS runtime. Checklist chính đã tích task này và các bước con thực sự hoàn thành của những task khác; 19 task chính còn lại mở theo đầu ra còn thiếu.

| Nhóm task | Đã chuẩn bị trong workspace | Điều kiện còn thiếu để đóng task |
| --- | --- | --- |
| W1-TV1-01 | Cấu trúc repo/template/checklist có sẵn, kế hoạch chi tiết | Tài khoản/quyền và milestone/issue thực tế chưa xác nhận |
| W1-TV1-02 | IP/VLSM và kiểm tĩnh subnet/sức chứa | TV2/TV3 đọc chéo, xác nhận dữ liệu và khóa baseline |
| W1-TV1-03 | **HOÀN THÀNH:** kiến trúc/sơ đồ WAN, OSPF/default, mapping, vai trò MPLS/SD-WAN và giới hạn; đã rà soát/kiểm tĩnh | Nghiệm thu G1 và triển khai/kiểm runtime được theo dõi ở task riêng |
| W1-TV1-04 | Bảng tải ISP, phương án WAN và chi phí giả định | TV4 xác nhận tải; hoàn tất danh mục dữ liệu/báo giá chờ có chủ trì/hạn |
| W1-TV1-05 | Danh mục tính năng cần thử và mẫu G1 | Thử model/phiên bản, quyết định công cụ và nghiệm thu nhóm |
| W2-TV1-01–05 | 9 config theo node, mapping, thứ tự nạp và thủ tục smoke test | Nạp IOS, project mở được, tích hợp TV2/TV3, log/biên bản G2 |
| W3-TV1-01–05 | Procedure TC03/TC06 và SUPP-01, contribution bản nháp | Actual/evidence, sửa/retest lỗi runtime, review G3 |
| W4-TV1-01–05 | Khung contribution/review/approval, lịch khóa/nộp | PDF và mô phỏng cuối, manifest/hash, review/duyệt và release đúng bản |

## Việc tiếp theo theo thứ tự

1. TV4 cùng TV1 thử feature support; chọn model/image/version và dựng lab theo [module WAN](../../simulation/modules/tv1-wan/README.md).
2. TV2/TV3 đọc chéo IP, gateway DMZ80, VLAN/trunk và firewall policy; ghép cấu hình trên node dùng chung. Routing stand-in chưa cô lập guest hoặc triển khai VPN.
3. Chạy TC03, TC06 và SUPP-01, thu log/ảnh và hash đúng bản; sửa/retest theo kết quả. Các ca TC01/02/04/05 vẫn do chủ trì tương ứng thực hiện.
4. TV1/TV2 thu báo giá, TV4 xác nhận tải ưu tiên khi một ISP còn hoạt động; ghi giả định còn lại thay vì chốt số liệu chưa có nguồn.
5. TV5 tổng hợp báo cáo khi nhận nội dung/bằng chứng; TV4 đóng gói; TV1 chỉ duyệt PDF/mô phỏng theo hash sau kiểm mở lại.

## Kiểm tra có thể chạy ngay

`python3 scripts/check_docs.py`: UTF-8, link, code fence, task ID. `python3 scripts/check_wan.py`: địa chỉ/route/track/PBR và các ca lỗi trong mô hình tĩnh đọc từ config. Script không kiểm IOS parser, trạng thái cổng/OSPF thật, NAT session, HTTP/DNS hoặc throughput; không được dùng output script thay PASS runtime. Kết quả chạy được báo lại trong lần bàn giao; không tạo số liệu mô phỏng.

## Kết quả kiểm tra workspace ngày 26/10/2026

- `python3 scripts/check_docs.py`: đạt kiểm tra UTF-8/link/fence/task ID trên **64 file Markdown**.
- `python3 scripts/check_wan.py`: đạt kiểm tra tĩnh **9 node**, **33 subnet VLAN/transit** và **9 tình huống** của mô hình route/track/PBR (bình thường, lỗi local/upstream, mất hai đường, phục hồi và Web health target hỏng).
- Đã thử trên các bản sao tạm: checker phát hiện đủ 5 lỗi cố tình đưa lại (default GW bỏ track, probe quay về gateway local, thiếu route trả về ISP2, thiếu đường ISP1 tới Internet chung, bỏ discard gây vòng lặp địa chỉ Main chưa cấp). Không sửa file làm việc trong các ca thử lỗi này.
- `git diff --check`: đạt sau sửa khoảng trắng. Workflow local đã bổ sung bước chạy checker WAN; chưa xác nhận một lần chạy CI trên GitHub.
- Các kết quả trên **chỉ là kiểm tra tĩnh**. Chưa chạy Cisco IOS/Packet Tracer/GNS3, chưa có project/hash hay bằng chứng runtime; TC03/TC06/SUPP-01 giữ NOT RUN, hồ sơ duyệt giữ PENDING.
