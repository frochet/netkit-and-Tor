
 
# common methods for netkit components
# 2 spaces indentation.
#
import os
import sys

class NetkitComponent:

  """
   This class is the super class of any network element in netkit. Classes
   Switch and Router inherit from it in their respective file.
   If you want to add a netkit component, you should use this class as a super
   class.

   /!\ this class should never be instanciated /!\ 
  """

  reminder = [] # static variable to share something between component.
                # like a config already used for a particular component

  def __init__(self, name, is_ipv6):
    
    self.attr = dict()
    self.attr['map_IF_zone'] = dict() # Map interface to netkit zone and its neighbor
    self.attr['map_IF_neighbor'] = []
    self.attr['map_IF_bandwidth'] = dict()
    self.attr['map_IF_delay'] = dict()
    self.attr['name'] = name
    self.attr['map_weight'] = dict()
    self.attr['IF'] = []
    self.attr['nbr_IF_max'] = 0
    self.is_ipv6 = is_ipv6
    self.attr['map_IF_prefix'] = dict()
    if is_ipv6 :
      self.attr['map_IF_ipv6'] = dict()     # more than 1 times
    else:
      self.attr['map_IF_ipv4'] = dict()
 
  def __cmp__(self, other):
    return cmp(self.attr['nbr_IF_max'], other.attr['nbr_IF_max'])


  def set_interface(self, interface, zone, neighbor): 
    """interface is an int and zone something between A and Z99"""
    self.attr['map_IF_zone'][interface] = zone.encode("ascii")
    self.attr['IF'] += [interface]

  def get_gw_ip(self, neighbor):
    IF = neighbor.get_interface_used_between(self.attr['name'])
    if self.is_ipv6:
      return neighbor.attr['map_IF_ipv6'][IF]
    else:
      return neighbor.attr['map_IF_ipv4'][IF]
  def get_next_interface(self):
    """
     Return the next disponnible interface for a component.
     Depends of nbr_IF_max attribute which is computed with node degree
     and zone.
    """
    if not self.attr['IF']:
      return 0
    else:
      self.attr['IF'].sort(reverse=True)
      L = self.attr['IF']
      if L[0]+1 < self.attr['nbr_IF_max']:
        return L[0]+1
      else:
	return None
  
  def get_interface_used_between(self, neighbor):
    """
     Return the interface used between self and
     its neighbor
     Return None if no iterface between them. => todo: this
     case should raise an exception and exit gracefully.
     For the moment it just print an error if None is returned.
    """
    for (interface, component) in self.attr['map_IF_neighbor']:
      if component.attr['name'] == neighbor:
	return interface
    return None

  def create_dir(self, path):
    """
     Create the directory for self, if it not exist yet.
    """
    if not os.path.isdir(path+"/"+self.attr['name']):
      try:
	os.mkdir(path+"/"+self.attr['name'])
      except OSError:
	if not os.path.isdir(path+"/"+self.attr['name']) :
	  print "Error happened when mkdir of "+self.attr['name']
  def create_startup(self, path):
    file(path+"/"+self.attr['name']+".startup", "w")

  def set_delay(self, pathToDir):
    """
     Set tc delay in the startup file. If bandwidth limitation already exists
     it set a new qdisc to htb class handling the limitation.
    """
    f = open(pathToDir+"/"+self.attr['name']+".startup", "a")

    for interface, delay in self.attr['map_IF_delay'].items():
    #add delay to startup file
      if interface in self.attr['map_IF_bandwidth'].keys():
      #If we already have bandwidth limitation over this interface
        f.write("tc qdisc add dev eth%d parent 1:1 handle 20: netem delay %dms\n"%(inteface, delay))
      else:
        f.write("tc qdisc add dev eth%s root netem delay %sms\n"%(interface, delay))
    f.close()

  def set_bandwidth(self, pathToDir):
    """
     Set tc bandwidth limitation in the startup file. The data come from the
     a mapping between an interface and its corresponding limitation. These
     data have parsed from the .dot file.
    """
    f = open(pathToDir+"/"+self.attr['name']+".startup", "a")
    for interface, speed in self.attr['map_IF_bandwidth'].items():
      f.write("insmod sch_htb\n")
      f.write("tc qdisc del dev eth%d\n"%interface)
      f.write("tc qdisc add dev eth%d root handle 1: htb default 1\n" % interface)
      f.write("tc class add dev eth%d parent 1: classid 1:1 htb rate%dkbit \n" %(interface, speed))

    f.close()
