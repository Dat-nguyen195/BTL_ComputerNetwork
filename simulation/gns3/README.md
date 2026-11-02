# Mô hình GNS3 ba cơ sở đã kiểm thử

**02/11/2026. GNS3 2.2.55 + Linux/FRR.** [Project](hospital-3sites.gns3) có52 node:9 router/firewall,5 switch bridge VLAN và38 endpoint;52 link,18 pool DHCP,14 server nội bộ đúng10/2/2. [Kết quả](../../test_results/runtime/README.md) có log thực sáu nhóm TC01–06, OSPF, DHCP/DNS, IDS/IPS, dual ISP và save/close/reopen. Đây là project GNS3 nguồn mở; cấu hình Cisco và `.pkt` TV2 là bộ tham chiếu riêng.

## Chạy tự động trên máy Linux có Docker

Lần đầu cần Internet tải image/package, khoảng3GB image/cache và khoảng2GB RAM trống cho lab; số liệu dung lượng là dự trù, phụ thuộc Docker/cache. Controller có Docker daemon riêng trong container, không mount socket máy thật. Namespace và interface thử lỗi nằm trong lab. API chỉ publish localhost3080; cần Docker hỗ trợ privileged container và cổng3080 đang trống.

```bash
python3 scripts/verify.py
python3 scripts/gns3_lab.py bootstrap
python3 scripts/test_gns3_runtime.py --failover
python3 scripts/gns3_lab.py status
python3 scripts/gns3_lab.py exec Main-GW vtysh -c 'show ip ospf neighbor'
python3 scripts/gns3_lab.py exec Main-PC10-A ping -c 3 10.20.10.10
python3 scripts/gns3_lab.py exec Main-PC10-A curl http://web.hospital.test
```

Không bootstrap đè container cùng tên. Lệnh `start`, `stop`, `reopen` dùng lab đã có. `remove` chỉ xóa container controller đúng tên, giữ `tmp/gns3-state` và named volume `btl2-gns3-docker` để khôi phục; không xóa Docker image/volume của dự án khác. Controller API không bật authentication vì chỉ bind localhost; không mở cổng ra mạng ngoài.

```bash
python3 scripts/gns3_lab.py stop
python3 scripts/gns3_lab.py reopen
```

Có thể kết nối GNS3 GUI2.2.55 tới controller localhost3080 để xem topology. Console telnet của từng node nằm trong controller; dùng lệnh `exec` ở trên, hoặc cấu hình publish console ports riêng khi cần GUI console. Script không tự mở GUI hoặc giả ảnh chụp màn hình.

## Mở trên GNS3 Linux/VM khác

1. Tại compute sẽ chạy node, build `hospital-netlab:20261102` từ thư mục `runtime/`: `docker build -t hospital-netlab:20261102 simulation/gns3/runtime`. Image này chứa mã/config đã sinh, không phải image trên Docker Hub.
2. Dùng GNS3 2.2.55 mở `hospital-3sites.gns3`; chọn local compute tương thích Docker/ubridge. Chạy image trong GNS3 VM cần build/load image **bên trong VM**, không chỉ trên máy GUI.
3. Start all nodes, chờ OSPF/DHCP/health probe; kiểm Web và Main–Aux trước demo. Không dùng biểu tượng xanh của node thay kiểm kết nối.
4. Fileproject đã được chép lại từ source, mở bằng GNS3 và chạy lại toàn bộ smoke; bằng chứng tại `test_results/runtime/persistence/`. Host/package khác vẫn cần chạy lại test, không mặc định PASS theo máy tạo.

## Nguồn, cập nhật và giới hạn

`build_gns3.py` lấy9 cấu hình IOS hợp nhất, CSV cáp/endpoint/port, ACL và18 pool; chuyển policy sang iptables/FRR và tạo native project/config JSON. Các cú pháp ACL ngoài parser hiện có làm build thất bại. `runtime-manifest.json` lưu hash source và sản phẩm; [live provenance](../../test_results/runtime/persistence/live-provenance.json) xác nhận file trong52 container khớp source.

Khi sửa nguồn: chạy `build_lab.py`, `build_campus.py`, `build_gns3.py`, rebuild/load image, tái tạo lab của riêng dự án rồi test lại. Chỉ sửa image tag không cập nhật container đang tồn tại. Không đưa private key hoặc thông tin người bệnh vào image/evidence.

Linux model dùng hai Ethernet P2P thay leased-line/DSL PHY; OSPF dùng hello1/dead4 và probe khoảng2s với hai mẫu thành công/thất bại. Đây không phải timer IOS IP SLA. Giới hạn45s ở test failover là ngân sách thử, không phải SLA. HTTP là ứng dụng đại diện; RF/WLC/AAA/GPON quang, HA chassis/state sync, VPN crypto và tải đủ1.120 PC chưa chạy.

Suricata trên Main-FW sử dụng NFQUEUE repeat, mark1/1 để quay lại firewall; không có queue-bypass. Nếu IPS không chạy, forwarding qua FW ngừng (fail closed). Hai URI marker chỉ kiểm rule mẫu; không kết luận chống mọi phishing/attack. DNS blocklist dùng miền `.invalid` an toàn. Xem [security plan](../../docs/04-security/ids-ips-plan.md).

Nguồn nền tảng: [GNS3 Docker](https://docs.gns3.com/docs/emulators/docker-support-in-gns3), [APIv2](https://api.gns3.net/en/stable/), [FRR OSPF](https://docs.frrouting.org/en/stable-8.4/ospfd.html), [Suricata NFQUEUE](https://docs.suricata.io/en/suricata-7.0.2/setting-up-ipsinline-for-linux.html). Package/image chính xác trong evidence; rebuild apt có thể nhận bản vá mới nên không cam kết binary bit-identical.
