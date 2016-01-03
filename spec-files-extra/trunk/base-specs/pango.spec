#
# spec file for package pango
#
# Copyright (c) 2003, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         pango
License:      LGPL v2
Group:        System/Libraries
Version:      1.36.8
# "grep pango_module_version configure.in" for the api version number.
%define module_api_version 1.6.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Gnome Community
Summary:      Library for layout and rendering of internationalized text
Source:       http://ftp.gnome.org/pub/GNOME/sources/pango/1.36/pango-%{version}.tar.xz
Patch3:	      pango/03-solaris-cjk-font-table.patch
Patch4:	      pango/04-disable-thai-modules.patch

URL:          http://www.gtk.org
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define freetype2_version 2.1.3
%define cairo_version 0.9.2
%define glib2_version 2.5.7
%define pkgconfig_version 0.15.0
%define XFree86_version 4.3.0
%define fontconfig_version 2.2.92

Requires:      freetype2 >= %{freetype2_version}
Requires:      cairo >= %{cairo_version}
Requires:      glib2 >= %{glib2_version}
Requires:      XFree86-libs >= %{XFree86_version}
Requires:      fontconfig >= %{fontconfig_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: freetype2-devel >= %{freetype2_version}
BuildRequires: XFree86-devel >= %{XFree86_version}

%description
Pango is a library for layout and rendering of text, with an emphasis on
internationalization. It forms the core of text and font handling in GTK+ 2.0.

%package devel
Summary:      Development Library for layout and rendering of internationalized text
Group:        Development/Libraries
Requires:     %{name} = %{version}-%{release}
Requires:     glib2-devel >= %{glib2_version}
Requires:     cairo-devel >= %{cairo_version}
Requires:     freetype2-devel >= %{freetype2_version}
Requires:     XFree86-devel >= %{XFree86_version}

%prep
%setup -q
%define _patch_options --unified
%patch3 -p1
%patch4 -p1

%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

#cp %{SOURCE1} docs/layout.gif
#cp %{SOURCE2} docs/rotated-text.png

aclocal $ACLOCAL_FLAGS
libtoolize --force --copy
gtkdocize
autoheader
autoconf
automake -a -c -f
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib -lgmodule-2.0"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --sysconfdir=%_sysconfdir \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
	    %{gtk_doc_option}

# disable "-j" on sparc to workaround build issue
%ifnarch sparc
#gmake -j $CPUS
gmake
%else
gmake
%endif

%install
gmake DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/pango/%{module_api_version}/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/pango/*/*/*.so
%{_libdir}/libpango*-*.so.*
%{_bindir}/pango-querymodules
%{_sysconfdir}/pango/*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_libdir}/libpango*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/pango
%{_mandir}/man3/*

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Sat Sep 15 2012 - brian.cameron@oracle.com
- Bump to 1.30.1.
...

* Tue May 13 2003 - Stephen.Browne@sun.com
- initial Sun release.
