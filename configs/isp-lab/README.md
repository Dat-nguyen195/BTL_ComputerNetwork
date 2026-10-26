# ISP/Internet lab

Ba node, ba file: [ISP1](isp-edge-lab.cfg), [ISP2](isp2-router.cfg), [INET-Core](internet-core-router.cfg). `isp-edge-lab.cfg` giữ tên cũ nhưng chỉ còn ISP1; không nạp cả ba file vào một router.

Web/DNS chung `192.0.2.100/26`, gateway `192.0.2.65`, HTTP/DNS ON, record `web.hospital.test -> 192.0.2.100`. INET-Core loopback .11/.22 làm đích probe phía sau ISP. Nối dây và test theo [module WAN](../../simulation/modules/tv1-wan/README.md). Chưa có project/runtime evidence; tên ISP không gắn với hợp đồng nhà mạng thật.
