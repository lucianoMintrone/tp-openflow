from mininet.topo import Topo


class TP3Topo(Topo):

    def build(self):

        number_of_switches = int(input("Numero de switches: "))

        # Add hosts and switches
        leftHost = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        rightHost = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        thirdHost = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        fourthHost = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')
        switches = []
        for i in range(number_of_switches):
            switches.append(self.addSwitch(f's{i}'))

        # Add links
        self.addLink(leftHost, switches[0])
        self.addLink(thirdHost, switches[0])
        for i in range(number_of_switches):
            if i == 0:
                continue

            self.addLink(switches[i - 1], switches[i])

        self.addLink(switches[-1], rightHost)
        self.addLink(switches[-1], fourthHost)


topos = {'TP3topo': (lambda: TP3Topo())}
