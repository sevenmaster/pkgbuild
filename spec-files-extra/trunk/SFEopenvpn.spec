##TODO## make IPS only require SFEtun if installed in a global zone, in non-global-zone
##       you need to add to the zone config: <device match="/dev/tun"/>
##       and install SFEtun into the global zone

#
# spec file for package SFEopenvpn
#
# includes module(s): openvpn
#
%include Solaris.inc
%include packagenamemacros.inc
%define srcname openvpn

Name:		SFEopenvpn
IPS_Package_Name:	system/network/openvpn
Summary:	Open source, full-featured SSL VPN package
Group:		System/Security
URL:		http://openvpn.net
License:	GPLv2
SUNW_copyright:	openvpn.copyright
Version:	2.4.4
#https://openvpn.net/index.php/download/community-downloads.html
Source:		http://swupdate.openvpn.net/community/releases/%srcname-%version.tar.gz
#retired Patch1:         openvpn-01-get_default_gateway.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElzo
Requires: SFElzo
#note: if you build in a non-global-zone, you might not necessarily have the tun package succeed
#but you need stuff like /usr/include/net/if_tun.h which comes from SFEtun
BuildRequires: SFEtun
Requires: SFEtun
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
Requires: %{pnm_requires_SUNWopenssl}

%description
openvpn

##TODO## make IPS only require SFEtun if installed in a global zone, in non-global-zone
##       you need to add to the zone config: <device match="/dev/tun"/>
##       and install SFEtun into the global zone

%prep
%setup -q -n %srcname-%version

#retired %patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
%if %{cc_is_gcc}
export CFLAGS="${CFLAGS} -std=c99"
%endif
export LDFLAGS="%_ldflags"
export AR=/usr/bin/ar
#ranlib is a dummy
export RANLIB="/usr/bin/ranlib"
export LIBS="-lnsl -lsocket"

gsed -i.bak -e 's?-std=c99??' configure

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/openvpn
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/openvpn
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/openvpn.8
%dir %attr (0755, root, other) %dir %_docdir
%_docdir/%srcname

%changelog
* Sun Nov 26 2017 - Thomas Wagner
- bump to 2.4.4
* Mon Jul 31 2017 - Thomas Wagner
- add -std=c99 if CC=gcc
- bump to 2.4.3
* Wed May 24 2017 - Thomas Wagner
- bump to 2.4.2 - fix remote DOS - http://www.prweb.com/releases/2017/05/prweb14326488.htm
* Sat Apr 22 2017 - Thomas Wagner
- bump to 2.4.1
- retire patch1 openvpn-01-get_default_gateway.diff
* Sun Nov 13 2016 - Thomas Wagner
- bump to 2.3.13
* Thu Oct 27 2016 - Thomas Wagner
- bump to 2.3.12
* Sat Apr  4 2015 - Thomas Wagner
- bump to 2.3.6
- add patch1 openvpn-01-get_default_gateway.diff (credits leoric)
* Sat Nov  1 2014 - Thomas Wagner
- bump to 2.3.5
* Mon Jan 27 2014 - Thomas Wagner
- add (Build)Requires: SFEtun
* Sun Aug 11 2013 - Logan Bruns <logan@gedanken.org>
- updated to 2.3.2
* Tue Jul 24 2012 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWopenssl}, %include packagenamacros.inc
* Mon Jul  2 2012 - Thomas Wagner
- bump to 2.2.2
* Wed Sep 28 2011 - Alex Viskovatoff
- Update to 2.2.1, fixing %files; add SUNW_copyright
- openssl is not in /usr/sfw
* Tue Jun 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 2.2.0, comes with integrated tun.c
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- Added modified tun.c
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
