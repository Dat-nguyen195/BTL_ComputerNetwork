#!/usr/bin/env python3
"""Browser regression: normal Chrome and Electron-identified browser without Node IPC.

Requires Playwright Python and an installed Chrome executable. Uses a fresh,
isolated browser context, never a user's saved browser profile.
"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright,expect

ELECTRON_UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Electron/36.0.0 Safari/537.36'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('tmp/web-ui-regression'));a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--disable-dev-shm-usage'])
        for mode,ua in [('normal',None),('embedded-electron',ELECTRON_UA)]:
            context=browser.new_context(**({'user_agent':ua} if ua else {}),viewport={'width':1600,'height':1000})
            # Tests need only the local controller; no analytics/external requests.
            context.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:3080/','ws://127.0.0.1:3080/')) else r.abort())
            page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto('http://127.0.0.1:3080/',wait_until='networkidle',timeout=30000)
            expect(page.get_by_text('Hospital-3Sites-FRR',exact=True)).to_be_visible(timeout=15000)
            assert 'Cannot read properties of null' not in page.locator('body').inner_text()
            page.get_by_text('Hospital-3Sites-FRR',exact=True).click()
            for label in ('Main-Core','DBP-GW','BHTQ-GW'):
                expect(page.get_by_text(label,exact=True).first).to_be_visible(timeout=15000)
            # A pasted project URL or browser refresh must retain the correct asset base.
            page.reload(wait_until='networkidle',timeout=30000)
            expect(page.get_by_text('Main-Core',exact=True).first).to_be_visible(timeout=15000)
            assert not errors,errors
            canvas=page.locator('svg#map g.canvas')
            for _ in range(12):
                bounds=canvas.bounding_box()
                if bounds['width']<=1120 and bounds['height']<=810:break
                page.locator('button[mattooltip="Zoom out"]').click()
            bounds=canvas.bounding_box()
            dx=650-(bounds['x']+bounds['width']/2)
            dy=520-(bounds['y']+bounds['height']/2)
            page.locator('button[mattooltip="Pan workspace"]').click()
            steps=max(1,int(max(abs(dx),abs(dy))/300)+1)
            for _ in range(steps):
                page.mouse.move(850,700);page.mouse.down()
                page.mouse.move(850+dx/steps,700+dy/steps,steps=12);page.mouse.up()
            expect(page.locator('svg#map').get_by_text('Main-Core',exact=True)).to_be_in_viewport()
            page.screenshot(path=str(a.output/(mode+'.png')))
            record={'mode':mode,'user_agent':page.evaluate('navigator.userAgent'),'has_node_require':page.evaluate('typeof window.require === "function"'),'url':page.url,'page_errors':errors,'visible_nodes':['Main-Core','DBP-GW','BHTQ-GW'],'status':'PASS'}
            print(json.dumps(record,ensure_ascii=False),flush=True);results.append(record)
            context.close()
        browser.close()
    with urlopen('http://127.0.0.1:3080/static/web-ui/hospital-webui-compat.json',timeout=10) as r:patch=json.load(r)
    (a.output/'browser-results.json').write_text(json.dumps({'timestamp_utc':datetime.now(timezone.utc).isoformat(),'patch':patch,'results':results},ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
