============
Instructions
============


This directory contains .py scripts which will let you generate netkit labs
from a network configuration given in a .dot file.

This directory was aimed to develop the different scripts, you will find the
same named directory in each netkit lab located to /labs with the .py you need
to generate the particular lab.

Basically, you will have each time the files : 

 - create_lab.py
 - create_[namedlab]_lab.py which is the only non-reutilisable file (correspond
   to a particular lab)
 - netkit_component.py
 - router.py or switch.py or ... any particular netkit_component (objects from
   these classes inherit from NetkitComponent object inside netkit_component.py)


What can you do with this script ? 

=> You can give to it a .dot file containing the representation of your
network. The netkit lab will be generated from it and ready to work.

The synthax used in the .dot file is the DOT language (http://www.graphviz.org/doc/info/lang.html)

Here's an example :

graph g{ 
  r1 -- r2 [zone=B, weight=100]
  r2 -- r3 [zone=C]
  r1 -- r4 [zone=D]
  r4 -- r3 [zone=E]
  r1 -- r5 [zone=A, weight=10]
  r1 -- r7 [zone=A]
  r1 -- r6 [zone=A, weight=10]
}

where you can easely guess what represents edges and what represents
nodes. The scripts handles 4 options for the edges: zone, weight, delay and
bandwidth. delay is in ms and bandwidth in kbits.

Setting a same zone for a bunch of nodes means that for the corresponding lab,
these nodes will be in the same collision domain. Of course, these node must be 
direct neighbours.

The script will handle itself interfaces and IP. For the exemple above, r1 will
be connected with the same interface toward r5, r6 and r7. If you don't want
one of them coming in the same interface in r1. Just change its zone option.

About this .dot file. For the moment, each .dot file you will found are graph.
But you can use digraph if you want, it will works.

Example:

digraph g{
  r1 -> r2 [zone=A]
  r2 -> r3 [zone=B]
  r1 -> r3 [zone=C, weight=100]
  r3 -> r1 [zone=C]

}

lab fully scripted
-------------------

1. static routing
2. rip
3. stp
4. ospfv3

For each of them, you should be able to give a .dot file of the configuration
you want.

lab partially scripted
-----------------------

traceroute:

if you want any other network architecture, you can use the script
static routing to generate your network architecture from a dot file and then edit yourself the
created .startup file to introduce your route errors or any bizarre stuff to
create the exercice

bgp :

The configurations of quagga are currently static for the set up lab. With the
script, you can create any network you want, but you have to modify the quagga
conf files to match your purpose.


webserver :

This lab is mainly used to collect traces. See its readme for details. This lab
is scripted to set tcp options you want.

dhcp :

no lab creaction script has been made for it. The reason is that a different
network topology doesn't change anything about the exercice. Anyway, if you
want to automatize this lab, see the section below.

if you want to add a new lab
----------------------------------------

Well, you will have to dive into the code. each function are commented. At
least each important one.

To add a new script to generate a new lab, you will have to create a .py file
like one of create_stp_lab.py, create_ospf_lab.py, ... they are very similar
and aims to set up the lab with the function inside the class Create_lab and
the netkit_component.

Let's take the example of dhcpv6 lab, which have currently a simple router
connected to 2 host. If you want to automatize this lab, you just have to
create a create_dhcp_lab.py similar to the other one. And write inside
router.py and pc.py a few lines to add what should be present in the .startup
file.



