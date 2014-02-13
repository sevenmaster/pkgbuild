#
# spec file for package SFEunrealircd
#

%include Solaris.inc
%include packagenamemacros.inc

%define srcname Unreal

%define  daemonuser  ircd
%define  daemonuid   121
%define  daemongcosfield UnrealIRCd Reserved UID
%define  daemongroup ircd
%define  daemongid   121

# Option to patch for 9-character nicklen limit instead of the default 30.
# This makes unreal RFC 2812-compliant.

%define option_with_rfc_nicklen %{?_with_rfc_nicklen:1}%{?!_with_rfc_nicklen:0}
%define nicklen_patch %option_with_rfc_nicklen

Name:		SFEunrealircd
IPS_Package_Name:	 irc/server/unreal
Summary:	Unreal IRCd
URL:		http://www.unrealircd.com
Vendor:		Bram Matthys <syzop@unrealircd.com>
Version:	3.2.10.1
License:	GPLv2
Source0:	http://www.unrealircd.com/downloads/%{srcname}%{version}.tar.gz
Source1:	unreal.xml
Patch1:		unrealircd-01-arch-fixes.diff
Patch2:		unrealircd-02-modules-Makefile.diff
Patch3:		unrealircd-03-nicklen.diff

SUNW_Copyright:	%{license}.copyright
SUNW_BaseDir:	/
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWzlib}
Requires:      %{pnm_requires_SUNWzlib}
BuildRequires: %{pnm_buildrequires_SUNWopenssl_devel}
Requires:      %{pnm_requires_SUNWopenssl}

%description
Unreal IRCd - the next generation ircd
WWW: http://www.unrealircd.com

%prep
%setup -q -n %srcname%version
%patch1 -p1
%patch2 -p1

%if %nicklen_patch
echo "Patching for RFC 2812-compliant max nicklen"
%patch3 -p1
%endif

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CFLAGS="-xO2 -xarch=pentium_pro -features=no%extinl"
export LDFLAGS="%_ldflags"

./configure \
	--with-showlistmodes \
	--with-listen=5 \
	--with-dpath=%{_sysconfdir}/unreal \
	--with-spath=%{_sbindir} \
	--with-nick-history=2000 --with-sendq=3000000 \
	--with-bufferpool=18 \
	--with-permissions=0600 --with-fd-setsize=1024 \
	--enable-dynamic-linking \
	--enable-ziplinks \
	--enable-ssl

#no parallel build please, might miss module object files
gmake -j1

%install
rm -rf $RPM_BUILD_ROOT
#gmake install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/unreal
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}

make IRCDDIR=$RPM_BUILD_ROOT/%{_sysconfdir}/unreal BINDIR=$RPM_BUILD_ROOT/%{_sbindir} install

cp -p src/ircd $RPM_BUILD_ROOT/%{_sbindir}/ircd
cp -p doc/example.conf $RPM_BUILD_ROOT/%{_sysconfdir}/unreal/unrealircd.conf

mkdir $RPM_BUILD_ROOT/%{_sysconfdir}/unreal/tmp
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/unreal
mv $RPM_BUILD_ROOT/%{_sysconfdir}/unreal/modules $RPM_BUILD_ROOT/%{_libdir}/unreal/
#use relative links
ln -s ../../../%{_libdir}/unreal $RPM_BUILD_ROOT%{_sysconfdir}/unreal/modules 

mkdir -p $RPM_BUILD_ROOT/%{_docdir}
cp -pr doc $RPM_BUILD_ROOT/%{_docdir}/%{name}

#removing duplicate doc files from %{_sysconfdir}/unreal/doc
#ls -l $RPM_BUILD_ROOT%{_sysconfdir}/unreal/doc/
rm -r $RPM_BUILD_ROOT%{_sysconfdir}/unreal/doc

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/log/unreal/
touch $RPM_BUILD_ROOT/%{_localstatedir}/log/unreal/ircd.log
#use relative links
ln -s ../../%{_localstatedir}/log/unreal/ircd.log $RPM_BUILD_ROOT%{_sysconfdir}/unreal/ircd.log

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/svc/manifest/network
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_localstatedir}/svc/manifest/network/

%clean
rm -rf $RPM_BUILD_ROOT

%actions
group groupname="%{daemongroup}" gid="%{daemongid}"
user ftpuser=false gcos-field="%{daemongcosfield}" username=%{daemonuser} uid=%{daemonuid} password=NP group="%{daemongroup}"

%files
%defattr (-, root, bin)
%dir %attr (0755,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal
%attr (0644,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/*.conf
%attr (0644,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/*.crt
%attr (0644,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/Donation
%attr (0644,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/LICENSE
%dir %attr (0755,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/aliases
%attr (0644,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/aliases/*
%dir %attr (0755,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/ircdcron
%attr (0755,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/ircdcron/*
%{_sysconfdir}/unreal/ircd.log
%{_sysconfdir}/unreal/modules
%dir %attr (0700,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/tmp
%attr (0755,%{daemonuser},%{daemongroup}) %{_sysconfdir}/unreal/unreal
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,bin) %{_libdir}/unreal
%attr (0755,root,bin) %{_libdir}/unreal/*
%dir %attr (0755,root,bin) %{_sbindir}
%attr (0755,root,bin) %{_sbindir}/*
%dir %attr (-,root,sys) %{_localstatedir}/log
%dir %attr (-,%{daemonuser},%{daemongroup}) %{_localstatedir}/log/unreal
%attr (0644,%{daemonuser},%{daemongroup}) %{_localstatedir}/log/unreal/ircd.log
%dir %attr (-, root, sys) %{_localstatedir}
%dir %attr (-, root, sys) %{_localstatedir}/svc
%dir %attr (-, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (-, root, sys) %{_localstatedir}/svc/manifest/network
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/network/unreal.xml

%changelog
* Thu Feb 13 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- add unrealircd-03-nicklen.diff for RFC-compliant nicklen
- define option_with_rfc_nicklen for nicklen patch
* Fri Nov 15 2013 - Thomas Wagner
- add (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_SUNWopenssl_devel}, %include packagenamemacros.inc
- renumber patches, use macros for paths in most places
- rename SMF service to network/irc/server:unreal
- use relative symlinks (better for pkg -R /a)
- relocate doc to %{_docdir}
* 23 Sep 2013 Ian Johnson <ianj@tsundoku.ne.jp>
- Added patches
- Wrote files section
* 22 Sep 2013 Ian Johnson <ianj@tsundoku.ne.jp>
- Initial package version 3.2.10.1
