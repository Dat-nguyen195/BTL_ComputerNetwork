# Bộ sơ đồ Cisco dùng trong báo cáo

Bộ hiện tại có 10 trang: thêm so sánh kiến trúc phân tầng và bố trí camera theo tầng. Các PDF vector đã được đưa vào chương tương ứng của báo cáo tích hợp.

Mở [hospital-cisco.drawio](hospital-cisco.drawio) bằng diagrams.net/draw.io. Tệp có tám trang: tổng thể WAN, vật lý Main, vật lý Aux, GPON, bảo mật, Wi-Fi/camera, MPLS và VPN. Các thiết bị và liên kết là đối tượng chỉnh sửa riêng.

Trong More Shapes, bật **Networking → Cisco 19 (Cisco 2019)**. Các shape dùng namespace `mxgraph.cisco19`; bản stencil được lưu tại [cisco19.xml](cisco19.xml), tải từ `https://app.diagrams.net/stencils/cisco19.xml` ngày 09/11/2026. Đây là thư viện mở rộng ký hiệu Cisco của diagrams.net. File XML stencil là dữ liệu nguồn, không phải tệp sơ đồ để mở trực tiếp.

OLT, ONT và splitter dùng biểu tượng mạng tổng quát có nhãn chức năng; không coi đó là biểu tượng phần cứng Cisco GPON chuyên dụng. Sơ đồ vật lý mô tả thiết kế dự trù; sơ đồ WAN mô tả baseline chức năng. VPN/GPON chưa có runtime; MPLS có bằng chứng Linux riêng.

SVG trong `exports` và PDF vector trong `docs/06-report/latex/assets` được sinh từ cùng danh sách node/link và hình học stencil bởi `scripts/build_cisco_diagrams.py`. Khi chỉnh trực tiếp draw.io, cần xuất lại PDF tương ứng trước khi biên dịch báo cáo; generator không tự đọc ngược các chỉnh sửa thủ công. Thư viện Python cần có `svglib` và `reportlab`.

Hai tệp physical-main.drawio/physical-aux.drawio cũ được giữ để đối chiếu; bộ mới dùng trong bản báo cáo tích hợp là hospital-cisco.drawio.
