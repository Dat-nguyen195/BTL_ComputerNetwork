#!/usr/bin/env python3
"""Package reviewable source/report/GNS3/evidence with SHA256; no approval or BKeL action."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ZIP=ROOT/'submission/hospital-network-delivery.zip'
MANIFEST=ROOT/'submission/package-manifest.json'
SUMS=ROOT/'submission/SHA256SUMS'
EXCLUDED={p.relative_to(ROOT).as_posix() for p in (ZIP,MANIFEST,SUMS)}


def digest(data):return hashlib.sha256(data).hexdigest()

def selected():
    r=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,check=True,stdout=subprocess.PIPE)
    names=sorted(set(r.stdout.decode().rstrip('\0').split('\0'))-EXCLUDED)
    output={}
    for name in names:
        path=ROOT/name
        if not path.is_file():continue
        if name.startswith(('tmp/','.git/')) or path.suffix in ('.pem','.key','.qcow2','.iso','.bin'):raise ValueError('Unexpected package input '+name)
        output[name]=path.read_bytes()
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    files=selected()
    for required in ('docs/06-report/final/report.pdf','simulation/gns3/hospital-3sites.gns3','test_results/runtime/after-reopen-runtime/results.json'):
        assert required in files,'Missing required deliverable '+required
    manifest={'format':1,'status':'TECHNICAL HANDOFF - TEAM APPROVAL AND BKEL SUBMISSION PENDING','sha256':{n:digest(data) for n,data in files.items()}}
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    internal_sums=''.join(f'{h}  {name}\n' for name,h in manifest['sha256'].items()).encode()
    if a.check:
        assert MANIFEST.read_bytes()==manifest_bytes,'Source changed: regenerate submission package'
        with zipfile.ZipFile(ZIP) as z:
            assert set(z.namelist())==set(files)|{'submission/package-manifest.json','submission/SHA256SUMS'}
            for name,expected in manifest['sha256'].items():assert digest(z.read(name))==expected,name
            assert z.read('submission/package-manifest.json')==manifest_bytes
            assert z.read('submission/SHA256SUMS')==internal_sums
        for line in SUMS.read_text().splitlines():
            expected,name=line.split('  ',1);assert digest((ROOT/name).read_bytes())==expected,name
        print('OK: ZIP contents, all source/PDF/project/evidence hashes and external checksums verified')
        return
    MANIFEST.parent.mkdir(parents=True,exist_ok=True);MANIFEST.write_bytes(manifest_bytes)
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in {**files,'submission/package-manifest.json':manifest_bytes,'submission/SHA256SUMS':internal_sums}.items():
            info=zipfile.ZipInfo(name,date_time=(2026,11,2,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,data)
    entries={**manifest['sha256'],'submission/package-manifest.json':digest(manifest_bytes),'submission/hospital-network-delivery.zip':digest(ZIP.read_bytes())}
    SUMS.write_text(''.join(f'{h}  {name}\n' for name,h in sorted(entries.items())))
    print(f'Packaged {len(files)} files, {ZIP.stat().st_size} bytes; technical handoff, no submission/approval claimed')

if __name__=='__main__':main()
