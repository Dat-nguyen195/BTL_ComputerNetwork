#!/usr/bin/env python3
"""Generate an executable GNS3/FRR lab from the reviewed IOS and endpoint sources."""
import argparse
import csv
import hashlib
import json
import re
import uuid
from collections import defaultdict
from ipaddress import IPv4Interface
from pathlib import Path
from check_wan import load_node
from check_security import load_acls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'simulation/gns3'
IMAGE = 'hospital-netlab:20261102'
NAMESPACE = uuid.UUID('ecf4c2e9-8bb8-5c67-8cb9-ae7f9bd75e25')


def ident(name):
    return str(uuid.uuid5(NAMESPACE, name))


def csv_rows(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def acl_commands(name, rules, target='RETURN'):
    result = [['iptables', '-N', name]]
    for action, proto, src, sport, dst, dport, flags in rules:
        cmd = ['iptables', '-A', name, '-s', str(src), '-d', str(dst)]
        if proto != 'ip':
            cmd += ['-p', proto]
        if sport is not None:
            cmd += ['--sport', str(sport)]
        if dport is not None:
            cmd += ['--dport', str(dport)]
        for flag in ('echo', 'echo-reply'):
            if flag in flags:
                cmd += ['--icmp-type', 'echo-request' if flag == 'echo' else flag]
        if 'established' in flags:
            # IOS 'established' checks ACK or RST, not connection tracking.
            for flag in ('ACK', 'RST'):
                result.append(cmd + ['--tcp-flags', flag, flag, '-j', target if action == 'permit' else 'DROP'])
        else:
            result.append(cmd + ['-j', target if action == 'permit' else 'DROP'])
    result.append(['iptables', '-A', name, '-j', 'DROP'])
    return result


def artifacts():
    routers = {p.stem: load_node(p) for p in sorted((ROOT/'simulation/generated/configs').glob('*.cfg'))}
    endpoints = csv_rows(ROOT/'simulation/lab/endpoints.csv')
    cables = csv_rows(ROOT/'simulation/lab/cabling.csv')
    ports = csv_rows(ROOT/'simulation/generated/switch-ports.csv')
    pools = csv_rows(ROOT/'simulation/generated/dhcp-pools.csv')
    adapters = defaultdict(dict)
    links = []
    switch_ports = defaultdict(list)
    def port(node, interface):
        if node in routers:
            if interface not in adapters[node]:
                adapters[node][interface] = len(adapters[node])
            return adapters[node][interface]
        return 0
    for c in cables:
        ends = []
        for side in ('a','b'):
            name, iface = c['node_'+side], c['interface_'+side]
            p = port(name,iface)
            ends.append({'node_id':ident(name),'adapter_number':p if name in routers else 0,
                         'port_number':0 if name in routers else p})
            if name.endswith('-Access'):
                trunk = 'trunk' in c['mode']
                vlan = 80 if name=='DMZ-Access' else 1
                switch_ports[name].append({'name':'uplink','port_number':0,'type':'dot1q' if trunk else 'access','vlan':vlan})
        links.append({'link_id':ident(c['link']),'nodes':ends})
    for p in ports:
        number = int(p['interface'].split('/')[-1])
        switch_ports[p['switch']].append({'name':p['endpoint'],'port_number':number,'type':'access','vlan':int(p['vlan'])})
        links.append({'link_id':ident('endpoint-'+p['endpoint']), 'nodes':[
            {'node_id':ident(p['switch']),'adapter_number':0,'port_number':number},
            {'node_id':ident(p['endpoint']),'adapter_number':0,'port_number':0}]})
    configs = {}
    for name, router in routers.items():
        interface_map = {ios:'eth'+str(n) for ios,n in adapters[name].items()}
        interface_map.update({ios:'lo' if ios.startswith('Loopback') else interface_map[ios.split('.')[0]]+'.'+ios.split('.')[1]
                              for ios in router.interfaces if ios not in interface_map})
        interfaces = {interface_map[ios]:str(ip) for ios,ip in router.interfaces.items()}
        commands = []
        acls = load_acls(router.text)
        if name in ('Main-Core','DBP-GW','BHTQ-GW'):
            for acl,rules in acls.items():
                commands += acl_commands(acl,rules)
            current=None
            for line in router.text.splitlines():
                if line.startswith('interface '): current=line.split()[1]
                elif line.startswith(' ip access-group '):
                    acl=line.split()[2]; iface=interface_map[current]
                    for chain in ('INPUT','FORWARD'):
                        commands.append(['iptables','-A',chain,'-i',iface,'-j',acl])
        frr=['frr defaults traditional',f'hostname {name}','service integrated-vtysh-config','log file /tmp/frr.log']
        active=[]
        for ios,iface in interface_map.items():
            if ios.startswith('Serial') or (name in ('Main-Core','Main-GW') and ios in ('GigabitEthernet0/1','GigabitEthernet0/0') and interfaces.get(iface,'').startswith('10.255.0.')):
                active.append(iface)
        if name in ('Main-Core','Main-GW','DBP-GW','BHTQ-GW'):
            for iface in active:
                frr += [f'interface {iface}',' ip ospf network point-to-point',' ip ospf hello-interval 1',' ip ospf dead-interval 4',' ip ospf cost '+('10' if name!='Main-Core' and '10.255.0.8/' not in interfaces.get(iface,'') and interfaces.get(iface,'').split('/')[0] not in ('10.255.0.10',) else '1')]
            rid = str(router.interfaces['Loopback0'].ip)
            frr += ['router ospf',f' ospf router-id {rid}',' passive-interface default']
            frr += [' no passive-interface '+iface for iface in active]
            frr += [f' network {ip} area 0' for iface,ip in interfaces.items() if iface!='lo' or ip.startswith('10.')]
            if name=='Main-GW': frr += [' default-information originate metric 10']
            if name=='Main-Core': frr += [' redistribute static route-map DMZ-ONLY','exit','ip prefix-list DMZ-PREFIX seq 5 permit 10.10.80.0/27','route-map DMZ-ONLY permit 10',' match ip address prefix-list DMZ-PREFIX','exit']
        for route in router.routes:
            if route.track: continue
            # All pinned probes and fallback discard routes remain explicit.
            hop = 'Null0' if route.interface=='Null0' else route.hop
            frr.append(f'ip route {route.net} {hop} {route.distance}')
        if name=='Main-FW':
            commands += [['iptables','-P','FORWARD','DROP'],['iptables','-A','FORWARD','-m','conntrack','--ctstate','ESTABLISHED,RELATED','-j','ACCEPT']]
            for src,dst,acl in [('eth0','eth1','FW-INTERNET'),('eth0','eth2','FW-LAN-DMZ'),('eth1','eth2','FW-PUBLISHED-WEB'),('eth2','eth1','FW-DMZ-UPDATE')]:
                commands += acl_commands(acl,acls[acl],target='ACCEPT')
                commands += [['iptables','-A','FORWARD','-i',src,'-o',dst,'-j',acl]]
        config={'loopbacks':[str(ip) for ios,ip in router.interfaces.items() if ios.startswith('Loopback')],'name':name,'role':'router','interfaces':interfaces,'interface_map':interface_map,'commands':commands,'frr':'\n'.join(frr)+'\n','adapters':len(adapters[name])}
        if name in ('Main-Core','Main-GW'):
            config['health_default']={'target':'192.0.2.100','source':str(router.interfaces['Loopback0'].ip),'gateway':'10.255.0.14' if name=='Main-Core' else '10.255.0.9'}
        if name=='Main-Edge':
            config['edge']=True
            # The PBR source groups are taken from the reviewed IOS ACLs.
            config['pbr']={k:[str(src) for action,src,dst in router.acls[k] if action=='permit'] for k in ('101','102')}
        if name in ('Main-Core','DBP-GW','BHTQ-GW'):
            site='Main' if name=='Main-Core' else name.split('-')[0]
            config['relay']={'server':next(p['server'] for p in pools if p['site']==site),
                             'interfaces':[interface_map['GigabitEthernet0/0.'+p['vlan']] for p in pools if p['site']==site]+[interface_map['GigabitEthernet0/0.70']]}
        configs[name]=config
    hosts={e['node']:e['ip'] for e in endpoints}
    for e in endpoints:
        name=e['node']; mac='02:'+':'.join(f'{b:02x}' for b in uuid.UUID(ident(name)).bytes[-5:])
        config={'name':name,'role':'endpoint','interfaces':{'eth0':e['ip']+'/'+e['prefix']},'gateway':e['gateway'],'dns':e['dns'],'mac':mac,'adapters':1,'services':e['services']}
        if e['kind']=='client-dhcp-example': config['dhcp']=True
        if name.endswith('-Infra') or name=='Web-Lab':
            lines=['no-resolv','no-hosts','bind-interfaces','interface=eth0','log-dhcp','log-queries','user=root']
            lines += [f'address=/{host.lower()}.hospital.test/{ip}' for host,ip in sorted(hosts.items())]
            lines += ['address=/phishing-test.invalid/0.0.0.0','address=/web.hospital.test/192.0.2.100','address=/portal.hospital.test/10.10.80.10']
            if name.endswith('-Infra'):
                lines+=['dhcp-authoritative']
                for p in pools:
                    if p['site']!=e['site']:continue
                    tag=p['name'];lines += [f"dhcp-range=set:{tag},{p['start']},{p['end']},{p['mask']},1h",f"dhcp-option=tag:{tag},option:router,{p['gateway']}",f"dhcp-option=tag:{tag},option:dns-server,{p['dns']}"]
                for client in endpoints:
                    if client['site']==e['site'] and client['kind']=='client-dhcp-example':
                        cmac='02:'+':'.join(f'{b:02x}' for b in uuid.UUID(ident(client['node'])).bytes[-5:])
                        lines.append(f"dhcp-host={cmac},{client['ip']},{client['node']},1h")
            config['dnsmasq']='\n'.join(lines)+'\n'
        configs[name]=config
    for name, entries in switch_ports.items():
        configs[name]={'name':name,'role':'switch','interfaces':{},'adapters':max(p['port_number'] for p in entries)+1,'ports':entries}
    switch_ids={ident(name) for name in switch_ports}
    for link in links:
        for end in link['nodes']:
            if end['node_id'] in switch_ids:
                end['adapter_number']=end['port_number'];end['port_number']=0
    nodes=[]
    xy={'Main-GW':(0,-180),'Main-Core':(0,0),'Main-FW':(0,180),'Main-Edge':(0,360),'DBP-GW':(-650,-180),'BHTQ-GW':(650,-180),'ISP1':(-180,520),'ISP2':(180,520),'INET-Core':(0,700),'Main-Access':(-180,0),'DBP-Access':(-650,0),'BHTQ-Access':(650,0),'DMZ-Access':(220,180),'Web-Access':(0,850)}
    idx=defaultdict(int)
    for name in [*routers,*switch_ports,*[e['node'] for e in endpoints]]:
        if name in configs:
            props={'image':IMAGE,'adapters':configs[name]['adapters'],'environment':'LAB_NODE='+name,'start_command':'python3 /usr/local/bin/hospital-node'}
            kind='docker';symbol=':/symbols/router.svg' if name in routers else ':/symbols/ethernet_switch.svg' if name in switch_ports else ':/symbols/computer.svg'
        else:
            props={'ports_mapping':switch_ports[name]};kind='ethernet_switch';symbol=':/symbols/ethernet_switch.svg'
        if name in xy:x,y=xy[name]
        else:
            ep=next(e for e in endpoints if e['node']==name)
            group=ep['site'] if ep['vlan']!='80' else 'DMZ'; n=idx[group];idx[group]+=1
            base={'Main':(-450,0),'DBP':(-850,0),'BHTQ':(850,0),'DMZ':(450,180),'Internet':(0,1000)}[group]
            x,y=base[0]+(n%3)*140,base[1]+100+(n//3)*100
        nodes.append({'node_id':ident(name),'name':name,'node_type':kind,'compute_id':'local','console_type':'telnet' if kind=='docker' else 'none','symbol':symbol,'x':x,'y':y,'properties':props,'label':{'text':name,'x':0,'y':-25}})
    project={'name':'Hospital-3Sites-FRR','project_id':ident('project'),'version':'2.2.55','type':'topology','revision':9,'auto_start':False,'auto_close':False,'auto_open':False,'zoom':65,'scene_width':2400,'scene_height':2200,'topology':{'nodes':nodes,'links':links,'drawings':[],'computes':[]}}
    output={'hospital-3sites.gns3':json.dumps(project,indent=2)+'\n'}
    output.update({'runtime/config/'+n+'.json':json.dumps(c,indent=2)+'\n' for n,c in sorted(configs.items())})
    source_paths=[*sorted((ROOT/'simulation/generated/configs').glob('*.cfg')),ROOT/'simulation/lab/endpoints.csv',ROOT/'simulation/lab/cabling.csv',ROOT/'scripts/build_gns3.py',OUT/'runtime/node.py',OUT/'runtime/Dockerfile',OUT/'controller/Dockerfile',OUT/'controller/start.sh',OUT/'controller/patch_web_ui.py']
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    output['runtime-manifest.json']=json.dumps({'source_sha256':source_hashes,'image':IMAGE,'platform':'GNS3 2.2.55 / FRR / Linux; not Cisco IOS','sha256':{p:hashlib.sha256(s.encode()).hexdigest() for p,s in sorted(output.items())}},indent=2)+'\n'
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    stale=[]
    for rel,content in artifacts().items():
        path=OUT/rel
        if args.check:
            if not path.exists() or path.read_text()!=content:stale.append(rel)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    if stale:parser.exit(1,'Stale GNS3 artifacts: '+', '.join(stale)+'\n')
    print('OK: GNS3 project, 9 FRR/Linux routers, 5 VLAN switches, 38 endpoints, compiled ACLs/DHCP and source manifest')

if __name__=='__main__':main()
