'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application
Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr, IPAddr
import pox.lib.packet as pkt
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):

        ''' First rule: discard all packages that have destination port {port} '''
        self._discard_dst_port(port= 80, event= event)

        ''' Second rule: discard all packages sent by host 1, dest. port 5001 and UDP '''
        self._discard_udp_from_host_to_port(host= "10.0.0.1", port= 5001, event= event)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

    def _discard_dst_port(self, port, event):

        discard_ipv4_tcp = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.TCP_PROTOCOL, tp_dst = port)
        
        discard_ipv4_udp = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.UDP_PROTOCOL, tp_dst = port)


        for discard_rule in [discard_ipv4_tcp, discard_ipv4_udp]:

            flow_mod = of.ofp_flow_mod()
            flow_mod.match = discard_rule
            event.connection.send(flow_mod)

    def _discard_udp_from_host_to_port(self, host, port, event):

        discard_rule = of.ofp_match(
            dl_type = pkt.ethernet.IP_TYPE, 
            nw_proto = pkt.ipv4.UDP_PROTOCOL,
            nw_src = IPAddr(host),
            tp_dst = port)

        flow_mod = of.ofp_flow_mod()
        flow_mod.match = discard_rule
        event.connection.send(flow_mod)



def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)