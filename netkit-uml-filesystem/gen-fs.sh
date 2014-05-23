#!/bin/bash

FSBUILD=fs-build
SKEL=skeleton
BUILD=netkit-fs-amd64-F6.0

rm -rf $BUILD
rm -rf $FSBUILD
cp -r $SKEL/$1 $FSBUILD
make -f Makefile.fs filesystem
rm -rf $FSBUILD
mv $BUILD $1
make -f Makefile.fs clean-all
