#
# spec file for package gtk3
#
# Copyright (c) 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         gtk3
License:      LGPL v2
Group:        System/Libraries
Version:      3.14.15
Release:      1
Distribution: Java Desktop System
Vendor:	      Gnome Community
Summary:      GTK+ - GIMP Toolkit Library for creation of graphical user interfaces
Source:       http://ftp.gnome.org/pub/GNOME/sources/gtk+/3.14/gtk+-%{version}.tar.xz
#Source1:      gtk.unset-hack.sh
#Source2:      gtk.unset-hack.csh

Patch1:		gtk3/01-configure.patch
Patch2:		gtk3/02-disable-papi.patch
Patch3:		gtk3/03-use-xim-for-all-locales.patch
Patch4:		gtk3/04-isinf.patch
Patch8:		gtk3/08-default-print-ps.patch
Patch10:	gtk3/10-filechooser-enterkey.patch
Patch16:	gtk3/16-remove-papi.patch
Patch17:	gtk3/17-unregister-callback.patch


Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define cairo_version 0.9.2
%define atk_version 1.7.0
%define pango_version 1.9.0
%define glib2_version 2.7.1
%define libpng_version 1.2.5
%define libjpeg_version 6.2.0

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: atk-devel >= %{atk_verGsion}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: libjpeg >= %{libjpeg_version}
Requires:      cairo >= %{cairo_version}
Requires:      glib2 >= %{glib2_version}
Requires:      atk >= %{atk_version}
Requires:      pango >= %{pango_version}
Requires:      libpng >= %{libpng_version}
Requires:      libjpeg >= %{libjpeg_version}

%description
This fast and versatile library is used all over the world for all
GNOME applications, the GIMP and several others. Originally it was
written for the GIMP and hence has the name Gimp ToolKit. Many people
like it because it is small, efficient and very configurable.

%package devel
Summary:      Library for creation of graphical user interfaces
Group:        Development/Libraries/X11
Autoreqprov:  on
Requires:     %{name} = %{version}
Requires:     cairo-devel >= %{cairo_version}
Requires:     atk-devel >= %{atk_version}
Requires:     pango-devel >= %{pango_version}

%description devel
This fast and versatile library is used all over the world for all
GNOME applications, the GIMP and several others. Originally it was
written for the GIMP and hence has the name Gimp ToolKit. Many people
like it because it is small, efficient and very configurable.

%prep
%setup -q -n gtk+-%{version} 

%define _patch_options --unified
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch8 -p1
%patch10 -p1
%patch16 -p1
%patch17 -p1


%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export SED="/usr/gnu/bin/sed"
# SFE's libtool prevents gtk3 from building, so use the system-provided one
/usr/bin/libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
gtkdocize
autoheader
automake -a -c -f
autoconf

# Our gobject-introspection is too old to enable introspection

./configure --prefix=%_prefix		\
	    --with-native-locale=yes	\
	    --with-xinput=xfree		\
	    --enable-shm		\
	    --enable-xim		\
	    --enable-fbmanager		\
	    --with-gdktarget=x11	\
	    --enable-explicit-deps=yes	\
	    --without-libjasper		\
	    --enable-man		\
	    --disable-glibtest		\
	    --disable-papi		\
	    %{gtk_doc_option}

# Temporary workaround to get examples built:
# For some reason, the following Makefile line gets added on hipster but not S11
# Needed for this command to get executed
#   glib-compile-resources --target=bloatpad-gresources.c --sourcedir=.
#			   --generate-source bloatpad.gresources.xml

pushd examples/bp
gsed -i -e "s/GLIB_COMPILE_SCHEMAS =/GLIB_COMPILE_RESOURCES = glib-compile-resources\nGLIB_COMPILE_SCHEMAS =/" Makefile
popd

# Again, do not use SFE's libtool, which is in /usr/gnu/bin
gsed -i -e 's|$(SHELL) $(top_builddir)/libtool|/usr/bin/libtool|' Makefile

gmake -j $CPUS

%install
gmake DESTDIR=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
# mkdir -p $RPM_BUILD_ROOT/etc/profile.d
# cp %SOURCE1 $RPM_BUILD_ROOT/etc/profile.d/
# cp %SOURCE2 $RPM_BUILD_ROOT/etc/profile.d

rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/*/printbackends/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/gtk-query-immodules-3.0 > %{_sysconfdir}/gtk-3.0/gtk.immodules
%{_bindir}/gdk-pixbuf-query-loaders > %{_sysconfdir}/gtk-3.0/gdk-pixbuf.loaders

%postun
#If this is the last version of the package remove the config files
if [ $1 = 0 ]
then
	rm %{_sysconfdir}/gtk-3.0/gtk.immodules
	rm %{_sysconfdir}/gtk-3.0/gdk-pixbuf.loaders
fi
/sbin/ldconfig

%files 
%{_bindir}/*query*
%{_bindir}/gtk-update-icon-cache
%{_libdir}/lib*.so.*
%{_libdir}/gtk-3.0/*/immodules/*.so
%{_libdir}/gtk-3.0/*/loaders/*.so
%{_libdir}/gtk-3.0/*/engines/*.so
%{_datadir}/themes/*/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_sysconfdir}/profile.d/gtk.unset-hack.sh
%{_sysconfdir}/profile.d/gtk.unset-hack.csh
%dir %{_sysconfdir}/gtk-3.0
%{_mandir}/man1/*.gz

%files devel
%{_bindir}/*-demo
%{_bindir}/*-csource
%{_includedir}/gtk-3.0
%{_libdir}/lib*.so
%{_libdir}/gtk-3.0/include
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-3.0
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/html/*
%{_mandir}/man3/*.gz

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
- Use patches and version at oi-userland
* Sat Sep 15 2012 - brian.cameron@oracle.com
- Bump to 3.4.4.  Add patch gtk3+-05-compile.diff.
...

* Tue Jul 12 2011 - brian.cameron@oracle.com
- Created with 3.1.8.
