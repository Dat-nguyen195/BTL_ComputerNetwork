// Explicit manual path selection, not automatic fault detection or failover.
// Run only after the full suite has finished and its native snapshot is saved.
// Restores the ISP2 route/PAT and writes startup config before finishing.
function testManualHospitalIsp() {
    var edge = ipc.network().getDevice("Main-Edge");
    var original = hospital.records;
    var result = {scope: "Manual ISP1 route/PAT selection and return to ISP2; no automatic failover",
                  commands: [], snapshots: [], records: []};
    hospital.records = [];
    function command(text, mode) {
        var response = edge.enterCommand(text, mode);
        result.commands.push({command: text, response: response});
        return response.first === 0;
    }
    function snapshot(stage) {
        var names = ["show ip route", "show ip nat translations", "show running-config"];
        for (var i = 0; i < names.length; i++) {
            result.snapshots.push({stage: stage, command: names[i], response: edge.enterCommand(names[i], "enable")});
        }
    }
    function save() {
        result.records = hospital.records.slice();
        $putData("manual-isp-results.json", JSON.stringify(result));
    }
    function finish() {
        snapshot("ISP2-restored");
        save();
        hospital.records = original;
        hospital.capture();
        captureWireless();
        dprint("MANUAL_ISP_TEST_DONE " + result.records.length);
    }
    function restore() {
        snapshot("ISP1-selected");
        command("clear ip nat translation *", "enable");
        command("no ip nat inside source list 100 interface GigabitEthernet0/1 overload", "global");
        command("no ip route 0.0.0.0 0.0.0.0 203.0.113.1", "global");
        command("ip route 0.0.0.0 0.0.0.0 198.51.100.1", "global");
        command("ip nat inside source list 100 interface GigabitEthernet0/2 overload", "global");
        command("end", "");
        command("write memory", "enable");
        setTimeout(function () {
            try { hospital.http("MANUAL-ISP2-RESTORED", "Main-PC10-A", "http://web.hospital.test",
                                "HOSPITAL-LAB-Web-Lab", "allow", finish); }
            catch (error) { result.error = String(error); finish(); }
        }, 4000);
    }
    snapshot("before");
    var ok = command("clear ip nat translation *", "enable");
    ok = command("no ip nat inside source list 100 interface GigabitEthernet0/2 overload", "global") && ok;
    ok = command("no ip route 0.0.0.0 0.0.0.0 198.51.100.1", "global") && ok;
    ok = command("ip route 0.0.0.0 0.0.0.0 203.0.113.1", "global") && ok;
    ok = command("ip nat inside source list 100 interface GigabitEthernet0/1 overload", "global") && ok;
    command("end", "");
    if (!ok) { result.error = "Manual selection had CLI errors"; restore(); return; }
    var sources = ["Main-PC10-A", "DBP-Guest", "BHTQ-Staff"];
    var position = 0;
    function next() {
        save();
        if (position === sources.length) { restore(); return; }
        var source = sources[position++];
        try { hospital.http("MANUAL-ISP1", source, "http://web.hospital.test", "HOSPITAL-LAB-Web-Lab", "allow", next); }
        catch (error) { result.error = String(error); restore(); }
    }
    setTimeout(next, 4000);
}
