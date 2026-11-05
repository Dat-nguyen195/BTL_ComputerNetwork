#!/usr/bin/env python3
"""Build a separate portable GNS3 MPLS topology from the same Linux runtime specification."""
import hashlib,importlib.util,json,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'simulation/mpls'
spec=importlib.util.spec_from_file_location('hospital_mpls',BASE/'mpls_runtime.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def ident(n):return str(uuid.uuid5(uuid.NAMESPACE_DNS,'hospital-mpls-l3vpn-'+n))
def artifacts():
 t=mod.topology();nodes=[]
 xy={'P-Core':(0,-150),'PE-Main':(0,0),'PE-DBP':(-500,0),'PE-BHTQ':(500,0),'CE-Main':(0,150),'CE-DBP':(-500,150),'CE-BHTQ':(500,150),'PC-Main':(-120,300),'PC-DBP':(-500,300),'PC-BHTQ':(500,300),'Web-Lab':(140,300)}
 for name,c in t['nodes'].items():
  x,y=xy[name];nodes.append({'node_id':ident(name),'name':name,'node_type':'docker','compute_id':'local','console_type':'telnet','symbol':':/symbols/computer.svg' if c['role'] in ('pc','web') else ':/symbols/router.svg','x':x,'y':y,'properties':{'image':'hospital-mpls:20261104','adapters':len(c['interfaces']),'start_command':'python3 /opt/mpls/mpls_runtime.py node --name '+name},'label':{'text':name,'x':0,'y':-25}})
 links=[]
 for a,ai,b,bi in t['links']:
  links.append({'link_id':ident(a+ai+b+bi),'nodes':[{'node_id':ident(n),'adapter_number':int(iface[3:]),'port_number':0} for n,iface in [(a,ai),(b,bi)]]})
 project={'name':t['name'],'project_id':ident('project'),'version':'2.2.55','type':'topology','revision':1,'auto_start':False,'auto_close':False,'auto_open':False,'zoom':80,'scene_width':1800,'scene_height':1200,'topology':{'nodes':nodes,'links':links,'drawings':[],'computes':[]}}
 out={'generated/topology.json':json.dumps(t,indent=2)+'\n','hospital-mpls.gns3':json.dumps(project,indent=2)+'\n'}
 out['generated/manifest.json']=json.dumps({'source_sha256':hashlib.sha256((BASE/'mpls_runtime.py').read_bytes()).hexdigest(),'artifacts':{n:hashlib.sha256(s.encode()).hexdigest() for n,s in out.items()},'scope':'Portable topology and shared config; runtime results recorded separately'},indent=2)+'\n';return out
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 for n,s in artifacts().items():
  f=BASE/n
  if a.check:assert f.read_bytes()==s.encode(),n
  else:f.parent.mkdir(exist_ok=True,parents=True);f.write_bytes(s.encode())
 print('OK MPLS artifacts: 11 nodes, 10 links; shared namespace/GNS3 node configurations; no runtime implied')
