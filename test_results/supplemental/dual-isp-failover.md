# SUPP01 - Dual ISP và thời gian phục hồi

**PASS trong GNS3 Linux, phạm vi đã thử.** [validated-runtime](../runtime/validated-runtime/results.json) có nhóm ISP-PBR, ISP-FAILOVER, ISP-CONVERGENCE, ISP-BOTH-DOWN và ISP-RECOVERY. Main-PC10 ưu tiênISP1, Main-PC20 ưu tiênISP2; HTTP server phản ánh địa chỉ NAT thật.

Tắt uplink phía sau ISP1/ISP2 để giữ egress Edge vẫn up nhưng probe thất bại; kiểm năm endpoint dùng ISP còn sống và ping Aux↔Aux. Thời gian từ fault tới HTTP từ cả năm máy phục hồi8,707s/6,521s; samples outage có trong JSON. Khi cả hai upstream mất, Web không dùng được, Aux rút default và nội bộ vẫn ping được. Sau phục hồi chạy lại đủ sáu nhóm.

Ngân sách thử45s không phải SLA; chưa đo local-link fault, duy trì phiên NAT cũ, MTU, throughput hoặc mọi timer. IOS IP SLA/PBR chưa chạy; Linux dùng health loop/timer riêng. Lần đầu hai FAIL do thử Aux trong cửa sổ hội tụ được giữ nguyên, không chuyển thành zero-downtime.
