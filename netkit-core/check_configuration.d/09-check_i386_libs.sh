#!/bin/false

#     Copyright 2004-2010 Massimo Rimondini
#     Computer Networks Research Group, Roma Tre University.
#
#     This file is part of Netkit.
# 
#     Netkit is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Netkit is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Netkit.  If not, see <http://www.gnu.org/licenses/>.

# This script is part of the Netkit configuration checker. Do not attempt to run
# it as a standalone script.

# This script should perform (and, optionally, output information about) a test
# to see if the host on which Netkit is run satisfies a specific requirement.
# The script is expected to always run till its end (i.e., there must be no exit
# instructions). If the host configuration does not comply to the requirement
# you should call one of the functions "check_warning" or "check_failure"
# (depending on the severity of the problem).

# Check whether 32 bit executable files can be run (on 64 bit hosts, this may
# require installing 32-bit compatibility libraries).

check_message "Checking whether 32-bit executables can run... "

if ! /usr/local/share/netkitcore/kernel/netkit-kernel --help >/dev/null 2>&1; then
   echo "failed!"
   echo
   echo "*** Error: Your system appears not to be able to run 32 bit applications."
   echo "If you are running a 64-bit Linux distribution, this can be fixed by installing"
   echo "the following packages: ia32-libs, libc6-i386. Otherwise, please check that"
   echo "you have installed all the Netkit packages correctly and try again."
   echo
   check_failure
else
   echo "passed."
fi

