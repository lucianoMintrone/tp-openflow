from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.addresses import EthAddr, IPAddr
import pox.lib.packet as pkt
from collections import namedtuple
import os
import json

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)

        with open('config.json', 'r') as f:
            self.config = json.load(f)

        log.info("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):


        log.info("Switch %s connecting", event.ofp.ports[0].name)

        current_switch_name = event.ofp.ports[0].name

        if current_switch_name == self.config["firewall_switch_name"]:

            rules = []            

            # First rule: discard all packages that have destination port {port}
            rules.extend(self._discard_dst_port(port= 80))

            # Second rule: discard all packages sent by host 1, dest. port 5001 and UDP
            rules.extend(self._discard_udp_from_host_to_port(host= "10.0.0.1", port= 5001))

            # Third rule: block the communication between two hosts
            rules.extend(self._discard_between_two_hosts())

            for rule in rules:

                flow_mod = of.ofp_flow_mod()
                flow_mod.match = rule
                event.connection.send(flow_mod)


            log.info("Firewall rules installed on switch %s", current_switch_name)

    def _discard_dst_port(self, port):

        discard_ipv4_tcp = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.TCP_PROTOCOL, tp_dst = port)
        
        discard_ipv4_udp = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.UDP_PROTOCOL, tp_dst = port)

        return [discard_ipv4_tcp, discard_ipv4_udp]


    def _discard_udp_from_host_to_port(self, host, port):

        discard_rule = of.ofp_match(
            dl_type = pkt.ethernet.IP_TYPE, 
            nw_proto = pkt.ipv4.UDP_PROTOCOL,
            nw_src = IPAddr(host),
            tp_dst = port)

        return [discard_rule]


    def _discard_between_two_hosts(self):

        host_a_mac_addr = self.config["rule_3_hosts_addr"][0]["mac_addr"]
        host_b_mac_addr = self.config["rule_3_hosts_addr"][1]["mac_addr"]

        discard_a_to_b = of.ofp_match(
            dl_src = EthAddr(host_a_mac_addr), 
            dl_dst = EthAddr(host_b_mac_addr))

        discard_b_to_a = of.ofp_match(
            dl_src = EthAddr(host_b_mac_addr), 
            dl_dst = EthAddr(host_a_mac_addr))

        return [discard_a_to_b, discard_b_to_a]



def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)