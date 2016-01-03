#
# spec file for package SFEat-spi2-atk-gpp
#
# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1

Name:                    SFEat-spi2-atk-gpp
IPS_package_name:        gnome/accessibility/g++/at-spi2-atk
#Meta(info.classification): %{classification_prefix}:Applications/Universal Access
Group:                   Applications/Universal Access
License:                 LGPL v2, MIT/X
Summary:                 Accessibility implementation on D-Bus for GNOME
Version:                 2.18.1
Source:	                 http://ftp.gnome.org/pub/GNOME/sources/at-spi2-atk/2.18/at-spi2-atk-%version.tar.xz
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright

%include default-depend.inc
Requires:       SFEglib2-gpp
Requires:       SUNWdbus
Requires:       SUNWdbus-glib
Requires:       SUNWgtk2
Requires:       SUNWlxml
Requires:       SUNWlibatk
Requires:       SUNWat-spi2-core
BuildRequires:  SFEglib2-gpp-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SUNWdbus-glib-devel
BuildRequires:  SUNWgtk2-devel
BuildRequires:  SUNWlxml
BuildRequires:  SFElibatk-gpp-devel
BuildRequires:  SFEat-spi2-core-gpp


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n at-spi2-atk-%{version}

%build
libtoolize -f
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib -lgmodule-2.0"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --bindir=%{_bindir}			\
            --sysconfdir=%{_sysconfdir}		\
            --mandir=%{_mandir}			\
            --libexecdir=%{_libexecdir}		\
            %{gtk_doc_option}
make

%install
rm -rf %buildroot
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm %buildroot%_libdir/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d  at-spi2-atk-%{version}/AUTHORS
%doc -d  at-spi2-atk-%{version}/COPYING
%doc -d  at-spi2-atk-%{version}/README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk-2.0/modules/*.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*
%{_libdir}/libatk-bridge-2.0.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/atk-bridge-2.0.pc
%_includedir

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Thu May 03 2012 - brian.cameron@oracle.com
- Bump to 2.4.0.
...

* Fri Nov 20 2009 - li.yuan@sun.com
- Initial version.
