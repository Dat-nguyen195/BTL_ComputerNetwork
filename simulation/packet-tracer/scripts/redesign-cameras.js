// PT9 factory catalog confirmed Webcam is type39; do not use stale addDevice help enum37.
function rdCameras(plan){
    if($getData('redesign-camera-config.json')){throw new Error('Camera journal exists: inspect before retry');}
    var w=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace(),n=ipc.network();
    var log={started:new Date().toISOString(),status:'CONFIGURING',cameras:[]};
    function save(){$putData('redesign-camera-config.json',JSON.stringify(log));}
    try{
        for(var i=0;i<plan.floors.length;i++){
            var f=plan.floors[i],p=plan.positions[f.camera],d;
            if(i===0){d=n.getDevice(f.camera);}
            else{var created=w.addDevice(39,'Webcam',p[0],p[1]);if(!created){throw new Error('Create failed '+f.camera);}d=n.getDevice(created);d.setName(f.camera);}
            var wired=d.getPort('GigabitEthernet3');
            wired.setDhcpClientFlag(false);wired.setIpSubnetMask(f.camera_ip,'255.255.255.0');wired.setDefaultGateway(f.gateway);
            d.getPort('Wireless0').setPower(false);
            if(i!==0&&!w.createLink(f.switch,'FastEthernet0/3',f.camera,'GigabitEthernet3',8100)){throw new Error('Camera cable failed '+f.camera);}
            log.cameras.push({node:f.camera,site:f.site,floor:f.id,ip:wired.getIpAddress(),mask:wired.getSubnetMask(),gateway:f.gateway,port:'GigabitEthernet3',switch:f.switch,switch_port:'FastEthernet0/3',vlan:110,wireless_power:d.getPort('Wireless0').getPower(),manager:f.manager,manager_ip:f.manager_ip,registration:'NOT_CONFIGURED_YET',time:new Date().toISOString()});save();
        }
        log.status='WIRED_ADDRESSED_REGISTRATION_PENDING';save();dprint('CAMERAS_WIRED '+log.cameras.length);
    }catch(e){log.status='FAILED_REQUIRES_INSPECTION';log.error=String(e);save();throw e;}
}
