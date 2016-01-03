#
# spec file for package SFEgobject-introspection-gpp
#

#
# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#%define owner yippi
#
# Note that there are some issues that you need to address to avoid build
# issues when building this module:
#
# 1) For some reason SUNWPython26.spec has a problem with ctypes that causes
#    gobject-introspection to fail to build.  Uninstalling and rebuilding this
#    package from spec-files seems to fix this problem. Need to figure this
#    out and get it fixed in the SUNWPython26 package.
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1

%define pythonver 2.7

%ifarch amd64 sparcv9
%include arch64.inc
%use gi_64 = gobject-introspection.spec
%endif

%include base.inc
%define gtk_doc_option --disable-gtk-doc
%use gi = gobject-introspection.spec

Name:               SFEgobject-introspection-gpp
Summary:            gobject-introspection - GObject introspection support
Version:            %{gi.version}
IPS_package_name:   library/desktop/g++/gobject/gobject-introspection
#Meta(info.classification): %{classification_prefix}:Development/GNOME and GTK+
Group:		    Desktop (GNOME)/Libraries
#SUNW_Copyright:     %{name}.copyright
License:            %{gi.license}
SUNW_BaseDir:       %{_basedir}

BuildRequires:      SFEglib2-gpp-devel
BuildRequires:      library/libffi
BuildRequires:      system/library/iconv/utf-8
BuildRequires:      runtime/python-27
%include default-depend.inc

%package devel
Summary:            %{summary} - development files
SUNW_BaseDir: %{_basedir}

%prep
rm -rf %name-%version
mkdir -p %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%{_arch64}
%gi_64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%gi.prep -d %name-%version/%{base_arch}

%build

export CC=gcc
export CXX=g++

%ifarch amd64 sparcv9
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags -L/usr/g++/lib/amd64 -R/usr/g++/lib/amd64"
export PKG_CONFIG_PATH="%_pkg_config_path64"
export PYTHON=%_std_bindir/amd64/python%pythonver
%gi_64.build -d %name-%version/%{_arch64}
%endif

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="%_pkg_config_path"
export PYTHON=%_std_bindir/python%pythonver
%gi.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
export PKG_CONFIG_PATH="%_pkg_config_path"

%ifarch amd64 sparcv9
%gi_64.install -d %name-%version/%{_arch64}
%endif

%gi.install -d %name-%version/%{base_arch}

%ifarch amd64 sparcv9
# Move the .so file into /usr/lib/gobject-introspection/giscanner/64.
#
mkdir $RPM_BUILD_ROOT%{_libdir}/gobject-introspection/giscanner/64
mv $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gobject-introspection/giscanner/_giscanner.so $RPM_BUILD_ROOT%{_libdir}/gobject-introspection/giscanner/64

# Remove the rest of the amd64 version of the Python code.  No need to deliver
# it twice.
#
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gobject-introspection
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/g-ir-scanner
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/g-ir-annotation-tool
%{_bindir}/g-ir-compiler
%{_bindir}/g-ir-generate
%{_bindir}/g-ir-scanner
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/girepository-1.0/*
%{_libdir}/gobject-introspection/*
%ifarch amd64 sparcv9
%dir %attr(0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/g-ir-annotation-tool
%{_bindir}/%{_arch64}/g-ir-compiler
%{_bindir}/%{_arch64}/g-ir-generate
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%{_libdir}/%{_arch64}/girepository-1.0/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0
%{_datadir}/gobject-introspection-1.0/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc -d %{base_arch}/gobject-introspection-%{version} AUTHORS README COPYING
%doc(bzip2) -d %{base_arch}/gobject-introspection-%{version} COPYING.GPL COPYING.LGPL NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Tue May 01 2012 - brian.cameron@oracle.com
- Fix packaging after update to 1.32.1.
...

* Sat Apr 04 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.


