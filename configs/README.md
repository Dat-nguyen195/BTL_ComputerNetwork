# Cấu hình thiết bị

Có bộ **cấu hình base WAN TV1 và bản hợp nhất TV1/TV3, chưa nạp/kiểm IOS runtime**. Mỗi file `.cfg` nạp đúng một node; danh mục và thứ tự nạp ở [module WAN](../simulation/modules/tv1-wan/README.md). Core/FW base dùng IOS router để kiểm đường đi; bản hợp nhất thêm ACL/ZBF/relay/PAT, chưa thay campus LAN thật hoặc triển khai VPN.

TV1 phụ trách WAN/edge; TV2 LAN/Wi-Fi; TV3 firewall/NAT policy/server/VPN; TV4 tích hợp. Khi ghép node dùng chung, đọc chéo một cấu hình hợp nhất, tránh ghi đè. Ghi model/image/version, interface mapping, subnet, thứ tự nạp, project/hash và test liên quan. Tên hostname khớp node thật.

Console dùng trong lab; VTY đang tắt, SSH/AAA chưa thiết lập. Không có secret vận hành trong bộ tham chiếu. Giữ trạng thái NOT RUN đến khi có project/evidence; lưu startup và kiểm đóng/mở lại. Thay IP/route/NAT/ACL phải đồng bộ thiết kế và retest.

## Bổ sung02/11/2026

Đã có [nguồn security TV3](security/README.md) và bộ [cấu hình hợp nhất](../simulation/generated/configs/) với ACL/relay tại Core/Aux, ZBF tại FW và static PAT ISP2 tại Edge. Chạy `python3 scripts/build_lab.py`; dùng bản hợp nhất khi dựng lab, không nạp riêng routing base rồi coi có security.5 switch tối thiểu cho TV4 trong `simulation/generated/switches/`; campus/Wi-Fi của TV2 vẫn cần ghép/đọc chéo.
