#!/usr/bin/env python3
"""Create/control this project's isolated GNS3 lab; no host Docker socket is mounted."""
import argparse
import json
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
PROJECT=json.loads((ROOT/'simulation/gns3/hospital-3sites.gns3').read_text())
PID=PROJECT['project_id']
CONTROLLER='btl2-gns3-controller'
URL='http://127.0.0.1:3080/v2'


def command(args,**kwargs):
    return subprocess.run(args,text=True,check=True,**kwargs)


def api(path,method='GET',body=None):
    data=None if body is None else json.dumps(body).encode()
    req=urllib.request.Request(URL+path,data=data,method=method,headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=180) as response:
            data=response.read();return json.loads(data) if data else None
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'{method} {path}: {exc.code} {exc.read().decode()}') from exc


def inner(*args,capture=True):
    return command(['docker','exec',CONTROLLER,'docker',*args],capture_output=capture)


def containers():
    return {n['name']:n['properties']['container_id'] for n in api(f'/projects/{PID}/nodes') if n['node_type']=='docker'}


def execute(name,args,check=False):
    cid=containers()[name]
    result=subprocess.run(['docker','exec',CONTROLLER,'docker','exec',cid,*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    if check and result.returncode:raise RuntimeError(result.stdout)
    return result


def create():
    projects=api('/projects')
    if any(p['project_id']==PID for p in projects):raise RuntimeError('Lab already exists; use start/reopen or remove this lab explicitly.')
    api('/projects','POST',{'name':PROJECT['name'],'project_id':PID,'auto_close':False,'scene_width':2400,'scene_height':2200})
    for node in PROJECT['topology']['nodes']:
        api(f'/projects/{PID}/nodes','POST',node)
        print('Created',node['name'],flush=True)
    for link in PROJECT['topology']['links']:api(f'/projects/{PID}/links','POST',link)
    start()


def start():
    # A restarted controller discovers saved projects in the closed state.
    if api(f'/projects/{PID}')['status'] != 'opened':
        api(f'/projects/{PID}/open', 'POST')
    api(f'/projects/{PID}/nodes/start','POST')
    print('GNS3 nodes started; waiting for services/OSPF/DHCP',flush=True)
    time.sleep(8)
    for _ in range(90):
        r=execute('Main-PC10-A',['ip','-4','-o','addr','show','eth0'])
        ping=execute('Main-PC10-A',['ping','-n','-c','1','-W','1','10.20.10.10'])
        web=execute('Main-PC10-A',['curl','--noproxy','*','--connect-timeout','1','--max-time','2','--fail','--silent','http://192.0.2.100'])
        ready=all(n['status']=='started' for n in api(f'/projects/{PID}/nodes'))
        if ready and '10.10.10.10/25' in r.stdout and ping.returncode==0 and web.returncode==0:
            print('Ready: DHCP lease and inter-site ICMP verified',flush=True);return
        time.sleep(2)
    raise RuntimeError('Lab convergence timed out; inspect node /tmp logs.')


def bootstrap():
    command(['docker','build','-t','btl2-gns3-controller:2.2.55',str(ROOT/'simulation/gns3/controller')])
    command(['docker','build','-t','hospital-netlab:20261102',str(ROOT/'simulation/gns3/runtime')])
    state=ROOT/'tmp/gns3-state';state.mkdir(parents=True,exist_ok=True)
    command(['docker','run','-d','--privileged','--name',CONTROLLER,'-p','127.0.0.1:3080:3080','--mount','type=volume,source=btl2-gns3-docker,target=/var/lib/docker','--mount',f'type=bind,source={state},target=/lab','btl2-gns3-controller:2.2.55'])
    for _ in range(90):
        try:api('/version');break
        except (OSError,RuntimeError):time.sleep(1)
    else:raise RuntimeError('GNS3 controller failed to start')
    archive=ROOT/'tmp/hospital-netlab.tar'
    command(['docker','save','hospital-netlab:20261102','-o',str(archive)])
    with archive.open('rb') as stream:subprocess.run(['docker','exec','-i',CONTROLLER,'docker','load'],stdin=stream,check=True)
    archive.unlink()
    create()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['bootstrap','create','start','stop','reopen','status','exec','remove'])
    p.add_argument('arguments',nargs=argparse.REMAINDER);a=p.parse_args()
    if a.action=='bootstrap':bootstrap()
    elif a.action=='create':create()
    elif a.action=='start':start()
    elif a.action=='stop':api(f'/projects/{PID}/nodes/stop','POST')
    elif a.action=='reopen':
        api(f'/projects/{PID}/nodes/stop','POST');api(f'/projects/{PID}/close','POST');api(f'/projects/{PID}/open','POST');start()
    elif a.action=='status':
        print(json.dumps({'server':api('/version'),'project':api(f'/projects/{PID}'),'nodes':[(n['name'],n['status']) for n in api(f'/projects/{PID}/nodes')]},indent=2))
    elif a.action=='exec':
        if len(a.arguments)<2:p.error('exec requires NODE COMMAND [ARGS]')
        r=execute(a.arguments[0],a.arguments[1:]);print(r.stdout,end='');raise SystemExit(r.returncode)
    else:
        # Only remove the specifically named controller. Retain project files/volume for recovery.
        command(['docker','rm','-f',CONTROLLER])

if __name__=='__main__':main()
