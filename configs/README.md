# Cấu hình thiết bị

Có bộ **cấu hình tham chiếu TV1, chưa nạp/kiểm IOS runtime**. Mỗi file `.cfg` nạp đúng một node; danh mục và thứ tự nạp ở [module WAN](../simulation/modules/tv1-wan/README.md). Core/FW reference dùng IOS router để kiểm đường đi; chưa thay campus LAN của TV2 hoặc firewall/VPN của TV3.

TV1 phụ trách WAN/edge; TV2 LAN/Wi-Fi; TV3 firewall/NAT policy/server/VPN; TV4 tích hợp. Khi ghép node dùng chung, đọc chéo một cấu hình hợp nhất, tránh ghi đè. Ghi model/image/version, interface mapping, subnet, thứ tự nạp, project/hash và test liên quan. Tên hostname khớp node thật.

Console dùng trong lab; VTY đang tắt, SSH/AAA chưa thiết lập. Không có secret vận hành trong bộ tham chiếu. Giữ trạng thái NOT RUN đến khi có project/evidence; lưu startup và kiểm đóng/mở lại. Thay IP/route/NAT/ACL phải đồng bộ thiết kế và retest.
