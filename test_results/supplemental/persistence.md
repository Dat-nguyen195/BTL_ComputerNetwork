# SUPP05 - Lưu, đóng/mở lại và nguồn thực

**PASS trên GNS3 2.2.55.** [reopen.json](../runtime/persistence/reopen.json) ghi hash native template đã chép từ source, mở lại bằng GNS3 và52 node started; [after-reopen-runtime](../runtime/after-reopen-runtime/results.json) có137 kiểm PASS,0 FAIL sau mở lại, gồm sáu nhóm demo và DHCP/DNS/OSPF/IDS/IPS.

Trước đóng đã ngắt toàn bộ container thuộc lab để kiểm hồi phục đột ngột; thao tác không tác động container dự án khác. Sau mở lại, [live-provenance](../runtime/persistence/live-provenance.json) xác nhận mã/config thực trong52 node khớp source. Bằng chứng này áp dụng project GNS3/image đã ghi; file `.pkt` TV2 gốc chưa được mở/chạy bằng Packet Tracer.
