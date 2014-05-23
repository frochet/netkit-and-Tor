fsdir = $(datadir)/$(PACKAGE)

fs = \
	default-ker \
	mptcp-ker

dist_fs_SCRIPTS = $(fs)

CLEANFILES = $(fs)

default-ker:
	chmod +x gen-ker.sh
	./gen-ker.sh 3.9.2 $@

mptcp-ker:
	chmod +x gen-ker.sh
	./gen-ker.sh mptcp $@
