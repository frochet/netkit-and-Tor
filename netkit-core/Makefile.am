script_in = \
	INSTALL.in \
	netkit.conf.in \
	check_configuration.d/02-check_environment.sh.in \
	check_configuration.d/04-check_path.sh.in \
	check_configuration.d/07-check_terminal_emulators.sh.in \
	check_configuration.d/03-check_man_pages.sh.in \
	check_configuration.d/09-check_i386_libs.sh.in \
	check_configuration.d/06-check_aux_tools.sh.in \
	man/man5/netkit.conf.5.in \
	man/man7/netkit.7.in \
	man/man1/lclean.1.in \
	man/man1/vconfig.1.in \
	man/man1/vclean.1.in \
	man/man1/vcrash.1.in \
	man/man1/lcrash.1.in \
	man/man1/vhalt.1.in \
	man/man1/vstart.1.in \
	man/man1/vlist.1.in \
	man/man1/lhalt.1.in \
	bin/vconfig.in \
	bin/vstart.in \
	bin/vlist.in \
	bin/lstart.in \
	bin/script_utils.in \
	bin/vhalt.in \
	bin/lclean.in \
	bin/linfo.in \
	bin/manage_tuntap.in \
	bin/lhalt.in \
	bin/vcrash.in \
	bin/vclean.in \
	bin/lcrash.in \
	bin/konsole-tabs.sh.in \
	bin/netkit_bash_completion.in \
	CHANGES.in \
	check_configuration.sh.in

bin_SCRIPTS = \
	bin/lstart \
	bin/vstart \
	bin/lhalt \
	bin/vhalt \
	bin/vcrash \
	bin/lcrash \
	bin/lclean \
	bin/vlist

netkitcoredir = $(datadir)/$(PACKAGE)

do_subst = $(SED) -e 's,@netkitdir@,$(netkitcoredir),g'

EXTRA_DIST = \
	$(script_in)

CLEANFILES = $(script_in:.in=)

SUFFIXES = .in 

%: %.in
	$(do_subst) < $(srcdir)/$< > $@

install-data-hook: $(script_in:.in=)
	cp -r . $(netkitcoredir)
	for f in `find . | grep -E '.git|autom4te|configure|configure.ac|\.in'`; do rm -rf  $(netkitcoredir)/$$f; done 

uninstall-hook:
	rm -rf $(netkitcoredir)
