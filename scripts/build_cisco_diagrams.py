"""Generate editable draw.io pages and vector figures from official Cisco19 stencils."""
from pathlib import Path
import xml.etree.ElementTree as E
import html,sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/report-libs'))
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
OUT=ROOT/'docs/02-design/diagrams'
ST=OUT/'cisco19.xml'
shapes={x.get('name'):x for x in E.parse(ST).getroot()}

def icon(name):
 s=shapes[name]; parts=[]
 for path in s.findall('.//path'):
  d=[]
  for c in path:
   a=c.attrib;t=c.tag
   if t in ('move','line'):d.append(('M' if t=='move' else 'L')+a['x']+','+a['y'])
   elif t=='curve':d.append('C'+','.join(a[k] for k in ['x1','y1','x2','y2','x3','y3']))
   elif t=='quad':d.append('Q'+','.join(a[k] for k in ['x1','y1','x2','y2']))
   elif t=='arc':d.append('A'+','.join(a.get(k,'0') for k in ['rx','ry','x-axis-rotation','large-arc-flag','sweep-flag','x','y']))
   elif t=='close':d.append('Z')
  parts.append('<path d="'+' '.join(d)+'" fill="#0875a5"/>')
 return float(s.get('w')),float(s.get('h')),''.join(parts)

PAGES=[]
def page(key,title,nodes,edges,note):PAGES.append((key,title,nodes,edges,note))
# node: id, label, stencil, column, row
page('wan-cisco','01 | THREE-SITE LOGICAL TOPOLOGY',[
 ('isp1','ISP1 / 203.0.113.0/30','router',1,0),('isp2','ISP2 / 198.51.100.0/30','router',3,0),
 ('edge','Main-Edge / PBR + PAT','router',2,1),('fw','Main-FW / stateful policy','firewall',2,2),
 ('dmz','DMZ / 10.10.80.0/27','server',4,2),('core','Main-Core / VLAN gateways','l3 switch',2,3),
 ('lan','Main LAN / 10.10.0.0/16','l2 switch',0,3),('gw','Main-GW / OSPF area 0','router',2,4),
 ('dbp','DBP / 10.20.0.0/16','router',0,4),('bhtq','BHTQ / 10.30.0.0/16','router',4,4)],
 [('isp1','edge','ISP1'),('isp2','edge','ISP2'),('edge','fw','10.255.0.16/30'),('fw','dmz','DMZ only'),('fw','core','10.255.0.12/30'),('core','lan','802.1Q'),('core','gw','10.255.0.8/30'),('gw','dbp','10.255.0.0/30'),('gw','bhtq','10.255.0.4/30')],
 'Functional baseline: single Core/FW/Edge. All Aux Internet traffic passes through Main.')
main=[('core1','Core 1 / MDF','l3 switch',1,0),('core2','Core 2 / MDF','l3 switch',3,0)]
links=[('core1','core2','2 x 40GbE')]
for floor in range(1,6):
 for building,col in [('A',0),('B',4)]:
  n=f'{building}{floor}';main.append((n,f'{building} F{floor}: IDF / 2 x 48 ports','l2 switch',col,floor));links.extend([(n,'core1','10G A'),(n,'core2','10G B')])
page('main-cisco','02 | MAIN CAMPUS - PHYSICAL DESIGN',main,links,'10 IDFs; 20 access switches; 600 to 720 PCs. Independent fiber routes A/B. HA is a production proposal.')
page('aux-cisco','03 | AUX CAMPUS - DBP OR BHTQ',[
 ('wan','Leased line to Main','router',2,0),('d1','Distribution 1 / MDF F1','l3 switch',1,1),('d2','Distribution 2 / MDF F1','l3 switch',3,1),
 ('f1','Floor 1: 4 x 48 ports','l2 switch',0,2),('f2','Floor 2: 4 x 48 ports','l2 switch',4,2),('srv','2 to 3 local servers','server',1,3),('nvr','Local NVR / VLAN110','server',3,3)],
 [('wan','d1','WAN'),('d1','d2','Interconnect'),('d1','f1','10G A'),('d2','f1','10G B'),('d1','f2','10G A'),('d2','f2','10G B'),('f1','srv','VLAN70'),('f1','nvr','VLAN110')],
 'Each site: 260 to 312 PCs; 384 access ports. One WAN remains a single point of failure.')
page('gpon-cisco','04 | HYBRID GPON - ADMINISTRATION',[
 ('c1','Core 1','l3 switch',1,0),('c2','Core 2','l3 switch',3,0),('olt','OLT / 2 PON + 2 x 10G','l2 switch',2,1),
 ('sa','Building A / splitter 1:16','l2 switch',0,2),('sb','Building B / splitter 1:16','l2 switch',4,2),
 ('oa','10 to 12 ONTs / 4GE each','l2 switch',0,3),('ob','10 to 12 ONTs / 4GE each','l2 switch',4,3),
 ('pa','40 to 48 PCs / VLAN60','server',0,4),('pb','40 to 48 PCs / VLAN60','server',4,4)],
 [('c1','olt','10G A'),('c2','olt','10G B'),('olt','sa','PON1 / OS2'),('olt','sb','PON2 / OS2'),('sa','oa','10 to 12 drops'),('sb','ob','10 to 12 drops'),('oa','pa','4GE / ONT'),('ob','pb','4GE / ONT')],
 'Design only. OLT/splitter/ONT use generic Cisco network symbols; labels define actual device roles. No GPON PHY simulation.')
page('security-cisco','05 | SECURITY ZONES AND PERMITTED FLOWS',[
 ('net','Internet / Web-Lab','router',2,0),('fw','Main-FW / IDS-IPS','firewall',2,1),('dmz','DMZ Web / 10.10.80.10','server',4,1),
 ('core','Core / ingress ACLs','l3 switch',2,2),('guest','Guest / VLAN100','wireless access point',0,3),('staff','Staff / VLAN120','wireless access point',2,3),('srv','Server Farm / VLAN70','server',4,3),
 ('admin','Admin / VLAN90','server',1,4),('cam','Camera / VLAN110','surveillance camera',3,4)],
 [('net','fw','PAT via Edge'),('fw','dmz','Inbound TCP8080 -> 80'),('fw','core','Zone policy'),('core','guest','Internet only; deny LAN'),('core','staff','Role-based access'),('core','srv','Approved applications'),('core','admin','Management only'),('core','cam','Local NVR; no Internet')],
 'Logical policy view: Edge omitted for clarity. Same-VLAN traffic also requires host policy / L2 isolation.')
page('wifi-cisco','06 | WI-FI AND CAMERA ACCESS',[
 ('core','Site core / distribution','l3 switch',2,0),('sw','PoE access switch / IDF','l2 switch',2,1),('wlc','WLC / management VLAN90','wireless lan controller',4,0),
 ('staff','Staff SSID / VLAN120','wireless access point',0,2),('guest','Guest SSID / VLAN100','wireless access point',2,2),('camera','Camera / VLAN110','surveillance camera',4,2),('nvr','NVR local / VLAN110','server',4,3)],
 [('core','sw','802.1Q uplink'),('core','wlc','Control / management'),('sw','staff','PoE / staff'),('sw','guest','PoE / guest'),('sw','camera','PoE / camera'),('camera','nvr','Local recording')],
 'Production: multi-SSID AP with VLAN mapping. Packet Tracer uses separate single-SSID APs. RF coverage has not been measured.')
page('mpls-cisco','07 | MPLS L3VPN - SEPARATE LAB',[
 ('p','Provider P / OSPF + LDP','router',2,1),('pe1','PE Main / RD 65000:1','router',0,2),('pe2','PE DBP / RD 65000:2','router',2,2),('pe3','PE BHTQ / RD 65000:3','router',4,2),
 ('ce1','CE Main / AS65101','router',0,3),('ce2','CE DBP / AS65102','router',2,3),('ce3','CE BHTQ / AS65103','router',4,3),
 ('pc1','10.10.10.0/25','server',0,4),('pc2','10.20.10.0/25','server',2,4),('pc3','10.30.10.0/25','server',4,4)],
 [('p','pe1','Labels'),('p','pe2','Labels'),('p','pe3','Labels'),('pe1','ce1','eBGP'),('pe2','ce2','eBGP'),('pe3','ce3','eBGP'),('ce1','pc1','LAN'),('ce2','pc2','LAN'),('ce3','pc3','LAN')],
 'Provider AS65000; PE VPNv4 MP-BGP; VRF HOSPITAL / RT65000:100. Linux namespace evidence, not GNS3 runtime. MPLS does not encrypt.')
page('vpn-cisco','08 | VPN PROPOSAL - NOT YET IMPLEMENTED',[
 ('main','Main-GW / IKEv2 VTI','router',2,1),('dbp','DBP-GW / VTI','router',0,2),('bhtq','BHTQ-GW / VTI','router',4,2),
 ('fw','Main-FW / remote access','firewall',2,3),('user','Teleworker / MFA','server',0,4),('app','HIS / CRM only','server',4,4)],
 [('main','dbp','IPsec over leased line'),('main','bhtq','IPsec over leased line'),('user','fw','IKEv2 or TLS VPN'),('fw','app','Approved services only')],
 'VTI: 10.255.1.0/30 and 10.255.1.4/30. Remote pool: 10.255.100.0/24. Underlay redundancy and crypto tests still required.')

page('layers-cisco','09 | MAIN: THREE FUNCTIONS / AUX: COLLAPSED CORE',[
 ('mc','Main / Core','l3 switch',0,0),('md','Main / Distribution','l3 switch',0,1),('ma','Main / Access','l2 switch',0,2),('ac','Aux / Core + Distribution','l3 switch',3,0),('aa','Aux / Access','l2 switch',3,2)],
 [('mc','md','Backbone'),('md','ma','Policy + aggregation'),('ac','aa','Collapsed design')],
 'Functional layers: Main production may collapse core/distribution in one chassis. Baseline lab uses one Main-Core.')
page('camera-cisco','10 | TYPICAL FLOOR - CAMERA PLACEMENT PROPOSAL',[
 ('sw','IDF / PoE switch','l2 switch',2,0),('c1','C1 / entrance','surveillance camera',0,1),('c2','C2 / corridor east','surveillance camera',1,2),('c3','C3 / corridor west','surveillance camera',3,2),('c4','C4 / lift + stair lobby','surveillance camera',4,1),('nvr','Site NVR / local recording','server',2,3)],
 [('sw','c1','Cat6 / PoE'),('sw','c2','Cat6 / PoE'),('sw','c3','Cat6 / PoE'),('sw','c4','Cat6 / PoE'),('sw','nvr','VLAN110')],
 '4 cameras/floor now; reserve C5 after survey. Functional placement, not an architectural floor plan; exclude sensitive clinical areas.')
mx=E.Element('mxfile',host='app.diagrams.net',type='device',libraries='cisco19')
for key,title,nodes,edges,note in PAGES:
 height=180+140*(max(n[4] for n in nodes)+1);width=1200
 diagram=E.SubElement(mx,'diagram',name=title,id=key);model=E.SubElement(diagram,'mxGraphModel',page='1',pageWidth=str(width),pageHeight=str(height));r=E.SubElement(model,'root');E.SubElement(r,'mxCell',id='0');E.SubElement(r,'mxCell',id='1',parent='0')
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/><text x="35" y="42" font-family="Arial" font-size="24" fill="#082f87">{html.escape(title)}</text>']
 for ident,label,y in [('title',title,20),('note',note,height-60)]:
  c=E.SubElement(r,'mxCell',id=ident,parent='1',vertex='1',value=label,style='text;html=0;whiteSpace=wrap;align=left;fontSize=16;');E.SubElement(c,'mxGeometry',x='35',y=str(y),width='1120',height='40',attrib={'as':'geometry'})
 pos={n[0]:(90+n[3]*235,90+n[4]*140) for n in nodes}
 for i,(a,b,label) in enumerate(edges):
  x,y=pos[a];u,v=pos[b];x+=40;y+=35;u+=40;v+=35
  route=f'M{x},{y} L{u},{v}'
  color='#8296a9'
  lx=(x+u)/2+8;ly=(y+v)/2-22
  if x==u:lx=x+95
  if key=='main-cisco' and b in ('core1','core2') and a not in ('core1','core2'):
   offset=-12 if b=='core1' else 12
   route=f'M{x},{y} L{x},{y+offset} L{u},{y+offset} L{u},{v}'
   color='#1682b0' if b=='core1' else '#d38a25'
   label=''
  svg.append(f'<path d="{route}" stroke="{color}" stroke-width="2" fill="none"/><text x="{lx}" y="{ly}" font-family="Arial" font-size="14" fill="#334155">{html.escape(label)}</text>')
  c=E.SubElement(r,'mxCell',id=f'e{i}',parent='1',edge='1',source=a,target=b,value=label,style='edgeStyle=orthogonalEdgeStyle;endArrow=none;strokeColor=#8296a9;fontSize=12;');E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
 for ident,label,shape,col,row in nodes:
  x,y=pos[ident];w,h,paths=icon(shape);scale=min(80/w,65/h)
  svg.append(f'<rect x="{x-2}" y="{y-2}" width="84" height="70" fill="white"/><g transform="translate({x},{y}) scale({scale})">{paths}</g><rect x="{x-85}" y="{y+76}" width="250" height="25" fill="white"/><text x="{x+40}" y="{y+94}" text-anchor="middle" font-family="Arial" font-size="15" fill="#18374b">{html.escape(label)}</text>')
  c=E.SubElement(r,'mxCell',id=ident,parent='1',vertex='1',value=label,style=f'shape=mxgraph.cisco19.{shape.replace(" ","_")};fillColor=#0875a5;strokeColor=none;verticalLabelPosition=bottom;verticalAlign=top;align=center;fontSize=13;');E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width='80',height='65',attrib={'as':'geometry'})
 svg.append(f'<text x="35" y="{height-30}" font-family="Arial" font-size="12" fill="#475569">{html.escape(note)}</text></svg>')
 path=OUT/'exports'/f'{key}.svg';path.write_text(''.join(svg),encoding='utf-8');renderPDF.drawToFile(svg2rlg(str(path)),str(ROOT/'docs/06-report/latex/assets'/f'{key}.pdf'))
E.ElementTree(mx).write(OUT/'hospital-cisco.drawio',encoding='utf-8',xml_declaration=True)
print('Built',len(PAGES),'editable Cisco19 pages and vector PDF figures')
