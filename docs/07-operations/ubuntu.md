# Công cụ Ubuntu cho Cisco Packet Tracer

Cần Packet Tracer9.0.1 hoặc mới hơn phù hợp file để mở mô hình; XeLaTeX/latexmk để biên dịch báo cáo. Bản GitHub không kèm thư mục công cụ `scripts/`. Có thể dùng `latexmk report.tex` trong thư mục nguồn báo cáo hoặc tải ZIP nguồn lên Overleaf và chọn XeLaTeX.

Trên máy làm việc có sẵn `scripts/`, dùng `./project doctor` để kiểm Python3, git, Poppler và các thư viện tài liệu; `bash scripts/setup_ubuntu.sh` chỉ xem trước gói cần cài. Chạy `--apply` và cung cấp `--packet-tracer /path/file.deb` khi muốn cài bộ chính thức.

```bash
./project check
./project report
```

`check` không phát gói. Test mới mở bản sao `.pkt`, chọn Realtime và làm theo [demo](../final-demo.md), lưu output thư mục mới. Không ghi đè run đã kiểm. Giữ mật khẩu lab trong phạm vi mô phỏng; khi triển khai dùng tài khoản/quyền riêng.
