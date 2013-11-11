#
# spec file for package SFEarora
#

# Call pkgbuild/tool with --with-CC to build with Sun Studio/stdcxx
%define with_gcc %{!?_with_CC:1}%{?_with_CC:0}

%include Solaris.inc
%if %with_gcc
%define cc_is_gcc 1
%include base.inc
IPS_Package_Name:	web/browser/arora
%else
IPS_Package_Name:	web/browser/stdcxx/arora
%end
%define srcname arora

Name:		SFEarora
%
Summary:	Lightweight Web browser using QtWebKit
URL:		http://code.google.com/p/arora
License:	GPLv2
Group:		Applications/Internet
SUNW_Copyright:	arora.copyright
Version:	0.11.0
Source:		http://%srcname.googlecode.com/files/%srcname-%version.tar.gz
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%if %with_gcc
BuildRequires: SFEqt-gpp-devel
Requires: SFEqt-gpp
%else
BuildRequires: SFEqt-stdcxx-devel
Requires: SFEqt-stdcxx
%end


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

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %with_gcc
export CC=gcc
export CXX=g++
export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++
%else
export PATH=/usr/stdcxx/bin:$PATH
export QMAKESPEC=solaris-cc-stdcxx
export QTDIR=/usr/stdcxx
%end
qmake PREFIX=%buildroot%_basedir
gmake -j$CPUS

%install
rm -rf %buildroot

gmake install

%if %build_l10n
%else
rm -rf %buildroot%_datadir/%srcname
%endif

%clean
rm -rf %buildroot


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
* Sun Nov  3 2013 - Alex Viskovatoff
- Allow selection of g++ or CC to do the build (since the main use of this
  spec now is for testing QtWebKit)
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
