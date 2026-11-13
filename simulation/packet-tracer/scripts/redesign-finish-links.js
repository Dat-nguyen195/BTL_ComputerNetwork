// Native IPC expansion, explicitly run on the redesign copy after layout-only verification.
// ES5 for Packet Tracer QtScript. No routing, firewall, DHCP-server or original WLAN changes.
function rdFinishLinks(plan) {
    // Saved-native readback confirmed 54 serialized cables. IPC count66 includes radio relationships.
    var prior=JSON.parse($getData('redesign-expansion.json'));
    if(prior.operations.length!==56 || prior.resume_started || prior.status!=='FAILED_REQUIRES_INSPECTION'){throw new Error('Unexpected checkpoint; inspect first');}
    var w=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace(),n=ipc.network();
    var journal=prior;journal.resume_started=new Date().toISOString();journal.status='RESUMING_LINKS';
    function log(op){journal.operations.push(op);$putData('redesign-expansion.json',JSON.stringify(journal));}
    function exists(name){for(var i=0;i<n.getDeviceCount();i++){if(n.getDeviceAt(i).getName()===name){return true;}}return false;}
    function add(name,type,model){
        if(exists(name)){if(name!=='Main-A-F1-SW'){throw new Error('Unexpected preexisting new node '+name);}return;}
        var p=plan.positions[name],created=w.addDevice(type,model,p[0],p[1]);
        if(!created){throw new Error('Cannot create '+name+' / '+model);}
        n.getDevice(created).setName(name);log({action:'add',node:name,type:type,model:model});
    }
    function ios(name,lines){
        var d=n.getDevice(name);d.skipBoot();
        var out=[],r=d.enterCommand('configure terminal','enable');
        if(r.first!==0){throw new Error('Cannot configure '+name);}
        for(var i=0;i<lines.length;i++){
            var line=lines[i],cmd=line.replace(/^\s+|\s+$/g,'');
            r=d.enterCommand(cmd,/^\s/.test(line)?'':'global');out.push({command:cmd,result:r});
            if(r.first!==0){log({action:'config-error',node:name,commands:out});throw new Error('IOS failed '+name+': '+cmd);}
        }
        d.enterCommand('end','');r=d.enterCommand('write memory','enable');
        log({action:'configure',node:name,commands:out,write_memory:r});
    }
    function vlans(ids){var a=[];for(var i=0;i<ids.length;i++){a.push('vlan '+ids[i]);a.push(' name FLOOR-V'+ids[i]);}return a;}
    function trunk(port,desc,allowed,mls){var a=['interface '+port,' description '+desc];
        if(mls){a.push(' switchport trunk encapsulation dot1q');}
        return a.concat([' switchport mode trunk',' switchport trunk allowed vlan '+allowed,' no spanning-tree portfast',' no spanning-tree bpduguard enable',' no shutdown']);}
    function access(port,desc,vlan){return ['interface '+port,' description '+desc,' switchport mode access',' switchport access vlan '+vlan,' spanning-tree portfast',' spanning-tree bpduguard enable',' no shutdown'];}
    function link(a,ap,b,bp){if(!w.createLink(a,ap,b,bp, /(?:-SW|-DIST|-Access)$/.test(b) ? 8101 : 8100)){throw new Error('Link failed '+a+':'+ap+' -> '+b+':'+bp);}log({action:'link',source:a,source_port:ap,target:b,target_port:bp});}
    function rewire(site,old,endpoint,ep,sw,sp){if(!w.deleteLink(site+'-Access','FastEthernet0/'+old)){throw new Error('Unlink failed '+endpoint);}log({action:'unlink',source:site+'-Access',source_port:'FastEthernet0/'+old,endpoint:endpoint});link(sw,sp,endpoint,ep);}
    var i,j,f;
    try {
        log({action:'link',source:'Main-Access',source_port:'FastEthernet0/14',target:'Main-A-DIST',target_port:'GigabitEthernet0/1',note:'Explicit crossover succeeded after AUTO false; observed count54'});link('Main-Access','FastEthernet0/15','Main-B-DIST','GigabitEthernet0/1');
        for(i=0;i<plan.floors.length;i++){
            f=plan.floors[i];link(f.distribution,f.distribution_port,f.switch,'GigabitEthernet0/1');
            for(j=0;j<f.pcs.length;j++){
                var pc=f.pcs[j];
                if(pc['new']){link(f.switch,pc.new_port,pc.node,'FastEthernet0');n.getDevice(pc.node).setDhcpFlag(true);}
                else{rewire(f.site,pc.old_switch_port,pc.node,'FastEthernet0',f.switch,pc.new_port);}
            }
            if(f.ap_new){link(f.switch,'FastEthernet0/2',f.ap,'Port 0');}
            else{rewire(f.site,f.ap_old_port,f.ap,'Port 0',f.switch,'FastEthernet0/2');}
        }
        for(i=0;i<plan.managers.length;i++){
            var m=plan.managers[i],dev=n.getDevice(m.node),port=dev.getPort('FastEthernet0');
            port.setDhcpClientFlag(false);port.setIpSubnetMask(m.ip,'255.255.255.0');dev.setDefaultGateway(m.gateway);port.setDnsServerIp(m.ip.replace(/110\.12$/,'70.'+(m.node.indexOf('Main-')===0?'10':'6')));
            dev.getProcess('HttpServer').setEnable(true);link(m.switch,m.switch_port,m.node,'FastEthernet0');
            log({action:'manager-address',node:m.node,ip:m.ip,gateway:m.gateway,scope:'IoT control appliance outside application-server production count; registration not yet configured'});
        }
        journal.status='INFRASTRUCTURE_DONE_CAMERA_PENDING';journal.finished=new Date().toISOString();$putData('redesign-expansion.json',JSON.stringify(journal));
        dprint('EXPANSION_INFRASTRUCTURE_DONE '+journal.operations.length+' operations');
    } catch(error){journal.status='FAILED_REQUIRES_INSPECTION';journal.error=String(error);$putData('redesign-expansion.json',JSON.stringify(journal));throw error;}
}
