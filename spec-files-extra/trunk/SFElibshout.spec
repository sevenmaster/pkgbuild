#
# spec file for package SFElibshout.spec
#
# includes module(s): libshout
#
# works: snv104 / pkgbuild 1.3.91 / Sun Ceres C 5.10 SunOS_i386 2008/10/22
# works: snv104 / pkgbuild 1.2.0  / Sun C 5.9 SunOS_i386 Patch 124868-02 2007/11/27
# works: snv103 / pkgbuild 1.3.0  / Sun C 5.9 SunOS_i386 Patch 124868-02 2007/11/27
# works: snv96  / pkgbuild 1.3.1  / Sun Ceres C 5.10 SunOS_i386 2008/07/10


%include Solaris.inc
%include packagenamemacros.inc

%define src_name	libshout
%define src_url		http://downloads.xiph.org/releases/libshout

Name:                   SFElibshout
IPS_Package_Name:       library/audio/libshout
Summary:                Library for broadcasting to an Icecast streaming media server
License:                LGPLv2
SUNW_Copyright:	        libshout.copyright
URL:                    http://www.icecast.org/download.php
Version:                2.2.2
Source:                 %{src_url}/libshout-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#BuildRequires: SFWoggl
BuildRequires: %{pnm_buildrequires_SUNWlibtheora_devel}
BuildRequires: %{pnm_buildrequires_SUNWlxml_devel}
BuildRequires: %{pnm_buildrequires_SUNWlxsl_devel}
BuildRequires: %{pnm_buildrequires_SUNWogg_vorbis_devel}
# TODO needed? BuildRequires: SUNWspeex-devel
#Requires: SFWoggl
Requires: %{pnm_requires_SUNWlibtheora}
Requires: %{pnm_requires_SUNWlxml}
Requires: %{pnm_requires_SUNWlxsl}
Requires: %{pnm_requires_SUNWogg_vorbis}
# TODO needed? Requires: SUNWspeex

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name



%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP -D_AVL_H"
export LDFLAGS="%_ldflags"

./configure --prefix=/usr               \
            --bindir=/usr/bin           \
            --mandir=/usr/share/man     \
            --libdir=/usr/lib           \
            --datadir=/usr/share        \
            --libexecdir=/usr/lib       \
            --sysconfdir=/etc           \
            --enable-shared             \
            --disable-static            \

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rmdir $RPM_BUILD_ROOT%{_bindir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*



%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*



%changelog
* Sun Mar 23 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- %include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_SUNWlibtheora_devel}
- change (Build)Requires to %{pnm_buildrequires_SUNWlxml_devel}
- change (Build)Requires to %{pnm_buildrequires_SUNWlxsl_devel}
- change (Build)Requires to %{pnm_buildrequires_SUNWogg_vorbis_devel}
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- added ips package name.
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Oct  3 2010 - Alex Viskovatoff
- Use gmake.
* Tue Jul 28 2009 - oliver.mauras@gmail.com
- fix that empty bindir and missing pkgconfig
* Sat Dec 20 2008 - Thomas Wagner
- remove wrong line /usr in %files
* Sat May 10 2008 - Thomas Wagner
- set SUNW_BaseDir: %{_basedir}
* Mon Nov 26 2007 - Thomas Wagner
- remove SFWoggl (libao, vorbis, ogg)
* Tue May 8 2007 - Thomas Wagner
- Initial version
