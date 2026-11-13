# Demo Cisco Packet Tracer

Mở `simulation/packet-tracer/hospital-3sites.pkt` bằng Packet Tracer9.0.1.0858. Native102 node/97 cáp, SHA256 `183953558f045e378ddbbed3205da84e357865381f03f95b4dc625cf79e0b31a`. Save As sang bản mới nếu thu thêm test, không ghi đè raw đã kiểm.

## Demo trực tiếp

1. Chọn **Realtime**, chờ hội tụ. Xem Main A/B năm tầng, DBP/BHTQ hai tầng; [bảng tầng](topology-redesign-floor-mapping.md).
2. Main-PC10-A/B: Desktop → Command Prompt → `ipconfig`, ping IP hiện tại của nhau. Main-PC10-A ping Main-PC20; mở `http://10.10.70.11/`, cần marker HIS.
3. Main-GW/DBP-GW/BHTQ-GW: `show ip ospf neighbor`, `show ip route`; FULL và ping liên site hai chiều.
4. Web-Lab: Browser `http://198.51.100.2:8080/`, cần marker Main-WebDMZ. Main-Edge: `show ip nat translations`.
5. Guest mỗi site mở HIS hoặc portal IoT local phải bị chặn; cùng Guest vẫn mở `http://web.hospital.test/`. Đọc `show access-lists` trước/sau tại Main-Core/DBP-GW/BHTQ-GW, deny tăng. Không chỉ dựa timeout.
6. Kiểm sáu Staff/Guest association, BSSID và DHCP lease; không suy thành RF/roaming/throughput production.
7. Main-Admin `10.10.90.11` → Browser: `http://10.10.110.12/`, `http://10.20.110.12/`, `http://10.30.110.12/`. Tài khoản **lab** `hospitalcam` / `HospitalLab2026Only`. Danh sách kết nối Main10/DBP2/BHTQ2. Mở dòng camera xem control/state. Nếu Simulation dừng, gói tin bị giữ; chuyển Realtime hoặc Capture/Forward. Portal `.12` không lưu video, PC-PT NVR `.11` chỉ đại diện thiết kế.
8. Main-Admin → Command Prompt: `ssh -l labadmin 10.10.90.1`, mật khẩu lab như trên, `show ip interface brief`, `exit`. Chỉ thử quyền đọc; hai đối chứng Telnet bị đóng và nguồn non-admin timeout chưa quy riêng cho VTY.

## Thu và kiểm bằng chứng

Native nhúng script. Extensions → Scripting → Edit File Script Module → Debug; cho phép IPC của script dự án. `warmupHospitalAndTest()` chạy suite32; `captureWireless()` thu association; test camera/PC bổ sung dùng `redesignTests("redesign-camera-tests.json",false)` từ script `simulation/packet-tracer/scripts/redesign-tests.js`. Chạy trên bản sao và thu baseline ACL trước test theo script; không gọi lại để ghi đè data store của run đang giữ.

```bash
python3 scripts/collect_packet_tracer.py --input /path/new-run.pkt --output /path/new-evidence
python3 scripts/check_packet_runtime.py --run /path/new-evidence --project /path/new-run.pkt
python3 scripts/check_redesign_packet.py
```

Hai lệnh đầu cần đúng file/raw của cùng run. Lệnh cuối đối chiếu bộ đã bàn giao, không chạy mạng. Evidence chính nằm tại `test_results/packet-tracer/redesign-20261112-162237/`:32 P0/WIFI +21 HTTP +3SSH; sau reopen12HTTP +3SSH. Lượt smoke đầu thiếu controls được giữ nguyên, không sửa thành PASS.

Chuyển ISP đã có helper `manual-isp.js`, thao tác thủ công và khôi phục ISP2; không demo như failover tự động. PBR/probe, IDS/IPS, VPN crypto, ghi video, HA, RF/GPON PHY và tải1120PC chưa nghiệm thu. Xem [phạm vi](cisco-scope.md).
