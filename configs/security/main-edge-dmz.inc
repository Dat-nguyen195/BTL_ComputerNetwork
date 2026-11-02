! TV3 overlay for Main-Edge; merge with TV1 base via scripts/build_lab.py.
! Publish only ISP2, which is also the DMZ source PBR preference.
! ISP2 failure removes inbound DMZ service; this is NOT inbound HA.
ip nat inside source static tcp 10.10.80.10 80 198.51.100.2 8080 extendable
no ip http server
no ip http secure-server
interface GigabitEthernet0/1
 no cdp enable
interface GigabitEthernet0/2
 no cdp enable
