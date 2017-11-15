#!/bin/bash
#
### Setup Port Forwarding
iptables -t nat -A POSTROUTING -j MASQUERADE
sysctl -w net.ipv4.ip_forward=1
echo 1 > /proc/sys/net/ipv4/ip_forward
#
### Adding routings
iptables -t nat -A PREROUTING -p tcp --dport 7041 -j DNAT --to-destination 10.8.0.20:22 #consumer
iptables -t nat -A PREROUTING -p tcp --dport 7046 -j DNAT --to-destination 10.8.0.25:22 #marketplace
iptables -t nat -A PREROUTING -p tcp --dport 7047 -j DNAT --to-destination 10.8.0.21:22 #merchant
iptables -t nat -A PREROUTING -p tcp --dport 7042 -j DNAT --to-destination 10.8.0.23:22 #ui
iptables -t nat -A PREROUTING -p tcp --dport 7045 -j DNAT --to-destination 10.8.0.22:22 #producer
iptables -t nat -A PREROUTING -p tcp --dport 7049 -j DNAT --to-destination 10.8.0.26:22 #logger
#
iptables-save
#
### Delete nat rules if necessary
#sudo iptables -t nat -F
#sudo iptables -L -t nat --line-numbers
#sudo iptables -t nat -D PREROUTING 4
