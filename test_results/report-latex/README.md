# QA báo cáo LaTeX và trang bìa

**02/11/2026. PASS kỹ thuật.** [PDF hiện tại](../../docs/06-report/final/report.pdf) có12 trang; [ZIP LaTeX](../../docs/06-report/final/report-latex.zip) chứa đủ nội dung, preamble/bìa/metadata và hai asset. [Hướng dẫn chỉnh sửa](../../docs/06-report/latex/README.md).

- Render đủ12 trang bằng Poppler và kiểm trực quan; xem [bìa đã render](cover.png).
- Logo trong source khớp SHA256 ảnh người dùng cung cấp; không vẽ lại hoặc thay logo.
- Biên dịch bằng XeLaTeX ba lượt; không có overfull box, thiếu glyph hoặc lệnh chưa định nghĩa.
- Giải nén ZIP vào thư mục riêng, dùng `latexmk -xelatex` biên dịch độc lập; không gọi Pandoc, script tạo báo cáo hoặc runtime GNS3. Toàn bộ text trích xuất khớp PDF bàn giao.
- Đối chiếu đủ bảy Step; phụ lục dùng209 kiểm sau sửa firewall và137 kiểm reopen lịch sử, nêu rõ phạm vi/thời điểm.

[qa.json](qa.json) lưu compiler, phạm vi kiểm, source/PDF/ZIP/logo SHA256. Đây là kiểm tra kỹ thuật do trợ lý thực hiện theo yêu cầu, không thay chữ ký duyệt học phần, dữ liệu giảng viên/lớp/MSSV hoặc biên nhận nộp BKeL. Chưa thực hiện biên dịch trên dịch vụ Overleaf.
