#!/usr/bin/env python3
"""Execute real packet/control-plane checks in the isolated hospital MPLS namespaces."""
import argparse,datetime,hashlib,itertools,json,re,signal,subprocess,time
from pathlib import Path
import mpls_runtime as lab

def main():
 p=argparse.ArgumentParser();p.add_argument('--run',default='initial');p.add_argument('--out',default='/root/mpls/evidence');a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 records=[];snap={}
 def command(node,args):
  r=lab.run(args,node,check=False);return {'node':node,'command':args,'returncode':r.returncode,'stdout':r.stdout}
 def vty(n,c):return command(n,['vtysh','-N',lab.PREFIX+n,'-c',c])
 def add(id,raw,passed,expected):records.append({'id':id,'status':'PASS' if passed else 'FAIL','expected':expected,**raw})
 # This is warmup/convergence, not a passing test record.
 start=time.monotonic();warmup=[]
 while time.monotonic()-start<120:
  r=command('PC-DBP',['ping','-c','1','-W','1','10.10.10.10']);warmup.append(r)
  if r['returncode']==0:break
  time.sleep(2)
 for x,y in itertools.permutations(lab.SITES,2):
  ip='10.'+str((lab.SITES.index(y)+1)*10)+'.10.10';r=command('PC-'+x,['ping','-c','2','-W','2',ip]);add('MPLS-PING-'+x+'-'+y,r,r['returncode']==0 and bool(re.search(r'(?<!\d)0% packet loss',r['stdout'])),'2/2 ICMP through hospital VPN')
 for site in lab.SITES:
  r=command('PC-'+site,['curl','--noproxy','*','--connect-timeout','3','--max-time','6','--fail','--silent','http://192.0.2.100/mpls-'+site])
  try:d=json.loads(r['stdout'])
  except ValueError:d={}
  add('MPLS-INTERNET-'+site,r,r['returncode']==0 and d.get('client')=='198.51.100.2' and d.get('node')=='Web-Lab' and d.get('path')=='/mpls-'+site,'HTTP succeeds via Main central PAT 198.51.100.2')
 for site in lab.SITES:
  n='PE-'+site
  r=vty(n,'show bgp neighbors');add('MPBGP-'+site,r,r['returncode']==0 and r['stdout'].count('BGP state = Established')==2,'two established MP-BGP VPN peers')
  r=vty(n,'show bgp ipv4 vpn');add('VPN-ROUTES-'+site,r,r['returncode']==0 and all(x in r['stdout'] for x in ['10.10.10.0/25','10.20.10.0/25','10.30.10.0/25']),'all three hospital LAN prefixes in VPN SAFI')
  r=command(n,['ip','-4','route','show','vrf','HOSPITAL']);add('VRF-FIB-'+site,r,r['returncode']==0 and all('10.'+str(i*10)+'.10.0/25' in r['stdout'] for i in range(1,4)),'all three LAN prefixes installed in isolated HOSPITAL table')
 for n in ['P-Core']+['PE-'+s for s in lab.SITES]:
  r=vty(n,'show mpls ldp neighbor');add('LDP-'+n,r,r['returncode']==0 and r['stdout'].count('OPERATIONAL')==(3 if n=='P-Core' else 1),'expected operational LDP adjacencies')
 r=command('P-Core',['ip','-4','route','show']);add('PROVIDER-NO-CUSTOMER-ROUTES',r,r['returncode']==0 and not any('10.'+str(i*10)+'.10.' in r['stdout'] for i in range(1,4)),'P global table contains provider transport only')
 r=command('P-Core',['ping','-c','1','-W','2','10.10.10.10']);add('PROVIDER-CUSTOMER-ISOLATION',r,r['returncode']!=0,'provider default namespace cannot reach customer LAN; six positive customer controls above')
 # Fault one provider access link: DBP has no alternate path; Main/BHTQ stay live.
 fault=[]
 try:
  fault.append(command('P-Core',['ip','link','set','eth1','down']))
  time.sleep(5)
  r=command('PC-DBP',['ping','-c','1','-W','2','10.10.10.10'])
  add('MPLS-LINK-DOWN-DBP',r,r['returncode']!=0,'DBP loses access when its single provider link is down')
  r=command('PC-Main',['ping','-c','2','-W','2','10.30.10.10'])
  add('MPLS-LINK-DOWN-CONTROL',r,r['returncode']==0 and bool(re.search(r'(?<!\d)0% packet loss',r['stdout'])),'Main to BHTQ remains reachable during DBP fault')
 finally:fault.append(command('P-Core',['ip','link','set','eth1','up']))
 recovery=[];start=time.monotonic()
 while time.monotonic()-start<60:
  r=command('PC-DBP',['ping','-c','2','-W','2','10.10.10.10']);recovery.append(r)
  if r['returncode']==0 and re.search(r'(?<!\d)0% packet loss',r['stdout']):break
  time.sleep(2)
 add('MPLS-LINK-RESTORED',r,r['returncode']==0 and bool(re.search(r'(?<!\d)0% packet loss',r['stdout'])),'DBP 2/2 ICMP restored after provider link returns')
 capture=out/'mpls.pcap'
 proc=subprocess.Popen(['ip','netns','exec',lab.PREFIX+'PE-DBP','tcpdump','-U','-s','0','-i','eth0','-w',str(capture),'ether proto 0x8847'],stdout=subprocess.DEVNULL,stderr=open(out/'tcpdump.log','w'))
 time.sleep(1);probe=command('PC-DBP',['ping','-c','3','-W','2','10.10.10.10']);time.sleep(1);proc.send_signal(signal.SIGINT);proc.wait(timeout=10)
 r=command(None,['tcpdump','-nn','-e','-r',str(capture)]);add('MPLS-LABELLED-DATA',r,probe['returncode']==0 and 'MPLS' in r['stdout'] and bool(re.search(r'label \d+.*label \d+',r['stdout'])),'captured MPLS Ethernet frames with transport + VPN label stack during successful ICMP')
 for n in lab.topology()['nodes']:
  snap[n]={'routes':command(n,['ip','-4','route','show']),'interfaces':command(n,['ip','-d','link','show'])}
  if n.startswith('PE-') or n=='P-Core':
   snap[n]['lfib']=command(n,['ip','-f','mpls','route','show']);snap[n]['ospf']=vty(n,'show ip ospf neighbor')
 version=lab.run(['vtysh','-c','show version'],check=False).stdout
 result={'run':a.run,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':{'kernel':lab.run(['uname','-a']).stdout,'packages':lab.run(['apk','info','-v']).stdout,'frr':lab.run(['/usr/lib/frr/bgpd','--version']).stdout,'scope':'Linux namespaces inside QEMU on Windows; GNS3 project generated separately, not executed by this runner'},'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(lab.__file__),Path(__file__)]},'warmup':warmup,'fault':fault,'recovery':recovery,'cases':records,'snapshots':snap,'pcap_sha256':hashlib.sha256(capture.read_bytes()).hexdigest(),'status':'PASS' if records and all(r['status']=='PASS' for r in records) else 'FAIL'}
 (out/(a.run+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'run':a.run,'cases':len(records),'status':result['status'],'failures':[r['id'] for r in records if r['status']!='PASS']}),flush=True)

if __name__=='__main__':main()
