# TC01 - Cùng VLAN

**PASS trên GNS3 Linux/FRR; Packet Tracer/IOS chưa chạy.** Run `after-reopen-runtime`, UTC 2026-11-02T14:04:06.477140+00:00. Native project52 node đã được mở lại từ source. [Toàn bộ command output, source/image/hash](../runtime/after-reopen-runtime/results.json), [bối cảnh/giới hạn](../runtime/README.md), [runbook Cisco tham chiếu](../../simulation/test-runbook.md).

| Index trong cases | Node | Lệnh | Expected | Returncode actual | Kết luận |
| --- | --- | --- | --- | --- | --- |
| 3 | Main-PC10-B | `ping -n -c 2 -W 1 10.10.10.10` | success | 0 | PASS |
| 4 | Main-PC10-A | `ping -n -c 2 -W 1 10.10.10.11` | success | 0 | PASS |

Chỉ số index bắt đầu0 trong JSON `cases`. Trường `output` chứa kết quả CLI/HTTP thật; negative case phải thất bại đúng dự kiến. TC05 có đối chứng Web/DNS và counter DROP tại cả ba gateway. Không dùng log GNS3 để khẳng định command/timer IOS hoặc ứng dụng thật đã được kiểm.
