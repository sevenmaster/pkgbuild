#
# spec file for package SFElibcanberra
#
# Copyright (c) 2010, 2014, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%use libcanberra_64 = libcanberra.spec
%endif

%include base.inc
%use libcanberra = libcanberra.spec

Name:                    SFElibcanberra-gpp
IPS_package_name:        library/desktop/g++/xdg/libcanberra
Meta(info.classification): %{classification_prefix}:System/Multimedia Libraries
Meta(com.oracle.info.name): %{libcanberra.name}
Meta(com.oracle.info.version): %{libcanberra.version}
Meta(com.oracle.info.description): %{libcanberra.summary}
Meta(com.oracle.info.tpno): 9315
Summary:                 Event Sound API Using XDG Sound Theming Specification
Version:                 %{libcanberra.version}
#Source1:                 %{name}-manpages-0.1.tar.gz
SUNW_Copyright:          libcanberra.copyright
License:                 %{libcanberra.license}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

BuildRequires: codec/ogg-vorbis
BuildRequires: gnome/config/gconf
BuildRequires: library/audio/gstreamer
BuildRequires: library/audio/pulseaudio
BuildRequires: library/desktop/gtk2
BuildRequires: SFEgtk3-gpp-devel
BuildRequires: library/libtool/libltdl
BuildRequires: x11/library/libxi

Requires: gnome/theme/sound/xdg-sound-theme
Requires: service/gnome/desktop-cache

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libcanberra_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%libcanberra.prep -d %name-%version/%base_arch

#cd %{_builddir}/%{name}-%{version}
#gzcat %SOURCE1 | tar xf -

%build
export CC=gcc
export CXX=g++

%ifarch amd64 sparcv9
export PKG_CONFIG_PATH="%_pkg_config_path64"
export CFLAGS="%optflags64"
export LDFLAGS="-R/usr/g++/lib/amd64"
%libcanberra_64.build -d %name-%version/%_arch64
%endif

export PKG_CONFIG_PATH="%_pkg_config_path"
export CFLAGS="%optflags"
export LDFLAGS="-R/usr/g++/lib"
%libcanberra.build -d %name-%version/%base_arch

%install
rm -rf %buildroot
%ifarch amd64 sparcv9
%libcanberra_64.install -d %name-%version/%_arch64
%endif

%libcanberra.install -d %name-%version/%base_arch

#cd %{_builddir}/%{name}-%{version}/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libcanberra-%{version}
%{_libdir}/lib*.so*
%{_libdir}/gtk-2.0/modules/libcanberra-gtk-module.so
%{_libdir}/gtk-3.0/modules/libcanberra-gtk-module.so
%{_libdir}/gtk-3.0/modules/libcanberra-gtk3-module.so
%{_libdir}/gnome-settings-daemon-3.0/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libcanberra-%{version}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/gtk-2.0/modules/libcanberra-gtk-module.so
#%{_libdir}/%{_arch64}/gtk-3.0/modules/libcanberra-gtk-module.so
#%{_libdir}/%{_arch64}/gtk-3.0/modules/libcanberra-gtk3-module.so
%{_libdir}/%{_arch64}/gnome-settings-daemon-3.0/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%doc -d %{base_arch} %{libcanberra.name}-%{libcanberra.version}/README
%doc -d %{base_arch} %{libcanberra.name}-%{libcanberra.version}/doc/README
%doc(bzip2) -d %{base_arch} %{libcanberra.name}-%{libcanberra.version}/LGPL
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/gdm
%dir %attr (0755, root, bin) %{_datadir}/gdm/autostart
%{_datadir}/gdm/autostart/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%{_datadir}/gtk-doc
%{_datadir}/vala/*
# %dir %attr(0755, root, bin) %{_mandir}
# %dir %attr(0755, root, bin) %{_mandir}/man1
# %dir %attr(0755, root, bin) %{_mandir}/man3
# %{_mandir}/man1/*
# %{_mandir}/man3/*

%attr(0755, root, sys) %dir %_prefix/etc
%_prefix/etc/gconf/schemas/libcanberra.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/libcanberra
%{_datadir}/doc/libcanberra/*
%dir %attr (0755, root, other) %{_datadir}/gnome

%changelog
* Fri Jan 29 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
- Build v. 0.28 instead of v0.26, which OI hipster builds, so do not use
  03-gtk3.patch, which did not apply
* Wed Apr 23 2014 - swaroop.sadare@oracle.com
- Added TPNO and modified the copyright file.
...

* Thu Aug 14 2008 - brian.cameron@sun.com
- Created with version 0.6.
