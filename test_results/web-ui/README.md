# GNS3 Web UI - lỗi nhận nhầm Electron

**02/11/2026.** Đã tái hiện lỗi người dùng báo: trình duyệt thường mở project được, nhưng User-Agent chứa `Electron/` trong khi không có Node/IPC bridge gây `Cannot read properties of null (reading 'on')`. [Before](before-fix.json) lưu body lỗi thật.

Bundle đi kèm GNS3 chỉ dựa User-Agent để gọi Electron IPC. Bản sửa chỉ vào chế độ desktop nếu thực sự có `window.require('electron').ipcRenderer`, bắt lỗi bridge không tồn tại và giữ chế độ Web. Điều kiện đổi base URL trong HTML cũng được bảo vệ để tải lại URL project không sai đường dẫn asset. Không bật Node integration hoặc giả lập IPC cho trang Web.

[Browser results](browser-results.json) kiểm bằng Chrome thật trong profile mới, cả User-Agent thường và Electron không có Node: danh sách project, mở Hospital-3Sites-FRR, thấy Main-Core/DBP-GW/BHTQ-GW, tải lại URL project và không có lỗi JavaScript. [Ảnh thường](normal.png), [ảnh embedded Electron](embedded-electron.png). Các request ngoài localhost bị chặn trong bài test; không dùng profile trình duyệt của người dùng.

`simulation/gns3/controller/patch_web_ui.py` kiểm mẫu upstream trước sửa, giữ bundle/index gốc, sinh tên bundle mới theo hash tránh cache cũ và lưu manifest patch. Dockerfile áp dụng khi build; bản đang chạy được áp dụng trực tiếp không dừng52 node. Script chạy lại không sửa lặp. [Network smoke sau sửa](../runtime/after-webui-fix-runtime/results.json) giữ kiểm chứng gói tin riêng.

Chạy lại bài kiểm trình duyệt bằng Python có Playwright và Google Chrome:

```bash
python3 scripts/test_gns3_web_ui.py --output tmp/web-ui-regression
```

Nếu tab cũ còn báo lỗi, mở `http://127.0.0.1:3080/?webfix=2` rồi Ctrl+Shift+R. Khi sơ đồ nằm ngoài vùng nhìn, dùng `Pan workspace` để kéo và `Zoom out` để thu nhỏ; không dùng nút Stop/Reload node cho thao tác xem sơ đồ.
