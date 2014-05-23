#!/bin/bash

#$1 Version
#$2 Name to be

BUILD=build/netkit/kernel/netkit-kernel

MPTCP_BRANCH=mptcp_v0.88
MPTCP_URL_BASE=https://github.com/multipath-tcp/mptcp/archive/

if [ $1 = 'mptcp' ]
then
	make -f Makefile.ker -j4 KERNEL_PACKAGE=$MPTCP_BRANCH.zip KERNEL_RELEASE=$MPTCP_BRANCH KERNEL_URL_BASE=$MPTCP_URL_BASE KERNEL_SUFFIX=.zip kernel
	cp $BUILD $2
	cp -r build/netkit/kernel/modules ../netkit-uml-filesystem/
	make -f Makefile.ker  KERNEL_PACKAGE=$MPTCP_BRANCH.zip KERNEL_RELEASE=$MPTCP_BRANCH KERNEL_URL_BASE=$MPTCP_URL_BASE KERNEL_SUFFIX=.zip clean-all
else
	make -f Makefile.ker -j4 KERNEL_RELEASE=$1 kernel
	cp $BUILD $2
	cp -r build/netkit/kernel/modules ../netkit-uml-filesystem/
	make -f Makefile.ker KERNEL_RELEASE=$1 clean-all
fi
