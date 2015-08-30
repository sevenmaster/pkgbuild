#
# spec file for package SFEsakura
#

%include Solaris.inc
%define srcname sakura
%include packagenamemacros.inc

Name:		SFEsakura
IPS_Package_Name:	terminal/sakura
Summary:	Lightweight terminal emulator based on GTK and VTE
Group:		Applications/System Utilities
URL:		http://www.pleyades.net/david/projects/sakura
# This is the last release that doesn't depend on gtk-3
Version:	2.4.2
License:	GPLv2
Source:		http://launchpad.net/%srcname/trunk/%version/+download/%srcname-%version.tar.bz2
%include default-depend.inc
SUNW_Copyright: sakura.copyright
SUNW_BaseDir:	%_basedir
BuildRequires:	%pnm_buildrequires_developer_build_cmake
BuildRequires:	SUNWgtk2-devel
Requires:	SUNWgtk2
BuildRequires:	SUNWgnome-terminal
Requires:	SUNWgnome-terminal
#BuildRequires:	library/ncurses   # Apparently not needed

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

cd build
cmake -DCMAKE_INSTALL_PREFIX=%_prefix ..

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
* Sun Aug 30 2015 - Alex Viskovatoff <hezen@imap.cc>
- use pnm macro for cmake depedency
* Sat Aug 22 2015 - Alex Viskovatoff <hezen@imap.cc>
- Allow use of system cmake
* Sun Feb 16 2014 - Alex Viskovatoff
- Update to 2.4.2
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Tue Mar 15 2011 - Alex Viskovatoff
- Use SFEcmake
* Wed Dec  8 2010 - Alex Viskovatoff
- Initial spec
