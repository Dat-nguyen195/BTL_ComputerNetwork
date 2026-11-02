# SUPP04 - IDS/IPS bằng marker HTTP vô hại

**PASS rule mẫu Suricata trong GNS3.** Main-FW dùng NFQUEUE repeat/mark1/1 rồi tiếp tục firewall; không dùng queue-bypass. [Run sau reopen](../runtime/after-reopen-runtime/results.json) nhóm IDS-IPS có7 kiểm, EVE/fast.log/rule thật và version; [PCAP](../runtime/persistence/hospital-demo.pcap) ghi thêm HTTP từ Web-Lab qua static PAT.

- `/hospital-ids-test`: HTTP thành công và alert SID1000001.
- `/hospital-ips-test`: HTTP bị chặn, SID1000002 và action blocked; positive control `/` vẫn thành công.
- DNS `phishing-test.invalid`: trả0.0.0.0 theo blocklist thử an toàn.

Chỉ xác nhận rule/inline path và positive/negative controls. Chưa chứng minh feed cập nhật, phát hiện phishing thật, full attack corpus, false positive/negative hoặc throughput khi inspect. Nếu Suricata dừng, FW fail closed; HA/bypass vận hành chưa triển khai. Đây không phải IOS ACL được đổi tên thành IDS.
