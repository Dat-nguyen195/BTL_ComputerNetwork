// Explicit virtual-lab NIC conversion. Keep the saved wired lab as a rollback.
// Complete each client profile through Config -> Wireless0 after installing the NIC.
// The tested profile API throws "invalid vector subscript" on this Packet Tracer build.
// The passphrase below is a public lab example, not an operational credential.
function optionalWirelessPort(device) {
    for (var i = 0; i < device.getPortCount(); i++) {
        var port = device.getPortAt(i);
        if (port.getName() === "Wireless0") { return port; }
    }
    return null;
}

function placeWirelessClients() {
    var workspace = ipc.appWindow().getActiveWorkspace().getLogicalWorkspace();
    var sites = ["Main", "DBP", "BHTQ"];
    var roles = ["Guest", "Staff"];
    for (var i = 0; i < sites.length; i++) {
        for (var j = 0; j < roles.length; j++) {
            var name = sites[i] + "-" + roles[j];
            var ap = workspace.getComponentItem(name + "-AP");
            workspace.getComponentItem(name).moveTo(ap.getXCoordinate(), ap.getYCoordinate() - 80);
        }
    }
}

function configureWirelessEndpoint(name) {
    var network = ipc.network();
    var client = network.getDevice(name);
    var accessPoint = network.getDevice(name + "-AP").getProcess("WirelessServer");
    var key = "HospitalLab2026Only";
    var ssid = name.replace(/-/g, "_");
    accessPoint.setSsid(ssid);
    accessPoint.setAuthenType(4);
    accessPoint.setEncryptType(4);
    accessPoint.getWpaProcess().setKey(key);
    accessPoint.setSsidBrdCastEnabled(true);
    var wireless = optionalWirelessPort(client);
    if (!wireless) {
        var ethernet = client.getPort("FastEthernet0");
        var mac = ethernet.getMacAddress();
        client.setDhcpFlag(false);
        client.setPower(false);
        var root = client.getRootModule();
        root.removeModuleAt(0);
        if (!root.addModuleAt("PT-HOST-NM-1W-AC", 0)) {
            root.addModuleAt("PT-HOST-NM-1CFE", 0);
            client.setPower(true);
            throw new Error("Wireless NIC insertion failed for " + name);
        }
        client.setPower(true);
        wireless = client.getPort("Wireless0");
        wireless.setMacAddress(mac);
    }
    var process = client.getProcess("WirelessClient");
    process.setPort("Wireless0");
    wireless.setPower(true);
    client.setDhcpFlag(false);
    client.setDhcpFlag(true);
    dprint("NIC_INSTALLED_SET_PROFILE_IN_GUI " + name + " SSID " + ssid);
}

function captureWireless() {
    var records = [];
    var sites = ["Main", "DBP", "BHTQ"];
    var roles = ["Guest", "Staff"];
    for (var i = 0; i < sites.length; i++) {
        for (var j = 0; j < roles.length; j++) {
            var name = sites[i] + "-" + roles[j];
            var device = ipc.network().getDevice(name);
            var process = device.getProcess("WirelessClient");
            var port = optionalWirelessPort(device);
            var profile = process.getCurrentProfile();
            records.push({node: name, wireless_port: !!port,
                          mac: port ? port.getMacAddress() : null,
                          ip: port ? port.getIpAddress() : null,
                          ssid: profile.ssid, ap_mac: port ? process.getCurrentApMac() : null,
                          auth_type: profile.authenType, encrypt_type: process.getEncryptType()});
        }
    }
    $putData("wireless-associations.json", JSON.stringify(records));
    dprint("WIRELESS_STATE " + JSON.stringify(records));
}
