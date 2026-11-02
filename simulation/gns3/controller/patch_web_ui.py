#!/usr/bin/env python3
"""Keep the GNS3 2.2.55 Web UI in browser mode without a desktop Electron bridge.

The upstream bundle checks only the User-Agent. Embedded browsers can advertise
Electron while correctly denying Node/IPC access. No bridge is injected here.
"""
import argparse
import hashlib
import json
from pathlib import Path

OLD='return!!window.navigator.userAgent.match(/Electron/)'
NEW='try{return!!(window.navigator.userAgent.match(/Electron/)&&typeof window.require==="function"&&window.require("electron").ipcRenderer)}catch(n){return!1}'


def patch(directory):
    index=directory/'index.html'
    html=index.read_text()
    marker=directory/'hospital-webui-compat.json'
    original_index=directory/'index.html.hospital-original'
    if marker.is_file():
        info=json.loads(marker.read_text())
        bundle=directory/info['patched_bundle']
        if bundle.is_file() and hashlib.sha256(bundle.read_bytes()).hexdigest()==info['patched_sha256'] and info['patched_bundle'] in html:
            if info.get('patch_version')==2:
                print('GNS3 Web UI compatibility patch already applied');return
            html=original_index.read_text()
        else:
            raise RuntimeError('Existing compatibility patch does not match its manifest')
    bundles=[p for p in directory.glob('main.*.js') if p.name in html]
    if len(bundles)!=1:raise RuntimeError('Expected exactly one referenced GNS3 main bundle')
    source=bundles[0];text=source.read_text()
    if text.count(OLD)!=2:raise RuntimeError('Unexpected upstream bundle; review Electron detectors before patching')
    fixed=text.replace(OLD,NEW).encode()
    sha=hashlib.sha256(fixed).hexdigest()
    name='main.webcompat.'+sha[:20]+'.js'
    (directory/name).write_bytes(fixed)
    # A new URL avoids the browser reusing the previously broken cached bundle.
    if not original_index.exists():original_index.write_text(html)
    base_guard="if (userAgent.indexOf(' electron/') > -1)"
    if html.count(base_guard)!=1:raise RuntimeError('Unexpected upstream HTML base-path detector')
    safe_base="if (userAgent.indexOf(' electron/') > -1 && typeof window.require === 'function' && (function(){try{return !!window.require('electron').ipcRenderer;}catch(error){return false;}})())"
    index.write_text(html.replace(source.name,name).replace(base_guard,safe_base))
    info={'patch_version':2,'base_detector_guarded':True,'upstream_bundle':source.name,'upstream_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'patched_bundle':name,'patched_sha256':sha,'changed_detectors':2,
          'reason':'User-Agent alone does not establish an Electron IPC bridge'}
    marker.write_text(json.dumps(info,indent=2)+'\n')
    print('Patched GNS3 browser/Electron detection:',name)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path);a=p.parse_args()
    if a.directory:directory=a.directory
    else:
        import gns3server
        directory=Path(gns3server.__file__).parent/'static/web-ui'
    patch(directory)

if __name__=='__main__':main()
