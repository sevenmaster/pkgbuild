#
# spec file for package SFEpigeonhole
#

%include Solaris.inc

Name:		SFEpigeonhole
IPS_Package_Name:	 service/network/imap/dovecot/plugin/pigeonhole
Summary:	Dovecot Pigeonhole Plugin
URL:		http://pigeonhole.dovecot.org/
Vendor:		Stephan Bosch <stephan@rename-it.nl>
Version:	0.4.2
License:	LGPL
Source0:	http://www.rename-it.nl/dovecot/2.2/dovecot-2.2-pigeonhole-%{version}.tar.gz

%define _prefix /usr

SUNW_Copyright:	pigeonhole.copyright
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

%description
Pigeonhole Sieve sorting plugin for Dovecot

%prep
%setup -q -n dovecot-2.2-pigeonhole-%{version}

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
LDFLAGS="-L/usr/lib/dovecot -R/usr/lib/dovecot" \
./configure \
	--prefix=%{_prefix} \
	--with-dovecot=/usr/lib/dovecot

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=%buildroot

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %{_includedir}/dovecot/sieve
%{_includedir}/dovecot/sieve/*
%{_libdir}/dovecot/libdovecot-sieve.*
%{_libdir}/dovecot/managesieve
%{_libdir}/dovecot/managesieve-login
%{_libdir}/dovecot/modules/lib90_sieve_plugin.*
%dir %{_libdir}/dovecot/modules/doveadm
%{_libdir}/dovecot/modules/doveadm/*
%dir %{_libdir}/dovecot/modules/settings
%{_libdir}/dovecot/modules/settings/*
%dir %{_libdir}/dovecot/sieve
%{_libdir}/dovecot/sieve/*
%{_datadir}/doc/dovecot/*
%{_mandir}/man1/*
%{_mandir}/man7/*

%changelog
* Sun Feb 09 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add copyright file
* Mon Oct 14 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial package version 0.4.2
