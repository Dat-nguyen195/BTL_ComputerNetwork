# QA báo cáo mở rộng ngày 09/11/2026

Cập nhật mới nhất: bản 47 trang, không còn phụ lục tách riêng, có 10 sơ đồ Cisco19 và kết quả từng nhóm TC01–TC06. Gói LaTeX cuối đã biên dịch độc lập và so văn bản khớp PDF. Đã render đủ 47 trang ở 45 dpi, kiểm contact sheets; log không có overfull hoặc missing character. Các thông tin 40 trang/65 dpi bên dưới là lần QA trước; `qa.json` và ảnh expanded-pages-* đã cập nhật theo bản 47 trang.

**PASS kỹ thuật bản 40 trang.** [PDF chính](../../docs/06-report/final/report.pdf) gồm bốn chương, đối chiếu bảy Step và phụ lục A-G; tham khảo bố cục nhóm 3, giữ dữ liệu nhóm 2.

- Pandoc và XeLaTeX/MiKTeX trên Windows, ba lượt cập nhật mục lục. Tái sử dụng PDF vector vì SVG không đổi. Font mã lệnh ưu tiên Consolas trên Windows, có font dự phòng.
- ZIP cuối giải nén độc lập và biên dịch XeLaTeX ba lượt thành công; văn bản từng trang PDF khớp bản bàn giao.
- Log cuối không có overfull hbox/vbox, missing character hoặc undefined control sequence.
- Poppler render đủ 40 trang cuối ở 65 dpi, kiểm qua contact sheets. Bảng và sơ đồ cũng đã xem trong bản 85 dpi trước khi chỉnh phụ lục. Hai sơ đồ phụ lục chuyển sang trang dọc để tránh tràn; mục lục một trang.
- Không chạy lại mạng. Kết quả runtime giữ ngày chạy và phạm vi nền tảng cũ.

[qa.json](qa.json) giữ SHA256 hiện tại. Ảnh kiểm: [bìa](expanded-cover.png), [trang 1-12](expanded-pages-1.png), [13-24](expanded-pages-2.png), [25-36](expanded-pages-3.png), [37-40](expanded-pages-4.png).

QA 21 trang cũ giữ tại [history](history/qa-2026-11-05-before-expanded-report.json). Ảnh cover.png/pages-*.jpg cũ thuộc bản trước. Phụ lục Packet Tracer hai trang có QA độc lập. QA không thay phê duyệt học phần hoặc biên nhận BKeL. Gói submission ZIP cũ chưa đóng gói lại trong lần chỉnh báo cáo này.
