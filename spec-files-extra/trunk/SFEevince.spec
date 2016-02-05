# spec file for package SFEevince
#
# Copyright (c) 2009, 2015, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc
%define srcname evince
%include osdistro.inc

Name:			SFEevince
IPS_package_name:	desktop/g++/pdf-viewer/evince

Meta(info.classification): Applications/Office
#Group:			Applications/Office
License:		GPLv2
Summary:		GNOME PDF document viewer
Version:		3.6.1
Source:       http://ftp.gnome.org/pub/GNOME/sources/evince/3.6/%srcname-%version.tar.xz
SUNW_BaseDir:		%_basedir
SUNW_Copyright:		%srcname.copyright

%include default-depend.inc
BuildRequires: library/desktop/libglade
BuildRequires: library/popt
BuildRequires: library/gnome/gnome-libs
BuildRequires: library/gnome/gnome-component
BuildRequires: runtime/python-27
BuildRequires: SFEfontconfig-gpp
BuildRequires: image/library/libtiff
BuildRequires: system/library/dbus
BuildRequires: gnome/config/gconf
BuildRequires: library/gnome/gnome-vfs
BuildRequires: image/library/libjpeg
BuildRequires: print/filter/ghostscript
BuildRequires: developer/gnome/gnome-doc-utils
BuildRequires: gnome/theme/gnome-icon-theme
BuildRequires: library/gnome/gnome-keyring
BuildRequires: SFEpoppler-gpp
BuildRequires: SFElibspectre-gpp
BuildRequires: SFEgtk3-gpp
BuildRequires: SFEtexlive
# This allows dvi files to be displayed without creating rasterized fonts
BuildRequires: SFEt1lib
BuildRequires: SFEdjvulibre
Requires: library/g++/poppler
# libspectre is delivered together with pango by OSolaris' evince package
Requires: library/desktop/g++/libspectre
# This build of evince supports dvi and djvu files
Requires: text/texlive
Requiers: system/library/t1lib
Requires: library/desktop/djvulibre
Requires: library/desktop/libglade
Requires: library/popt
Requires: library/gnome/gnome-libs
Requires: library/gnome/gnome-component
Requires: system/library/g++/fontconfig
Requires: image/library/libtiff
Requires: system/library/dbus
Requires: system/library/freetype-2
Requires: gnome/config/gconf
Requires: library/gnome/gnome-vfs
Requires: image/library/libjpeg
Requires: system/library/math
Requires: library/libxml2
Requires: library/zlib
Requires: service/gnome/desktop-cache

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
BuildRequires: runtime/perl-512

%package l10n
Summary:                 %{summary} - l10n files

%prep
%setup -q -n %srcname-%version


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export PKG_CONFIG_PATH=%_pkg_config_path
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib:/usr/g++/lib -lX11 -lm"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

export PKG_CONFIG_PATH=%_pkg_config_path

# SFE's libtool gets confused if the S11 libtool is installed
# so place /usr/bin in front of /usr/gnu/bin
export PATH=/opt/dtbld/bin:/usr/g++/bin:/usr/bin:/usr/gnu/bin:/usr/sbin
libtoolize --force
intltoolize --force --copy --automake

#export PATH=/usr/g++/bin:$PATH
aclocal $ACLOCAL_FLAGS 
# Need gnu gettext, so place /usr/gnu/bin in front again
export PATH=/opt/dtbld/bin:/usr/g++/bin:/usr/gnu/bin:/usr/bin:/usr/sbin
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/libxml2" \
LDFLAGS="$LDFLAGS -lgmodule-2.0" \
  ./configure \
	--prefix=%{_prefix} \
        --libexecdir=%{_libexecdir} \
	--disable-static		\
	--disable-comics		\
	--disable-nautilus		\
	--enable-thumbnailer		\
	--enable-t1lib			\
	--mandir=%{_mandir}

# Line with contents "@YELP_HELP_RULES@" produces a "missing separator" error
pushd help
grep -v YELP_HELP_RULES Makefile > Makefile.fixed
mv Makefile.fixed Makefile
popd

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=%buildroot

rm %buildroot%_libdir/*.la
rm %buildroot%_libdir/evince/*/backends/*.la

cd %buildroot%_bindir
ln -s evince gpdf

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/evince
%{_libdir}/libev*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/evince
%_datadir/GConf/gsettings/evince.convert
%_datadir/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%_datadir/thumbnailers/evince.thumbnailer
#%dir %attr (0755, root, other) %{_datadir}/gnome
#%{_datadir}/gnome/help/evince/C
#%{_datadir}/omf/evince/*-C.omf
%attr (-, root, other) %{_datadir}/icons
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc README
%doc(bzip2) AUTHORS
%doc(bzip2) COPYING
%doc(bzip2) ChangeLog
%doc(bzip2) po/ChangeLog
%doc(bzip2) help/ChangeLog
%doc(bzip2) NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service
%{_libdir}/evinced

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/html

%changelog
* Sun Jan 17 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from solaris-desktop~spec-files; eliminate base spec
- Move libspectre to a separate spec/package
* Mon Nov 18 2013 - abhijit.nath@Oracle.Com
- Added TPNO information. Bug 17795775. 
...

* Mon Feb 23 2004 - <niall.power@sun.com>
- install gconf schemas at end of install stage.



