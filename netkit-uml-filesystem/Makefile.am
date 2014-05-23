fsdir = $(datadir)/$(PACKAGE)

fs = \
	default-fs

dist_fs_DATA = $(fs)

CLEANFILES = $(fs)

default-fs:
	chmod +x gen-fs.sh
	./gen-fs.sh $@

install-data-hook:
	cp -r modules $(fsdir)

uninstall-hook:
	rm -rf $(fsdir)/modules
