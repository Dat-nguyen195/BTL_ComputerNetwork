// Layout only: documented native Packet Tracer IPC; no network/config mutation.
function rdLayout(plan) {
    var w=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace();
    var n=ipc.network(), existing={}, i, d, ids=[], changes=[];
    for(i=0;i<n.getDeviceCount();i++){d=n.getDeviceAt(i);existing[d.getName()]=true;}
    var previous=$getData("redesign-layout.json");
    if(previous){try{var old=JSON.parse(previous);for(i=0;i<old.annotation_ids.length;i++){w.removeCanvasItem(old.annotation_ids[i]);}}catch(ignore){}}
    // Remove only our initial capability-probe note, if present.
    var notes=w.getCanvasNoteIds();
    for(i=0;i<notes.length;i++){if(w.getCanvasNoteText(notes[i]).indexOf("HOSPITAL THREE-SITE / REDESIGN")>=0){w.removeCanvasItem(notes[i]);}}
    function note(x,y,text,size){ids.push(w.addNote(x,y,w.getUnusedLayer(),'<span style="font-family:Arial;font-size:'+(size||16)+'px;color:#18374b">'+text+'</span>'));}
    // Use workspace coordinates directly; verify frame bounds after save/reopen.
    function line(x,y,a,b,color,width){ids.push(w.drawLine(x,y,a,b,w.getUnusedLayer(),width||2,color[0],color[1],color[2]));}
    function box(x,y,a,b,title,c){
        line(x,y,x+a,y,c);line(x,y+b,x+a,y+b,c);line(x,y,x,y+b,c);line(x+a,y,x+a,y+b,c);
        line(x+2,y+16,x+a-2,y+16,[235,243,249],28);note(x+14,y+3,'<b>'+title+'</b>',18);
    }
    box(1180,20,1240,290,'INTERNET LAB / TWO ISP / WEB-LAB',[112,157,181]);
    box(65,350,3475,1240,'MAIN SITE / HCMC / A + B: FIVE FLOORS EACH',[99,138,169]);
    box(1260,350,1080,1140,'MAIN DC / MDF / SERVER FARM / DMZ',[120,147,167]);
    box(90,440,1020,990,'BUILDING A / representative floor access',[145,174,196]);
    box(2490,440,1020,990,'BUILDING B / representative floor access',[145,174,196]);
    box(120,1640,1400,910,'DBP / 10.20.0.0/16 / TWO FLOORS',[104,155,144]);
    box(2080,1640,1420,910,'BHTQ / 10.30.0.0/16 / TWO FLOORS',[104,155,144]);
    note(75,318,'PT representation only: campus access is not the full 1,120-PC production deployment.',18);
    note(1310,465,'EDGE + FIREWALL / VLAN80 DMZ behind FW',16);
    note(1300,1000,'SERVER FARM / VLAN70 / 8 internal servers',18);
    note(1300,1330,'ADMIN90 / NVR design endpoint110 / IoT control appliance110',15);
    note(1260,1550,'WAN / OSPF AREA0 / AUX INTERNET VIA MAIN',18);
    note(1500,1680,'DBP leased line                           BHTQ leased line',16);
    note(150,1740,'DBP IT/MDF / GW + local infrastructure + camera control',17);
    note(2170,1740,'BHTQ IT/MDF / GW + local infrastructure + camera control',17);
    for(i=0;i<plan.floors.length;i++){
        var f=plan.floors[i],b=f.box;
        box(b[0],b[1],b[2],b[3],f.id+' / PC VLAN'+f.vlan+' / WLAN'+f.ap_vlan+' / CAM110',[180,197,211]);
    }
    for(var name in plan.positions){if(existing[name]){
        var item=w.getComponentItem(name),p=plan.positions[name];
        changes.push({node:name,before:[item.getXCoordinate(),item.getYCoordinate()],after:p});item.moveTo(p[0],p[1]);
    }}
    var result={time:new Date().toISOString(),scope:"Display coordinates and our annotations only; no link/IP/VLAN/hostname/config operations",annotation_ids:ids,moved:changes};
    $putData("redesign-layout.json",JSON.stringify(result));dprint("LAYOUT_DONE "+changes.length+" nodes / "+ids.length+" annotations");return result;
}
