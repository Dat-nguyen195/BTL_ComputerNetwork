# Sơ đồ đi dây và hạ tầng vật lý

**Chủ trì:** TV2. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

Main có phòng trung tâm riêng cách A/B 50 m, mỗi tòa 5 tầng × 10 phòng. Mỗi Aux 2 tầng, IT/CCL tại tầng 1. Chiều dài 50 m là dữ kiện vị trí, không phải chiều dài cáp thực đã đo.

- Backbone quang từ trung tâm đến IDF tòa/tầng; access Ethernet đến thiết bị.
- Nếu chọn GPON: thiết kế OLT, ODN/ODF, splitter, ONT và optical budget; phân biệt với uplink Ethernet quang.
- 1GbE phía máy trạm; 10/40GbE phía uplink/core theo nhu cầu, không tuyên bố đã test hiệu năng.
- Bản `.drawio` hiện là bố cục khởi tạo, chưa phải sơ đồ thi công.

| Link ID | Đầu A / port | Đầu B / port | Tầng/phòng | Môi trường | Tốc độ | Chiều dài | Dự phòng |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chờ khảo sát | MDF Main | IDF A/B | Chờ xác nhận | Quang dự kiến | Chờ sizing | Chưa đo | Chờ thiết kế |


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
