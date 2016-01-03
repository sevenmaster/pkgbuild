#
# spec file for package SFEat-spi2-core-gpp
#
# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%define _sysconfdir %_prefix/etc

Name:                    SFEat-spi2-core-gpp
IPS_package_name:        gnome/accessibility/g++/at-spi2-core
#Meta(info.classification): %{classification_prefix}:Applications/Universal Access
Group:                   Applications/Universal Access
License:                 LGPL v2, MIT/X
Summary:                 Accessibility implementation on D-Bus
Version:                 2.18.3
Source:	                 http://ftp.gnome.org/pub/GNOME/sources/at-spi2-core/2.18/at-spi2-core-%version.tar.xz
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright

%include default-depend.inc
Requires:       SFEglib2-gpp
Requires:       SUNWdbus
Requires:       SUNWdbus-glib
Requires:       SUNWgtk2
BuildRequires:  SFEglib2-gpp-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SUNWdbus-glib-devel
BuildRequires:  SUNWgtk2-devel

%if 0
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n at-spi2-core-%{version}

%build
aclocal -I . -I ./m4 $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib -lgmodule-2.0"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --bindir=%{_bindir}			\
            --sysconfdir=%{_sysconfdir}		\
            --mandir=%{_mandir}			\
            --libexecdir=%{_libexecdir}		\
            --enable-xevie=no			\
            --with-dbus-daemondir=/usr/lib      \
            %{gtk_doc_option}
make

%install
rm -rf %buildroot
make DESTDIR=$RPM_BUILD_ROOT install

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d  at-spi2-core-%{version}/AUTHORS
%doc -d  at-spi2-core-%{version}/COPYING
%doc -d  at-spi2-core-%{version}/README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/girepository-1.0/*
%{_libdir}/at-spi*
%{_libdir}/libatspi*
%dir %attr (0755, root, sys) %{_datadir}
%_datadir/dbus-1
%_datadir/gir-1.0
%_datadir/gtk-doc
%attr (-, root, other) %{_datadir}/locale

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

#%files root
#%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/at-spi2/accessibility.conf
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Thu May 17 2012 - brian.cameron@oracle.com
- Bump to 2.4.2.
...

* Fri Nov 20 2009 - li.yuan@sun.com
- Initial version.
