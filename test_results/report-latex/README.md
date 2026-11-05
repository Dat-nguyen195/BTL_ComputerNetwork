# QA báo cáo và bộ LaTeX ngày05/11/2026

**PASS kỹ thuật bản21 trang.** [PDF chính](../../docs/06-report/final/report.pdf) gồm bảy Step, phụ lục A-G, IP/VLAN, BOM, sơ đồ vật lý Main/Aux, demo và kết quả GNS3 mới209+137. [Phụ lục Packet Tracer hai trang](../../docs/06-report/final/packet-tracer-validation.pdf) có nội dung khác và QA độc lập.

- Build bằng Pandoc3.1.3 và XeLaTeX/TeX Live2023 trên Linux; ba lượt cập nhật mục lục. Font TeX Gyre Termes/Heros và DejaVu Sans Mono; không cần font Microsoft.
- Đã sửa compiler từ pdfLaTeX sang XeLaTeX qua magic comment, `.latexmkrc` và recipe LaTeX Workshop. Chạy nhầm pdfLaTeX dừng sớm với thông báo rõ ràng thay vì hàng loạt lỗi Unicode.
- ZIP LaTeX cuối được giải nén sang thư mục độc lập và chạy `latexmk report.tex`: exit0, text toàn bộ PDF khớp bản nộp. Build từ root/editor cũng exit0 và text khớp.
- Không có overfull hbox/vbox, missing character hoặc undefined control sequence trong ba log biên dịch thành công.
- Poppler render đủ21 trang ở1500px; kiểm trực quan bìa, mục lục một trang, bảng/email, sơ đồ, trang ngang và phụ lục. Sau chỉnh thứ tự chọn font, render cuối có raster hash giống toàn bộ21 trang đã kiểm.

[qa.json](qa.json) giữ hash đúng PDF, ZIP nguồn, LaTeX, Markdown, hình, cấu hình editor và bằng chứng runtime dùng trong báo cáo. [Ảnh bìa](cover.png); contact sheets: [trang1-6](pages-1.jpg), [7-12](pages-2.jpg), [13-18](pages-3.jpg), [19-21](pages-4.jpg). Ảnh render từng trang và các thư mục biên dịch/giải nén tạm đã được dọn sau khi QA; có thể render lại từ PDF chính.

QA trước04/11 được giữ trong [history](history/qa-2026-11-04-before-finalization.json). Bản PDF local lỗi và `.pkt` resave không thuộc bản nộp; các backup tạm này đã được xoá trong lần dọn dự án theo yêu cầu chủ workspace. QA này không tạo phê duyệt học phần hoặc biên nhận BKeL.
