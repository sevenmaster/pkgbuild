# spec file for package SFElibspectre-gpp
#
# Copyright (c) 2009, 2015, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc

%use libspectre = libspectre.spec

Name:                    SFElibspectre-gpp
IPS_package_name:        library/desktop/g++/libspectre
Group:			 Desktop (GNOME)/Libraries
# License(libspectre):         %{libspectre.license}(libspectre)

Summary:                 Small library for rendering PostScript documents
Version:                 %{libspectre.version}
SUNW_BaseDir:            %{_basedir}
# The tag SUNW_Copyright is only used for building SVR4 packages and could not
# be removed because it acts as a safeguard against missing copyright files.
SUNW_Copyright(libspectre):       %{libspectre.name}.copyright

%include default-depend.inc
BuildRequires: library/desktop/libglade
BuildRequires: library/popt
BuildRequires: library/gnome/gnome-libs
BuildRequires: library/gnome/gnome-component
BuildRequires: SFEfontconfig-gpp
BuildRequires: image/library/libtiff
BuildRequires: image/library/libjpeg
Requires: library/desktop/libglade
Requires: library/popt
Requires: library/gnome/gnome-libs
Requires: library/gnome/gnome-component
Requires: system/library/g++/fontconfig
Requires: image/library/libtiff
Requires: system/library/freetype-2
Requires: gnome/config/gconf
Requires: image/library/libjpeg
Requires: system/library/math
Requires: library/libxml2
Requires: library/zlib

%description
libspectre is a small library for rendering Postscript documents. It provides
a convenient easy to use API for handling and rendering Postscript documents. 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}

%prep
rm -rf %name-%version
mkdir %name-%version
%libspectre.prep -d %name-%version

%build

export CC=gcc
export CXX=g++
export PKG_CONFIG_PATH=%_pkg_config_path
# Don't need /usr/g++/lib in RUNPATH, but might in the future
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib:/usr/g++/lib -lX11 -lm"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export RPM_OPT_FLAGS="$CFLAGS"

%libspectre.build -d %name-%version

%install
rm -rf %buildroot
%libspectre.install -d %name-%version

%clean
rm -rf %buildroot

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %_libdir
%_libdir/libspectre.so*
%doc libspectre-%{libspectre.version}/AUTHORS
%doc libspectre-%{libspectre.version}/README
%doc libspectre-%{libspectre.version}/NEWS
%doc libspectre-%{libspectre.version}/COPYING
%doc libspectre-%{libspectre.version}/ChangeLog
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc

%files devel
%defattr (-, root, bin)
%dir %_libdir
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/libspectre.pc
%_includedir/libspectre

%changelog
* Sun Jan 17 2016 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec extracted from SFEgnome-pdf-viewer-gpp.spec (now SFEevince.spec)
