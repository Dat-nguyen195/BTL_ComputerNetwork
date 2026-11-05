// Run inside Packet Tracer's File Script Module, with exactly one 2911 router.
// Uses the Cisco Extensions API installed with Packet Tracer. No external network/file access.
function main() {
    dprint("HOSPITAL_PROBE_BEGIN");
    try {
        var net = ipc.network();
        var router = null;
        for (var n = 0; n < net.getDeviceCount(); n++) {
            var candidate = net.getDeviceAt(n);
            if (candidate.getModel() === "2911" && router === null) {
                router = candidate;
            } else if (candidate.getModel() !== "Power Distribution Device") {
                throw new Error("Probe requires one 2911 router; automatic power distribution is allowed.");
            }
        }
        if (router === null) { throw new Error("No 2911 probe router found."); }
        router.skipBoot();
        var commands = [
            ["show version", "enable"],
            ["show ip interface brief", "enable"],
            ["ip sla ?", "global"],
            ["track ?", "global"],
            ["route-map HOSPITAL-PROBE permit 10", "global"],
            ["match interface GigabitEthernet0/1", ""],
            ["set ip next-hop verify-availability 203.0.113.1 1 track 1", ""],
            ["end", ""],
            ["ip nat inside source route-map ?", "global"],
            ["class-map type inspect match-all PROBE", "global"],
            ["end", ""]
        ];
        var records = [];
        for (var i = 0; i < commands.length; i++) {
            var command = commands[i];
            try {
                var result = router.enterCommand(command[0], command[1]);
                records.push({command: command[0], mode: command[1], result: result});
                dprint(JSON.stringify(records[records.length - 1]));
            } catch (error) {
                records.push({command: command[0], error: String(error)});
                dprint(JSON.stringify(records[records.length - 1]));
            }
        }
        $putData("probe-results.json", JSON.stringify(records));
    } catch (error) {
        dprint("HOSPITAL_PROBE_ERROR " + String(error));
    }
    dprint("HOSPITAL_PROBE_END");
}

function cleanUp() {}
