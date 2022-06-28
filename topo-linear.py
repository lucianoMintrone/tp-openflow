"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."
        number_of_switches = int(input("Numero de switches: "))

        # Add hosts and switches
        leftHost = self.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
        rightHost = self.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
        switches = []
        for i in range(number_of_switches):
            switches.append( self.addSwitch( f's{i}' ) )

        # Add links
        self.addLink( leftHost, switches[0] )
        for i in range(number_of_switches):
            if i == 0:
                continue

            self.addLink( switches[i-1], switches[i] )

        self.addLink( switches[-1], rightHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }
