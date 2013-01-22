#
# spec file for package SFEnetspeed-applet
#
# includes module(s): netspeed_applet
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SFEparcellite
IPS_Package_Name:	desktop/clipboard/parcellite
Summary:                 The lightweight GTK+ clipboard manager.
Group:                   System/GUI/GNOME
Version:                 1.0.2rc5
IPS_Component_Version:	1.0.2.0.5
Source:                  %{sf_download}/parcellite/parcellite-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-libs
Requires:    SUNWgnome-panel
BuildRequires:    SUNWgnome-libs-devel
BuildRequires:    SUNWgnome-common-devel
BuildRequires:    SUNWperl-xml-parser

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
rm -rf %name_%version
%setup -q -n parcellite-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags"

aclocal
automake -a -f
autoconf -f

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

sed -i.orig -e 's/pl_PL/pl/' po/Makefile
mv po/pl_PL.po po/pl.po

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%files root
%defattr(-, root, sys)
%dir %attr (-, root, sys) %{_sysconfdir}/xdg
%dir %attr (-, root, sys) %{_sysconfdir}/xdg/autostart
%attr (-, root, sys) %{_sysconfdir}/xdg/autostart/*

%changelog
* Mon Jan 21 2013 - Luca De Pandis (lucadepandis@gmail.com)
- Fixed conflict with pkg:/gnome/locale/pl
* Mon Oct 27 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec
