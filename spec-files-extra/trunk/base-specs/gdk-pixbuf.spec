#
# spec file for package gdk-pixbuf
#
# Copyright (c) 2011, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

#%define none:none

Name:         gdk-pixbuf
License:      Unknown
Group:        System/Libraries
Version:      2.31.6
Release:      1
Distribution: Java Desktop System
Vendor:	      Gnome Community
Summary:      Library
Source:       ftp://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.31/gdk-pixbuf-%version.tar.xz
Patch1:       gdk-pixbuf-01-dlopen-medialib.patch
URL:          http://cairographics.org
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%description
gdk-pixbuf

%prep
%setup -q
%patch1 -p1

%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
	    %{gtk_doc_option}

gmake

%install
gmake DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Sat Sep 15 2012 - brian.cameron@oracle.com
- Bump to 2.26.3.
* Tue May 01 2012 - brian.cameron@oracle.com
- Bump to 2.26.1.
* Thu Sep 08 2011 - brian.cameron@oracle.com
- Bump to 2.24.0.
* Thu Jul 21 2011 - brian.cameron@oracle.com
- Added patch gdk-pixbuf-01-dlopen-medialib.diff.
* Tue Jul 05 2011 - brian.cameron@oracle.com
- Created with 2.23.5.
