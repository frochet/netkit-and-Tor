from netkit_component import NetkitComponent


class Switch(NetkitComponent):
   
  Mac="00:01"
 
  def __init__(self, name):
     NetkitComponent.__init__(self, name)  
     self.attr['mac-addr-if']=dict()

  def _define_hw_addr(self):
    for i in self.attr['IF']:
      self.attr['mac-addr-if'][i]="00:00:00:00:"+Switch.Mac
      temp=Switch.Mac.split(":")
      temp2=[0, 0]
      i=0
      while i < 2:
        temp2[i]=int("0x"+temp[i], 0)
        i+=1
      if temp2[0]>=255:
        printf("you made way too much switch!")
        exit()
      if temp2[1]>=255:
        temp2[0]+=1
        temp2[1]=0
      else:
        temp2[1]+=1
      
      temp2[0]="%0.2x" % temp2[0]
      temp2[1]="%0.2x" % temp2[1]
      Switch.Mac=":".join(temp2)
    
    
    

  def fill_startup_file(self, path):
    self._define_hw_addr()
    f = open(path+"/"+self.attr['name']+".startup","w")
    for IF in self.attr['IF']:
      f.write("ifconfig eth"+str(IF)+" hw ether "+self.attr['mac-addr-if'][IF]+" up\n")

    f.write("brctl addbr br0\n")
    for IF in self.attr['IF']:
      f.write("brctl addif br0 eth"+str(IF)+"\n")
    
    for key, value in self.attr['map_weight'].items():
      f.write("brctl setpathcost br0 eth%s %s" % (key, value))
    
    self.set_bandwidth(path)
    self.set_delay(path)
    f.close()
