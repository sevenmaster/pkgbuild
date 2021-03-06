#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define srcname mpc

Name:                SFEmpc
IPS_package_name:    audio/mpd/mpc
Summary:             Command line tool and client for Music Player Daemon
License:             GPLv2
SUNW_Copyright:	     mpc.copyright
Meta(info.upstream): Max Kellermann <max@duempel.org>
Version:             0.27
Source:		     http://www.musicpd.org/download/%srcname/0/%srcname-%version.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFElibmpdclient-devel
Requires:	SFElibmpdclient

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n mpc-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --disable-iconv

# Be modern and use libxnet instead of libsocket
sed 's/-lsocket -lnsl/-lxnet/' Makefile > Makefile.xnet
mv Makefile.xnet Makefile

%if %{cc_is_gcc}
#cc_is_gcc
%else
#remove unsuitable switches for solarisstudio
# -ffunction-sections -fdata-sections -fvisibility=hidden 
gsed -i.back_remove_compileroptions '/^CFLAGS =/ s?\(-ffunction-sections\|-fdata-sections\|-fvisibility=hidden\)??g' Makefile
%endif

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mpc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/mpc.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Fri May 27 2016 - Thomas Wagner
- remove switches not for solarisstudio from Makefile: -ffunction-sections -fdata-sections -fvisibility=hidden  (S11 S12)
* Wed Mar 16 2016 - Thomas Wagner
- bump to 0.27
* Mon Apr 14 2014 - Thomas Wagner
- switch to .gz download file (old pkgbuild)
* Sat Jan 25 2013 - Alex Viskovatoff
- update to 0.25; follow new naming convention for mpd clients
* Tue Sep 17 2013 - Thomas Wagner
- fix IPS package name /media/ (duplicate)
* Sat Sep 14 2013 - Alex Viskovatoff
- add IPS package name
* Fri Aug 10 2012 - Thomas Wagner
- fix download URL
* Thu Jul  5 2012 - Thomas Wagner
- bump to 0.22
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Jan 18 2011 - Alex Viskovatoff
- Bump to 0.20; use libxnet
* Wed Oct 25 2006 - Eric Boutilier
- Add devel package and fix attributes
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
