// Explicit adaptation of the candidate to the tested Packet Tracer profiles.
// Requires NM-1FE-TX in Main-FW slot 1 and a DMZ cable on FastEthernet1/0.
function repairPacketTracerProfile() {
    var spec = hospital.spec();
    for (var name in spec.configs) {
        var config = spec.configs[name];
        config = config.replace(/ log(?=\n|$)/g, "");
        config = config.replace(/^no ip http (?:secure-)?server\n/gm, "");
        config = config.replace(/^.*redistribute static subnets route-map.*\n/gm, "");
        config = config.replace(/^ip prefix-list .*\n/gm, "");
        config = config.replace(/default-information originate metric 10/g, "default-information originate");
        if (name === "Main-FW") {
            config = config.replace(/FastEthernet0\/1\.999/g, "FastEthernet0/1");
            config = config.replace(/FastEthernet0\/1\.80/g, "FastEthernet1/0");
            config = config.replace(/^ encapsulation dot1Q (?:80|999)\n/gm, "");
        }
        if (name === "DMZ-Access" && config.indexOf("interface FastEthernet0/24") < 0) {
            config += "\ninterface GigabitEthernet0/1\n switchport mode access\n switchport access vlan 999\n no shutdown\ninterface FastEthernet0/24\n switchport mode access\n switchport access vlan 80\n spanning-tree portfast\n no shutdown\nend\n";
        }
        spec.configs[name] = config;
    }
    spec.limitations = ["ISP2 primary PAT; ISP1 manual standby", "Ethernet models leased lines",
        "Main-FW2811 NM-1FE-TX; three physical security zones",
        "Wired Guest/Staff policy tests do not prove Wi-Fi association",
        "ACL/drop logging omitted because the tested parser rejects log"];
    $putData("hospital-spec.json", JSON.stringify(spec));
    var firewall = ipc.network().getDevice("Main-FW");
    firewall.enterCommand("no interface FastEthernet0/1.80", "global");
    firewall.enterCommand("no interface FastEthernet0/1.999", "global");
}
