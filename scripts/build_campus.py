#!/usr/bin/env python3
"""Reproduce TV2 budgets, cable schedule, editable diagrams and IOS port adapters."""
import argparse
import csv
import hashlib
import io
import json
from math import ceil
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'docs/02-design'


def rows():
    with (DESIGN / 'campus-inputs.csv').open(encoding='utf-8', newline='') as stream:
        data = list(csv.DictReader(stream))
    return [{k: v if k == 'site' else float(v) for k, v in row.items()} for row in data]


def budget(row):
    floors = int(row['buildings'] * row['floors_per_building'])
    ap_now, camera_now = floors * int(row['ap_per_floor']), floors * int(row['cameras_per_floor'])
    pc_future = ceil(row['pcs'] * (1 + row['growth']))
    ap_floor = ceil(row['ap_per_floor'] * (1 + row['growth']))
    camera_floor = ceil(row['cameras_per_floor'] * (1 + row['growth']))
    server_future = ceil(row['servers_on_access'] * (1 + row['growth']))
    switch_count = floors * int(row['access_per_floor'])
    ports = switch_count * int(row['ports_per_access'])
    now = int(row['pcs'] + ap_now + camera_now + row['servers_on_access'] + row['nvr_on_access'])
    future = pc_future + floors * (ap_floor + camera_floor) + server_future + int(row['nvr_on_access'])
    worst_floor = ceil(pc_future / floors) + ap_floor + camera_floor + server_future + int(row['nvr_on_access'])
    return dict(site=row['site'], floors=floors, access_switches=switch_count, access_ports=ports,
                pcs_now=int(row['pcs']), pcs_future=pc_future, aps_now=ap_now, aps_future=floors * ap_floor,
                cameras_now=camera_now, cameras_future=floors * camera_floor,
                used_now=now, used_future=future, spare_future=ports-future, worst_floor_future=worst_floor,
                floor_ports=int(row['access_per_floor'] * row['ports_per_access']),
                floor_poe_now_w=row['ap_per_floor'] * row['ap_pse_w'] + row['cameras_per_floor'] * row['camera_pse_w'],
                floor_poe_future_w=ap_floor * row['ap_pse_w'] + camera_floor * row['camera_pse_w'],
                floor_poe_budget_w=row['access_per_floor'] * row['poe_w_per_switch'],
                optical_links=switch_count*2, sfp_required=switch_count*4,
                sfp_with_spares=switch_count*4 + ceil(switch_count*4*0.1),
                cat6_boxes_305m=ceil(future*30*1.1/305),
                video_now_mbps=camera_now*row['camera_mbps'],
                video_future_mbps=floors*camera_floor*row['camera_mbps'],
                nvr_raw_now_gb=camera_now*row['camera_mbps']*86400*row['retention_days']/8000,
                nvr_usable_now_gb=camera_now*row['camera_mbps']*86400*row['retention_days']/8000*(1+row['recording_overhead'])/row['fill_ratio'],
                nvr_usable_future_gb=floors*camera_floor*row['camera_mbps']*86400*row['retention_days']/8000*(1+row['recording_overhead'])/row['fill_ratio'])


def csv_text(data):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(data[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(data)
    return stream.getvalue()


def diagrams(nodes, edges, width, height, title):
    # Same source geometry feeds both diagrams.net and a portable SVG export.
    mxfile = ET.Element('mxfile', host='app.diagrams.net', type='device')
    diagram = ET.SubElement(mxfile, 'diagram', id=title, name=title)
    model = ET.SubElement(diagram, 'mxGraphModel', page='1', pageWidth=str(width), pageHeight=str(height))
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', id='0')
    ET.SubElement(root, 'mxCell', id='1', parent='0')
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(width), height=str(height), viewBox=f'0 0 {width} {height}')
    ET.SubElement(svg, 'rect', width=str(width), height=str(height), fill='#f8fafc')
    by_id = {n[0]: n for n in nodes}
    for index, (source, target, label) in enumerate(edges):
        _, x1, y1, w1, h1, _, _ = by_id[source]
        _, x2, y2, w2, h2, _, _ = by_id[target]
        cx1, cy1, cx2, cy2 = x1+w1/2, y1+h1/2, x2+w2/2, y2+h2/2
        points = [(cx1,cy1),(cx2,cy2)]
        if target == 'core' and re.fullmatch(r'[AB][1-5]', source):
            left = source.startswith('A')
            side, bus, core_side = (x1+w1,480,x2) if left else (x1,1120,x2+w2)
            points = [(side,cy1),(bus,cy1),(bus,cy2),(core_side,cy2)]
        elif source == 'core' and target in ('sf','wlc'):
            gap = 535 if target == 'sf' else 700
            points = [(cx1,y1+h1),(cx1,gap),(cx2,gap),(cx2,y2)]
        elif source == 'fw' and target == 'edge':
            points = [(x1+w1,cy1),(1090,cy1),(1090,cy2),(x2+w2,cy2)]
        ET.SubElement(svg, 'polyline', points=' '.join(f'{x},{y}' for x,y in points), fill='none', stroke='#64748b', **{'stroke-width':'2'})
        if label:
            lx,ly=((480 if source.startswith('A') else 1120),215) if target=='core' and re.fullmatch(r'[AB][1-5]',source) else ((cx1+cx2)/2,(cy1+cy2)/2-8)
            text = ET.SubElement(svg, 'text', x=str(lx), y=str(ly), fill='#334155', **{'font-family':'DejaVu Sans,Arial', 'font-size':'12','text-anchor':'middle'})
            text.text = label
        cell = ET.SubElement(root,'mxCell', id=f'e{index}', edge='1', parent='1', source=source, target=target, value=label,
                             style='edgeStyle=orthogonalEdgeStyle;endArrow=none;strokeColor=#64748b;html=0;')
        geometry=ET.SubElement(cell,'mxGeometry',relative='1', **{'as':'geometry'})
        if len(points)>2:
            bends=ET.SubElement(geometry,'Array', **{'as':'points'})
            for x,y in points[1:-1]: ET.SubElement(bends,'mxPoint',x=str(x),y=str(y))
    for node_id, x, y, w, h, label, fill in nodes:
        ET.SubElement(svg,'rect',x=str(x),y=str(y),width=str(w),height=str(h),rx='10',fill=fill,stroke='#94a3b8')
        lines = label.split('\n')
        for offset, line in enumerate(lines):
            text = ET.SubElement(svg,'text',x=str(x+w/2),y=str(y+h/2-(len(lines)-1)*10+offset*20+5),fill='#0f172a',
                                 **{'font-family':'DejaVu Sans,Arial','font-size':'14','text-anchor':'middle'})
            text.text = line
        cell = ET.SubElement(root,'mxCell',id=node_id,parent='1',vertex='1',value=label,
                             style=f'rounded=1;whiteSpace=wrap;html=0;fillColor={fill};strokeColor=#94a3b8;fontSize=14;')
        ET.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h), **{'as':'geometry'})
    return ET.tostring(mxfile,encoding='unicode')+'\n', ET.tostring(svg,encoding='unicode')+'\n'


def native_adapters():
    original = (ROOT / 'simulation/generated/configs/Main-Core.cfg').read_text(encoding='utf-8')
    text = re.sub(r'interface GigabitEthernet0/0\n(?: .+\n)*', '', original)
    text = re.sub(r'^ encapsulation dot1Q \d+\n', '', text, flags=re.M)
    text = re.sub(r'GigabitEthernet0/0\.(\d+)', r'Vlan\1', text)
    for old, new in (('GigabitEthernet0/1','GigabitEthernet1/0/23'),('GigabitEthernet0/2','GigabitEthernet1/0/24')):
        text = text.replace(old, new)
        text = text.replace(f'interface {new}\n', f'interface {new}\n no switchport\n')
    text = re.sub(r'^end\n?', '', text, flags=re.M)
    vlans = (10,20,30,40,50,60,70,90,100,110,120)
    allowed = ','.join(map(str, vlans))
    prefix = '! TV2 3650 ADAPTER - APPLY TO A COPY; ORIGINAL PKT UNCHANGED; NOT RUN\n'
    prefix += '! Replace ROAS Main-Core with this node; never keep both gateways active.\nip routing\n'
    for vlan in vlans:
        prefix += f'vlan {vlan}\n name HOSPITAL-V{vlan}\n'
    extra = ['spanning-tree mode rapid-pvst','spanning-tree vlan '+allowed+' priority 24576']
    for group, ports in ((1, (1,2)), (2, (3,4))):
        extra += [f'interface Port-channel{group}',' switchport mode trunk',' switchport trunk allowed vlan '+allowed]
        for port in ports:
            extra += [f'interface GigabitEthernet1/0/{port}',' switchport mode trunk',
                      ' switchport trunk allowed vlan '+allowed,f' channel-group {group} mode active',' no shutdown']
    extra += ['interface GigabitEthernet1/0/5',' description Add-Main-Infra-10.10.70.10',
              ' switchport mode access',' switchport access vlan 70',' spanning-tree portfast',' no shutdown',
              'interface GigabitEthernet1/0/6',' description Main-Admin-10.10.90.11',
              ' switchport mode access',' switchport access vlan 90',' spanning-tree portfast',' no shutdown',
              'interface range GigabitEthernet1/0/7 - 22',' shutdown',
              'interface range GigabitEthernet1/1/1 - 4',' shutdown','line vty 0 15',' transport input none','end']
    result = {'Main-Core-3650.cfg': prefix+text+'\n'.join(extra)+'\n'}
    for letter, group, address in (('A',1,'10.10.90.32'),('B',2,'10.10.90.42')):
        lines = ['! TV2 2960 adapter - NOT RUN; optional staff AP must be created.',f'hostname Main-Access-{letter}', 'spanning-tree mode rapid-pvst']
        for vlan in vlans:
            lines += [f'vlan {vlan}',f' name HOSPITAL-V{vlan}']
        lines += [f'interface Port-channel{group}',' switchport mode trunk',' switchport trunk allowed vlan '+allowed]
        for port in (1,2):
            lines += [f'interface GigabitEthernet0/{port}',' switchport mode trunk',' switchport trunk allowed vlan '+allowed,
                      f' channel-group {group} mode passive',' no shutdown']
        for port, vlan, desc in ((1,10,'PC-VLAN10'),(2,20,'PC-VLAN20'),(3,100,'AP-PT-GUEST-UNTAGGED'),(4,120,'ADD-AP-PT-STAFF-UNTAGGED')):
            lines += [f'interface FastEthernet0/{port}',f' description {desc}',' switchport mode access',f' switchport access vlan {vlan}',
                      ' spanning-tree portfast',' spanning-tree bpduguard enable',' no shutdown']
        lines += ['interface range FastEthernet0/5 - 24',' shutdown','interface Vlan90',f' ip address {address} 255.255.255.0',
                  ' no shutdown','ip default-gateway 10.10.90.1','line vty 0 15',' transport input none','end']
        result[f'Main-Access-{letter}-2960.cfg'] = '\n'.join(lines)+'\n'
    return result


def artifacts():
    data = rows()
    budgets = [budget(row) for row in data]
    output = {'docs/02-design/campus-budget.csv':csv_text(budgets)}
    cables=[]
    for row in data:
        site=row['site']
        index=0
        for building in range(int(row['buildings'])):
            for floor in range(1,int(row['floors_per_building'])+1):
                for switch in range(1,int(row['access_per_floor'])+1):
                    index+=1
                    access=f"{site}-{chr(65+building)}{floor}-S{switch}"
                    for core in (1,2):
                        cables.append(dict(link=f'{access}-C{core}',site=site,access=access,access_port=f'Te1/1/{core}',
                                           core=f'{site}-Core{core}',core_port=f'Te1/0/{index}',
                                           route='A' if core==1 else 'B',medium='OM3 duplex',speed_gbps=10,
                                           strands=2,length_status='SURVEY REQUIRED; independent conduit not verified'))
    output['docs/02-design/campus-uplinks.csv']=csv_text(cables)
    nodes=[('title',30,20,1540,65,'MAIN: THIẾT KẾ VẬT LÝ - CHƯA KHẢO SÁT / CHƯA HA RUNTIME','#dbeafe'),
           ('note',30,100,1540,60,'A/B: mỗi tòa 5 tầng × 10 phòng; phòng MDF cách tòa 50 m (không phải chiều dài cáp)\n20 switch ×48 cổng; PC 600→720, AP 30→40, camera 40→50; còn 150 cổng sau tăng trưởng','#ffffff'),
           ('core',540,245,520,100,'MDF: 2 CORE L3 (DỰ TRÙ)\nMỗi core: 20 uplink access +8 cổng dịch vụ =28/32\n2×40G core-core; HA gateway cần cấu hình/test riêng','#bfdbfe'),
           ('wan',545,405,235,95,'WAN gateway pair dự trù\n2 leased lines→DBP/BHTQ\nWAN nối Core, không nối FW','#e0e7ff'),
           ('fw',825,405,235,95,'Firewall pair dự trù\nCore↔FW↔Internet Edge\nZBF lab một node','#fee2e2'),
           ('sf',545,565,235,100,'2 switch SERVER FARM\nVLAN70/90/110\n8→10 server nội bộ +NVR','#dcfce7'),
           ('dmz',825,565,235,100,'2 switch DMZ RIÊNG\n2 server; VLAN80 gateway FW\nKhông uplink thẳng Core','#fee2e2'),
           ('wlc',545,730,235,85,'2 WLC dự trù\nMỗi WLC hỗ trợ ≥64 AP\nAP uplink 1G trong baseline','#fef3c7'),
           ('edge',825,730,235,85,'Edge /2 modem xDSL\nPBR/PAT tại Edge\nISP2:8080 công bố DMZ','#fef3c7'),
           ('foot',30,925,1540,75,'Mỗi IDF có 2 switch; tổng 4 link 10G/IDF (2 link tới mỗi core), tuyến A/B riêng cần khảo sát.\nUplink độc lập/RSTP; chỉ LACP xuyên core khi có một logical switch được cấu hình. GPON: phương án riêng, chưa triển khai.','#ffffff')]
    edges=[('wan','core',''),('core','fw',''),('core','sf',''),('fw','dmz',''),('core','wlc',''),('fw','edge','')]
    for letter,x in (('A',35),('B',1185)):
        for floor in range(1,6):
            nid=f'{letter}{floor}';y=195+(5-floor)*140
            nodes.append((nid,x,y,380,100,f'TÒA {letter} - TẦNG {floor}: 1 IDF /2 switch\nSau tăng trưởng:72 PC +4 AP +5 camera\n81/96 cổng; Cat6 tới 10 phòng','#ffffff'))
            edges.append((nid,'core','4×10G/IDF' if floor==3 else ''))
    drawing,svg=diagrams(nodes,edges,1600,1030,'Main campus - reviewed TV2')
    output['docs/02-design/diagrams/physical-main.drawio']=drawing
    output['docs/02-design/diagrams/exports/physical-main.svg']=svg
    nodes=[('title',30,20,1340,65,'DBP /BHTQ: THIẾT KẾ MỖI SITE - CHƯA NGHIỆM THU','#dbeafe'),
           ('main',490,120,420,80,'Main WAN gateway\n2 leased lines tách biệt; một tuyến/site','#e0e7ff'),
           ('foot',30,820,1340,80,'Mỗi site:8×48=384 cổng; dùng 277 hiện tại /334 sau tăng trưởng, dư 50.\nAP6→8, camera8→10, server2→3 và1 NVR; NVR ghi local. ACL/SSID theo từng site, không kéo VLAN qua WAN.','#ffffff')]
    edges=[]
    for site,x in (('DBP',55),('BHTQ',755)):
        nodes += [(site+'-wan',x,270,590,75,f'{site}: WAN router (lab một node)\nDuy nhất một leased line; không có local Internet breakout','#e0e7ff'),
                  (site+'-core',x,410,590,95,'TẦNG 1 - IT /CCL /MDF\n2 distribution dự trù,8 uplink access/core\nServer2→3 +NVR1; mỗi NVR≥16 kênh','#bfdbfe'),
                  (site+'-f1',x,580,270,120,'TẦNG 1:4 switch /192 cổng\nSau tăng trưởng:156 PC\n4 AP+5 camera+3 server+1NVR\n169/192 cổng','#ffffff'),
                  (site+'-f2',x+320,580,270,120,'TẦNG 2: IDF /4 switch\nSau tăng trưởng:156 PC\n4 AP+5 camera\n165/192 cổng','#ffffff')]
        edges += [('main',site+'-wan','leased line'),(site+'-wan',site+'-core',''),
                  (site+'-core',site+'-f1','uplink đôi'),(site+'-core',site+'-f2','2 tuyến quang A/B')]
    drawing,svg=diagrams(nodes,edges,1400,930,'Aux campuses - reviewed TV2')
    output['docs/02-design/diagrams/physical-aux.drawio']=drawing
    output['docs/02-design/diagrams/exports/physical-aux.svg']=svg
    for name,text in native_adapters().items():
        output['simulation/modules/tv2-lan-wireless/configs/'+name]=text
    hashes={name:hashlib.sha256(text.encode()).hexdigest() for name,text in sorted(output.items())}
    output['simulation/modules/tv2-lan-wireless/reference-manifest.json']=json.dumps(dict(status='REFERENCE ONLY; ORIGINAL PKT UNCHANGED; RUNTIME NOT RUN',sha256=hashes),indent=2)+'\n'
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    stale=[]
    for name,text in artifacts().items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_bytes()!=text.encode(): stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(text.encode())
    if stale: parser.exit(1,'Run build_lab.py then build_campus.py; stale: '+', '.join(stale)+'\n')
    print('OK TV2: 3 site budgets,72 optical links,2 editable diagrams/SVG and3 IOS adapters'+(' (freshness checked)' if args.check else ''))


if __name__=='__main__':
    main()
