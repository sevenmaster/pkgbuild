#
# spec file for package SFEglib2
#
# includes module(s): glib2
#
# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use glib_64 = glib2.spec
%endif

%include base.inc
# S11.3's gtk-doc is too old to build documentation
%define gtk_doc_option --disable-gtk-doc

%use glib = glib2.spec

Name:                    SFEglib2-gpp
IPS_package_name:        library/g++/glib2
#Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Group:			 Desktop (GNOME)/Libraries
Summary:                 GNOME core libraries
Version:                 %{glib.version}
License:                 %{glib.license}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright

%include default-depend.inc
Requires: system/library/math
Requires: library/zlib
Requires: runtime/python-26
BuildRequires: runtime/perl-512
BuildRequires: system/library/math
BuildRequires: runtime/python-26
BuildRequires: developer/documentation-tool/gtk-doc
BuildRequires: developer/gnome/gettext
BuildRequires: data/sgml-common
BuildRequires: data/xml-common
BuildRequires: data/docbook/docbook-style-dsssl
BuildRequires: data/docbook/docbook-style-xsl
BuildRequires: data/docbook/docbook-dtds
# required for including X11/extensions/Xtsol.h in gio-rbac.diff
BuildRequires: x11/trusted/libxtsol

%if %(/bin/test -e /usr/sfw/include/glib.h && echo 1 || echo 0)
BuildConflicts: SUNWGlib
%endif

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEglib2

%package l10n
Summary:                 %{summary} - l10n content
Requires: SFEglib2

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%glib_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%glib.prep -d %name-%version/%{base_arch}

#cd %{_builddir}/%name-%version
#gzcat %SOURCE0 | tar xf -

%build

# Build with gcc because it is one of the four compilers officially
# supported, whereas Sun Studio is not
# https://wiki.gnome.org/Projects/GLib/CompilerRequirements
export CC=gcc
export CXX=g++

PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

export PERL_PATH=/usr/perl5/bin/perl
export PERL=/usr/perl5/bin/perl
export GLIB_EXTRA_CONFIG_OPTIONS=""

%ifarch amd64 sparcv9
export DFLAGS=-64
%glib_64.build -d %name-%version/%_arch64
%endif

export GLIB_EXTRA_CONFIG_OPTIONS="--disable-largefile"

%glib.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%glib_64.install -d %name-%version/%_arch64
%endif

%glib.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
#cd %{_builddir}/%name-%version/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

%ifarch amd64 sparcv9
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/glib-{genmarshal,gettextize,mkenums}
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gobject-query
#FIXME: remove the empty dir
rmdir $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gio/modules
rmdir $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gio
%endif

#FIXME: remove the empty dir
rmdir $RPM_BUILD_ROOT%{_libdir}/gio/modules
rmdir $RPM_BUILD_ROOT%{_libdir}/gio

# These shouldn't get installed in the wrong place to begin with
mv %buildroot%_datadir/gdb/auto-load/usr/g++/lib %buildroot%_datadir/gdb/auto-load/usr
rmdir %buildroot%_datadir/gdb/auto-load/usr/g++

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc -d %{base_arch} glib-%{glib.version}/README
%doc -d %{base_arch} glib-%{glib.version}/AUTHORS
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-1-2
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-0
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-2
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-4
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-6
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-8
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-10
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-12
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-14
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gio/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gmodule/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gobject/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gthread/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/po/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/COPYING
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/NEWS
%dir %attr (0755, root, sys) %dir %_datadir
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gtester
%{_bindir}/gtester-report
%{_bindir}/gio-querymodules
%{_bindir}/glib-compile-resources
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gdbus-codegen
%_bindir/gapplication
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/charset.alias
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/gtester
%{_bindir}/%{_arch64}/gtester-report
%{_bindir}/%{_arch64}/gio-querymodules
%{_bindir}/%{_arch64}/gresource
%{_bindir}/%{_arch64}/gsettings
%{_bindir}/%{_arch64}/gdbus
%{_bindir}/%{_arch64}/gdbus-codegen
%{_bindir}/%{_arch64}/glib-compile-resources
%{_bindir}/%{_arch64}/glib-compile-schemas
%_bindir/%_arch64/gapplication
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/charset.alias
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/glib*/include
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gresource
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%{_libdir}/%{_arch64}/glib*/include
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bash-completion/*
%{_datadir}/glib-2.0
%{_datadir}/gdb/auto-load/usr/lib/*.py
%ifarch amd64 sparcv9
%{_datadir}/gdb/auto-load/usr/lib/%{_arch64}
%endif

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Sat Sep 15 2012 - brian.cameron@oracle.com
- Fix packaging after update to 2.32.4.
...

* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)


