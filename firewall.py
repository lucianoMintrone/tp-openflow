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
from pox.lib.addresses import EthAddr
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
        print("ARRANCA EL Firewall")
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''

        self.__block_dst_port(port= 80, event= event)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

    def __block_dst_port(self, port, event):
        ''' First rule: discard all packages that have destination port 80 (IPv4, TCP only for now) '''

        block = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.TCP_PROTOCOL, tp_dst = port)

        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)


def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)