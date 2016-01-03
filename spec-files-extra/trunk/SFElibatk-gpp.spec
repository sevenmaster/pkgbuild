#
# spec file for package SFElibatk-gpp
#

# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%use atk_64 = atk.spec
%endif

%include base.inc
%define gtk_doc_option --disable-gtk-doc
%use atk = atk.spec

Name:                    SFElibatk-gpp
License:		 LGPL v2
IPS_package_name:        library/desktop/g++/atk
#Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Group:			 Desktop (GNOME)/Libraries
Summary:                 GNOME accesibility toolkit libraries
Version:                 %{atk.version}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright

%include default-depend.inc
BuildRequires: SFEglib2-gpp-devel
BuildRequires: SFEgobject-introspection-gpp-devel
BuildRequires: SUNWuiu8

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: name
Requires: SFEglib2-gpp-devel

%package l10n
Summary:                 %{summary} - l10n content
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%atk_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%atk.prep -d %name-%version/%{base_arch}

# cd %{_builddir}/%name-%version
# gzcat %SOURCE0 | tar xf -

%build

export CC=gcc
export CXX=g++

PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
export LDFLAGS="-L/usr/g++/lib/amd64 -R/usr/g++/lib/amd64"
%atk_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
%atk.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%atk_64.install -d %name-%version/%_arch64
%endif

%atk.install -d %name-%version/%{base_arch}

# rm -rf $RPM_BUILD_ROOT%{_mandir}
# cd %{_builddir}/%name-%version/sun-manpages
# export PATH=/usr/sfw/bin:/usr/gnu/bin:$PATH
# make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%{_libdir}/%{_arch64}/girepository-1.0/Atk-1.0.typelib
%endif
%{_libdir}/girepository-1.0/Atk-1.0.typelib
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/Atk-1.0.gir
# %dir %attr(0755, root, bin) %{_mandir}
# %dir %attr(0755, root, bin) %{_mandir}/man3
# %{_mandir}/man3/*

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Tue Jun 08 2010 - Michal.Pryc@Oracle.Com
- Updated BuildRequires to fit SourceJuicer.
* Fri Mar  5 2010 - christian.kelly@sun.com
- Add dependency on SUNWgobject-introspection.
* Tue Jun 02 2009 - dave.lin@sun.com
- fixed dependency issue(CR6843654).
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)


