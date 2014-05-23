
import os
import sys
import subprocess
import re
from router import Router
import shutil
from netkit_component import NetkitComponent
class TorNode(NetkitComponent):

  def __init__(self, name, is_ipv6):
    NetkitComponent.__init__(self, name, is_ipv6)
    self.dirServer = None

  def install_tor(self, pathToDir, pathToTor):
    """
       just copy tor binary into the virtual machine
    """
    
    if not os.path.isdir(pathToDir+"/"+self.attr['name']+"/root"):
      try:
	os.makedirs(pathToDir+"/"+self.attr['name']+"/root")
      except OSError:
	print "error when makedirs of /usr/sbin"
    shutil.copyfile(pathToTor+"/tor",pathToDir+"/"+self.attr['name']+"/root/tor")

 
  def fill_startup_file(self, path):
    """
    	configure the node to run those command in startup
    """
    f = open(path+"/"+self.attr['name']+".startup", "w")

    for IF in self.attr['IF']:
      f.write("ifconfig eth"+str(IF)+" up\n")
      if self.is_ipv6:
	f.write("ifconfig eth"+str(IF)+" add "+self.attr['map_IF_ipv6'][IF]+"/64\n")
      else:
	f.write("ifconfig eth"+str(IF)+" "+self.attr['map_IF_ipv4'][IF]+"\n")
       #flush routing table
      interface, neighbor = self.attr['map_IF_neighbor'][0]
      if interface == IF:
        ip = self.get_gw_ip(neighbor)
      else:
	print "error, this node should have only one interface\n"
	sys.exit(-1)
      f.write("ip route flush dev eth"+str(IF)+"\n")
      f.write("route add -net "+ip+" netmask 255.255.255.255 dev eth"+str(IF)+"\n")
      f.write("route add default gw "+ip+"\n")
      break
    f.write("sysctl fs.file-max=100000\n")
    f.write("chmod +x /root/tor\n")
    #f.write("chown debian-t /etc/tor\n")
    #f.write("sysctl net.mptcp.mptcp_ndiffports=2")
    f.write("chown -R debian-tor /var/lib/tor\n")
    f.write("/etc/init.d/tor restart\n") #fix the issue of debian-t user
    f.write("chown -R debian-tor /var/lib/tor\n")
    # LAUNCH TOR
    #f.write("tor\n")

  def preConfig(self, path):
    """
    path - path to root netkit lab
    Configuration of dir on the virtual machine
    /etc/tor/ contains torrc
    /var/lib/tor/ contains keys and other data stored by the tor process
    """
    # to match the default configuration file directory
    if not os.path.isdir(path+"/"+self.attr['name']+"/etc/tor/"):
      try:
	os.makedirs(path+"/"+self.attr['name']+"/etc/tor/")
      except OSError:
	print "Error when mkdir /etc/tor/"
    # to match the default DataDirectory
    if not os.path.isdir(path+"/"+self.attr['name']+"/var/lib/tor/"):
      try:
	os.makedirs(path+"/"+self.attr['name']+"/var/lib/tor/")
      except OSError:
	print "Error when mkdir /var/lib/tor"


  def config(self, path):
    """ Called of each ToR node to build Torrc file"""

    if self.dirServer is not None:

      f = open(path+"/"+self.attr['name']+"/etc/tor/torrc","w")
      f.write("TestingTorNetwork 1\n")
      f.write("RunAsDaemon 1\n")
      f.write("Nickname "+self.attr['name']+"\n")
      f.write("ShutdownWaitLength 0\n")
      f.write("Log notice file /etc/tor/notice.log\n")
      f.write("Log info file /etc/tor/info.log\n")
      f.write("ProtocolWarnings 1\n")
      f.write("SafeLogging 0\n")

    else:
      print "DirServer must be configured \n"
      sys.exit(-1)

  def set_dirServer(self, dirServer):
    """ dirServer is a list of directory servers """
    self.dirServer = dirServer

class TorClient(TorNode):

  def __init__(self, name, is_ipv6):
    TorNode.__init__(self, name, is_ipv6)

  def config(self, path):
    TorNode.config(self, path)
    f = open(path+"/"+self.attr['name']+"/etc/tor/torrc","a")
    for dirserver in self.dirServer:
      f.write("DirServer "+dirserver+"\n")
    f.write("SocksPort 9050\n")
 
  
class TorRelay(TorNode):
  
  def __init__(self, name, is_ipv6):
    TorNode.__init__(self, name, is_ipv6)

  def config(self, path):
    TorNode.config(self, path)
    f = open(path+"/"+self.attr['name']+"/etc/tor/torrc","a")
    for dirserver in self.dirServer:
      f.write("DirServer "+dirserver+"\n")

    f.write("SocksPort 9050\n")
    f.write("OrPort auto\n")
    if self.is_ipv6:
      key, value = self.attr['map_IF_ipv6'].popitem()
      f.write("Address "+value+"\n")
    else:
      key, value = self.attr['map_IF_ipv4'].popitem()
      f.write("Address "+value+"\n")

class TorAuthorityServer(TorNode):
  """

  authority server should have 1 interface
  """
  def __init__(self, name, is_ipv6):
    TorNode.__init__(self, name, is_ipv6)
    self.fingerprint = None
    self.ip_addr = []

  def set_ip(self):
    for IF in self.attr['IF']:
      if not self.is_ipv6:
        self.ip_addr += [self.attr['map_IF_ipv4'][IF]]
  
  def preConfig(self, path):
    TorNode.preConfig(self, path)
    if not os.path.isdir(path+"/"+self.attr['name']+"/var/lib/tor/keys"):
      try:
        os.mkdir(path+"/"+self.attr['name']+"/var/lib/tor/keys")
      except OSError:
	print "Error occured when mkdir /var/lib/tor/keys"


  def config(self, path):
    TorNode.config(self, path)
    
    if(len(self.ip_addr) > 1):
      print "this authority server has more than one interface. The IP used for torrc is %s" % self.ip_addr[0] 

    f = open(path+"/"+self.attr['name']+"/etc/tor/torrc","a")
    for dirserver in self.dirServer:
      f.write("DirServer "+dirserver+"\n")
	
    f.write("SocksPort 9050\n")
    f.write("OrPort auto\n")
    f.write("Address "+self.ip_addr[0]+"\n")
    f.write("DirPort 7000\n")
    f.write("AuthoritativeDirectory 1\n")
    f.write("V3AuthoritativeDirectory 1\n")
    f.write("ExitPolicy reject *:*\n") 
    f.write("TestingV3AuthInitialVotingInterval 300\n")
    f.write("TestingV3AuthInitialVoteDelay 50\n")
    f.write("TestingV3AuthInitialDistDelay 50\n")
   #f.write("TestingV3AuthVotingStartOffset 0\n")

  def genAuthKey(self, path):
    """
	Generate an identity key for this authority server
	and get the fingerprint
    """
    tor_gencert = "/usr/bin/tor-gencert"
    datadir = path+"/"+self.attr['name']+"/var/lib/tor" #default dir. Maybe add the possibility to choose
    lifetime = 12
    idfile   = os.path.join(datadir,'keys',"authority_identity_key")
    skfile   = os.path.join(datadir,'keys',"authority_signing_key")
    certfile = os.path.join(datadir,'keys',"authority_certificate")
    addr = self.ip_addr[0]+":7000"
    passphrase = "flo" #Security first :')
    #if all(os.path.exists(f) for f in [idfile, skfile,  certfile]):
     # return
    cmdline = [
	tor_gencert,
	'--create-identity-key',
	'--passphrase-fd', '0',
	'-i', idfile,
	'-s', skfile,
	'-c', certfile,
	'-m', str(lifetime),
	'-a', addr]
    p = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    p.communicate(passphrase+"\n")
    if p.returncode < 0 :
      print "error occured in tor_gencert\n"
      sys.exit(-1)

    tor = "/usr/sbin/tor"
    idfile = os.path.join(datadir, 'keys', 'identity_key')
    cmdline = [
       tor,
       "--quiet",
       "--list-fingerprint",
       "--orport", "1",
       "--dirserver",
          "xyzzy 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff",
       "--datadirectory", datadir ]

    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    self.fingerprint = "".join(stdout.split()[1:])
    if p.returncode < 0:
      print "error occured tor command line"
      sys.exit(-1)

  def getDirServerLine(self, path):
    """
      DirServer [nickname] [flags] address:port fingerprint
    """ 
    datadir = path+"/"+self.attr['name']+"/var/lib/tor" 
    certfile = os.path.join(datadir,'keys',"authority_certificate")
    v3id = None
    with open(certfile, 'r') as f:
      for line in f:
	if line.startswith("fingerprint"):
	  v3id = line.split()[1].strip()
	  break
    return ""+self.attr['name']+" hs v3ident="+v3id+" "+self.ip_addr[0]+":7000 "+str(self.fingerprint)
