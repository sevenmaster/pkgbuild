##TODO## ist this necessary? if ye,s then might use SFEboost-gpp (gcc!)
#Requires: SFEboost
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
#%include usr-gnu.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

# TODO: write SMF manifest for rtmpsrv

Name:                SFErtmpdump
Summary:             RTMPdump -- a toolkit for RTMP streams
IPS_package_name:    video/rtmpdump
Group:               Applications/Sound and Video
License:             GPLv2+, LGPLv2+
SUNW_copyright:      rtmpdump.copyright
URL:                 http://rtmpdump.mplayerhq.hu/
Version:             2.4
Source:		http://rtmpdump.mplayerhq.hu/download/rtmpdump-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:          %{pnm_buildrequires_SUNWopenssl_include}
Requires:               %{pnm_requires_SUNWopenssl_libraries}


%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n rtmpdump

%build
export CC=gcc
export CXX=g++
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


# Rtmpdump has no configure. We'll make do.
sed -e 's:/usr/local:%{_prefix}:g' Makefile > Makefile.new
mv Makefile.new Makefile
sed -e 's:/usr/local:%{_prefix}:g' librtmp/Makefile > librtmp/Makefile.new
mv librtmp/Makefile.new librtmp/Makefile

XLIBS="-lnsl -lsocket" gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/librtmp.a
mv ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ${RPM_BUILD_ROOT}%{_bindir}
rm -r ${RPM_BUILD_ROOT}%{_prefix}/sbin

# move mandirs to a more sensible home
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}
mv ${RPM_BUILD_ROOT}%{_prefix}/man/* ${RPM_BUILD_ROOT}%{_mandir}
rm -r ${RPM_BUILD_ROOT}%{_prefix}/man

cd %buildroot%_libdir/pkgconfig
sed 's/libssl,libcrypto/openssl/' librtmp.pc > librtmp.pc.new
mv librtmp.pc.new librtmp.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/rtmpdump.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/librtmp.3
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/rtmpgw.8

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/librtmp/*


%changelog
* Fri Jun 28 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWopenssl_include}, 
  %{pnm_requires_SUNWopenssl_libraries}, %include packagenamemacros.inc
* Sat Feb 09 2013 - Milan Jurik
- bump to 2.4
* Oct 12 2011 - Alex Viskovatoff
- Fix librtmp.pc; add SUNW_copyright and IPS_package_name
* Dec 28 2010 - jchoi42@pha.jhu.edu
- Initial spec
