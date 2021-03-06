#
# spec file for package SFEsakura
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname sakura
%include packagenamemacros.inc

Name:		SFEsakura
IPS_Package_Name:	terminal/sakura
Summary:	Lightweight terminal emulator based on GTK and VTE
Group:		Applications/System Utilities
URL:		http://www.pleyades.net/david/projects/sakura
Version:	3.3.4
License:	GPLv2
Source:		http://launchpad.net/%srcname/trunk/%version/+download/%srcname-%version.tar.bz2
%include default-depend.inc
SUNW_Copyright: sakura.copyright
SUNW_BaseDir:	%_basedir
BuildRequires:	%pnm_buildrequires_developer_build_cmake
BuildRequires:	SFEgtk3-gpp-devel
Requires:	SFEgtk3-gpp
BuildRequires:	SFEvte-gpp
Requires:	SFEvte-gpp

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version
mkdir build

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/gnu/lib/pkgconfig

cd build
cmake	-DCMAKE_INSTALL_PREFIX=%_prefix \
	-DCMAKE_INSTALL_RPATH=/usr/g++/lib:/usr/gnu/lib \
	..

make -j$CPUS

%install
rm -rf %buildroot

cd build
make install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"

%if %build_l10n
%else
rm -rf %buildroot%_datadir/locale
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/sakura
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/sakura.desktop
%dir %attr (-, root, other) %_datadir/doc
%_datadir/doc/sakura
%dir %attr (-, root, other) %_datadir/pixmaps
%_datadir/pixmaps/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/locale
%attr (-, root, other) %_datadir/locale/*
%endif


%changelog
* Thu Jan  7 2016 - Alex Viskovatoff <herzen@imap.cc>
- update to 3.1.5; build with gcc
* Sun Aug 30 2015 - Alex Viskovatoff <herzen@imap.cc>
- use pnm macro for cmake depedency
* Sat Aug 22 2015 - Alex Viskovatoff <herzen@imap.cc>
- Allow use of system cmake
* Sun Feb 16 2014 - Alex Viskovatoff
- Update to 2.4.2
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Tue Mar 15 2011 - Alex Viskovatoff
- Use SFEcmake
* Wed Dec  8 2010 - Alex Viskovatoff
- Initial spec
