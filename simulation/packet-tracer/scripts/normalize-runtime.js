// Explicit cleanup of residue from the initial CLI mode bug; preserves loopback IPs.
// Call after the current test suite finishes, then save and repeat validation.
function normalizeHospitalRuntime() {
    var cleanup = {
        "Main-Core": ["no description", "no ip helper-address 10.10.70.10",
            "no ip access-group MAIN-CAMERA-IN in", "no ip ospf network point-to-point", "no ip ospf priority"],
        "Main-GW": ["no bandwidth", "no ip ospf network point-to-point", "no ip ospf priority"],
        "DBP-GW": ["no bandwidth", "no ip helper-address 10.20.70.6",
            "no ip ospf cost", "no ip access-group DBP-CAMERA-IN in"],
        "BHTQ-GW": ["no bandwidth", "no ip helper-address 10.30.70.6",
            "no ip ospf cost", "no ip access-group BHTQ-CAMERA-IN in"]
    };
    var records = [];
    for (var name in cleanup) {
        var router = ipc.network().getDevice(name);
        router.enterCommand("interface Loopback0", "global");
        for (var i = 0; i < cleanup[name].length; i++) {
            records.push({node: name, command: cleanup[name][i],
                          response: router.enterCommand(cleanup[name][i], "")});
        }
        router.enterCommand("end", "");
        router.enterCommand("write memory", "enable");
    }
    // PT recreates serverPool on reopen when it is absent. Retain it with zero
    // capacity so it cannot allocate addresses outside the 18 planned pools.
    var servers = ["Main-Infra", "DBP-Infra", "BHTQ-Infra"];
    for (var s = 0; s < servers.length; s++) {
        var process = ipc.network().getDevice(servers[s]).getProcess("DhcpServerMain")
            .getDhcpServerProcessByPortName("FastEthernet0");
        for (var p = 0; p < process.getPoolCount(); p++) {
            var pool = process.getPoolAt(p);
            if (pool.getDhcpPoolName() === "serverPool") {
                pool.setMaxUsers(0);
                records.push({node: servers[s], pool: "serverPool", max_users: pool.getMaxUsers()});
            }
        }
    }
    $putData("normalization.json", JSON.stringify(records));
    dprint("NORMALIZATION " + JSON.stringify(records));
}
