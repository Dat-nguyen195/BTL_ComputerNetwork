#!/usr/bin/env python3
"""Run actual GNS3 packet tests and save command output/provenance (never IOS evidence)."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
from gns3_lab import ROOT, PID, CONTROLLER, api, containers

CASES=[]
MAPPING={}
START=time.monotonic()


def execute(node,args):
    before=time.monotonic()
    r=subprocess.run(['docker','exec',CONTROLLER,'docker','exec',MAPPING[node],*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=40)
    return {'node':node,'command':args,'returncode':r.returncode,'output':r.stdout,'duration_seconds':round(time.monotonic()-before,3)}


def check(group,node,args,expect=True,contains=None,description=''):
    record=execute(node,args)
    passed=(record['returncode']==0)==expect
    if contains is not None:passed=passed and contains in record['output']
    record.update(group=group,expected='success' if expect else 'blocked/nonzero',description=description,status='PASS' if passed else 'FAIL')
    CASES.append(record)
    print(record['status'],group,node,description or ' '.join(args),flush=True)
    return record


def ping(group,source,dest):return check(group,source,['ping','-n','-c','2','-W','1',dest])


def http(group,source,dest,expect=True,contains=None):
    return check(group,source,['curl','--noproxy','*','--connect-timeout','2','--max-time','3','--fail','--silent','--show-error','http://'+dest],expect,contains)


def parallel(items):
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(lambda f:f(),items))


def health(expected):
    for _ in range(30):
        r=execute('Main-Edge',['cat','/tmp/edge-health.json'])
        if r['returncode']==0 and json.loads(r['output'])==expected:return
        time.sleep(1)
    raise RuntimeError('Edge health failed to converge to '+str(expected))


def converge(group, expected_public, since):
    attempts=[];deadline=time.monotonic()+45
    while time.monotonic()<deadline:
        sample=[execute(n,['curl','--noproxy','*','--connect-timeout','1','--max-time','2','--fail','--silent','--show-error','http://192.0.2.100']) for n in ('Main-PC10-A','Main-PC20','DBP-PC10','BHTQ-PC10','Main-Guest')]
        attempts.append(sample)
        if all(r['returncode']==0 and (expected_public is None or expected_public in r['output']) for r in sample):
            CASES.append({'group':group,'status':'PASS','expected':'five endpoints recover within a 45-second test budget; not a production SLA','convergence_seconds':round(time.monotonic()-since,3),'attempts':attempts})
            print('PASS',group,'end-to-end recovery',round(time.monotonic()-since,3),'seconds',flush=True);return
        time.sleep(1)
    CASES.append({'group':group,'status':'FAIL','expected':'five endpoints recover within test budget','attempts':attempts})


def smoke():
    parallel([lambda:ping('TC01','Main-PC10-A','10.10.10.11'),lambda:ping('TC01','Main-PC10-B','10.10.10.10'),lambda:ping('TC02','Main-PC10-A','10.10.20.10'),lambda:ping('TC02','Main-PC20','10.10.10.10'),lambda:http('TC02','Main-PC10-A','10.10.70.11',contains='Main-HIS')])
    parallel([lambda s=s,d=d:ping('TC03',s,d) for s,d in [('Main-PC10-A','10.20.10.10'),('DBP-PC10','10.10.10.10'),('Main-PC10-A','10.30.10.10'),('BHTQ-PC10','10.10.10.10'),('DBP-PC10','10.30.10.10'),('BHTQ-PC10','10.20.10.10')]])
    parallel([lambda s=s:http('TC04',s,'10.10.80.10',contains='Main-WebDMZ') for s in ('Main-PC10-A','DBP-PC10','BHTQ-PC10')]+[lambda:http('TC04','Web-Lab','198.51.100.2:8080',contains='Main-WebDMZ'),lambda:http('TC04','Web-Lab','198.51.100.2:8081',expect=False),lambda:http('TC04','Web-Lab','203.0.113.2:8080',expect=False)])
    # First prove that every guest has a functional route/DNS/Web path, then test isolation.
    parallel([lambda s=s:http('TC05',s,'web.hospital.test',contains='Web-Lab') for s in ('Main-Guest','DBP-Guest','BHTQ-Guest')])
    parallel([lambda s=s,d=d:http('TC05',s,d,expect=False) for s in ('Main-Guest','DBP-Guest','BHTQ-Guest') for d in ('10.10.70.11','10.10.80.10')]+[lambda s=s,d=d:check('TC05',s,['ping','-n','-c','1','-W','1',d],False) for s in ('Main-Guest','DBP-Guest','BHTQ-Guest') for d in ('10.10.10.10','10.20.10.10','10.30.10.10')])
    parallel([lambda s=s:http('TC06',s,'web.hospital.test',contains='Web-Lab') for s in ('Main-PC10-A','Main-PC20','DBP-PC10','BHTQ-PC10','Main-Guest','DBP-Guest','BHTQ-Guest')])


def main():
    global MAPPING
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--failover',action='store_true');p.add_argument('--run-name',default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'));a=p.parse_args()
    if not a.run_name.replace('-','').replace('T','').replace('Z','').isalnum():p.error('run-name must contain only letters/digits/hyphens')
    MAPPING=containers()
    out=ROOT/'test_results/runtime'/a.run_name;out.mkdir(parents=True,exist_ok=False)
    versions={n:execute(n,cmd) for n,cmd in [('Main-Core',['vtysh','-c','show version']),('Main-FW',['iptables','--version']),('Main-Infra',['dnsmasq','--version'])]}
    try:
        smoke()
        check('TC03','DBP-PC10',['traceroute','-I','-n','-m','10','-w','1','10.30.10.10'],contains='10.30.10.10')
        for node in ('Main-Core','Main-GW','DBP-GW','BHTQ-GW'):
            check('OSPF',node,['vtysh','-c','show ip ospf neighbor'],contains='Full/')
            check('OSPF',node,['vtysh','-c','show ip route ospf'],contains='O')
        configs=ROOT/'simulation/gns3/runtime/config'
        for path in sorted(configs.glob('*.json')):
            c=json.loads(path.read_text());n=c['name']
            if not c.get('dhcp'):continue
            check('DHCP-DNS',n,['ip','-4','-o','addr','show','eth0'],contains=c['interfaces']['eth0'])
            check('DHCP-DNS',n,['ip','route','show','default'],contains=c['gateway'])
            check('DHCP-DNS',n,['dig','+short','+tries=1','+time=1','@'+c['dns'],'web.hospital.test'],contains='192.0.2.100')
            check('DHCP-DNS',n,['cat','/tmp/dhclient.log'],contains='DHCPACK')
        for site in ('Main','DBP','BHTQ'):
            router='Main-Core' if site=='Main' else site+'-GW'
            r=check('TC05',router,['iptables','-nvx','-L',site.upper()+'-V100-IN'])
            # Confirm an actual DROP counter, not merely a failed client command.
            drops=[int(line.split()[0]) for line in r['output'].splitlines() if ' DROP ' in line]
            if not drops or sum(drops)==0:r['status']='FAIL'
        http('IDS-IPS','Main-PC10-A','10.10.80.10/hospital-ids-test',contains='Main-WebDMZ')
        http('IDS-IPS','Main-PC10-A','10.10.80.10/hospital-ips-test',expect=False)
        http('IDS-IPS','Main-PC10-A','10.10.80.10/',contains='Main-WebDMZ')
        check('IDS-IPS','Main-FW',['cat','/tmp/suricata/fast.log'],contains='1000001')
        check('IDS-IPS','Main-FW',['cat','/tmp/suricata/fast.log'],contains='1000002')
        check('IDS-IPS','Main-FW',['tail','-n','200','/tmp/suricata/eve.json'],contains='blocked')
        check('IDS-IPS','Main-Guest',['dig','+short','+tries=1','+time=1','@192.0.2.100','phishing-test.invalid'],contains='0.0.0.0')
        if a.failover:
            for n in ('Main-PC10-A','Main-PC20'):
                expected='203.0.113.2' if n=='Main-PC10-A' else '198.51.100.2'
                http('ISP-PBR',n,'192.0.2.100',contains=expected)
            # Faults are confined to interfaces inside this lab's nodes.
            for failed,expected,public in [('ISP1',[False,True],'198.51.100.2'),('ISP2',[True,False],'203.0.113.2')]:
                fault_started=time.monotonic()
                check('ISP-FAILOVER',failed,['ip','link','set','eth1','down'])
                try:
                    health(expected)
                    converge('ISP-CONVERGENCE',public,fault_started)
                    parallel([lambda n=n:http('ISP-FAILOVER',n,'192.0.2.100',contains=public) for n in ('Main-PC10-A','Main-PC20','DBP-PC10','BHTQ-PC10','Main-Guest')])
                    ping('ISP-FAILOVER','DBP-PC10','10.30.10.10')
                finally:
                    check('ISP-RECOVERY',failed,['ip','link','set','eth1','up']);health([True,True]);converge('ISP-RECOVERY',None,time.monotonic())
            check('ISP-BOTH-DOWN','ISP1',['ip','link','set','eth1','down']);check('ISP-BOTH-DOWN','ISP2',['ip','link','set','eth1','down'])
            try:
                health([False,False]);http('ISP-BOTH-DOWN','Main-PC10-A','192.0.2.100',expect=False)
                ping('ISP-BOTH-DOWN','DBP-PC10','10.30.10.10')
                time.sleep(7)
                r=check('ISP-BOTH-DOWN','DBP-GW',['ip','route','show','default'])
                if r['output'].strip():r['status']='FAIL'
            finally:
                check('ISP-RECOVERY','ISP1',['ip','link','set','eth1','up']);check('ISP-RECOVERY','ISP2',['ip','link','set','eth1','up']);health([True,True]);converge('ISP-RECOVERY',None,time.monotonic())
            smoke()
    except Exception as exc:
        CASES.append({'group':'HARNESS','status':'FAIL','error':repr(exc)})
    finally:
        captures={}
        versions['Suricata']=execute('Main-FW',['suricata','--build-info'])
        for n,cmd in [('Main-FW',['iptables-save','-c']),('Main-FW',['tail','-n','300','/tmp/suricata/eve.json']),('Main-FW',['cat','/tmp/suricata/hospital.rules']),('Main-Edge',['conntrack','-L']),('Main-Edge',['ip','rule','show']),('Main-Edge',['ip','route','show','table','101']),('Main-Edge',['ip','route','show','table','102']),('Main-Infra',['cat','/var/lib/misc/dnsmasq.leases']),('DBP-Infra',['cat','/var/lib/misc/dnsmasq.leases']),('BHTQ-Infra',['cat','/var/lib/misc/dnsmasq.leases'])]:
            captures[n+'-'+'-'.join(cmd)]=execute(n,cmd)
        hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'simulation/gns3/hospital-3sites.gns3',ROOT/'simulation/gns3/runtime-manifest.json',ROOT/'simulation/gns3/runtime/node.py',ROOT/'scripts/test_gns3_runtime.py']}
        image= subprocess.run(['docker','exec',CONTROLLER,'docker','image','inspect','hospital-netlab:20261102','--format','{{.Id}}'],text=True,capture_output=True).stdout.strip()
        data={'run_id':a.run_name,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'platform':api('/version'),'image_id':image,'project_id':PID,'source_sha256':hashes,'scope':'Actual GNS3 Linux/FRR/iptables/DHCP/DNS/HTTP; not Cisco IOS or clinical workload','duration_seconds':round(time.monotonic()-START,2),'versions':versions,'cases':CASES,'captures':captures}
        (out/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        groups={}
        for c in CASES:groups.setdefault(c['group'],[]).append(c['status'])
        summary={g:{'pass':v.count('PASS'),'fail':v.count('FAIL')} for g,v in groups.items()}
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(summary,indent=2),flush=True)
        if any(c['status']=='FAIL' for c in CASES):raise SystemExit(1)

if __name__=='__main__':main()
