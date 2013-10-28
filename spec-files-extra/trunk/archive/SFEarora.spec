#
# spec file for package SFEarora
#
# includes module: arora
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname arora

Name:		SFEarora
IPS_Package_Name:	web/browser/arora
Summary:	Lightweight Web browser using QtWebKit
URL:		http://code.google.com/p/arora
License:	GPLv2
Group:		Applications/Internet
SUNW_Copyright:	arora.copyright
Version:	0.11.0
Source:		http://%srcname.googlecode.com/files/%srcname-%version.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgmake
%if %(/usr/bin/pkginfo -q SFEcoreutils 2>/dev/null  && echo 1 || echo 0)
BuildRequires:	SFEcoreutils
%else
BuildRequires:	SUNWgnu-coreutils
%endif
BuildRequires: SUNWgtar
BuildRequires: SFEqt-gpp-devel

Requires: SFEqt-gpp
Requires: SUNWzlib


%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++
qmake PREFIX=$RPM_BUILD_ROOT%_basedir
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/%srcname
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/*.desktop
%_mandir
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/arora.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/arora.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128/apps
%_datadir/icons/hicolor/128x128/apps/arora.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable/apps
%_datadir/icons/hicolor/scalable/apps/arora.svg
%dir %attr (-, root, other) %_datadir/pixmaps
%_datadir/pixmaps/arora.xpm

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/%srcname/locale
%attr (-, root, other) %_datadir/%srcname/locale/*
%endif


%changelog
* Mon Oct 28 2013 - Alex Viskovatoff
- Archive: development stopped in January 2012
* Mon Dec 10 2012 - Logan Bruns <logan@gedanken.org>
- Accept either SFEcoreutils or SUNWgnu-coreutils for buildrequires.
* Fri Jul 29 2011 - Alex Viskovatoff
- Build with gcc (to avoid building a second Qt); add SUNW_Copyright
* Thu Jan 27 2011 - Alex Viskovatoff
- Accommodate to Qt being in /usr/stdcxx; define QMAKESPEC and QTDIR
* Sat Dec 11 2010 - Alex Viskovatoff
- Initial spec
