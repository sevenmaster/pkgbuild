##TODO## provide better vpnc-script (maybe in a separate package)
#http://www.infradead.org/openconnect/platforms.html
#For Solaris support, and for IPv6 on any platform, the vpnc-script shipped with vpnc itself (as of v0.5.3) is not sufficient. It is necessary to use the script from the vpnc-scripts repository instead. That repository also contains an updated version of vpnc-script-win.js which is required for correct IPv6 configuration under Windows.
#http://git.infradead.org/users/dwmw2/vpnc-scripts.git

#
# spec file for package SFEopenconnect.spec
#
# includes module(s): openconnect
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define src_name	openconnect

Name:		SFEopenconnect
IPS_Package_Name:	system/network/openconnect
Version:	7.07
IPS_Component_Version: 7.7
Summary:	Open client for Cisco AnyConnect VPN
Group:		Productivity/Networking/Security
License:	LGPLv2+
URL:		http://www.infradead.org/openconnect.html
Source:		ftp://ftp.infradead.org/pub/%{src_name}/%{src_name}-%{version}.tar.gz
#vpnc-script ... no controlled version, just fetch the very latest one from http://git.infradead.org/users/dwmw2/vpnc-scripts.git/tree
##TODO## Problem: That way, we *never* get the script updated once it exists in out local $SOURCE directory...
Source1:        http://git.infradead.org/users/dwmw2/vpnc-scripts.git/blob_plain/HEAD:/vpnc-script
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SFEtun
Requires:	SFEtun

BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 )
#S11 S12 need zlib.pc
BuildRequires:  %{pnm_buildrequires_SFEzlib-pkgconfig}
#for pkgtool's dependency resoultion
Requires:       %{pnm_requires_SFEzlib-pkgconfig}
%endif


%description
This package provides a client for Cisco's AnyConnect VPN, which uses
HTTPS and DTLS protocols.
Notes:
For Solaris support, and for IPv6 on any platform, the vpnc-script shipped with vpnc itself (as of v0.5.3) is not sufficient. It is necessary to use the script from the vpnc-scripts repository instead. That repository also contains an updated version of vpnc-script-win.js which is required for correct IPv6 configuration under Windows.
http://git.infradead.org/users/dwmw2/vpnc-scripts.git

%if %cc_is_gcc
BuildRequires:	SFEgcc
Requires:	SFEgcc-runtime
%endif

%package devel
Summary:	%{summary} - developer files
Group:	Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	 %{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}

cp -p %{SOURCE1} .

%build

#note: all variables are on the same line with the "configure" call
#therefore *no* export
#replaced by package carrying zlib.pc ZLIB_CFLAGS="-I/usr/include" ZLIB_LIBS=-lz \

CC=gcc \
LD=`which ld-wrapper` \
CFLAGS="%{optflags} -D__sun__" LDFLAGS="%{_ldflags}" \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
	--docdir=%{_docdir}/openconnect \
	--disable-static \
        --enable-shared \
	--with-vpnc-script=/etc/vpnc/vpnc-script \
        --without-libpcsclite

gmake

%install
rm -rf %{buildroot}
gmake install DESTDIR=%{buildroot}
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done
mkdir -p %{buildroot}/%{_mandir}/man1m
mv %{buildroot}/%{_mandir}/man8/openconnect.8 %{buildroot}/%{_mandir}/man1m/openconnect.1m
rmdir %{buildroot}/%{_mandir}/man8

VPNCSCRIPT=$( basename ${SOURCE1} )
cp -p ${VPNCSCRIPT} $RPM_BUILD_ROOT/%{_bindir}/
chmod a+rx $RPM_BUILD_ROOT/%{_bindir}/${VPNCSCRIPT}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{buildroot}/%{_datadir}/locale
%endif

rm -f %{buildroot}%{_libdir}/libopenconnect.la

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_sbindir}/openconnect
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/openconnect
%{_mandir}/man1m/*
%{_libdir}/libopenconnect.so*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Dec  9 2016 - Thomas Wagner
- add missing %include packagenamemacros.inc
- change (Build)Requires to pnm_buildrequires_SFEzlib-pkgconfig
* Thu Nov 24 2016 - Thomas Wagner
- bump to 7.07 (IPS 7.7)
* Sat Mar 12 2016 - Thomas Wagner
- add vpnc-script (no controlled verison, just fetch the latest one), copy to %{_bindir}
##TODO## Problem: That way, we *never* get the script updated once it exists in out local $SOURCE directory...
* Thu Aug 20 2015 - Thomas Wagner
- add BuildRequires SFEzlib-pkgconfig, remove variables pointing to ZLIB
* Mon Aug 10 2015 - Thomas Wagner
- bump to 7.06 (IPS 7.6)
* Tue Mar  4 2015 - Thomas Wagner
- fix %files for %docdir
* Thu Jan 22 2015 - Thomas Wagner
- bump to 7.03 (IPS 7.3)
- --without-libpcsclite or fail finding files related to pcsc
* Fri Oct 24 2014 - Thomas Wagner
- bump to 6.00
- switched to gcc because no solution to get studio compile (missing: "openconnect.h".. warning: attribute "format" is unknown, ignored. ) - try again when solarisstudio 12.4 is released
* Mon Sep 09 2013 - Milan Jurik
- bump to 5.01
* Sun Nov  4 2012 - Thomas Wagner
- bump to 4.07
- add IPS_Component_Version 4.7
* Sun Jun 17 2012 - Milan Jurik
- bump to 3.99
* Thu Oct 06 2011 - Milan Jurik
- bump to 3.13
- add IPS package name
* Thu May 05 2011 - Knut Anders Hatlen
- Do not require gcc
* Mon May 02 2011 - Milan Jurik
- bump to 3.02
* Thu Dec 02 2010 - Milan Jurik
- Initial spec based on opensuse
