#!/usr/bin/env python3
"""Real Linux packet forwarding/services inside isolated GNS3 Docker nodes."""
import http.server
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
import time


def run(*args, check=True):
    return subprocess.run(list(args), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)


def start(args, log):
    return subprocess.Popen(args, stdout=open('/tmp/'+log,'a'), stderr=subprocess.STDOUT)


def vty(command):
    return run('vtysh','-c','configure terminal','-c',command)


def health_default(config):
    h=config['health_default'];last=None;success=0;failure=0
    while True:
        up=run('ping','-n','-c','1','-W','1','-I',h['source'],h['target'],check=False).returncode==0
        success=success+1 if up else 0;failure=failure+1 if not up else 0
        state=True if success>=2 else False if failure>=2 else last
        if state!=last and state is not None:
            vty(('' if state else 'no ')+f"ip route 0.0.0.0/0 {h['gateway']}")
            print('DEFAULT_HEALTH',state,flush=True);last=state
        time.sleep(2)


def edge(config):
    run('ip','rule','add','priority','50','to','10.0.0.0/8','lookup','main')
    for group,networks in config['pbr'].items():
        for i,net in enumerate(networks):
            run('ip','rule','add','priority',str(int(group)*100+i),'from',net,'lookup',group)
    for interface in ('eth1','eth2'):
        run('iptables','-t','nat','-A','POSTROUTING','-s','10.0.0.0/8','!','-d','10.0.0.0/8','-o',interface,'-j','MASQUERADE')
    run('iptables','-t','nat','-A','PREROUTING','-i','eth2','-d','198.51.100.2','-p','tcp','--dport','8080','-j','DNAT','--to-destination','10.10.80.10:80')
    previous=None; good=[0,0];bad=[0,0];state=[False,False]
    while True:
        for i,(target,interface) in enumerate((('192.0.2.11','eth1'),('192.0.2.22','eth2'))):
            up=run('ping','-n','-c','1','-W','1','-I',interface,target,check=False).returncode==0
            good[i]=good[i]+1 if up else 0;bad[i]=bad[i]+1 if not up else 0
            if good[i]>=2:state[i]=True
            if bad[i]>=2:state[i]=False
        if state!=previous:
            for table,order in [('101',(0,1)),('102',(1,0))]:
                choice=next((i for i in order if state[i]),None)
                if choice is None:
                    run('ip','route','replace','unreachable','default','table',table)
                else:
                    run('ip','route','replace','default','via',('203.0.113.1','198.51.100.1')[choice],'dev','eth'+str(choice+1),'table',table)
            # Main table is used for router-originated traffic and private RIB lookups.
            run('ip','route','del','default',check=False)
            choice=next((i for i in (0,1) if state[i]),None)
            if choice is not None:run('ip','route','replace','default','via',('203.0.113.1','198.51.100.1')[choice])
            Path('/tmp/edge-health.json').write_text(json.dumps(state))
            print('ISP_HEALTH',state,flush=True);previous=list(state)
        time.sleep(2)


def http_service(config):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            data=json.dumps({'node':config['name'],'client':self.client_address[0],'path':self.path,'application':'HTTP demonstration; not clinical software'}).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    http.server.ThreadingHTTPServer(('0.0.0.0',80),Handler).serve_forever()


def main():
    config=json.loads(Path('/opt/hospital/config/'+os.environ['LAB_NODE']+'.json').read_text())
    for i in range(config['adapters']):
        for attempt in range(120):
            if Path('/sys/class/net/eth'+str(i)).exists():break
            time.sleep(.5)
        else:raise RuntimeError('GNS3 interface missing')
    run('ip','link','set','lo','up')
    run('sysctl','-w','net.ipv4.conf.all.rp_filter=0','net.ipv4.conf.default.rp_filter=0')
    for i in range(config['adapters']):
        run('ip','link','set','eth'+str(i),'up')
        run('sysctl','-w','net.ipv4.conf.eth'+str(i)+'.rp_filter=0')
    if config.get('mac'):run('ip','link','set','eth0','address',config['mac'])
    for iface,address in config['interfaces'].items():
        if '.' in iface:
            base,vlan=iface.split('.')
            run('ip','link','add','link',base,'name',iface,'type','vlan','id',vlan)
            run('ip','link','set',iface,'up')
        if not config.get('dhcp'):run('ip','address','add',address,'dev',iface)
    for address in config.get('loopbacks',[]):run('ip','address','replace',address,'dev','lo')
    if config['role']=='switch':
        run('ip','link','add','br0','type','bridge','vlan_filtering','1')
        run('ip','link','set','br0','up')
        vlans={p['vlan'] for p in config['ports'] if p['type']=='access'}
        # Include configured site VLANs even when no representative host is attached.
        if config['name'] in ('Main-Access','DBP-Access','BHTQ-Access'):
            vlans.update((10,20,30,70,90,100,110,120))
            if config['name']=='Main-Access':vlans.update((40,50,60))
        for p in config['ports']:
            iface='eth'+str(p['port_number'])
            run('ip','link','set',iface,'master','br0')
            run('bridge','vlan','del','dev',iface,'vid','1')
            for vlan in sorted(vlans if p['type']=='dot1q' else {p['vlan']}):
                cmd=['bridge','vlan','add','dev',iface,'vid',str(vlan)]
                if p['type']=='access':cmd+=['pvid','untagged']
                run(*cmd)
    elif config['role']=='router':
        run('sysctl','-w','net.ipv4.ip_forward=1')
        for command in config['commands']:run(*command)
        Path('/etc/frr/frr.conf').write_text(config['frr'])
        Path('/etc/frr/daemons').write_text('zebra=yes\nospfd=yes\nstaticd=yes\nvtysh_enable=yes\nzebra_options=" -A 127.0.0.1 -s 90000000"\nospfd_options=" -A 127.0.0.1"\nstaticd_options=" -A 127.0.0.1"\n')
        run('chown','frr:frr','/etc/frr/frr.conf')
        run('/usr/lib/frr/frrinit.sh','start')
        if config['name']=='Main-FW':
            directory=Path('/tmp/suricata');directory.mkdir(exist_ok=True)
            rules=directory/'hospital.rules'
            rules.write_text('alert http any any -> 10.0.0.0/8 any (msg:"Hospital lab IDS marker"; flow:established,to_server; http.uri; content:"/hospital-ids-test"; sid:1000001; rev:1;)\n'
                             'drop http any any -> 10.0.0.0/8 any (msg:"Hospital lab IPS marker blocked"; flow:established,to_server; http.uri; content:"/hospital-ips-test"; sid:1000002; rev:1;)\n')
            run('suricata','-T','-S',str(rules),'-l',str(directory))
            run('suricata','-D','-q','0','--runmode','workers','-S',str(rules),'-l',str(directory),
                '--set','nfq.mode=repeat','--set','nfq.repeat-mark=1','--set','nfq.repeat-mask=1',
                '--set','stream.inline=yes','--set','max-pending-packets=1024')
            time.sleep(1)
            run('kill','-0',Path('/var/run/suricata.pid').read_text().strip())
            # Repeat verdict marks the packet and reinjects it through the firewall.
            # IPS acceptance therefore cannot bypass the subsequent zone policies.
            run('iptables','-I','FORWARD','1','-m','mark','!','--mark','1/1','-j','NFQUEUE','--queue-num','0')
        if config.get('relay'):
            r=config['relay'];args=['dhcrelay','-4','-d']
            for iface in r['interfaces']:args+=['-i',iface]
            start(args+[r['server']],'dhcrelay.log')
        for key,func in [('health_default',health_default),('edge',edge)]:
            if config.get(key):threading.Thread(target=func,args=(config,),daemon=True).start()
    else:
        if config.get('dnsmasq'):
            Path('/tmp/dnsmasq.conf').write_text(config['dnsmasq']);Path('/var/lib/misc').mkdir(exist_ok=True)
            start(['dnsmasq','--keep-in-foreground','--conf-file=/tmp/dnsmasq.conf','--log-facility=-'],'dnsmasq.log')
        if config.get('dhcp'):
            start(['dhclient','-4','-v','-d','eth0'],'dhclient.log')
        else:run('ip','route','replace','default','via',config['gateway'])
        Path('/etc/resolv.conf').write_text('nameserver '+config['dns']+'\n')
        if 'HTTP' in config['services']:
            threading.Thread(target=http_service,args=(config,),daemon=True).start()
    Path('/tmp/hospital-ready').write_text(config['name'])
    print('READY',config['name'],flush=True)
    while True:signal.pause()


if __name__=='__main__':main()
