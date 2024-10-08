#!/usr/bin/python
""" This example shows how to create a Mininet object and add nodes to
it manually.  """

"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

"Function definition:  This is called from the main function"
def firstNetwork():

	"Create an empty network and add nodes to it."
	net = Mininet()

	info( '*** Adding controller\n' ) 
	net.addController( 'c0' )

	info( '*** Adding hosts \n' )
	h1 = net.addHost( 'h1', ip='10.0.0.1/24') 
	h2 = net.addHost( 'h2', ip='10.0.0.2/24')
	h3 = net.addHost( 'h3', ip='10.0.1.3/24') 

	info( '*** Adding router \n' )
	r1 = net.addHost( 'r1', ip='10.0.0.100/24' ) 

	info( '*** Adding switch \n' ) 
	s12 = net.addSwitch( 's12' )

	info( '*** Creating links\n' ) 
	net.addLink( h1, s12 ) 
	net.addLink( h2, s12 )
	net.addLink( s12, r1, intfName2='r1-eth0' )
	net.addLink( r1, h3, intfName1='r1-eth1' )

	info( '*** Starting network\n') 
	net.start()
	"This is used to run commands on the hosts"

	info( '*** Configuring hosts\n' )
	r1.cmd('ifconfig r1-eth1 10.0.1.100 netmask 255.255.255.0')
	r1.cmd('echo 0 > /proc/sys/net/ipv4/ip_forward') # wrong
	# r1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward') # active
	h1.cmd('ip route add default via 10.0.0.100')
	h2.cmd('ip route add default via 10.0.0.101') # wrong
	# h2.cmd('ip route add default via 10.0.0.100') # ip route del default via 10.0.0.101 # ip route add default via 10.0.0.100
	h3.cmd('ip route add default via 10.0.1.100')

	info( '*** Starting xterm on hosts\n' )
	h1.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h1 &') 
	h2.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h2 &')
	h3.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h3 &')
	r1.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T r1 &')

	info( '*** Running the command line interface\n' ) 
	CLI( net )

	info( '*** Closing the terminals on the hosts\n' ) 
	h1.cmd("killall xterm")
	h2.cmd("killall xterm")
	h3.cmd("killall xterm")
	r1.cmd("killall xterm")

	info( '*** Stopping network' )
	net.stop()

"main Function: This is called when the Python file is run" 
if __name__ == '__main__':
	setLogLevel( 'info' )
	firstNetwork()