# Setting up the client
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

# Start the system.
osc_startup()

# Make client channels to send packets.
# Need to get ip and port as input field 
ip = # please contact Nima or Karsten for access to IP
port = # please contact Nima or Karsten for access to port
clientName = "sac"
osc_udp_client(ip, port, clientName)