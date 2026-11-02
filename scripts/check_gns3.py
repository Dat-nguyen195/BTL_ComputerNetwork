#!/usr/bin/env python3
"""Validate portable topology, compiled source hashes and recorded real-packet evidence."""
from collections import Counter
import csv
import hashlib
from ipaddress import ip_interface
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'simulation/gns3'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    project=json.loads((BASE/'hospital-3sites.gns3').read_text())
    nodes={n['node_id']:n for n in project['topology']['nodes']}
    assert len(nodes)==52 and len({n['name'] for n in nodes.values()})==52
    assert len(project['topology']['links'])==52
    used=set()
    for link in project['topology']['links']:
        assert len(link['nodes'])==2
        for endpoint in link['nodes']:
            node=nodes[endpoint['node_id']]
            port=(endpoint['node_id'],endpoint['adapter_number'],endpoint['port_number'])
            assert port not in used and endpoint['port_number']==0
            assert 0<=endpoint['adapter_number']<node['properties']['adapters']
            used.add(port)
    roles=Counter();configs={}
    for node in nodes.values():
        config=json.loads((BASE/'runtime/config'/f"{node['name']}.json").read_text())
        roles[config['role']]+=1;configs[node['name']]=config
        assert config['adapters']==node['properties']['adapters']
    assert roles=={'router':9,'switch':5,'endpoint':38},roles
    with (ROOT/'simulation/generated/dhcp-pools.csv').open() as f:pools=list(csv.DictReader(f))
    dhcp_clients=[c for c in configs.values() if c.get('dhcp')]
    assert len(dhcp_clients)==19
    assert {str(ip_interface(c['interfaces']['eth0']).network) for c in dhcp_clients}=={p['network'] for p in pools}
    manifest=json.loads((BASE/'runtime-manifest.json').read_text())
    for name,expected in manifest['sha256'].items():assert digest(BASE/name)==expected,name
    for name,expected in manifest['source_sha256'].items():assert digest(ROOT/name)==expected,name
    latest=json.loads((ROOT/'test_results/runtime/after-webui-fix-runtime/results.json').read_text())
    validated=json.loads((ROOT/'test_results/runtime/validated-runtime/results.json').read_text())
    for run in (latest,validated):
        assert run['platform']['version']=='2.2.55'
        assert all(c['status']=='PASS' for c in run['cases'])
        groups={c['group'] for c in run['cases']}
        assert {'TC01','TC02','TC03','TC04','TC05','TC06','OSPF','DHCP-DNS','IDS-IPS'}<=groups
        assert run['project_id']==project['project_id']
    assert {'ISP-FAILOVER','ISP-BOTH-DOWN','ISP-RECOVERY','ISP-PBR','ISP-CONVERGENCE'}<={c['group'] for c in validated['cases']}
    for name,expected in latest['source_sha256'].items():assert digest(ROOT/name)==expected,name
    reopen=json.loads((ROOT/'test_results/runtime/persistence/reopen.json').read_text())
    assert reopen['status']=='PASS' and reopen['loaded_committed_template']
    assert reopen['project_sha256']==digest(BASE/'hospital-3sites.gns3')
    assert len(reopen['after_nodes'])==52 and all(status=='started' for _,status in reopen['after_nodes'])
    live=json.loads((ROOT/'test_results/runtime/persistence/live-provenance.json').read_text())
    assert live['status']=='PASS' and set(live['live_node_sha256'])==set(configs)
    for name,hashes in live['live_node_sha256'].items():
        assert hashes['/usr/local/bin/hospital-node']==digest(BASE/'runtime/node.py')
        assert hashes['/opt/hospital/config/'+name+'.json']==digest(BASE/'runtime/config'/f'{name}.json')
    browser=json.loads((ROOT/'test_results/web-ui/browser-results.json').read_text())
    assert browser['patch']['patch_version']==2 and browser['patch']['base_detector_guarded']
    assert {r['mode'] for r in browser['results']}=={'normal','embedded-electron'}
    assert all(r['status']=='PASS' and not r['page_errors'] and not r['has_node_require'] for r in browser['results'])
    capture=ROOT/'test_results/runtime/persistence/hospital-demo.pcap'
    assert capture.stat().st_size>100 and capture.read_bytes()[:4] in (b'\xd4\xc3\xb2\xa1',b'\xa1\xb2\xc3\xd4')
    print('OK: portable GNS3 52 nodes/52 links; 18 pools/19 clients; source/live hashes; 209 + 137 recorded checks; actual PCAP/reopen and Web UI browser regression')
    print('This checker validates recorded evidence; it does not rerun the GNS3 network.')

if __name__=='__main__':main()
