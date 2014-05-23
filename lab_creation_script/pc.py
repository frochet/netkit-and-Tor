class Pc(NetkitComponent):


  def __init__(self, name):
    NetkitComponent.__init__(self, name)


 
  def fill_startup_file(self, path):
    f = open(path+"/"+self.attr['name']+".startup", "w")
    for IF in self.attr['IF']:
      f.write("ifconfig eth"+str(IF)+" up\n")
      f.write("ifconfig eth"+str(IF)+" add "+self.attr['map_IF_ipv6'][IF]+"/64\n")
    
    f.write("#add ipv6 route here\n")

    f.write("/etc/init.d/ssh start\n")
