# TC04 - DMZ và static PAT

**PASS trên GNS3 Linux/FRR.** Hồ sơ này giữ bằng chứng GNS3; [kết quả Packet Tracer riêng](../packet-tracer/README.md) đã có và không thay thế log của lần chạy này. Run `after-reopen-runtime`, UTC 2026-11-02T14:04:06.477140+00:00. Native project52 node đã được mở lại từ source. [Toàn bộ command output, source/image/hash](../runtime/after-reopen-runtime/results.json), [bối cảnh/giới hạn](../runtime/README.md), [runbook Cisco tham chiếu](../../simulation/test-runbook.md).

| Index trong cases | Node | Lệnh | Expected | Returncode actual | Kết luận |
| --- | --- | --- | --- | --- | --- |
| 11 | Main-PC10-A | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.80.10` | success | 0 | PASS |
| 12 | DBP-PC10 | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.80.10` | success | 0 | PASS |
| 13 | BHTQ-PC10 | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.80.10` | success | 0 | PASS |
| 14 | Web-Lab | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://198.51.100.2:8080` | success | 0 | PASS |
| 15 | Web-Lab | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://198.51.100.2:8081` | blocked/nonzero | 7 | PASS |
| 16 | Web-Lab | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://203.0.113.2:8080` | blocked/nonzero | 7 | PASS |

Chỉ số index bắt đầu0 trong JSON `cases`. Trường `output` chứa kết quả CLI/HTTP thật; negative case phải thất bại đúng dự kiến. TC05 có đối chứng Web/DNS và counter DROP tại cả ba gateway. Không dùng log GNS3 để khẳng định command/timer IOS hoặc ứng dụng thật đã được kiểm.
