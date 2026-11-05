#!/usr/bin/env python3
"""Run a demo command in the current isolated MPLS QEMU VM (local workspace only)."""
import argparse,base64,json,re,shlex,socket,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=4556);p.add_argument('--node');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
 state=ROOT/'tmp/wan-tools/whpx-vm.json'
 if not state.exists():p.error('Local VM state is absent. Use the Linux/GNS3 runbook in simulation/mpls/README.md to create a lab.')
 config=json.loads(state.read_text());assert any('127.0.0.1:'+str(a.port) in x for x in config['args']),'Port does not match this lab VM'
 if a.node:
  nodes=json.loads((ROOT/'simulation/mpls/generated/topology.json').read_text())['nodes']
  if a.node not in nodes:p.error('Unknown lab node')
  command=a.command[1:] if a.command[:1]==['--'] else a.command
  if not command:p.error('Provide a command after --node NAME --')
  shell='ip netns exec '+shlex.quote('hospmpls-'+a.node)+' '+shlex.join(command)
 else:shell='uname -a; ip netns list'
 marker='HOSP_DONE_'+uuid.uuid4().hex
 start_marker=marker+'_START'
 encoded=base64.b64encode(("printf '\\n"+start_marker+"\\n'; "+shell).encode()).decode()
 line="printf '%s' '"+encoded+"' | base64 -d | sh; printf '\\n"+marker+":%s\\n' \"$?\"\r"
 with socket.create_connection(('127.0.0.1',a.port),timeout=5) as s:
  s.settimeout(.5);s.sendall(line.encode());out=b'';deadline=time.monotonic()+40
  while time.monotonic()<deadline:
   try:
    b=s.recv(65536)
    if not b:break
    out+=b
   except socket.timeout:pass
   match=re.search(rb'\r?\n'+marker.encode()+rb':(\d+)\r?\n',out)
   if match:
    text=out[:match.start()].decode(errors='replace');start=text.find(start_marker);print(text[start+len(start_marker):].lstrip('\r\n') if start>=0 else text)
    raise SystemExit(int(match[1]))
  raise RuntimeError('No completion marker; VM may be busy. Do not run concurrent console commands.')
if __name__=='__main__':main()
