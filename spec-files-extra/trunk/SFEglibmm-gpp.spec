#
# spec file for package SFEglibmm-gpp
#
# includes module(s): glibmm
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc
%include usr-g++.inc

%use glibmm = glibmm.spec

Name:                    SFEglibmm-gpp
IPS_Package_Name:	library/g++/glibmm
Summary:                 C++ Wrapper for the Glib2 Library (g++-built)
Group:                   Desktop (GNOME)/Libraries
License:                 LGPLv2
SUNW_Copyright:          glibmm.copyright
Version:                 %{glibmm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:   %{pnm_buildrequires_SUNWgnome_base_libs_devel}
Requires:        %{pnm_requires_SUNWgnome_base_libs}
BuildRequires:   SFEsigcpp-gpp-devel
Requires:        SFEsigcpp-gpp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: %{pnm_buildrequires_SUNWgnome_base_libs_devel}

%prep
rm -rf %name-%version
mkdir %name-%version
%glibmm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
export LDFLAGS="-L/usr/g++/lib:/usr/gnu/lib -R/usr/g++/lib:/usr/gnu/lib"
export PERL_PATH=/usr/perl5/bin/perl
%glibmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%glibmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/m4
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/pm
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/libglibmm_generate_extra_defs*.so*
rm -rf $RPM_BUILD_ROOT%{_cxx_includedir}/glibmm-2.4/glibmm_generate_extra_defs
rm -rf $RPM_BUILD_ROOT%_datadir/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%_includedir
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/glibmm*
%{_libdir}/giomm*
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%_datadir/doc/glibmm-2.4
%_datadir/glibmm-2.4
%_datadir/devhelp

%changelog
* Thu Nov 14 2013 - Thomas Wagner
- fix dependencies to be g++ compiled SFEsigcpp-gpp.spec (we are fully in g++ world)
- change (Build)Requires to %{pnm_requires_SUNWgnome_base_libs_devel}, %include packagenamemacros.inc
- change _prefix to %include usr-g++.inc
* Thu Oct 24 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Change Requires: SUNW* to %{pnm_requires_SUNW*}
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Fri Nov 06 2009 - jchoi42@pha.jhu.edu
- comment deprecated patch
* Fri Sep 25 2009 - jchoi42@pha.jhu.edu
- specified giomm dir in %files section
* Sun Jun 29 2008 - river@wikimedia.org
- force to use gcc in /usr/sfw, not /usr/gnu
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWglibmm.spec to build with g++
