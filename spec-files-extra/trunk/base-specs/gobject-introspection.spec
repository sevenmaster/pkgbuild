#
# spec file for package gobject-introspection
#
# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%{?!pythonver:%define pythonver 2.7}

Name:         gobject-introspection
License:      LGPL v2+ (giscanner), GPL v2+ (tools), MIT, BSD
Group:        Libraries
Version:      1.34.2
Release:      1
Distribution: Java Desktop System
Vendor:       Gnome Community
Summary:      Introspection for GObject libraries
URL:          http://live.gnome.org/GObjectIntrospection
Source:       http://download.gnome.org/sources/%{name}/1.34/%{name}-%{version}.tar.xz
# We only deliver one set of the Python files, so it is necessary to modify
# /usr/bin/amd64/g-ir-scanner to point to the right python files.
# date:2010-04-09 owner:yippi type:feature
Patch1:       gobject-introspection/gobject-introspection-01-amd64.patch
Patch2:	      gobject-introspection/disable_tests.patch
Patch3:       gobject-introspection/Makefile-gir.am.patch
Patch4:       gobject-introspection/respect_cflags.patch

BuildRequires:  autoconf >= 2.59
BuildRequires:  automake >= 1:1.8
BuildRequires:  bison
BuildRequires:  glib2-devel >= 1:2.16.0
BuildRequires:  libffi-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  python >= 1:2.5
BuildRequires:  python-devel >= 1:2.5

%description
Tools for introspecting GObject-based frameworks.

%package devel
Summary:        Header files for gobject-introspection
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       glib2-devel >= 2.16.0

%description devel
Header files for gobject-introspection.

%package static
Summary:        Static gobject-introspection library
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
Static gobject-introspection library.

%prep
%setup -q
%define _patch_options --unified
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#substitute python to 2.6, CR6924142
pyfiles="
giscanner/shlibs.py
giscanner/scannermain.py
"

for i in $pyfiles
do
  sed -e s,/usr/bin/env\ python,$PYTHON, $i > $i.new
  mv $i.new $i
done

aclocal $ACLOCAL_FLAGS -I m4
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir} \
            --disable-tests

# disable parallel builds as it's broken for 0.6.10
#gmake -j $CPU
gmake

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

find $RPM_BUILD_ROOT -type f -name "*.pyc" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libgirepository-everything-1.0.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libgirepository-everything-1.0.so.1
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libgirepository-1.0.so.0
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/g-ir-compiler
%attr(755,root,root) %{_bindir}/g-ir-generate
%attr(755,root,root) %{_bindir}/g-ir-scanner
%{_mandir}/man1/g-ir-compiler.1*
%{_mandir}/man1/g-ir-generate.1*
%{_mandir}/man1/g-ir-scanner.1*
%attr(755,root,root) %{_libdir}/libgirepository-everything-1.0.so
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so
%{_libdir}/pkgconfig/gobject-introspection-1.0.pc
%{_includedir}/gobject-introspection-1.0
%{_libdir}/libgirepository-1.0.la
%{_libdir}/libgirepository-everything-1.0.la
%{_datadir}/aclocal/introspection.m4
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*.gir

%files static
%defattr(-,root,root)
%{_libdir}/libgirepository-1.0.a
%{_libdir}/libgirepository-everything-1.0.a

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Mon Apr 30 2012 - brian.cameron@oracle.com
- Bump to 1.32.1.
...

* Mon Aug 24 2009 - halton.huo@sun.com
- Initial version.

