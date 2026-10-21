# Hệ thống camera

**Chủ trì:** TV3 về quyền/lưu trữ; TV2 về cáp/PoE. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

Camera/NVR ở VLAN 110 riêng từng site; chỉ cho phép NVR và máy quản trị được cấp quyền truy cập. Chưa xác nhận số camera, bitrate, codec, thời gian lưu và vị trí thực.

```text
B_camera = tổng bitrate các luồng camera (Mbps)
Storage_GB = B_camera × 10^6 / 8 × 86400 × số_ngày_lưu / 10^9
```

Cộng overhead, dự phòng và phương án lưu trữ phù hợp sau khi chốt dữ liệu; chỉ cộng tải WAN nếu luồng thực đi qua WAN. Kiểm PoE budget và số port. Xác nhận quyền riêng tư trước đặt camera ở khu vực nhạy cảm.


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
