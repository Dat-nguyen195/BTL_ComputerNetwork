! IOS ZBF overlay, NOT ASA syntax. No NAT here; Main-Edge owns all NAT.
! The self-zone is not hardened by these transit policies. VTY stays disabled.
zone security LAN
zone security OUTSIDE
zone security DMZ
!
ip access-list extended FW-INTERNET
 permit tcp 10.10.0.0 0.0.255.255 any eq 80
 permit tcp 10.10.0.0 0.0.255.255 any eq 443
 permit tcp 10.20.0.0 0.0.255.255 any eq 80
 permit tcp 10.20.0.0 0.0.255.255 any eq 443
 permit tcp 10.30.0.0 0.0.255.255 any eq 80
 permit tcp 10.30.0.0 0.0.255.255 any eq 443
 permit udp 10.0.0.0 0.255.255.255 host 192.0.2.100 eq 53
 permit tcp 10.0.0.0 0.255.255.255 host 192.0.2.100 eq 53
 permit icmp 10.0.0.0 0.255.255.255 host 192.0.2.100
!
ip access-list extended FW-LAN-DMZ
 deny ip 10.10.100.0 0.0.1.255 any
 deny ip 10.20.100.0 0.0.1.255 any
 deny ip 10.30.100.0 0.0.1.255 any
 permit tcp host 10.10.90.11 10.10.80.0 0.0.0.31 eq 22
 permit tcp 10.10.0.0 0.0.255.255 host 10.10.80.10 eq 80
 permit tcp 10.20.0.0 0.0.255.255 host 10.10.80.10 eq 80
 permit tcp 10.30.0.0 0.0.255.255 host 10.10.80.10 eq 80
!
ip access-list extended FW-PUBLISHED-WEB
 permit tcp any host 10.10.80.10 eq 80
!
ip access-list extended FW-DMZ-UPDATE
 permit udp 10.10.80.0 0.0.0.31 host 192.0.2.100 eq 53
 permit tcp 10.10.80.0 0.0.0.31 host 192.0.2.100 eq 53
 permit tcp 10.10.80.0 0.0.0.31 any eq 80
 permit tcp 10.10.80.0 0.0.0.31 any eq 443
!
class-map type inspect match-all CM-INTERNET
 match access-group name FW-INTERNET
class-map type inspect match-all CM-LAN-DMZ
 match access-group name FW-LAN-DMZ
class-map type inspect match-all CM-PUBLISHED-WEB
 match access-group name FW-PUBLISHED-WEB
class-map type inspect match-all CM-DMZ-UPDATE
 match access-group name FW-DMZ-UPDATE
!
policy-map type inspect PM-INTERNET
 class type inspect CM-INTERNET
  inspect
 class class-default
  drop log
policy-map type inspect PM-LAN-DMZ
 class type inspect CM-LAN-DMZ
  inspect
 class class-default
  drop log
policy-map type inspect PM-PUBLISHED-WEB
 class type inspect CM-PUBLISHED-WEB
  inspect
 class class-default
  drop log
policy-map type inspect PM-DMZ-UPDATE
 class type inspect CM-DMZ-UPDATE
  inspect
 class class-default
  drop log
!
zone-pair security LAN-OUT source LAN destination OUTSIDE
 service-policy type inspect PM-INTERNET
zone-pair security LAN-DMZ source LAN destination DMZ
 service-policy type inspect PM-LAN-DMZ
zone-pair security OUT-DMZ source OUTSIDE destination DMZ
 service-policy type inspect PM-PUBLISHED-WEB
zone-pair security DMZ-OUT source DMZ destination OUTSIDE
 service-policy type inspect PM-DMZ-UPDATE
! No OUTSIDE->LAN or DMZ->LAN initiation policy. Inspected replies are stateful.
interface GigabitEthernet0/0
 zone-member security LAN
interface GigabitEthernet0/1
 zone-member security OUTSIDE
interface GigabitEthernet0/2
 zone-member security DMZ
no ip http server
no ip http secure-server
