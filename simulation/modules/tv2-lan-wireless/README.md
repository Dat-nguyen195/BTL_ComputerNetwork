# Module TV2 của Phạm Tiến Đạt: tiếp nhận, review và cách sửa

**Nguồn:** nhánh `tiendat`, commit `3f52588ca9d11cf2e54356495b77a52ac019f62c` (tác giả tien dat). **Review02/11/2026:** đã kiểm cấu trúc file lưu và đối chiếu cấu hình/tài liệu; **chưa mở/chạy Packet Tracer**, chưa nghiệm thu. File gốc giữ nguyên byte, chỉ chuyển từ `file_cisco.pkt` sang [tiendat-lan-original.pkt](tiendat-lan-original.pkt). Đây là **module Main một phần**, không phải mô phỏng tổng 3 site.

## Nội dung file lưu được kiểm

[Inventory/hash](audit/inventory.json) ghi Packet Tracer version được lưu **9.0.0.0810**,10 thiết bị/10 cáp:1 MLS3650,2 switch2960,4 PC,2 AP,1 PDU. Không có routerWAN/Aux/ISP/FW/server. Core chỉ cóSVI10/20/100/120, chưaACL/DHCP/OSPF/NAT;3 switch còn cùnghostname`Switch`; startup-config3 switch trống.4 PC chưa lưu IP/gateway,2 AP SSID `BenhVien_Guest` nốiFa0/3 trunk/native1. VLAN10/20/100/120 có trong VLAN DB.

Đây là **dữ liệu tĩnh đã lưu**, không chứng minh người dùng chưa từng chạy thử ngoài bản này. Tuy nhiên nó không đủ chứng minhPASS đã ghi ở tài liệu cũ; không có ảnh/log/phiên bản tương ứng nên TC01/02 vẫn NOT RUN trong hồ sơ nghiệm thu.

XML được đọc cục bộ bằng [Unpacket upstream](https://github.com/Punkcake21/Unpacket), pinned commit`54cb6d6a9b46c6b4973356258cb8df6ae58b2ec7`, sau khi xem source; không uploadfile ra ngoài và không chạy script nhúng. `scripts/audit_packet_xml.py` chỉ xuất summary và 3 running-config đã lọc secret, không commitXMLraw/userprofile. Cách tái lập tùy chọn: clone đúngcommit upstream, decodefile ra thư mục tạm, rồi:

```bash
python3 scripts/audit_packet_xml.py --xml /tmp/tiendat.xml --packet simulation/modules/tv2-lan-wireless/tiendat-lan-original.pkt --output-dir simulation/modules/tv2-lan-wireless/audit
```

Tooldecode không phảiCisco và không kiểm runtime. CI không tải/chạytool ngoài, chỉ kiểm hash file gốc với audit.

## Cấu hình sửa để nạp vào BẢN SAO

Chạy `python3 scripts/build_lab.py` rồi `python3 scripts/build_campus.py`; [manifest tham chiếu](reference-manifest.json) chứa hash file sinh ra. Không repackXML thành `.pkt` rồi tuyên bố bản đó mở/chạy được.

| Node file gốc | File sửa | Vai trò /điều kiện |
| --- | --- | --- |
| Multilayer Switch0 | [Main-Core-3650.cfg](configs/Main-Core-3650.cfg) | ĐổihostnameMain-Core, SVI thay ROAS; giữ IP/ACL/relay/OSPF/trackeddefault TV1/TV3; bổ sungVLAN; Gi1/0/23/24 làroutedport |
| Switch_toa_A | [Main-Access-A-2960.cfg](configs/Main-Access-A-2960.cfg) | LACPgroup1 trênGi0/1–2; PCport1/2 VLAN10/20; APGuestport3 access100; StaffAPport4 access120 nếu thêm |
| Switch_toa_B | [Main-Access-B-2960.cfg](configs/Main-Access-B-2960.cfg) | LACPgroup2; sửaPCport2 khỏiVLAN1; APGuest/Staff nhưA; hostname/management khácA |

Chỉ thay Main-CoreROAS bằng 3650, **không để hai gateway .1/loopback .255.1 cùng hoạt động**. Đối với TV4 file tổng: nốiGi1/0/23 .9→Main-GW .10, Gi1/0/24 .13→Main-FW .14; chuyển cáp theo mapping, không copy cấu hìnhSerial lênswitch. DMZ80 vẫn kết thúcMain-FW, không tạoSVI80 hoặc uplinkDMZ trực tiếpCore. Phải thử IP SLA/PBR/ZBF theo model; giữ BLOCKED nếuCLI không hỗ trợ, không bỏ lệnh rồi ghi đạt.

Thêm Main-InfraServer `.70.10/27`, gateway `.70.1`, nốiGi1/0/5 access70; nhập pool/DNS từ [serverplan](../../../docs/02-design/server-dmz-plan.md). Router/switchadapter không tự tạo server/DNS. Admin .90.11 nốiGi1/0/6 nếu cần. AP-PT hiện là guest untagged; thêmAPStaff vàoFa0/4, đặtSSIDStaff/VLAN120; không giả địnhAP-PT hỗ trợWLC/Enterprise/2 SSID.

Để smokeTC01/02 trước DHCP, tạm đặt PC0`10.10.10.10/25`, PC2`10.10.10.11/25`, PC1`10.10.20.10/25`, PC3`10.10.20.11/25`, gateway theoVLAN. Tắt poolDHCP tương ứng khi dùngstatic trongpool; chuyển vềDHCP/ghi lease thực trước test tích hợp để tránh trùng IP. Không khẳng định đây là địa chỉ đã lưu trong `.pkt` gốc.

Kiểm `show etherchannel summary`, `show interfaces trunk`, `show vlan brief`, `show ip interface brief`, ACLhit và ứng dụng; chạy [runbook](../../test-runbook.md). Lưu `copy running-config startup-config`, lưu project ở **file mới**, đóng/mở lại, thu actual/ảnh/log/hash. Giữ nguyên file gốc để truy vết; bản đã sửa phải được TV4/TV1 nghiệm thu riêng.9.0.0.0810 là metadata lưu, chưa xác nhận compatibility với phiên bản thấp hơn.

## Phạm vi bàn giao

[BOM/cổng/quang](../../../docs/02-design/equipment-bom.md), [port/VLANplan](../../../docs/02-design/lan-port-plan.md), [wireless](../../../docs/02-design/wireless-plan.md), [cabling/GPON](../../../docs/02-design/physical-cabling.md), sơ đồ nguồn+SVG đã chuẩn bị. AP/RF, dualcoreHA,10/40 G, GPON, roaming/AAA/clientisolation vẫn DESIGN ONLY hoặc chưa kiểm. Cấu hình sửa là text đã kiểm tĩnh, chưa được nạp vào `.pkt` gốc. [Review chi tiết](../../../docs/00-management/tv2-review.md).
