#
# spec file for package SFEgtk3-gpp
#
# Copyright (c) 2011,2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-g++.inc
%define _pkg_docdir %_docdir/pango
%define cc_is_gcc 1
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define _sysconfdir /etc/%{_arch64}
%use gtk_64 = gtk3.spec
%endif

%include base.inc
%define _sysconfdir %_prefix/etc
%define gtk_doc_option --disable-gtk-doc

%use gtk = gtk3.spec

Name:                    SFEgtk3-gpp
IPS_package_name:        library/desktop/g++/gtk3
#Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Group:                   Desktop (GNOME)/Libraries
Summary:                 GTK+ - GIMP toolkit libraries
Version:                 %{gtk.version}
License:                 %{gtk.license}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright

%include default-depend.inc
Requires: library/desktop/g++/cairo
Requires: library/desktop/g++/pango
Requires: library/desktop/g++/atk
Requires: image/library/libjpeg
Requires: image/library/libpng
Requires: system/library/math
Requires: service/gnome/desktop-cache
Requires: x11/library/libxinerama
BuildRequires: SFEat-spi2-atk-gpp
BuildRequires: SFEgobject-introspection-gpp-devel
BuildRequires: system/library/iconv/utf-8
BuildRequires: SFEcairo-gpp-devel
BuildRequires: SFEpango-gpp-devel
BuildRequires: SFElibatk-gpp-devel
BuildRequires: image/library/libjpeg
BuildRequires: image/library/libpng
BuildRequires: image/library/libtiff
BuildRequires: x11/server/xorg
BuildRequires: x11/library/libxi
BuildRequires: system/library/math
BuildRequires: SFEgdk-pixbuf-gpp-devel

# %package root
# Summary:                 %{summary} - / filesystem
# SUNW_BaseDir:            /
# %include default-depend.inc

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc


%package print-cups
IPS_package_name:        library/desktop/g++/gtk3/gtk-backend-cups
Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Summary:                 %{summary} - CUPS Print Backend
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
# static dependencies needed in this package as some of the libraries
# needed to detect the dependencies are built in the same spec but are
# not in the same package (e.g. libatk)
Requires: library/g++/glib2
Requires: library/desktop/g++/cairo
Requires: library/desktop/g++/pango
Requires: library/desktop/g++/atk
Requires: library/desktop/g++/gtk2
Requires: print/cups
BuildRequires: print/cups

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n content
Requires: %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

%if 0
#%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%gtk_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gtk.prep -d %name-%version/%{base_arch}

#cd %{_builddir}/%name-%version
#gzcat %SOURCE0 | tar xf -

%build

export CC=gcc
export CXX=g++

%if 0
#%ifarch amd64 sparcv9
export CFLAGS="%optflags64 -I/usr/X11/include"
export CXXFLAGS="%cxx_optflags64 -I/usr/X11/include"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="$FLAG64"
export PKG_CONFIG_PATH="%{_pkg_config_path64}"
%gtk_64.build -d %name-%version/%_arch64
%endif

export CFLAGS="%optflags -I/usr/g++/include/glib-2.0 -I/usr/g++/lib/glib-2.0/include -I/usr/X11/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include/glib-2.0 -I/usr/g++/lib/glib-2.0/include -I/usr/X11/include"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib -lglib-2.0"
export PKG_CONFIG_PATH="%_pkg_config_path"
export PATH=/usr/g++/bin:$PATH
%gtk.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%if 0
#%ifarch amd64 sparcv9
%gtk_64.install -d %name-%version/%_arch64
%endif

%gtk.install -d %name-%version/%{base_arch}

#rm -rf $RPM_BUILD_ROOT%{_mandir}
#cd %{_builddir}/%name-%version/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

# Move demo to demo directory.
#
# install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
# mv $RPM_BUILD_ROOT%{_bindir}/gtk3-demo $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
# mv $RPM_BUILD_ROOT%{_bindir}/gtk3-demo-application $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin

rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/*/immodules/im-[a-wyz]*.so

# on linux, these config files are created in %post
# that would be more complicated on Solaris, especially
# during jumpstart or live upgrade, so it's better to do
# it during the build
$RPM_BUILD_ROOT%{_bindir}/gtk-query-immodules-3.0 \
    $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/*/immodules/im-xim.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0/gtk.immodules

%if 0
#%ifarch amd64 sparcv9
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gtk-3.0/*/immodules/im-[a-wyz]*.so

export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}/%{_arch64}

mkdir  -p $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/gtk-3.0

$RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtk-query-immodules-3.0 \
    $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gtk-3.0/*/immodules/im-xim.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/gtk-3.0/gtk.immodules

mkdir -p $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtk3-demo \
    $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtk3-demo-application \
    $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/%{_arch64}
%endif

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri pixbuf-loaders-installer input-method-cache

%files
%defattr (-, root, bin)
%doc -d %{base_arch} gtk+-%{gtk.version}/README
%doc -d %{base_arch} gtk+-%{gtk.version}/AUTHORS
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/COPYING
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gtk-update-icon-cache
%{_bindir}/gtk3-widget-factory
%{_bindir}/gtk-*3.0
# %{_bindir}/%{_arch64}/gtk-*3.0
# %{_bindir}/%{_arch64}/gtk-update-icon-cache
# %{_bindir}/%{_arch64}/gtk3-widget-factory

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gtk*/*/printbackends/libprintbackend-file.so
%{_libdir}/gtk*/*/printbackends/libprintbackend-lpr.so
#%{_libdir}/girepository-1.0/*
%{_libdir}/gtk-3.0/3.0.0/immodules
%if 0
#%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/gtk*/*/printbackends/libprintbackend-file.so
%{_libdir}/%{_arch64}/gtk*/*/printbackends/libprintbackend-lpr.so
%{_libdir}/%{_arch64}/gtk-3.0/3.0.0/immodules
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/girepository-1.0
%{_libdir}/%{_arch64}/girepository-1.0/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/glib-2.0
%{_datadir}/themes
#%{_datadir}/gir-1.0/*
%{_datadir}/gtk-3.0/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
#%dir %attr (0755, root, bin) %dir %{_bindir}
%_bindir
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
# %dir %attr (0755, root, bin) %dir %{_prefix}/demo
# %dir %attr (0755, root, bin) %dir %{_prefix}/demo/jds
# %dir %attr (0755, root, bin) %dir %{_prefix}/demo/jds/bin
# %{_prefix}/demo/jds/bin/gtk3-demo
# %{_prefix}/demo/jds/bin/gtk3-demo-application
%if 0
#%ifarch amd64 sparcv9
%{_prefix}/demo/jds/bin/%{_arch64}/gtk3-demo
%{_prefix}/demo/jds/bin/%{_arch64}/gtk3-demo-application
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man1
%defattr (-, root, other)
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/*.desktop
%dir %attr (-, root, other) %_datadir/icons
%_datadir/icons/hicolor

#%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%ghost %ips_tag(original_name=SFEgtk3-gpp:%{@} preserve=true) %{_sysconfdir}/gtk-3.0/gtk.immodules
%ips_tag(original_name=SFEgtk3-gpp:%{@} preserve=true) %{_sysconfdir}/gtk-3.0/im-multipress.conf
%if 0
#%ifarch amd64 sparcv9
%ghost %ips_tag(original_name=SFEgtk3-gpp:%{@} preserve=true) %{_sysconfdir}/%{_arch64}/gtk-3.0/gtk.immodules
%ips_tag(original_name=SFEgtk3-gpp:%{@} preserve=true) %{_sysconfdir}/%{_arch64}/gtk-3.0/im-multipress.conf
%endif

%files print-cups
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk*/*/printbackends/libprintbackend-cups.so
%if 0
#%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/gtk*/*/printbackends/libprintbackend-cups.so
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Jan 29 2016 - Alex Viskovatoff <herzen@imap.cc>
- Build examples
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Sat Sep 15 2012 - Brian.Cameron@oracle.com
- Set C++ environment variables for amd64 so tests build.
* Tue May 01 2012 - brian.cameron@oracle.com
- Fix Requires/BuildRequires and packaging after update to 3.4.1.
* Fri Aug 26 2011 - brian.cameron@oracle.com
- Fix packaging after updating to GTK3 3.1.12.
* Tue Jul 12 2011 - brian.cameron@oracle.com
- Created.
