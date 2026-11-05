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
    latest=json.loads((ROOT/'test_results/runtime/after-firewall-restart-runtime/results.json').read_text())
    validated=json.loads((ROOT/'test_results/runtime/validated-runtime/results.json').read_text())
    for run in (latest,validated):
        assert run['platform']['version']=='2.2.55'
        assert all(c['status']=='PASS' for c in run['cases'])
        groups={c['group'] for c in run['cases']}
        assert {'TC01','TC02','TC03','TC04','TC05','TC06','OSPF','DHCP-DNS','IDS-IPS'}<=groups
        assert run['project_id']==project['project_id']
    assert {'ISP-FAILOVER','ISP-BOTH-DOWN','ISP-RECOVERY','ISP-PBR','ISP-CONVERGENCE'}<={c['group'] for c in validated['cases']}
    # Keep the original tested manifest intact when only the build tool changes.
    # Runtime products and executable sources must still match the tested bytes.
    tested_path=ROOT/'test_results/runtime/persistence/runtime-manifest-tested.json'
    tested=json.loads(tested_path.read_text(encoding='utf-8'))
    assert digest(tested_path)==latest['source_sha256']['simulation/gns3/runtime-manifest.json']
    assert tested['sha256']==manifest['sha256'],'Runtime products differ from the tested build; rerun the lab'
    changed_sources={name for name in set(tested['source_sha256'])|set(manifest['source_sha256'])
                     if tested['source_sha256'].get(name)!=manifest['source_sha256'].get(name)}
    assert changed_sources <= {'scripts/build_gns3.py', 'simulation/gns3/controller/start.sh'},changed_sources
    if 'simulation/gns3/controller/start.sh' in changed_sources:
        # A controller lifecycle fix needs fresh runtime evidence; it cannot be
        # justified by the historical manifest whose node products are unchanged.
        proof=json.loads((ROOT/'test_results/runtime/controller-restart/restart.json').read_text())
        assert proof['status']=='PASS' and len(proof['cycles'])==2
        for name,expected in proof['source_sha256'].items():assert digest(ROOT/name)==expected,name
        for name,expected in proof['sha256'].items():assert digest(ROOT/name)==expected,name
        assert proof['live_controller_sha256']==digest(BASE/'controller/start.sh')
        for cycle in proof['cycles']:
            assert len(cycle['nodes'])==52 and all(s=='started' for _,s in cycle['nodes'])
            assert cycle['docker_info_returncode']==0
        for index,name in enumerate(proof['runs']):
            fresh=json.loads((ROOT/name).read_text())
            assert fresh['project_id']==project['project_id'] and fresh['platform']['version']=='2.2.55'
            assert all(c['status']=='PASS' for c in fresh['cases'])
            assert len(fresh['cases'])==(209 if index==0 else 137)
            for source,expected in fresh['source_sha256'].items():assert digest(ROOT/source)==expected,source
        print('OK current controller: 2 successful boots, 209 live checks and 137 checks after controller restart')
    for name,expected in latest['source_sha256'].items():
        if name=='simulation/gns3/runtime-manifest.json':continue
        assert digest(ROOT/name)==expected,name
    restart=json.loads((ROOT/'test_results/runtime/firewall-restart/restart.json').read_text())
    assert restart['status']=='PASS' and restart['source_sha256']==digest(BASE/'runtime/node.py')
    assert len(restart['cycles'])==2 and all(c['status']=='PASS' and c['live_suricata_process_check']==0 for c in restart['cycles'])
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
    print('OK: portable GNS3 52 nodes/52 links; 18 pools/19 clients; source/live hashes; recorded smoke/failover; firewall restart cycles; actual PCAP/reopen and Web UI browser regression')
    print('This checker validates recorded evidence; it does not rerun the GNS3 network.')

if __name__=='__main__':main()
