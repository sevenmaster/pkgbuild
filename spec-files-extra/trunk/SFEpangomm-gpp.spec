#
#
# spec file for package SFEpangomm-gpp
#
# includes module(s): pangomm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc

%use pangomm = pangomm.spec

Name:                    SFEpangomm-gpp
IPS_Package_Name:	library/desktop/g++/pangomm
Summary:                 C++ Wrapper for the pango Library (g++ built)
License:                 LGPLv2+
SUNW_Copyright:          pangomm.copyright
Version:                 %{pangomm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: %{pnm_buildrequires_SUNWpango_devel}
Requires:      %{pnm_requires_SUNWpango}
BuildRequires: %{pnm_buildrequires_SUNWcairomm_devel}
Requires:      %{pnm_requires_SUNWcairomm}
BuildRequires: SFEsigcpp-gpp-devel
Requires:      SFEsigcpp-gpp
BuildRequires: SFEglibmm-gpp-devel
Requires:      SFEglibmm-gpp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEsigcpp-gpp-devel
Requires: %{pnm_buildrequires_SUNWpango_devel}

%prep
rm -rf %name-%version
mkdir %name-%version
%pangomm.prep -d %name-%version
#cd %{_builddir}/%name-%version
#gzcat %SOURCE0 | tar -xf -

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"

#libtoolize --f
%pangomm.build -d %name-%version

%install
%pangomm.install -d %name-%version

# delete files already included in SUNWpangomm-devel:
#rm -r $RPM_BUILD_ROOT%{_datadir}
#rm -r $RPM_BUILD_ROOT%{_includedir}

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_libdir}/pangomm-1.4/proc/m4*
rm -rf $RPM_BUILD_ROOT%{_libdir}/g++//pangomm-1.4/proc/m4*

#rm -rf $RPM_BUILD_ROOT%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
#%dir %attr(0755, root, bin) %{_mandir}
#%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/pangomm*
%_includedir
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%_datadir/doc/pangomm-1.4
%_datadir/devhelp

%changelog
* Fri Nov 15 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_requires_SUNWpango_devel}, pnm_requires_SUNWcairomm_devel, %include packagenamemacros.inc
- cleanup (Build)Requires
- standardize CFLAGS, LDFLAGS, CXXFLAGS
* Thu Oct 24 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Change (Build)Requires: SUNW* to %{pnm_(build)requires_SUNW*}
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Wed Sep 23 2009 - jchoi42@pha.jhu.edu
- Intially reworked from SUNWpangomm to build w gcc
