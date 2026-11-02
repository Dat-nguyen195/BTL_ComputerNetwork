# Hồ sơ duyệt bản bàn giao

**PENDING xác nhận người phụ trách; cập nhật02/11/2026.** Tác vụ hoàn thiện/kiểm kỹ thuật đã thực hiện theo yêu cầu chủ repo; không tự ký thay TV1/TV5 hoặc tạo biên nhận BKeL.

| Sản phẩm/điều kiện | Kiểm kỹ thuật đã có | Phê duyệt học phần |
| --- | --- | --- |
| PDF/source | Có bản10 trang, đã render QA; hash ởSHA256SUMS | PENDING TV1/TV5 |
| Native GNS3 | Đã chép template từ source, mở lại bằng GNS3,52 node started và137 kiểm PASS | PENDING TV4/TV1 |
| LAN/WAN/security |209 kiểm tích hợp PASS,18 pool/OSPF/NAT/PBR/IDS-IPS; giới hạn có ghi | PENDING đọc chéo nhóm |
| Config thực | Hash mã/config trong52 node khớp source; IOS vẫn chưa chạy | PENDING phạm vi nền tảng |
| Gói/checksum | package_submission.py và manifest/checksum, không thay chữ ký | PENDING bản nộp đã chọn |
| Thông tin môn học/nhân sự/BKeL | Nhóm xác nhận tên/lớp/MSSV, quy định nhóm và hạn; chưa nộp | PENDING |

[Manifest](manifest.md), [review cuối](../docs/00-management/project-review.md), [evidence](../test_results/runtime/README.md) ghi kết quả có thật. Khi người phụ trách duyệt, ghi ngày/người/hash và kết luận riêng cho PDF/project. Sửa sau duyệt phải cập nhật hash, kiểm phần bị ảnh hưởng và tái duyệt.
