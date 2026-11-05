# Nhật ký rà soát báo cáo

**TV5:** biên tập. **TV1:** duyệt cuối. **Trạng thái:** đã có PDF và QA kỹ thuật; phê duyệt học phần của người phụ trách còn PENDING.

| Ngày thực tế | Phiên bản / file | Người thực hiện | Mục | Nhận xét / hành động | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 26/10/2026 | Tài liệu/config TV1 trong workspace | Rà soát và hiệu chỉnh qua trợ lý theo yêu cầu người dùng | WAN/default/ISP/chi phí và evidence | Bổ sung tracking và Internet lab chung; đồng bộ trạng thái, bỏ kết quả CLI/RTT chưa có project; cần TV2/TV3/TV4 đọc chéo và test | ĐÃ SỬA TÀI LIỆU, CHƯA NGHIỆM THU |

Khi có PDF: ghi file/phiên bản/hash, ngày/reviewer thật, trang/mục, nhận xét, người sửa và kết quả. Không ghi review 19–20/11 hoặc APPROVED như sự kiện đã xảy ra khi chưa có sản phẩm/xác nhận.

## Rà soát source/tích hợp TV2 ngày 02/11/2026

Đã rà soát/cải thiện source TV2 vàđối chiếu toànrepo theo yêu cầu chủ repo; xem [review TV2](../00-management/tv2-review.md) và [reviewtoàn bộ](../00-management/project-review.md). Đây là trạng thái trước đợt hoàn thiện GNS3; PDF đã có trong cập nhật dưới đây. MergeGitHub là duyệtthay đổisource, không thayacademicapproval/runtime test.

## QA báo cáo sau GNS3 ngày02/11/2026

Đã xuất PDF từ Markdown/SVG và JSON evidence, render đủ10 trang; kiểm font Việt, bảng/hình/mục lục, ngắt trang và tràn lề. Đã sửa các chuỗi hash dài bằng ngắt dòng và tách bìa/mục lục. Đã đối chiếu209 kiểm tích hợp +137 kiểm sau reopen, hash native project và giới hạn mô hình. Đây là QA do trợ lý thực hiện theo yêu cầu chủ repo, không phải chữ ký cá nhân TV1/TV5. Hash sản phẩm cuối ở `submission/SHA256SUMS`; biên nhận BKeL chưa có.

## Bổ sung nguồn LaTeX và logo Bách Khoa ngày02/11/2026

Trước cập nhật này chỉ bàn giao Markdown/SVG và PDF, chưa giữ bộ LaTeX độc lập. Đã bổ sung [nguồn LaTeX](latex/README.md), [ZIP biên dịch độc lập](final/report-latex.zip), bìa có logo do người dùng cung cấp và `metadata.tex` để sửa thông tin nhóm. PDF mới có12 trang, font Việt, mục lục/số trang, bảng và sơ đồ vector. Đã render kiểm đủ12 trang và biên dịch ZIP bằng XeLaTeX/latexmk trong thư mục riêng; không còn overfull box hoặc thiếu glyph. [Bằng chứng QA và hash](../../test_results/report-latex/README.md). Giảng viên/lớp/MSSV chưa có dữ liệu xác nhận nên các trường này được để rỗng và tự ẩn trên bìa.

## Kiểm tính toàn vẹn ngày03/11/2026

`scripts/check_report.py` xác nhận toàn bộ hash trong QA khớp PDF12 trang, Markdown, LaTeX, hình và công cụ build; ZIP LaTeX chứa đúng các file nguồn hiện tại. Không sửa nội dung PDF hoặc biên dịch/render lại trong lần này. Đã sửa hồ sơ approval còn ghi10 trang thành12 trang. Thông tin giảng viên/lớp/thành viên/MSSV và phê duyệt TV1/TV5 vẫn chờ dữ liệu thật.

Yêu cầu bổ sung cả Packet Tracer và GNS3 được ghi trong quản lý/gói bàn giao. Ngày04/11 đã có native Packet Tracer58 node/53 cáp/sáu Wi-Fi và32 quan sát riêng, kèm lịch sử24 job có dây. Sáu BSSID/IP đã xác nhận; ba ping có mất gói đầu cần lặp lại, persistence đang chờ xác nhận IPC để mở file. Chưa đưa kết quả chưa nghiệm thu vào PDF12 trang đã QA; chi tiết ở [hồ sơ Packet Tracer](../../test_results/packet-tracer/README.md). Không đổi hash PDF hoặc nhận QA cũ là QA cho nội dung mới.


## Phụ lục Packet Tracer hoàn tất04/11/2026

[Phụ lục PDF hai trang](final/packet-tracer-validation.pdf) và [nguồn Markdown](source/packet-tracer-validation.md) bổ sung32 quan sát sau reopen, sáu Wi-Fi,19 DHCP client và bốn HTTP chọn ISP thủ công. Đã render/đọc cả hai trang, không tràn/chồng chữ; [QA/hash](../../test_results/packet-tracer/report-qa.json) riêng. PDF/LaTeX12 trang chính giữ nguyên QA/hash trước đó; không gọi QA cũ là QA của phụ lục mới. Nhóm vẫn cần điền/duyệt thông tin học phần thật.

## 04/11/2026 - Hoàn thiện thông tin L08, nhóm 2 và nội dung cuối

Theo thông tin nhóm trưởng, đã cập nhật danh sách năm thành viên/email và ghi BTL2 do Nguyễn Thành Đạt, Phạm Tiến Đạt thực hiện; ba người còn lại thực hiện BTL1. Bìa ghi hai người BTL2, nội dung mục 1.1 có đầy đủ danh sách. Giảng viên chưa cung cấp tên nên không điền suy đoán.

PDF chính hiện 13 trang, bổ sung Packet Tracer 32+4, sửa mô tả chưa thử/có dây, giữ riêng phạm vi GNS3 dual ISP/IDS-IPS. Nguồn VNPT và giới hạn giá dự toán/WAN mới được bổ sung. Đã render/đọc đủ13 trang; không overfull/missing glyph. ZIP LaTeX biên dịch độc lập bằng Tectonic, text khớp PDF. Phụ lục Packet Tracer hai trang cũng được cập nhật tên nhóm/người thực hiện và QA lại. Hash ở hồ sơ QA mới; các mục trước đây là lịch sử.

## 04/11/2026 - MPLS thực thi và nguồn giá WAN

Bổ sung mục5.3 MPLS L3VPN11node/10link; hai run28/28 trong Linux namespaces/QEMU, PCAP hai nhãn, route/control-plane và sự cố một đường DBP. GNS3 module sinh từ cùng nguồn nhưng chưa chạy native; baseline tổng vẫn giữ hash. Bảng cước VNPT Hải Phòng2020 chỉ là nguồn lịch sử, không gắn thành báo giáTP.HCM hiện hành. PDF13 trang được render/đọc toàn bộ, không overfull/missing glyph; ZIP LaTeX biên dịch độc lập exit0 và text khớp.

## Chốt bộ nộp ngày05/11/2026

Đã xác định `latex/report.pdf` cũ được tạo bằng pdfLaTeX nên mất tiếng Việt; backup bản lỗi local rồi bỏ khỏi vị trí nguồn. Báo cáo chính mới21 trang dùng XeLaTeX, font portable, `.latexmkrc` và recipe editor. ZIP LaTeX giải nén độc lập và build từ root/editor đều exit0, text khớp PDF; sai engine dừng sớm với thông báo rõ ràng. Đã render/kiểm đủ21 trang, không tràn dòng hoặc thiếu glyph; [QA/hash hiện tại](../../test_results/report-latex/README.md).

Thêm phụ lục IP/VLAN, transit/policy, BOM Main/Aux/quang/GPON, sơ đồ vật lý Main/Aux, demo và kiểm trực tiếp05/11. Giữ phụ lục Packet Tracer hai trang làm bản tra nhanh khác nội dung báo cáo chính. `.pkt` chính được trả về đúng byte của bản evidence32+4; bản Save lại chỉ khác đồng hồ/môi trường được backup local.

Sửa controller Docker PID/socket stale bằng exec-root mới mỗi boot và tự mở project closed. Đã chạy209 kiểm trực tiếp và137 sau restart controller, toàn bộ PASS; code/config52 node khớp source sau cả hai lần boot. [Bằng chứng mới](../../test_results/runtime/controller-restart/README.md) giữ source hash và output thực, không ghi đè JSON lịch sử. Cập nhật tài liệu trạng thái cũ, khóa hash, đóng gói lại và kiểm bản giải nén. Việc upload BKeL vẫn do nhóm thực hiện.
