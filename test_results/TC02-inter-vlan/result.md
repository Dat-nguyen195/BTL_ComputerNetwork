# TC02 - Giữa VLAN

**PASS trên GNS3 Linux/FRR.** Hồ sơ này giữ bằng chứng GNS3; [kết quả Packet Tracer riêng](../packet-tracer/README.md) đã có và không thay thế log của lần chạy này. Run `after-reopen-runtime`, UTC 2026-11-02T14:04:06.477140+00:00. Native project52 node đã được mở lại từ source. [Toàn bộ command output, source/image/hash](../runtime/after-reopen-runtime/results.json), [bối cảnh/giới hạn](../runtime/README.md), [runbook Cisco tham chiếu](../../simulation/test-runbook.md).

| Index trong cases | Node | Lệnh | Expected | Returncode actual | Kết luận |
| --- | --- | --- | --- | --- | --- |
| 0 | Main-PC10-A | `curl --noproxy * --connect-timeout 2 --max-time 3 --fail --silent --show-error http://10.10.70.11` | success | 0 | PASS |
| 1 | Main-PC10-A | `ping -n -c 2 -W 1 10.10.20.10` | success | 0 | PASS |
| 2 | Main-PC20 | `ping -n -c 2 -W 1 10.10.10.10` | success | 0 | PASS |

Chỉ số index bắt đầu0 trong JSON `cases`. Trường `output` chứa kết quả CLI/HTTP thật; negative case phải thất bại đúng dự kiến. TC05 có đối chứng Web/DNS và counter DROP tại cả ba gateway. Không dùng log GNS3 để khẳng định command/timer IOS hoặc ứng dụng thật đã được kiểm.
