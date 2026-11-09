# File báo cáo để nộp

Bản hiện tại: 47 trang, tích hợp bảng địa chỉ và kết quả kiểm thử vào các chương; 10 sơ đồ Cisco có nguồn chỉnh sửa tại [hospital-cisco.drawio](../../02-design/diagrams/hospital-cisco.drawio). Đã bổ sung nội dung theo file góp ý Word. Các mô tả phụ lục bên dưới thuộc cấu trúc bản trước; bản PDF hiện tại trình bày chúng trong chương 2–4. Ảnh chụp Packet Tracer từng ca chưa có; phần kiểm thử đưa trực tiếp CLI và quan sát đã lưu.

- **[report.pdf](report.pdf): báo cáo chính**, viết lại ngày 09/11/2026 theo bố cục bốn chương: giới thiệu; phân tích và thiết kế; mô phỏng và kiểm thử; kết luận và hướng phát triển. Nội dung đối chiếu đủ bảy Step, bổ sung phân tích luồng dữ liệu, khảo sát, BOM/cổng/PoE, GPON, Wi-Fi/camera, chi phí WAN, sizing ISP và phương pháp kiểm thử. Phụ lục giữ bằng chứng GNS3/Packet Tracer/MPLS, IP/VLAN và hướng dẫn demo.
- **[report-latex.zip](report-latex.zip): nguồn của báo cáo chính**, dùng XeLaTeX; [hướng dẫn](../latex/README.md).
- **[packet-tracer-validation.pdf](packet-tracer-validation.pdf): phụ lục kiểm thử hai trang**, nội dung khác báo cáo chính, dùng để tra nhanh 32 quan sát, Wi-Fi và ISP thủ công.

PDF sinh trong `latex/build/` hoặc `output/pdf/` là bản xem trước local. Thư mục này là nơi lấy PDF để nộp. [QA/hash](../../../test_results/report-latex/README.md) và [manifest bàn giao](../../../submission/manifest.md) xác nhận đúng phiên bản. Nguồn Markdown nằm ở [source](../source/README.md).
