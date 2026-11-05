#!/usr/bin/env python3
"""Hospital MPLS L3VPN supplement: shared node configuration for Linux namespaces/GNS3."""
import argparse, hashlib, http.server, json, os, signal, socket, subprocess, sys, threading, time, shutil
from pathlib import Path

PREFIX='hospmpls-'
SITES=['Main','DBP','BHTQ']

def topology():
    nodes={};links=[]
    def node(n,role,**kw):nodes[n]={'name':n,'role':role,'interfaces':{},'commands':[], 'configs':{},**kw}
    def link(a,ai,addr,b,bi,baddr):
        nodes[a]['interfaces'][ai]=addr;nodes[b]['interfaces'][bi]=baddr;links.append([a,ai,b,bi])
    node('P-Core','p',rid='172.31.255.4')
    for i,site in enumerate(SITES,1):
        node('PE-'+site,'pe',rid=f'172.31.255.{i}',index=i)
        node('CE-'+site,'ce',rid=f'10.{i*10}.255.2',index=i)
        node('PC-'+site,'pc',index=i)
        link('PE-'+site,'eth0',f'172.31.0.{(i-1)*4+1}/30','P-Core','eth'+str(i-1),f'172.31.0.{(i-1)*4+2}/30')
        link('PE-'+site,'eth1',f'172.30.0.{(i-1)*4+1}/30','CE-'+site,'eth0',f'172.30.0.{(i-1)*4+2}/30')
        link('CE-'+site,'eth1',f'10.{i*10}.10.1/25','PC-'+site,'eth0',f'10.{i*10}.10.10/25')
    node('Web-Lab','web',rid='192.0.2.100')
    link('CE-Main','eth2','198.51.100.2/30','Web-Lab','eth0','198.51.100.1/30')
    for n,c in nodes.items():
        commands=c['commands'];role=c['role'];idx=c.get('index',0)
        if role in ('p','pe','ce'):
            commands += [['sysctl','-w','net.ipv4.ip_forward=1']]
        if role in ('p','pe'):
            commands += [['sysctl','-w','net.mpls.platform_labels=100000']]
            for iface in [x for x in c['interfaces'] if x!='eth1' or role=='p']:
                commands += [['sysctl','-w',f'net.mpls.conf.{iface}.input=1']]
            ospf=['hostname '+n,'interface lo',' ip ospf area 0','exit']
            for iface in [x for x in c['interfaces'] if x!='eth1' or role=='p']:
                ospf += ['interface '+iface,' ip ospf area 0',' ip ospf network point-to-point',' ip ospf hello-interval 1',' ip ospf dead-interval 4','exit']
            ospf += ['router ospf',' ospf router-id '+c['rid'],' passive-interface lo','exit']
            c['configs']['ospfd']='\n'.join(ospf)+'\n'
            ld=['hostname '+n,'mpls ldp',' router-id '+c['rid'],' address-family ipv4','  discovery transport-address '+c['rid']]
            for iface in [x for x in c['interfaces'] if x!='eth1' or role=='p']:ld+=['  interface '+iface,'  exit']
            ld+=[' exit-address-family','exit'];c['configs']['ldpd']='\n'.join(ld)+'\n'
        if role=='pe':
            # These commands precede address assignment in setup_node().
            commands += [['ip','link','add','HOSPITAL','type','vrf','table','1001'],['ip','link','set','HOSPITAL','up'],['ip','link','set','eth1','master','HOSPITAL']]
            b=['hostname '+n,'router bgp 65000',' bgp router-id '+c['rid'],' no bgp default ipv4-unicast']
            for j in range(1,4):
                if j!=idx:b += [f' neighbor 172.31.255.{j} remote-as 65000',f' neighbor 172.31.255.{j} update-source lo']
            b += [' address-family ipv4 vpn']
            for j in range(1,4):
                if j!=idx:b += [f'  neighbor 172.31.255.{j} activate']
            b += [' exit-address-family','exit',f'router bgp 65000 vrf HOSPITAL',' bgp router-id '+c['rid'],' no bgp ebgp-requires-policy',f' neighbor 172.30.0.{(idx-1)*4+2} remote-as {65100+idx}',' address-family ipv4 unicast',f'  rd vpn export 65000:{idx}','  rt vpn both 65000:100','  label vpn export auto','  nexthop vpn export '+c['rid'],'  import vpn','  export vpn',' exit-address-family','exit']
            c['configs']['bgpd']='\n'.join(b)+'\n'
        if role=='ce':
            hop=f'172.30.0.{(idx-1)*4+1}'
            b=['hostname '+n,f'router bgp {65100+idx}',' bgp router-id '+c['rid'],' no bgp ebgp-requires-policy',f' neighbor {hop} remote-as 65000',' address-family ipv4 unicast',f'  network 10.{idx*10}.10.0/25']
            if n=='CE-Main':
                b += [f'  neighbor {hop} default-originate']
                commands += [['ip','route','add','default','via','198.51.100.1'],['iptables','-t','nat','-A','POSTROUTING','-s','10.0.0.0/8','!','-d','10.0.0.0/8','-o','eth2','-j','MASQUERADE']]
            b+=[' exit-address-family','exit'];c['configs']['bgpd']='\n'.join(b)+'\n'
        if role=='pc':commands += [['ip','route','add','default','via',f'10.{idx*10}.10.1']]
        if role in ('p','pe','ce'):c['configs']['zebra']='hostname '+n+'\n'
    return {'name':'Hospital-MPLS-L3VPN','asn':65000,'rt':'65000:100','nodes':nodes,'links':links}


def run(args,ns=None,check=True,timeout=30):
    if ns:args=['ip','netns','exec',PREFIX+ns]+args
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
    if check and p.returncode:raise RuntimeError(str(args)+'\n'+p.stdout)
    return p


def setup_node(c,work,ns=None):
    n=c['name'];r=lambda a,check=True:run(a,ns,check)
    r(['ip','link','set','lo','up'])
    r(['sysctl','-w','net.ipv4.conf.all.rp_filter=0','net.ipv4.conf.default.rp_filter=0'])
    if c.get('rid'):r(['ip','addr','add',c['rid']+'/32','dev','lo'])
    # Create/assign VRF before putting CE-facing addresses into it.
    early=[x for x in c['commands'] if x[:2]==['ip','link']]
    for a in early:r(a)
    for iface,addr in c['interfaces'].items():
        r(['ip','link','set',iface,'up']);r(['ip','addr','add',addr,'dev',iface]);r(['sysctl','-w',f'net.ipv4.conf.{iface}.rp_filter=0'])
    for a in c['commands']:
        if a not in early:r(a)
    d=work/n;d.mkdir(parents=True,exist_ok=True);shutil.chown(d,user='frr',group='frr')
    for daemon,conf in c['configs'].items():
        (d/(daemon+'.conf')).write_text(conf)
    rundir=Path('/run/frr')/(PREFIX+n);rundir.mkdir(parents=True,exist_ok=True);shutil.chown(rundir,user='frr',group='frr')
    state=Path('/lib/frr')/(PREFIX+n);state.mkdir(parents=True,exist_ok=True);shutil.chown(state,user='frr',group='frr')
    confdir=Path('/etc/frr')/(PREFIX+n);confdir.mkdir(parents=True,exist_ok=True)
    (confdir/'frr.conf').write_text('hostname '+n+'\n');(confdir/'vtysh.conf').write_text('')
    for daemon in ['zebra','ospfd','ldpd','bgpd']:
        if daemon in c['configs']:
            args=['/usr/lib/frr/'+daemon,'-d','-N',PREFIX+n,'-u','frr','-g','frr','-f',str(d/(daemon+'.conf')),'-i',str(rundir/(daemon+'.pid')),'--log','file:'+str(d/(daemon+'.log'))]
            if ns:args=['ip','netns','exec',PREFIX+ns]+args
            # Daemon children may retain stderr: a PIPE makes communicate() wait
            # forever for EOF even after the launcher has exited successfully.
            with (d/(daemon+'-startup.log')).open('a') as log:
                subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=30)

    if c['role']=='web':
        subprocess.Popen((['ip','netns','exec',PREFIX+n] if ns else [])+[sys.executable,str(Path(__file__).resolve()),'http'],stdout=open(d/'http.log','w'),stderr=subprocess.STDOUT)


def cleanup(t):
    # Only namespaces created with this lab's fixed names; never the guest's eth0.
    for n in t['nodes']:
        ns=PREFIX+n
        p=run(['ip','netns','pids',ns],check=False)
        if p.returncode==0:
            for pid in p.stdout.split():
                try:os.kill(int(pid),signal.SIGTERM)
                except ProcessLookupError:pass
            run(['ip','netns','del',ns])
    # Recover only the exact veth names reserved by this isolated lab if a prior
    # creation was interrupted before moving both ends into their namespaces.
    for i in range(len(t['links'])):
        for end in ('a','b'):run(['ip','link','del','hm'+str(i)+end],check=False)


def create(t,work):
    existing=run(['ip','netns','list']).stdout
    if any(PREFIX+n+' ' in existing for n in t['nodes']):raise RuntimeError('Lab namespace already exists; use cleanup explicitly')
    for module in ['mpls_router','mpls_iptunnel','vrf']:run(['modprobe',module])
    for n in t['nodes']:
        run(['ip','netns','add',PREFIX+n]);print('namespace',n,flush=True)
    for i,(a,ai,b,bi) in enumerate(t['links']):
        x,y='hm'+str(i)+'a','hm'+str(i)+'b'
        run(['ip','link','add',x,'type','veth','peer','name',y])
        for v,n,iface in [(x,a,ai),(y,b,bi)]:
            run(['ip','link','set',v,'netns',PREFIX+n]);run(['ip','link','set',v,'name',iface],n)
    for c in t['nodes'].values():
        print('configure',c['name'],flush=True);setup_node(c,work,c['name'])
    print('CREATE_COMPLETE',flush=True)


def serve_http():
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            b=json.dumps({'node':'Web-Lab','client':self.client_address[0],'path':self.path}).encode();self.send_response(200);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    http.server.ThreadingHTTPServer(('0.0.0.0',80),Handler).serve_forever()


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['generate','create','cleanup','http','node']);p.add_argument('--work',default='/tmp/hospital-mpls');p.add_argument('--name');a=p.parse_args();t=topology();work=Path(a.work)
    if a.action=='generate':
        work.mkdir(parents=True,exist_ok=True);(work/'topology.json').write_text(json.dumps(t,indent=2)+'\n');print('Generated',len(t['nodes']),'nodes',len(t['links']),'links')
    elif a.action=='create':create(t,work)
    elif a.action=='cleanup':cleanup(t)
    elif a.action=='node':
        setup_node(t['nodes'][a.name],work)
        while True:time.sleep(30)
    else:serve_http()

if __name__=='__main__':main()
