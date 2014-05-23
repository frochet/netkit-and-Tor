import networkx as nx
import random
import os
import sys
class Create_lab():
  """
   This class is a super class of any netkit labs. For each new netkit lab, you
   have to create a create_[name]_la.py python file which will inherits from
   this class.

   /!\ This class should never be instancied /!\ 
  """

  def __init__(self, pathToGraph):
    self.graph = nx.read_dot(pathToGraph)
   # self.graph = nx.to_agraph(self.graph)
    self.netkit_components = []
    self.zones_given = []

  
  def create_conf(self, pathToDir, lab_descr=None, lab_ver=None, lab_auth="O.Bonaventure,F.Rochet, J.Vellemans", lab_email=None, lab_web=None, memory=64):
    """
    This function is used to create the lab.conf file. You should always finish
    to use this when scripting a new lab, in a create_[name]_lab.py file

    """
    f = open(pathToDir+"/lab.conf", "w")
    if lab_descr:
      f.write("LAB_DESCRIPTION=\""+lab_descr+"\"\n")
    if lab_ver:
      f.write("LAB_VERSION="+lab_ver+"\n")
    if lab_auth :
      f.write("LAB_AUTHOR=\""+lab_auth+"\"\n")
    if lab_email:
      f.write("LAB_EMAIL="+lab_email+"\n")
    if lab_web:
      f.write("LAB_WEB="+lab_web+"\n")


    for component in self.netkit_components:
      f.write(""+str(component.attr['name'])+"[M]="+str(memory)+"\n")
      for interface in component.attr['map_IF_zone']:
        f.write("%s[%d]=%s\n"%(component.attr['name'], interface, component.attr['map_IF_zone'][interface]))

    f.close()
    self._create_sniffer(pathToDir)
 
  def _set_nbr_interface(self):
    for s in self.netkit_components :
      s.attr['nbr_IF_max'] = self.graph.degree(s.attr['name'])
    
 
  def set_interface_and_zone(self):
    """
    This function is used to set interfaces and zone for the given graph. This
    function should be called after the creation of all netkit_components from
    the given graph. See one of create_[name]_lab.py for example.
    """
    self._set_nbr_interface()
    for node_from, nbrs in self.graph.adjacency_iter():
      zone_remind = []
      for node_to, edges in nbrs.items():
	for edge in edges.values():
	  s = self.get_component(node_from)
	  s_neighbor = self.get_component(node_to)
	  if "zone" in edge:
	    IF = s.get_next_interface()
	    if IF != None and edge['zone'] not in zone_remind:
              zone = edge['zone']
	      s.set_interface(IF, zone, s_neighbor)
              self._add_zone_given(zone)
	      zone_remind+=[zone]
          else:
            print "Error: zone is missing for edge "+node_from+"--"+node_to+"."
	    sys.exit()
    self._set_mapping_IF_neighbors()
 
  def _set_mapping_IF_neighbors(self):

    L = self.netkit_components[:]
    L.sort(reverse=True)
    for s in L:
      for neighbor in self.graph.neighbors(s.attr['name']):
	for IF, zone in s.attr['map_IF_zone'].items():
	  s_neighbor = self.get_component(neighbor)
	  if zone in s_neighbor.attr['map_IF_zone'].values():
	    s.attr['map_IF_neighbor'] += [(IF, s_neighbor)]

  def set_data_from_edges(self):
    """
    This function is used to get the options from the edges of a given .dot
    file
    3 options are handled :
     - weight
     - delay
     - bandwidth
     - prefix_ipv4
     -%TODO: prefix_ipv6
    """

    for node_from, nbrs in self.graph.adjacency_iter():
      for node_to, edges in nbrs.items():
	for edge in edges.values():
	  if node_from!=node_to:
	    s = self.get_component(node_to)
	    IF = s.get_interface_used_between(node_from)
	    if "weight" in edge :
	      w = edge['weight']
	      if IF != None:
	        if s:
                  s.attr['map_weight'][IF] = w
	        else:
		  print "Error occured, no netkit_component called "+node_to
	      else:
                 print "Error occured, no interface has been matched from "+node_to+" to neighbor "+node_from
	    else:
	       print "no weight attribute to the "+node_from+ " -> "+node_to+" edge. Default value is taken"
            if "delay" in edge:
              delay = edge['delay']
	      if IF != None:
	        if s:
		  s.attr['map_IF_delay'][IF] = delay
		else:
		  print "Error occured, no netkit_component called "+node_to
	      else:
		print "Error occured, no interface has been matched from "+node_to+" to neighbor "+node_from
	    if "bandwidth" in edge: 
	      bandwidth = edge['bandwidth']
	      if IF != None:
		if s:
		  s.attr['map_IF_bandwidth'][IF] = bandwidth
		else:
		  print "Error occured, no netkit_component called "+node_to
	      else:
		print "Error occured, no interface has been matched from "+node_to+" to neighbor "+node_from
	    if "prefix" in edge:
	      prefix = edge['prefix']
	      if IF != None:
		if s:
		  s.attr['map_IF_prefix'][IF] = prefix
		else:
		  print "Error occured, no netkit_component called "+node_to
	      else:
		print "Error occured, no interface has been matched from "+node_to+" to neighbor"
  
  def get_component(self, node):
    for elem in self.netkit_components :
      if node == elem.attr['name'] :
	return elem
    print "Error occured, no node %s\n" %node
    return None
 


  def new_zone(self):
    """ create a random zone A0 ~ Z99  """
    cond = True
    while cond:
      zone = ""
      zone+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
      zone+=random.choice('01234566789')
      if zone not in self.zones_given :
	cond = False
    return zone
    
    
  def _create_sniffer(self, pathToDir):
    IF=0
    f = open(pathToDir+"/lab.conf", "a")
    f.write("sniffer[M]=64\n")
    for zone in self.zones_given :
      f.write("sniffer["+str(IF)+"]="+zone+"\n")
      IF+=1
    f.close()
  
    f = open(pathToDir+"/sniffer.startup", "w")
    j=0
    while j<IF:
      f.write("ifconfig eth"+str(j)+" up\n")
      j+=1
    f.close()
    try:
      os.makedirs(pathToDir+"/sniffer")
    except OSError:
      if not os.path.isdir(pathToDir+"/sniffer"):
	print "Bad things happened during directory set up. lab could not working properly"
  
  
  def _add_zone_given(self, zone):
    if zone not in self.zones_given:
      self.zones_given += [zone]
      
      
      
  def give_ipv6(self,Prefix):
    """
     This function is used to give ipV6 to component of the graph.
    """
    
    zones_ip=dict()
    ipzone="0000:0001"
    for zone in self.zones_given:
      zones_ip[zone]=ipzone
      temp=ipzone.split(":")
      i=0
      while i<2:
        temp[i]=int("0x"+temp[i],0)
        i+=1
      if temp[0]>=65535:
        printf("too much subnetworks")
      if temp[1]>=65535:
        temp[0]+=10000  #to have more differents subnetworks, not only 0001,0002,...
        temp[1]=0
      else:
        temp[1]+=10000  #to have more differents subnetworks, not only 0001,0002,...
        
      temp[0]= "%0.4x" % temp[0]
      temp[1]= "%0.4x" % temp[1]
      ipzone=":".join(temp)
      
    ipend="0000"  
    for components in self.netkit_components:
      for IF in components.attr['IF']:
        components.attr['map_IF_ipv6'][IF]=""+Prefix+""+zones_ip[components.attr['map_IF_zone'][IF]]+"::"+ipend
        ipend=int("0x"+ipend,0)
        ipend+=1
        ipend="%0.4x" % ipend

  def give_ipv4(self):
    """
	give ipv4 address to node, from the prefix stored in
	NetkitComponent.attr['map_IF_prefix']
    """
    ip_8_bit_pos = 0
    ip_16_bit_pos = 128
    ip_24_bit_pos = 1
    for component in self.netkit_components:
      for IF in component.attr['IF']:
	prefix = component.attr['map_IF_prefix'][IF]
	prefix_length = len(prefix)
	if prefix_length <= 3: # 8 first bits
	  component.attr['map_IF_ipv4'][IF]=""+prefix+"."+str(ip_8_bit_pos)+"."+str(ip_16_bit_pos)+"."+str(ip_24_bit_pos)
	elif prefix_length <= 7: # ex : 123.201
	  component.attr['map_IF_ipv4'][IF]=""+prefix+"."+str(ip_16_bit_pos)+"."+str(ip_24_bit_pos)
	elif prefix_length <= 11:
	  component.attr['map_IF_ipv4'][IF]=""+prefix+"."+str(ip_24_bit_pos)
	else :
	  print "Error in prefix, this length is not supported"
	  sys.exit(-1)
        if ip_24_bit_pos < 255:
	  ip_24_bit_pos+=1
	else:
	  ip_24_bit_pos = 1
	  if ip_16_bit_pos < 255:
	    ip_16_bit_pos+=1
	  else:
	    ip_16_bit_pos=128
	    if ip_8_bit_pos < 255:
	      ip_8_bit_pos +=1
	    else:
	      print "Error, to much elements. trololol this error will never be printed"
	      sys.exit(-1)

   
