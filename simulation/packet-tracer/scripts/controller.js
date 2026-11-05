// File Script Module helpers for the hospital candidate. No host file or Internet access.
// Calls are explicit in Debug: hospital.configure(), hospital.services(), hospital.tests().
var hospital = {
    records: [],
    snapshots: [],
    spec: function () { return JSON.parse($getData("hospital-spec.json")); },
    save: function () {
        $putData("hospital-results.json", JSON.stringify({records: this.records, snapshots: this.snapshots}));
    },
    add: function (record) {
        record.time = new Date().toISOString();
        this.records.push(record);
        this.save();
        dprint(JSON.stringify(record));
    },
    configure: function () {
        var configs = this.spec().configs;
        var results = [];
        for (var name in configs) {
            var device = ipc.network().getDevice(name);
            device.skipBoot();
            device.enterCommand("configure terminal", "enable");
            // Recreate named ACLs so a retry preserves first-match ordering.
            var aclNames = configs[name].match(/^ip access-list extended .+$/gm) || [];
            for (var a = 0; a < aclNames.length; a++) {
                device.enterCommand("no " + aclNames[a], "global");
            }
            var lines = configs[name].split(/\r?\n/);
            var policyClass = false;
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i].replace(/^\s+|\s+$/g, "");
                if (!line || line.charAt(0) === "!") { continue; }
                // Saved configuration markers are not interactive IOS commands.
                if (/^boot-(start|end)-marker$/.test(line)) { continue; }
                var globalLine = !/^\s/.test(lines[i]);
                if (globalLine) { policyClass = false; }
                if (!globalLine && /^class /.test(line)) {
                    if (policyClass) { device.enterCommand("exit", ""); }
                    policyClass = true;
                }
                var response = device.enterCommand(line, globalLine ? "global" : "");
                if (response.first !== 0) {
                    results.push({node: name, command: line, response: response});
                }
            }
            device.enterCommand("end", "");
            device.enterCommand("write memory", "enable");
        }
        $putData("config-check.json", JSON.stringify(results));
        dprint("CONFIG_ERRORS " + JSON.stringify(results));
    },
    services: function () {
        var spec = this.spec();
        var results = [];
        for (var i = 0; i < spec.endpoints.length; i++) {
            var endpoint = spec.endpoints[i];
            var device = ipc.network().getDevice(endpoint.node);
            try {
                device.setDefaultGateway(endpoint.gateway);
                this.port(endpoint.node).setDnsServerIp(endpoint.dns);
                if (endpoint.kind === "server" || endpoint.kind === "external-server") {
                    var http = device.getProcess("HttpServer");
                    var marker = "HOSPITAL-LAB-" + endpoint.node;
                    if (endpoint.services.indexOf("HTTP") >= 0) {
                        http.setEnable(true);
                        http.setPageContents("index.html", "<html><body><h1>" + marker + "</h1></body></html>");
                    } else {
                        http.setEnable(false);
                    }
                    if (endpoint.node.indexOf("-Infra") >= 0 || endpoint.node === "Web-Lab") {
                        var dns = device.getProcess("DnsServer");
                        dns.setEnable(true);
                        dns.addARecordToNameServerDb("web.hospital.test", "192.0.2.100");
                        if (endpoint.node !== "Web-Lab") {
                            dns.addARecordToNameServerDb("his.hospital.test", "10.10.70.11");
                            dns.addARecordToNameServerDb("dmz.hospital.test", "10.10.80.10");
                            var dhcp = device.getProcess("DhcpServerMain").getDhcpServerProcessByPortName("FastEthernet0");
                            while (dhcp.getPoolCount() > 0) { dhcp.removePool(dhcp.getPoolAt(0).getDhcpPoolName()); }
                            for (var p = 0; p < spec.pools.length; p++) {
                                var pool = spec.pools[p];
                                if (pool.server === endpoint.ip) {
                                    dhcp.addNewPool(pool.name, pool.gateway, pool.dns, pool.start, pool.mask, Number(pool.max_users), "0.0.0.0", "0.0.0.0");
                                }
                            }
                            dhcp.setEnable(true);
                        }
                    }
                }
                results.push({node: endpoint.node, configured: true});
            } catch (error) {
                results.push({node: endpoint.node, error: String(error)});
            }
        }
        for (var j = 0; j < spec.endpoints.length; j++) {
            var client = spec.endpoints[j];
            if (client.kind === "client-dhcp-example") {
                try {
                    var dhcpClient = ipc.network().getDevice(client.node);
                    dhcpClient.setDhcpFlag(false);
                    dhcpClient.setDhcpFlag(true);
                }
                catch (error) { results.push({node: client.node, dhcp_error: String(error)}); }
            }
        }
        $putData("services-check.json", JSON.stringify(results));
        dprint("SERVICES " + JSON.stringify(results));
    },
    port: function (name) {
        var device = ipc.network().getDevice(name);
        var ethernet = null;
        for (var p = 0; p < device.getPortCount(); p++) {
            var port = device.getPortAt(p);
            if (port.getName() === "Wireless0") { return port; }
            if (port.getName() === "FastEthernet0") { ethernet = port; }
        }
        if (!ethernet) { throw new Error("No host network port for " + name); }
        return ethernet;
    },
    address: function (name) {
        return this.port(name).getIpAddress();
    },
    ping: function (group, source, target, expected, next) {
        var output = "";
        var active = true;
        var line = ipc.network().getDevice(source).getCommandPrompt();
        var command = "ping " + target;
        function finish(reason) {
            if (!active) { return; }
            active = false;
            hospital.add({kind: "ping", group: group, source: source, target: target,
                          source_ip: hospital.address(source), expected: expected,
                          command: command, completion: reason, output: output});
            // Let the native terminal finish writing its footer and return to the prompt.
            setTimeout(next, 500);
        }
        line.registerEvent("outputWritten", null, function (event, args) {
            if (active) {
                output += args.newOutput;
                if (output.indexOf(command) >= 0 && /Packets: Sent = \d+, Received = \d+, Lost = \d+/.test(output)) {
                    finish("statistics");
                }
            }
        });
        line.enterCommand(command);
        setTimeout(function () { finish("timeout"); }, 22000);
    },
    http: function (group, source, url, marker, expected, next) {
        var client = ipc.network().getDevice(source).getProcess("HttpClient");
        var events = [];
        var active = true;
        client.registerEvent("onDone", null, function (event, args) {
            if (active) { events.push(args); }
        });
        var started = client.go(url);
        setTimeout(function () {
            active = false;
            hospital.add({kind: "http", group: group, source: source, url: url,
                          source_ip: hospital.address(source), marker: marker, expected: expected,
                          initiated: started, events: events, page: client.getLastPageContent()});
            client.cancel();
            next();
        }, 12000);
    },
    capture: function () {
        var commands = {
            "Main-GW": ["show ip ospf neighbor", "show ip route"],
            "Main-Core": ["show ip route", "show access-lists"],
            "DBP-GW": ["show ip ospf neighbor", "show ip route", "show access-lists"],
            "BHTQ-GW": ["show ip ospf neighbor", "show ip route", "show access-lists"],
            "Main-Edge": ["show ip nat translations", "show ip nat statistics", "show ip route"],
            "Main-FW": ["show zone-pair security", "show policy-map type inspect zone-pair", "show ip route"]
        };
        this.snapshots = [];
        for (var name in commands) {
            for (var i = 0; i < commands[name].length; i++) {
                this.snapshots.push({node: name, command: commands[name][i],
                                     result: ipc.network().getDevice(name).enterCommand(commands[name][i], "enable")});
            }
        }
        var addresses = [];
        var endpoints = this.spec().endpoints;
        for (var j = 0; j < endpoints.length; j++) {
            var node = endpoints[j].node;
            addresses.push({node: node, ip: this.address(node)});
        }
        $putData("addresses.json", JSON.stringify(addresses));
        this.save();
        dprint("HOSPITAL_CAPTURE_DONE");
    },
    tests: function () {
        var endpoints = this.spec().endpoints;
        for (var e = 0; e < endpoints.length; e++) {
            if (endpoints[e].kind === "client-dhcp-example") {
                var address = this.address(endpoints[e].node);
                if (!address || address === "0.0.0.0" || address.indexOf("169.254.") === 0) {
                    throw new Error("DHCP not ready for " + endpoints[e].node + ": " + address);
                }
            }
        }
        this.records = [];
        var jobs = [];
        function ping(group, source, target, expected) {
            jobs.push(function (next) { hospital.ping(group, source, target, expected, next); });
        }
        function http(group, source, url, marker, expected) {
            jobs.push(function (next) { hospital.http(group, source, url, marker, expected, next); });
        }
        ping("TC01", "Main-PC10-A", this.address("Main-PC10-B"), "allow");
        ping("TC01", "Main-PC10-B", this.address("Main-PC10-A"), "allow");
        ping("TC02", "Main-PC10-A", this.address("Main-PC20"), "allow");
        ping("TC02", "Main-PC20", this.address("Main-PC10-A"), "allow");
        for (var i = 0; i < 2; i++) {
            var site = ["DBP", "BHTQ"][i];
            ping("TC03", "Main-PC10-A", this.address(site + "-PC10"), "allow");
            ping("TC03", site + "-PC10", this.address("Main-PC10-A"), "allow");
        }
        http("TC02", "Main-PC10-A", "http://10.10.70.11", "HOSPITAL-LAB-Main-HIS", "allow");
        http("TC04", "Main-PC10-A", "http://10.10.80.10", "HOSPITAL-LAB-Main-WebDMZ", "allow");
        http("TC04", "Web-Lab", "http://198.51.100.2:8080", "HOSPITAL-LAB-Main-WebDMZ", "allow");
        for (var j = 0; j < 3; j++) {
            var current = ["Main", "DBP", "BHTQ"][j];
            var pc = current === "Main" ? "Main-PC10-A" : current + "-PC10";
            ping("TC05", current + "-Guest", this.address(pc), "deny");
            http("TC05", pc, "http://10.10.70.11", "HOSPITAL-LAB-Main-HIS", "allow");
            http("TC05", current + "-Guest", "http://10.10.70.11", "HOSPITAL-LAB-Main-HIS", "deny");
            http("TC06", pc, "http://web.hospital.test", "HOSPITAL-LAB-Web-Lab", "allow");
            http("TC06", current + "-Guest", "http://web.hospital.test", "HOSPITAL-LAB-Web-Lab", "allow");
            http("WIFI", current + "-Staff", "http://10.10.70.11", "HOSPITAL-LAB-Main-HIS", "allow");
            http("WIFI", current + "-Staff", "http://web.hospital.test", "HOSPITAL-LAB-Web-Lab", "allow");
        }
        var position = 0;
        function next() {
            if (position === jobs.length) {
                hospital.capture();
                dprint("HOSPITAL_TESTS_DONE " + hospital.records.length);
                return;
            }
            var job = jobs[position++];
            try { job(next); }
            catch (error) { hospital.add({kind: "exception", job: position, error: String(error)}); next(); }
        }
        next();
    }
};
function main() {}
function cleanUp() {}

// Keep convergence/ARP observations separately; never replace the initial run.
function warmupHospitalAndTest() {
    var pairs = [["Main-PC10-A", "Main-PC10-B"], ["Main-PC10-B", "Main-PC10-A"],
        ["Main-PC10-A", "Main-PC20"], ["Main-PC20", "Main-PC10-A"],
        ["Main-PC10-A", "DBP-PC10"], ["DBP-PC10", "Main-PC10-A"],
        ["Main-PC10-A", "BHTQ-PC10"], ["BHTQ-PC10", "Main-PC10-A"]];
    hospital.records = [];
    var position = 0;
    function next() {
        if (position === pairs.length) {
            $putData("warmup-results.json", JSON.stringify(hospital.records));
            hospital.tests();
            return;
        }
        var pair = pairs[position++];
        hospital.ping("WARMUP", pair[0], hospital.address(pair[1]), "allow", next);
    }
    next();
}
