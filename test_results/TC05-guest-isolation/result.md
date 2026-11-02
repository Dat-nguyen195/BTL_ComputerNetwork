# TC05 - Cách ly Guest

**PASS trên GNS3 Linux/FRR; Packet Tracer/IOS chưa chạy.** Run `after-reopen-runtime`, UTC 2026-11-02T14:04:06.477140+00:00. Native project52 node đã được mở lại từ source. [Toàn bộ command output, source/image/hash](../runtime/after-reopen-runtime/results.json), [bối cảnh/giới hạn](../runtime/README.md), [runbook Cisco tham chiếu](../../simulation/test-runbook.md).

| Index trong cases | Node | Lệnh | Expected | Returncode actual | Kết luận |
| --- | --- | --- | --- | --- | --- |
| 17 | BHTQ-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://web.hospital.test` | success | 0 | PASS |
| 18 | Main-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://web.hospital.test` | success | 0 | PASS |
| 19 | DBP-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://web.hospital.test` | success | 0 | PASS |
| 20 | DBP-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.70.11` | blocked/nonzero | 28 | PASS |
| 21 | BHTQ-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.70.11` | blocked/nonzero | 28 | PASS |
| 22 | Main-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.70.11` | blocked/nonzero | 28 | PASS |
| 23 | Main-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.80.10` | blocked/nonzero | 28 | PASS |
| 24 | DBP-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.80.10` | blocked/nonzero | 28 | PASS |
| 25 | BHTQ-Guest | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.80.10` | blocked/nonzero | 28 | PASS |
| 26 | Main-Guest | `ping -n -c 1 -W 1 10.10.10.10` | blocked/nonzero | 1 | PASS |
| 27 | DBP-Guest | `ping -n -c 1 -W 1 10.30.10.10` | blocked/nonzero | 1 | PASS |
| 28 | DBP-Guest | `ping -n -c 1 -W 1 10.20.10.10` | blocked/nonzero | 1 | PASS |
| 29 | Main-Guest | `ping -n -c 1 -W 1 10.20.10.10` | blocked/nonzero | 1 | PASS |
| 30 | Main-Guest | `ping -n -c 1 -W 1 10.30.10.10` | blocked/nonzero | 1 | PASS |
| 31 | DBP-Guest | `ping -n -c 1 -W 1 10.10.10.10` | blocked/nonzero | 1 | PASS |
| 32 | BHTQ-Guest | `ping -n -c 1 -W 1 10.20.10.10` | blocked/nonzero | 1 | PASS |
| 33 | BHTQ-Guest | `ping -n -c 1 -W 1 10.10.10.10` | blocked/nonzero | 1 | PASS |
| 34 | BHTQ-Guest | `ping -n -c 1 -W 1 10.30.10.10` | blocked/nonzero | 1 | PASS |
| 127 | Main-Core | `iptables -nvx -L MAIN-V100-IN` | success | 0 | PASS |
| 128 | DBP-GW | `iptables -nvx -L DBP-V100-IN` | success | 0 | PASS |
| 129 | BHTQ-GW | `iptables -nvx -L BHTQ-V100-IN` | success | 0 | PASS |

Chỉ số index bắt đầu0 trong JSON `cases`. Trường `output` chứa kết quả CLI/HTTP thật; negative case phải thất bại đúng dự kiến. TC05 có đối chứng Web/DNS và counter DROP tại cả ba gateway. Không dùng log GNS3 để khẳng định command/timer IOS hoặc ứng dụng thật đã được kiểm.
