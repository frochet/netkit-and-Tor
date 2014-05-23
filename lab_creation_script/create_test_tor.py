
import sys
from router import Router
from create_lab import Create_lab
from torNode import *
class Create_test_tor(Create_lab):

  def __init__(self, pathToGraph, pathToDir, pathToTor):

    Create_lab.__init__(self, pathToGraph)
    ncomp = None
    for node in self.graph.nodes():
      if "torclient" in node :
	ncomp = TorClient(node, False)
      elif "relay" in node:
	ncomp = TorRelay(node, False)
      elif "directory" in node:
	ncomp = TorAuthorityServer(node, False)
      elif "router" in node: 
	ncomp = Router(node, False) 
      self.netkit_components += [ncomp]

    self.set_interface_and_zone()
    self.set_data_from_edges()
    self.give_ipv4() 
	
    data_directory_server = []
    for node in self.netkit_components:
      node.create_dir(pathToDir)
      node.create_startup(pathToDir)
      node.fill_startup_file(pathToDir)
      if "directory" in node.attr['name']:
	node.set_ip()
	node.preConfig(pathToDir)
	node.genAuthKey(pathToDir)
	data_directory_server += [node.getDirServerLine(pathToDir)] #get the information
							   #to put after
							   #DirServer in torrc
      if "router" in node.attr['name']: 
        node.create_ospf_dir(pathToDir)
    for node in self.netkit_components:
      if "torclient" in node.attr['name'] or "relay" in node.attr['name'] or "directory" in node.attr['name'] :
	node.set_dirServer(data_directory_server)
	node.preConfig(pathToDir)
	node.config(pathToDir)
	node.install_tor(pathToDir, pathToTor)
    
    self.create_conf(pathToDir, memory=128)
# END of class

def usage():
  print "Usage : python create_test_tor.py -f path_to_dot_file path_to_lab path_to_tor\n"
	
def main(argv):
  if len(argv)==0:
    usage()
  else:
    if argv[0] == "-f":
      lab = Create_test_tor(argv[1], argv[2], argv[3])
    else:
      usage()


if __name__ == "__main__":
  main(sys.argv[1:])

