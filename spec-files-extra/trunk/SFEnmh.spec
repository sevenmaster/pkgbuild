#
# spec file for package SFEnmh
#
# includes module(s): nmh
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname nmh

Name:                    SFEnmh
IPS_Package_Name:	 mail/nmh
Summary:                 nmh - Mail Handling System
Group:                   Utility
Version:                 1.5
URL:		         http://www.nongnu.org/nmh/
Source:		         http://download.savannah.nongnu.org/releases/nmh/nmh-%{version}.tar.gz
License: 		 Modified BSD License
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%description
nmh (new MH) is a powerful electronic mail handling system. It was
originally based on version 6.8.3 of the MH message system developed
by the RAND Corporation and the University of California. It is
intended to be a (mostly) compatible drop-in replacement for MH.

nmh consists of a collection of fairly simple single-purpose programs
to send, receive, save, retrieve, and manipulate e-mail
messages. Since nmh is a suite rather than a single monolithic
program, you may freely intersperse nmh commands with other commands
at your shell prompt, or write custom scripts which use these commands
in flexible ways.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --sysconfdir=%{_sysconfdir}/nmh

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr(0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Mon Nov 19 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
