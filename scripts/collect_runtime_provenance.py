#!/usr/bin/env python3
"""Record and verify the live files/image actually used by every GNS3 node."""
from concurrent.futures import ThreadPoolExecutor
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
from gns3_lab import ROOT,PID,CONTROLLER,api,containers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'test_results/runtime/persistence/live-provenance.json')
    args = parser.parse_args()
    mapping=containers()
    code="import hashlib,json,os,pathlib; n=os.environ['LAB_NODE']; paths=['/usr/local/bin/hospital-node','/opt/hospital/config/'+n+'.json']; print(json.dumps({p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest() for p in paths}))"
    expected_code=hashlib.sha256((ROOT/'simulation/gns3/runtime/node.py').read_bytes()).hexdigest()
    def collect(pair):
        name,cid=pair
        r=subprocess.run(['docker','exec',CONTROLLER,'docker','exec',cid,'python3','-c',code],text=True,capture_output=True,check=True)
        actual=json.loads(r.stdout)
        expected_config=hashlib.sha256((ROOT/'simulation/gns3/runtime/config'/f'{name}.json').read_bytes()).hexdigest()
        assert actual['/usr/local/bin/hospital-node']==expected_code,name
        assert actual['/opt/hospital/config/'+name+'.json']==expected_config,name
        return name,actual
    with ThreadPoolExecutor(max_workers=6) as pool:live=dict(pool.map(collect,mapping.items()))
    out=args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),'project_id':PID,'live_node_sha256':live},indent=2)+'\n')
    print('Verified live source and config hashes on',len(live),'GNS3 nodes')

if __name__=='__main__':main()
