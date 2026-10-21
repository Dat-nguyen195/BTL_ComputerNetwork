# Rủi ro, tồn tại và hướng phát triển

| ID | Rủi ro / thiếu dữ liệu | Ảnh hưởng | Phụ trách | Hành động | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| R01 | Chưa rõ tải server tổng hay từng máy | Sizing ISP/WAN sai | TV4 | Tính kịch bản và xác nhận | OPEN |
| R02 | Chưa có số khách và upload khách/PACS/camera | Thiếu throughput/AP/subnet | TV5/TV2/TV3 | Khảo sát, cập nhật giả định | OPEN |
| R03 | Hai xDSL có thể không đủ down/up | Nút thắt Internet Main | TV1 | So yêu cầu với năng lực hiệu dụng, đề xuất nâng cấp nếu cần | OPEN |
| R04 | Mỗi Aux chỉ có một leased line | Mất liên site khi lỗi tuyến | TV1 | Ghi SPOF, đề xuất đa tuyến giai đoạn sau | OPEN |
| R05 | Nền tảng không hỗ trợ IDS/IPS/GPON/SD-WAN thật | Không chứng minh được tính năng | TV3/TV4 | Thử sớm, ghi modeled/design only hoặc đổi môi trường | OPEN |
| R06 | Nhiều người sửa cùng file .pkt | Ghi đè, khó ghép | TV4 | Module/config text và lịch giữ file | OPEN |
| R07 | Báo cáo và file mô phỏng khác phiên bản | Nộp sai bằng chứng | TV5/TV4 | Manifest/hash, kiểm mở lại, TV1 duyệt | OPEN |

Hướng phát triển: đa dạng nhà mạng/tuyến WAN, HA nguồn/core/firewall, monitoring, backup/DR, khảo sát RF/camera thực và mở rộng 5 năm. Mỗi đề xuất phải nêu chi phí/phụ thuộc; chưa được coi là đã triển khai.
