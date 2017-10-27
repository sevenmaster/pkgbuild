#
# spec file for package SFEpigeonhole
#

%include Solaris.inc

%define dovecot_version_major_minor 2.2

Name:		SFEpigeonhole
IPS_Package_Name:	 service/network/imap/dovecot/plugin/pigeonhole
Summary:	Dovecot Pigeonhole Plugin
URL:		http://pigeonhole.dovecot.org/
Vendor:		Stephan Bosch <stephan@rename-it.nl>
Version:	0.4.21
License:	LGPL
Source0:	http://pigeonhole.dovecot.org/releases/%{dovecot_version_major_minor}/dovecot-%{dovecot_version_major_minor}-pigeonhole-%{version}.tar.gz

%define _prefix /usr

SUNW_Copyright:	pigeonhole.copyright
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires: SFEdovecot
Requires:      SFEdovecot

%description
Pigeonhole Sieve sorting plugin for Dovecot

%prep
%setup -q -n dovecot-%{dovecot_version_major_minor}-pigeonhole-%{version}

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags} -L/usr/lib/dovecot -R/usr/lib/dovecot"

./configure \
	--prefix=%{_prefix} \
	--with-dovecot=/usr/lib/dovecot

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=%buildroot

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

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
%{_libdir}/dovecot/modules/lib*
%{_libdir}/dovecot/modules/sieve/lib*
%dir %{_libdir}/dovecot/modules/doveadm
%{_libdir}/dovecot/modules/doveadm/*
%dir %{_libdir}/dovecot/modules/settings
%{_libdir}/dovecot/modules/settings/*
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/doc/dovecot/*
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_mandir}/man1/*
%{_mandir}/man7/*


%changelog
* Thu Oct 26 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 0.4.21
* Tue Jun 13 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 0.4.18
* Wed Jan  4 2017 - Thomas Wagner
- bump to 0.4.16
* Fri Jan  8 2016 - Thomas Wagner
- bump to 0.4.11
* Wed Jan  7 2015 - Thomas Wagner
- bump to 0.4.6
- add (Build)Requires SFEdovecot
* Sun Feb 09 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add copyright file
* Mon Oct 14 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial package version 0.4.2
