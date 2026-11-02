# Review phần TV2 của Tiendat và bản sửa tích hợp

**02/11/2026; thực hiện theo yêu cầu kiểm/sửa/merge của chủ repo.** Nguồn `origin/tiendat` tại`3f52588ca9d11cf2e54356495b77a52ac019f62c`. Bản TV1/TV3/TV4 trước đó được lưu riêng commit`39fab95`. Review này xác nhận việc đối chiếu/sửa tĩnh, không thay chữ ký nghiệm thu hoặc runtime.

## Kết quả theo mức ảnh hưởng

| Mức | Phát hiện ở nhánhTiendat | Xử lý /phạm vi còn lại |
| --- | --- | --- |
| P1 | `github-project-structure.md` chứaTC01 PASS/ngày 12/11/2026, file/hình/log không có, ngày tương lai so02/11 | Gỡ đoạn kết quả chưa được chứng minh; testcase giữNOT RUN, thêm quy tắc chặn citation placeholder |
| P1 | `.pkt` chỉ 10 node Main, chưa cóIP/gateway4 PC, không cóDHCP/server/Aux/WAN/FW; startup trống | Giữ nguyênbyte vàhash, đặt đúng thư mụcmodule, audit cấu trúc; không gọi đây là bản tổng/G3 hoặc PASS |
| P1 | AP-PTGuest nốitrunk/native1; SwitchBPCport2 cònVLAN1 | Adapteraccess100/120, PCport2 VLAN20; hướng dẫn thêmAPStaff vàInfra; binarygốc chưa được sửa/chạy |
| P1 | Không cóACL guest tạiMLS, đường định tuyếnLAN bypassFW | Adapter3650 giữpolicy TV3 trênSVI vàrelay/OSPF/default TV1;37 flowMainACL kiểm lại |
| P1 | Sơ đồlogicalWAN nốiFW thay vìCore; DMZswitchBOM cóuplinkCore | WAN nốiCore theo10.255.0.8/30; DMZswitch tách riêng và chỉnốiFW, khôngVLAN80 trêncampustrunk |
| P1 | LACP được mô tảnhưdualcoreHA và 2 sợi=2 link | Tách2 uplink độc lập/RSTP tới2 core; LACPxuyênchassis chỉ khi logicalswitch; duplex10 G1 link=2 sợi, tuyến A/B cầnkhácống |
| P2 | C9200L-48P-4X ghi370 W, modelAP2.5 G nốiswitch1 G không nêugiới hạn | Sửa740 W vớiPSU1 kW, nguồnCisco; APfallback1 Gghi rõ |
| P2 | Portbudget bỏNVR tạiAux, AP/camera giữ nguyên5 năm, WLC50 AP thiếu | Main810/960, Aux334/384; AP42→56 theoceil từngtầng, WLC≥64; thùngCat6 Main88/Aux37 |
| P2 | NVRBOM3 Mbps nhưngcamera4 Mbps, dự phòng/lưu trữ không cùnggiả định | Đồng bộ4 Mbps/30 ngày/5%overhead/80%fill, usableMain85.050 GB/Aux17.010 GB5 năm; không giữ RAID64 TB thiếu |
| P2 | `physical-main.drawio` dùng3560/2960 vàFa0/1 nhưng gán10 G/1 G; Auxscaffold; ảnhPNG chưa có | Tạo drawio+SVGMain/Aux từcùngsource, tách sản xuấtvslab, khôngtham chiếuPNGvắng; đãrenderxem |
| P2 | ActiveEthernet được tích như đãđược duyệt thayGPON | Ghi thiết kếEthernet làbaseline nhóm, GPONcònthiếu/chờxác nhận; bổ sungOLT/ODN/ONT/OS2 vàopticalbudget |
| P2 | Wireless/portplan/contribution TV2 cònkhung | Hoàn thiệnSSID/VLAN/IP/cổng/phân bổPC, RF/AAA/isolationcònchờ; viếtcontribution TV2 |

## Sản phẩm và kiểm chứng

- [Module/hướng dẫn sửa native](../../simulation/modules/tv2-lan-wireless/README.md), [audit/hash](../../simulation/modules/tv2-lan-wireless/audit/inventory.json); file gốcđổi đường dẫn nhưng cùngbyte với commitTiendat.
- [BOM](../02-design/equipment-bom.md), [portplan](../02-design/lan-port-plan.md), [wireless](../02-design/wireless-plan.md), [cabling](../02-design/physical-cabling.md), [camera](../02-design/camera-plan.md), nguồn/sơ đồSVG vàCSVbudget/uplinks.
- `build_campus.py --check`, `check_lan.py`: kiểm3 sitebudget/lưu trữ,72 uplink,2 diagramXML/SVG,3 adapter và 37 flowMainACLgiữđúngquyền; sourcehashnativekhớp.
- Bộ `verify.py` tiếp tục kiểm9 routerWAN/33 subnet/9 faultscenario/61 ACLflow/18 DHCPpool/inventory/capacity vàlink/fence/citation/conflictmarkers.

Đây là merge source/thiết kế/module **chưa nghiệm thu mô phỏngtổng**. Cần mở bản sao trong Packet Tracer9, nạpadapter, thêmInfra/Staff/Aux/WAN/FW/ISP, kiểmfeature, save/reopen vàTC01–06. Không repackXML hoặc giảCLI/ảnh để lấp phần này. Native compatibility/throughput/RF/HA/VPN/IDS/IPS/GPON chưa được chứng minh.
