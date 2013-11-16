#
# spec file for package SFEcairomm-gpp
#
# includes module(s): cairomm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc
%include usr-g++.inc

%define cc_is_gcc 1
%include base.inc


#default version for most osdistros
%define cairomm_osspecific_version    1.8.6

%if %( expr '%openindiana'+'%solaris12' '>=' 1 && echo 1 || echo 0 )
##TODO## improve version detection
%define cairo_version              $( LC_ALL=C pkg info cairo | grep -i Version | gsed -e 's?.*Version: *??' )
#%define cairo_version_major_minor  $( echo %{cairo_version} | gsed -e 's?^\([0-9]*\.[0-9]*\).*?\1?' )
%define cairo_version_major        $( echo %{cairo_version} | gsed -e 's?^\([0-9]*\).*?\1?' )
%define cairo_version_minor        $( echo %{cairo_version} | gsed -e 's?^[0-9]*\.\([0-9]*\).*?\1?' )
%if %( expr %{cairo_version_major} >= 1 >/dev/null && expr %{cairo_version_minor} >= 10 >/dev/null && echo 1 || echo 0 )
%define cairomm_osspecific_version    1.10.0
%endif
%endif


%use cairomm = cairomm.spec

Name:                    SFEcairomm-gpp
IPS_Package_Name:	 library/desktop/g++/cairomm
Summary:                 C++ API for the Cairo Graphics Library (g++-built)
Version:	%{cairomm_osspecific_version}
Version:                 %{cairomm.version}
Group:                   Desktop (GNOME)/Libraries
License:                 LGPLv2
SUNW_Copyright:          cairomm.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_SUNWgnome_base_libs_devel}
Requires:      %{pnm_requires_SUNWgnome_base_libs}
BuildRequires: %{pnm_buildrequires_SUNWcairo_devel}
Requires:      %{pnm_requires_SUNWcairo}
BuildRequires: SFEsigcpp-gpp-devel
Requires:      SFEsigcpp-gpp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: %{pnm_buildrequires_SUNWcairo_devel}
Requires: SFEsigcpp-gpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%cairomm.prep -d %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export CFLAGS="%optflags"
export PERL_PATH=/usr/perl5/bin/perl
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
%cairomm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%cairomm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# delete files already included in SUNWcairomm-devel:
#rm -r $RPM_BUILD_ROOT%{_datadir}
#rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%_libdir/cairomm-1.0
%_includedir
#%dir %attr (0755, root, sys) %_datadir
#%dir %attr (0755, root, other) %dir %_docdir
#%_datadir/doc/cairomm-1.0
#%_datadir/devhelp

%changelog
* Sat Nov 16 2013 - Thomas Wagner
- implement version switch for openindiana, solaris12, set 1.10.0 version
  version (0.151.1.7 -> 1.8.6, 0.151.1.8 -> 1.10.0)
  version (5.11 -> 1.8.6)
  version (5.12 -> 1.10.0)
- merge changes from Thu Oct 24 2013 for Ian 
* Fri Nov 15 2013 - Thomas Wagner
- add/change (Build)Requires to %{pnm_buildrequires_SUNWcairo_devel}, correct Requires in -devel
- use standard LDFLAGS
* Wed Oct 30 2013 - Alex Viskovatoff
- adapt to updated base spec
* Thu Oct 24 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Change (Build)Requires: SUNW* to %{pnm_(build)requires_SUNW*}
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout add SUNW_Copyright
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWcairomm.spec to build with g++
