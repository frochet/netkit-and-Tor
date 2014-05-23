from netkit_component import NetkitComponent
import os
import sys


class Router(NetkitComponent):
  #static varibles which must be share between instances.
  As = 1
  Rid = '0.0.0.1' 

  def __init__(self, name, is_ipv6):
    NetkitComponent.__init__(self, name, is_ipv6)
    self.attr['as'] = 0
    self.attr['router-id'] = ''
    
  def define_router_id(self):
    self.attr['router-id'] = Router.Rid
    temp=map(int, Router.Rid.split("."))
    if temp[0] >= 255:
      printf("you made way too much router!")
      exit()
    if temp[1] >= 255:
      temp[1]=0
      temp[0]+=1
    if temp[2] >= 255:
      temp[2] = 0
      temp[1]+=1
    if temp[3] >= 255:
      temp[3] =0
      temp[2] +=1
    else:
      temp[3] +=1
      
    temp= map(str,temp)
    Router.Rid=".".join(temp)

  def define_as(self):
    self.attr['as'] = Router.As
    Router.As += 1

  def fill_startup_file(self, path):
    f = open(path+"/"+self.attr['name']+".startup","w")
    for IF in self.attr['IF']:
      f.write("ifconfig eth"+str(IF)+" up\n")
      if self.is_ipv6:
        f.write("ifconfig eth"+str(IF)+" add "+self.attr['map_IF_ipv6'][IF]+"/64\n")
      else:
	prefix = self.attr['map_IF_prefix'][IF]
	if len(prefix) <= 3:
	  f.write("ifconfig eth"+str(IF)+" "+self.attr['map_IF_ipv4'][IF]+"/8\n")
	elif len(prefix) <= 7:
	  f.write("ifconfig eth"+str(IF)+" "+self.attr['map_IF_ipv4'][IF]+"/16\n")
	elif len(prefix) <= 11:
	  f.write("ifconfig eth"+str(IF)+" "+self.attr['map_IF_ipv4'][IF]+"/24\n")
	elif len(prefix) <= 15:
	  f.write("ifconfig eth"+str(IF)+" "+self.attr['map_IF_ipv4'][IF]+"/32\n")
	else:
	  print "Prefix length not supported\n"
	  sys.exit(-1)

    if self.is_ipv6:
      f.write("# Active ipv6 forwarding\n") 
      f.write("sysctl -w net.ipv6.conf.all.forwarding=1\n")

    f.write("/etc/init.d/zebra start\n")
    f.close()
    self.set_bandwidth(path) 
    self.set_delay(path)
   

  def create_ospf_dir(self, path):
    self.define_router_id()
    self.define_as()
    try:
      os.makedirs(path+"/"+self.attr['name']+"/etc/quagga")
    except OSError:
      if not os.path.isdir(path+"/"+self.attr['name']+"/etc/quagga"):
	print "Bad things happened during directory set up. lab could not working properly"
    #fichier daemons
    f = open(path+"/"+self.attr['name']+"/etc/quagga/daemons","w")
    if self.is_ipv6:
      f.write("zebra=yes\nbgpd=no\nospfd=no\nospf6d=yes\nripd=no\nripngd=no")
    else:
      f.write("zebra=yes\nbgpd=no\nospfd=yes\nospf6d=no\nripd=no\nripngd=no")
    f.close()
    
    #fichier zebra.conf
    f = open(path+"/"+self.attr['name']+"/etc/quagga/zebra.conf","w")
    f.write("hostname Router\npassword zebra\nlog file /var/log/quagga/zebra.log")
    f.close()
    
    #fichier ospf6d.conf and ospfd.conf
    if self.is_ipv6:
      f = open(path+"/"+self.attr['name']+"/etc/quagga/ospf6d.conf","w")
      f.write("hostname ospf6d\npassword zebra\n")
      for IF in self.attr['map_weight']:
        f.write("interface eth"+str(IF)+"\n")
        f.write("ipv6 ospf6 cost "+self.attr['map_weight'][IF]+"\n")
      f.write("router ospf6\n")
      f.write("router-id "+self.attr['router-id']+"\n")
	#for IF in ...
      for IF in self.attr['IF']:
       f.write("interface eth"+str(IF)+" area 0.0.0.0\n")
      f.write("log file /var/log/zebra/ospf6d.log\n")
    else: 
      f = open(path+"/"+self.attr['name']+"/etc/quagga/ospfd.conf","w")
      f.write("hostname ospfd\npassword zebra\n")
      f.write("log file /var/log/zebra/ospfd.log\n")
      for IF in self.attr['map_weight']:
	f.write("interface eth"+str(IF)+"\n")
	f.writt("ip ospf cost "+self.attr['map_weight'][IF]+"\n")
      f.write("router ospf\n")
      f.write("router-id "+self.attr['router-id']+"\n")
      
      prefix = None
      tmplist = []
      for IF in self.attr['IF'] :
	prefix = self.attr['map_IF_prefix'][IF]
	if prefix in tmplist: continue
	tmplist += [prefix]
        if len(prefix) <= 3:
	  f.write("network "+prefix+".0.0.0/8 area 0.0.0.0\n")
	#f.write("area 0.0.0.0 range "+prefix+".0.0.0/8\n")
        elif len(prefix) <= 7:
	  f.write("network "+prefix+".0.0/16 area 0.0.0.0\n")
	#f.write("area 0.0.0.0 range "+prefix+".0.0/16\n")
        elif len(prefix) <= 11:
	  f.write("network "+prefix+".0/24 area 0.0.0.0\n")
	#f.write("area 0.0.0.0 range "+prefix+".0/24\n")
        elif len(prefix) <= 15:
	  f.write("network "+prefix+"/32 area 0.0.0.0\n")
	#f.write("area 0.0.0.0 range "+prefix+"/32\n")
        else:
	  print "Error: prefix length not supported"
	  sys.exit(-1)
      
    f.close()

  def create_ripng_dir(self,path):
    self.define_router_id()
    self.define_as()
    try:
      os.makedirs(path+"/"+self.attr['name']+"/etc/quagga")
    except OSError:
      if not os.path.isdir(path+"/"+self.attr['name']+"/etc/quagga"):
	print "Bad things happened during directory set up. lab could not working properly"
    #fichier daemons
    f = open(path+"/"+self.attr['name']+"/etc/quagga/daemons","w")
    f.write("zebra=yes\nbgpd=no\nospfd=no\nospf6d=no\nripd=no\nripngd=yes")
    f.close()
  
    #fichier zebra.conf
    f = open(path+"/"+self.attr['name']+"/etc/quagga/zebra.conf","w")
    f.write("hostname Router\npassword zebra\nlog file /var/log/quagga/zebra.log")
    f.close()

    #fichier ripngd.conf
    f = open(path+"/"+self.attr['name']+"/etc/quagga/ripngd.conf","w")
    f.write("router ripng\nnetwork ::/0")
    f.close()

  def create_bgp_dir(self,path):
    self.define_router_id()
    self.define_as()
    try:
      os.makedirs(path+"/"+self.attr['name']+"/etc/quagga")
    except OSError:  
      if not os.path.isdir(path+"/"+self.attr['name']+"/etc/quagga"):
	print "Bad things happened during directory set up. lab could not working properly"
       
    #fichier daemons
    f = open(path+"/"+self.attr['name']+"/etc/quagga/daemons","w")
    f.write("zebra=yes\nbgpd=yes\nospfd=no\nospf6d=no\nripd=no\nripngd=no")
    f.close()

    #fichier zebra.conf
    f = open(path+"/"+self.attr['name']+"/etc/quagga/zebra.conf","w")
    f.write("hostname Router\npassword zebra\nlog file /var/log/quagga/zebra.log")
    f.close()

    #fichier bgpd.conf
    f = open(path+"/"+self.attr['name']+"/etc/quagga/bgpd.conf","w")
    f.write("hostname bgpd\npassword zebra\n")
    f.write("router bgp "+str(Router.As)+"\n")
    f.write("!\n")
    f.write("bgp router-id "+str(self.attr['router-id'])+"\n")
    for (IF, neighbor) in self.attr['map_IF_neighbor']:
      f.write("neighbor "+neighbor.attr['map_IF_ipv6'][neighbor.get_interface_used_between(self.attr['name'])]+" remote-as "+str(neighbor.attr['as'])+"\n")
      f.write("!add routemap if it's needed.\n")
    f.write("!\n")
    for (IF, neighbor) in self.attr['map_IF_neighbor']:
      f.write("no neighbor "+neighbor.attr['map_IF_ipv6'][neighbor.get_interface_used_between(self.attr['name'])]+" activate\n")
    f.write("!\n")
    f.write("address-family ipv6\n")
    f.write("!add the network that the router must share below\n")
    f.write("!\n")
    for (IF, neighbor) in self.attr['map_IF_neighbor']:
      f.write("neighbor "+neighbor.attr['map_IF_ipv6'][neighbor.get_interface_used_between(self.attr['name'])]+" activate\n")
    f.write("exit-address-family\n")
    f.write("!\n")
    f.write("!make your community list and route map below\n")
    f.close()
      
