#
# spec file for package SFEabiword
#
# includes module(s): abiword
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%use abiword = abiword.spec

Name:               SFEabiword
IPS_Package_Name:	desktop/word-processor/abiword
Summary:            %abiword.summary
Version:            %{default_pkg_version}
URL:                http://www.abisource.com/
License:            GPLv2
SUNW_BaseDir:       %{_basedir}
SUNW_Copyright:     %{name}.copyright
Group:		    Applications/Office
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:      SFEgcc
Requires:           SFEgccruntime
Requires:           SUNWuiu8
Requires:           SUNWzlib
Requires:           SUNWgnome-base-libs
Requires:           SUNWpng
Requires:           SUNWlxml
Requires:           SUNWlibpopt
Requires:           SUNWgnome-spell
Requires:           SUNWgnome-character-map
Requires:           SUNWgnome-print
Requires:           SUNWfontconfig
Requires:           SUNWlibgoffice
Requires:           %pnm_requires_perl_default
Requires:           SUNWlibgsf
Requires:           SUNWlibrsvg
Requires:           SFElibfribidi
Requires:           SFEwv
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWpng-devel
BuildRequires:      SUNWlxml-devel
BuildRequires:      SUNWlibpopt-devel
BuildRequires:      SUNWgnome-spell-devel
BuildRequires:      SUNWgnome-character-map-devel
BuildRequires:      SUNWgnome-print-devel
BuildRequires:      SUNWlibgoffice
BuildRequires:      SUNWlibgsf-devel
BuildRequires:      SFElibfribidi-devel
BuildRequires:      SFEwv-devel
BuildRequires:      SUNWgnome-common-devel
BuildRequires:      SUNWlibrsvg-devel

Requires: SUNWmyspell-dictionary-en
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%abiword.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%{_ldflags}"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%abiword.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%abiword.install -d %name-%version
#mkdir -p $RPM_BUILD_ROOT%{_bindir}
#cp $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/* $RPM_BUILD_ROOT%{_bindir}/
#rm -rf $RPM_BUILD_ROOT%{_prefix}/X11R6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*
%{_cxx_libdir}/abiword-2.8
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/abiword*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/icons
%{_datadir}/icons/*.png
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*

%changelog
* Wed Sep 14 2011 - Alex Viskovatoff
- Add missing dependency on runtime/gcc
* Fri Nov 12 2010 - Alex Viskovatoff
- Abiword has an internal spell checker, so do not require SFEaspell
  but require library/myspell/dictionary/en (with SUNW name)
- Do not install in /usr/lib, since compilation is with g++
* May 2010 - Gilles dauphin
- set PKG_CONFIG_PATH in case of install in /opt/SFE
* Wed May 05 2010 - Milan Jurik
- added missing build dependencies
* Wed Feb 03 2010 - brian.cameron@sun.com
- Now build with gcc since the new 2.8.1 version does not build with Sun
  Studio.
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add copyright and grouping
* Mon Apr 14 2008 - nonsea@users.sourceforge.net
- s/SUNWdesktop-search-libs/SUNWlibgsf cause the pkg name change.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWaspell or SFEaspell. Also add support for
  building on Indiana systems.
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Initial spec
