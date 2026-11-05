#!/usr/bin/env python3
"""Verify recorded MPLS packets, runtime/source correspondence and required observations."""
import hashlib,json,re,socket,struct
from pathlib import Path
import build_mpls
ROOT=Path(__file__).resolve().parents[1]

def frames(path):
 data=path.read_bytes();assert data[:4] in [b'\xd4\xc3\xb2\xa1',b'\xa1\xb2\xc3\xd4'],'not PCAP'
 endian='<' if data[:4]==b'\xd4\xc3\xb2\xa1' else '>';assert struct.unpack(endian+'I',data[20:24])[0]==1,'Ethernet required'
 pos=24;found=[]
 while pos<len(data):
  assert pos+16<=len(data);_,_,length,_=struct.unpack(endian+'IIII',data[pos:pos+16]);pos+=16;frame=data[pos:pos+length];pos+=length;assert len(frame)==length
  if len(frame)<18 or frame[12:14]!=b'\x88\x47':continue
  offset=14;labels=[]
  while True:
   assert offset+4<=len(frame);value=int.from_bytes(frame[offset:offset+4],'big');labels.append(value>>12);offset+=4
   if value&256:break
   assert len(labels)<8
  ip=frame[offset:];assert len(ip)>=20 and ip[0]>>4==4
  found.append({'labels':labels,'src':socket.inet_ntoa(ip[12:16]),'dst':socket.inet_ntoa(ip[16:20]),'protocol':ip[9]})
 return found

def check_run(directory):
 r=json.loads((directory/'results.json').read_text(encoding='utf8'));cases={c['id']:c for c in r['cases']}
 assert r['status']=='PASS' and len(cases)==len(r['cases'])==28
 assert all(c['status']=='PASS' for c in cases.values())
 for name,digest in r['source_sha256'].items():assert hashlib.sha256((ROOT/'simulation/mpls'/name).read_bytes()).hexdigest()==digest,name
 pc=directory/'mpls.pcap';assert hashlib.sha256(pc.read_bytes()).hexdigest()==r['pcap_sha256']
 observed=frames(pc)
 assert any(len(f['labels'])==2 and f['src']=='10.20.10.10' and f['dst']=='10.10.10.10' and f['protocol']==1 for f in observed),'No actual transport+VPN labelled ICMP frame'
 assert any(f['src']=='10.10.10.10' and f['dst']=='10.20.10.10' for f in observed),'No return data'
 sites=['Main','DBP','BHTQ'];required=set()
 def successful(id):
  required.add(id);c=cases[id];assert c['returncode']==0,id;return c['stdout']
 for src in sites:
  for dst in sites:
   if src!=dst:assert re.search(r'(?<!\d)0% packet loss',successful('MPLS-PING-'+src+'-'+dst))
  raw=successful('MPLS-INTERNET-'+src);d=json.loads(raw);assert d=={'node':'Web-Lab','client':'198.51.100.2','path':'/mpls-'+src}
  assert successful('MPBGP-'+src).count('BGP state = Established')==2
  assert all(prefix in successful('VPN-ROUTES-'+src) for prefix in ['10.10.10.0/25','10.20.10.0/25','10.30.10.0/25'])
  assert all(prefix in successful('VRF-FIB-'+src) for prefix in ['10.10.10.0/25','10.20.10.0/25','10.30.10.0/25'])
 for node,count in [('P-Core',3),('PE-Main',1),('PE-DBP',1),('PE-BHTQ',1)]:assert successful('LDP-'+node).count('OPERATIONAL')==count
 assert not any(prefix in successful('PROVIDER-NO-CUSTOMER-ROUTES') for prefix in ['10.10.10.','10.20.10.','10.30.10.'])
 for id in ['PROVIDER-CUSTOMER-ISOLATION','MPLS-LINK-DOWN-DBP']:
  required.add(id);assert cases[id]['returncode']!=0
 for id in ['MPLS-LINK-DOWN-CONTROL','MPLS-LINK-RESTORED']:assert re.search(r'(?<!\d)0% packet loss',successful(id))
 assert 'MPLS' in successful('MPLS-LABELLED-DATA');assert set(cases)==required
 assert len(r['fault'])==2 and all(x['returncode']==0 for x in r['fault']) and r['fault'][0]['command'][-1]=='down' and r['fault'][1]['command'][-1]=='up'
 return len(observed)

def main():
 for name,content in build_mpls.artifacts().items():assert (ROOT/'simulation/mpls'/name).read_bytes()==content.encode(),name
 for stage in ['validated','recreated']:
  n=check_run(ROOT/'test_results/mpls'/stage);print(f'OK recorded MPLS {stage}: 28 observations, {n} actual labelled frames; source hashes match')
 print('MPLS runtime is Linux namespaces inside QEMU; generated GNS3 module is separate. This checker does not execute the network.')
if __name__=='__main__':main()
