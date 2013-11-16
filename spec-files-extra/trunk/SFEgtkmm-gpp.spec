#
#
# spec file for package SFEgtkmm-gpp
#
# includes module(s): gtkmm
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

%use gtkmm = gtkmm.spec

Name:                    SFEgtkmm-gpp
IPS_Package_Name:	library/desktop/g++/gtkmm
Summary:                 C++ Wrapper for the Gtk+ Library (g++-built)
Group:                   Desktop (GNOME)/Libraries
License:                 LGPLv2+    
Version:                 %{gtkmm.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEglibmm-gpp-devel
Requires: SFEglibmm-gpp
BuildRequires: SFEcairomm-gpp-devel
Requires: SFEcairomm-gpp
BuildRequires: SFEpangomm-gpp-devel
Requires: SFEpangomm-gpp
BuildRequires: SFEsigcpp-gpp-devel
Requires: SFEsigcpp-gpp
BuildRequires: %{pnm_buildrequires_SUNWgnome_base_libs_devel}
Requires: %{pnm_requires_SUNWgnome_base_libs}

Requires: %{pnm_requires_SUNWlibms}
Requires: %{pnm_requires_SUNWlibC}

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name
Requires: %{pnm_buildrequires_SUNWgnome_base_libs_devel}
Requires: SFEglibmm-gpp-devel
Requires: SFEsigcpp-gpp-devel
Requires: SFEcairomm-gpp-devel
Requires: SFEpangomm-gpp-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%gtkmm.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
%gtkmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gtkmm.install -d %name-%version

# Move demo to demo directory
#
#install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
#mv $RPM_BUILD_ROOT%{_bindir}/gtkmm-demo \
#    $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/gtkmm-gpp-demo
#rm -r $RPM_BUILD_ROOT%{_bindir}

# delete files already included in SUNWgtkmm-devel:
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
%{_libdir}/gtkmm*
%{_libdir}/gdkmm*
%_includedir
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%_datadir/doc/gtkmm-2.4
%_datadir/gtkmm-2.4
%_datadir/devhelp
#%dir %attr (0755, root, bin) %{_prefix}/demo
#%dir %attr (0755, root, bin) %{_prefix}/demo/jds
#%dir %attr (0755, root, bin) %{_prefix}/demo/jds/bin
#%{_prefix}/demo/jds/bin/gtkmm-gpp-demo


%changelog
* Fri Nov 15 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWgnome_base_libs_devel}, SUNWlibms, SUNWlibC, %include packagenamemacros.inc
- remove SUNW version of BuildRequires
- %include usr-g++.inc
- use standard LDFLAGS
- merge changes from Ian
* Thu Oct 24 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Change (Build)Requires SUNW* to %{pnm_(build)requires_SUNW*}
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Thu Oct 4 2009 - jchoi42@pha.jhu.edu
- added SFEpango dependency 
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWgtkmm.spec to build with g++
