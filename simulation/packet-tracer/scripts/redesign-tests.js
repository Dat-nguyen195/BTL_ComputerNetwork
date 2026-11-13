// Run only after HOSPITAL_TESTS_DONE 32. Read-only network tests; no IOS/service edits.
function redesignTests(storeName, smoke) {
    if (typeof rdBusy !== 'undefined' && rdBusy) { throw new Error('Redesign tests already running'); }
    rdBusy=true;
    var report={started_at:new Date().toISOString(),scope:smoke?'After-reopen smoke':'Camera authorization and new-floor application regression',records:[],before:[],after:[]};
    var add=hospital.add;
    function snapshots(){var a=[];['Main-Core','DBP-GW','BHTQ-GW'].forEach(function(n){a.push({node:n,command:'show access-lists',result:ipc.network().getDevice(n).enterCommand('show access-lists','enable')});});return a;}
    function save(){$putData(storeName,JSON.stringify(report));}
    hospital.add=function(r){r.time=new Date().toISOString();r.source_vlan=r.source==='Main-Admin'?90:r.source.indexOf('Guest')>=0?100:r.source.indexOf('Staff')>=0?120:r.source.indexOf('B-F4')>=0?20:r.source.indexOf('B-F5')>=0?60:10;report.records.push(r);save();dprint('REDESIGN_RECORD '+JSON.stringify(r));};
    report.before=snapshots();save();var jobs=[];
    function http(g,s,u,m,e){jobs.push(function(n){hospital.http(g,s,u,m,e,n);});}
    ['Main','DBP','BHTQ'].forEach(function(site,i){
        var ip='10.'+[10,20,30][i]+'.110.12';
        http('CAM04','Main-Admin','http://'+ip,'IoT','allow');
        http('CAM05',site+'-Guest','http://'+ip,'IoT','deny');
        http('CAM05-CONTROL',site+'-Guest','http://web.hospital.test','HOSPITAL-LAB-Web-Lab','allow');
        if(!smoke){
            http('CAM-CLINICAL-DENY',site==='Main'?'Main-PC10-A':site+'-PC10','http://'+ip,'IoT','deny');
            http('CAM-STAFF-DENY',site+'-Staff','http://'+ip,'IoT','deny');
        }
    });
    ['Main-B-F3-PC','Main-B-F4-PC','Main-B-F5-PC'].forEach(function(pc){
        http('FLOOR-HIS',pc,'http://10.10.70.11','HOSPITAL-LAB-Main-HIS','allow');
        if(!smoke)http('FLOOR-DNS-WEB',pc,'http://web.hospital.test','HOSPITAL-LAB-Web-Lab','allow');
    });
    var pos=0;
    function next(){
        if(pos===jobs.length){report.after=snapshots();report.completed_at=new Date().toISOString();report.status='COMPLETE_REQUIRES_OFFLINE_REVIEW';hospital.add=add;rdBusy=false;save();dprint('REDESIGN_TESTS_DONE '+report.records.length);return;}
        try{jobs[pos++](next);}catch(e){report.records.push({kind:'exception',error:String(e),time:new Date().toISOString()});save();next();}
    }
    next();
}

function redesignSsh(storeName) {
    var r={started_at:new Date().toISOString(),commands:[],records:[]};
    ['show ip ssh','show running-config'].forEach(function(c){r.commands.push({time:new Date().toISOString(),command:c,result:ipc.network().getDevice('Main-Core').enterCommand(c,'enable')});});
    function save(){$putData(storeName,JSON.stringify(r));}
    var line=ipc.network().getDevice('Main-Admin').getCommandPrompt(),output='',stage=0,active=true;
    function record(id,source,protocol,command,text){r.records.push({id:id,time:new Date().toISOString(),source:source,source_ip:hospital.address(source),source_vlan:source==='Main-Admin'?90:10,destination:'10.10.90.1',destination_vlan:90,protocol:protocol,command:command,expected:id==='SSH-ADMIN-ALLOW'?'allow as privilege1':'deny',output:text});save();}
    line.registerEvent('outputWritten',null,function(e,a){
        if(!active)return;output+=a.newOutput;
        if(stage===0 && output.indexOf('Password:')>=0){stage=1;line.enterCommand('HospitalLab2026Only');}
        else if(stage===1 && /Main-Core>/.test(output)){stage=2;line.enterCommand('show ip interface brief');}
        else if(stage===2 && /10.10.90.1/.test(output) && /Vlan1/.test(output) && /Main-Core>\s*$/.test(output)){
            stage=3;active=false;record('SSH-ADMIN-ALLOW','Main-Admin','SSH/TCP22','ssh -l labadmin 10.10.90.1',output);line.enterCommand('exit');
            setTimeout(telnet,2000);
        }
    });
    function telnet(){
        var out='',on=true;
        line.registerEvent('outputWritten',null,function(e,a){if(on)out+=a.newOutput;});
        line.enterCommand('telnet 10.10.90.1');
        setTimeout(function(){on=false;record('TELNET-ADMIN-DENY','Main-Admin','Telnet/TCP23','telnet 10.10.90.1',out);nonadmin();},6000);
    }
    function nonadmin(){
        var cp=ipc.network().getDevice('Main-PC10-A').getCommandPrompt(),out='',on=true;
        cp.registerEvent('outputWritten',null,function(e,a){if(on)out+=a.newOutput;});
        cp.enterCommand('ssh -l labadmin 10.10.90.1');
        setTimeout(function(){on=false;record('SSH-NONADMIN-DENY','Main-PC10-A','SSH/TCP22','ssh -l labadmin 10.10.90.1',out);r.completed_at=new Date().toISOString();save();dprint('REDESIGN_SSH_DONE '+r.records.length);},25000);
    }
    save();line.enterCommand('ssh -l labadmin 10.10.90.1');
    setTimeout(function(){if(active){active=false;r.error='SSH allow probe did not finish within 30 seconds';r.output=output;save();dprint('REDESIGN_SSH_INCOMPLETE');}},30000);
}
