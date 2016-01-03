#
# spec file for package atk
#
# Copyright (c) 2003, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         atk
License:      LGPL v2
Group:        System/Libraries
Version:      2.18.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Gnome Community
Summary:      ATK - Accesibility Toolkit Libraries
Source:       http://ftp.gnome.org/pub/GNOME/sources/atk/2.18/%{name}-%{version}.tar.xz
Patch1:	      atk-01-visibility-hidden.patch
URL:          http://www.gtk.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
AutoReqProv:  on
Prereq:	      /sbin/ldconfig

%define glib2_version 2.5.7

Requires:      glib2 >= %{glib2_version}
BuildRequires: glib2-devel >= %{glib2_version}

%description
The ATK Library provides a set of interfaces for accesibility. By supporting the ATK interfaces, an application or toolkit can be used with such tools as screen readers, magnifiers, and alternate input devices.

%package devel
Summary:      ATK - Accessibility Toolkit Developer Libraries
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     glib2-devel >= %{glib2_version}

%description devel
The ATK Library provides a set of interfaces for accesibility. By supporting the ATK interfaces, an application or toolkit can be used with such tools as screen readers, magnifiers, and alternate input devices.

%prep
%setup -q
%patch1 -p1

%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize -f
aclocal $ACLOCAL_FLAGS
gtkdocize
autoheader
automake -a -c -f
autoconf

export CFLAGS="%{optflags}"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
export LIBS="-lgmodule-2.0"
./configure \
            --prefix=%{_prefix}         \
            --sysconfdir=%{_sysconfdir}	\
            --libdir=%{_libdir}         \
            --bindir=%{_bindir}         \
	    --disable-fvisibility-hidden \
	    %{gtk_doc_option}
make -j $CPUS

%install
export PATH=/usr/sfw/bin:/usr/gnu/bin:$PATH
make DESTDIR=$RPM_BUILD_ROOT install

find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -exec rm {} \;
find $RPM_BUILD_ROOT%{_libdir} -name "*.a" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_libdir}/libatk*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/atk-1.0/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libatk*.so
%{_datadir}/gtk-doc/html/atk
#%{_mandir}/man3/*

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Mon Apr 30 2012 - brian.cameron@oracle.com
- Bump to 2.4.0.
...

* Tue May 13 2003 - Stephen.Browne@sun.com
- initial Sun release
