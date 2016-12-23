#
# spec file for package glib2 
#
# Copyright (c) 2003, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         glib2 
License:      LGPL v2
Group:        System/Libraries
Version:      2.44.1
Release:      1
Distribution: Java Desktop System
Vendor:       Gnome Community
Summary:      Low level core compatibility library for GTK+ and GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/glib/2.44/glib-%version.tar.xz

# Patch default-path to not include "." because on Solaris we want to avoid
# setting PATH to include the current working directory.  This was an
# ARC requirement.  The GNOME community already decided to not change
# this behavior (bugzilla bug 317945), but this change is safe.  This
# code only gets executed when the user's PATH is unset, which should
# be never.  Safer to avoid adding "." to PATH.
#owner:yippi date:2005-08-14 type:feature 
Patch1:       glib/glib-01-default-path.patch
# owner:laca type:bug date:2005-10-13
Patch2:       glib/glib-02-gmodule-always-lazy.patch
#owner:padraig date:2008-01-10 type:bug bugster:5105006
Patch4:       glib/glib-04-gio-trash-only-home.patch
#owner:dcarbery date:2008-01-30 type:bug bugzilla:385132
Patch5:       glib/glib-05-ac-canonical-host.patch
#owner:erwannc date:2011-04-11 type:feature (port)
Patch6:	      glib/glib-06-solaris-port.patch
#owner:dcarbery date:2008-05-21 type:bug bugzilla:528506
Patch7:       glib/glib-07-ss12-visibility.patch
#owner:erwannc date:2008-09-17 type:bug bugzilla:551919
Patch8:       glib/glib-08-gsize.patch
#owner:gheet date:2011-03-11 type:bug bugster:6956527
Patch9:       glib/glib-09-cleanup-libs.patch
Patch10:      glib/glib-10-gfilemonitorcanelled.patch
URL:          http://www.gtk.org
Docdir:	      %{_defaultdocdir}/doc
AutoReqProv:  on
Prereq:       /sbin/ldconfig

%define pkgconfig_version 0.15.0
%define gtk_doc_version 1.1
%define intltool_version 0.34.1

Requires:      aaa_base
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: intltool >= %{intltool_version}

%description
Glib is the base compatibility library for GTK+ and GNOME. It provides data
structure handling for C, portability wrappers, and interfaces for such
runtime functionality as an event loop, threads, dynamic laoding, and an
object system

%package devel
Summary:        GIMP Toolkit and GIMP Drawing Kit support library
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Glib is the base compatibility library for GTK+ and GNOME. It provides data
structure handling for C, portability wrappers, and interfaces for such
runtime functionality as an event loop, threads, dynamic laoding, and an
object system

%prep
%setup -q -c -T -n glib-%version
xz -dc %SOURCE0 | (cd ..; tar xf -)

# Don't pass --fuzz=0 to patch
%define _patch_options --unified
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export SED="/usr/gnu/bin/sed"
libtoolize --force --copy
gtkdocize
autoheader
%if %{solaris11}
#easy fix, needs to be improved (S11 might not be fixed to this exact automake version...)
#needs requirement on the package
#there is a mediator as well
aclocal-1.15 -I m4macros
automake-1.15 -a -c -f
%else
#use what we can find
aclocal -I m4macros
automake -a -c -f
%endif
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lsecdb -lnsl"


./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --datadir=%{_datadir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
	    --sysconfdir=%{_sysconfdir}	\
	    --disable-fam	\
	    --disable-dtrace \
	    --enable-shared \
	    $GLIB_EXTRA_CONFIG_OPTIONS \
	    %{gtk_doc_option}

gmake V=2 -j$CPUS

%install
export SED="/usr/gnu/bin/sed"

gmake DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
rm -Rf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/lib*.so
%{_includedir}/glib-2.0/*
%{_libdir}/glib-2.0/include/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_datadir}/glib-2.0/*
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Dec 23 2016 - Thomas Wagner
- add (Build)Requires SFElibffi-gpp-devel on Solaris 11 with older libffi (SFElibffi-gpp is in /usr/g++/) (S11)
- on Solaris 11 with older libffi load instead SFElibffi-gpp from /usr/g++/ (S11)
* Sun May 29 2016 - Thomas Wagner
- remove dependency on SUNWGlib
- fix dependency on itself for -devel and -l10n
- change (Build)Requires to pnm_macros, include packagenamemacros.inc
##TODO##
- needs more fresh automake
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Sat Sep 15 2012 - brian.cameron@oracle.com
- Bump to 2.32.4.
...

* Thu May 12 2003 - <ghee.teo@sun.com>
- Initial spec file for glib2
