#
# spec file for package SFEtransmission
#

################################################################################
#				  Note on GTK+                                 #
#                                                                              #
#  Version 2.33 is the last Transmission version that uses GTK+ 2 and not      #
#  GTK+ 3.  This means that there is no point in "bumping" this package to a   #
#  newer version until GTK+ 3 is built on Solaris.                             #
################################################################################

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include usr-gnu.inc
%define source_name transmission

Name:			SFEtransmission
IPS_package_name:	sfe/desktop/torrent/transmission
Summary:		GTK and console BitTorrent client
Version:		2.33
Source:			http://download.m0k.org/transmission/files/transmission-%version.tar.bz2
License:		MIT
URL:			http://transmission.m0k.org/
SUNW_Copyright:		transmission.copyright
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%source_name-%version-build
%include default-depend.inc
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWdbus-glib-devel
BuildRequires: SFElibevent2
Requires: SUNWgtk2
Requires: SUNWgnome-panel
Requires: SUNWdbus-glib
Requires: SUNWopenssl-libraries
Requires: SUNWcurl
Requires: SFElibevent2
Requires: SFElibiconv
Requires: SUNWgnu-gettext


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -n %{source_name}-%{version}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
#export CFLAGS="%optflags -mt -D__inline=inline -xc99"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
#export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
#export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
export CFLAGS="$CFLAGS -I/usr/gnu/include"
export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -liconv"
export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig

./configure --prefix=%{_prefix}   \
            --datadir=%{_datadir} \
	    --mandir=%{_mandir}   \
	    --disable-wx	\
            --program-prefix=""

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_mandir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/transmission
%{_datadir}/transmission/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/transmission.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/transmission.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/transmission.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/transmission.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/transmission.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256/apps
%{_datadir}/icons/hicolor/256x256/apps/transmission.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/transmission.svg

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
# Do not set the group attribute correctly, so as not to conflict with system packages (e.g., gnu-binutils)
#%attr (-, root, other) %{_datadir}/locale
%{_datadir}/locale
%endif

%changelog
* Fri Sep 13 2013 - Alex Viskovatoff
- bring down to 2.33, so that the GUI builds
* Sat Dec 8 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 2.73; GTK client needs gtk+ >= 3.4.0
* Sun Aug  7 2011 - Alex Viskovatoff
- install in /usr/gnu, to avoid conflict with system package
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Tue Jun 14 2011 - Alex Viskovatoff
- go back to 2.22, since 2.31 has issues with seeding
* Wed Jun  1 2011 - Alex Viskovatoff
- bump to 2.31; use gcc because build fails with Sun Studio
* Fri Mar 18 2011 - Alex Viskovatoff
- Reintroduce and update to 2.22
* Fri May 22 2009 - elaine.xiong@sun.com
- Bump to 1.61. Remove upstream patches.
* Wed Jun 25 2008 - darren.kenny@sun.com
- Bump to 1.2.2 and remove upstream patch for compiler. Add patch for solaris
  getgateway implementation.
* Tue May 27 2008 - trisk@acm.jhu.edu
- Add SUNWcurl dependency
* Sat May 24 2008 - trisk@acm.jhu.edu
- Bump to 1.21, drop patch2
* Sun Mar 02 2008 - trisk@acm.jhu.edu
- Bump to 1.06, add patch2 (fixed upstream)
* Tue Feb 26 2008 - markwright@internode.on.net
- Bump to 1.05, bump patch1, add icons.
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Enable building on Indiana systems.
* Thu Nov 01 2007 - trisk@acm.jhu.edu
- Bump to 0.91, replace patch1
* Mon Sep 10 2007 - trisk@acm.jhu.edu
- Bump to 0.82
* Thu Sep 6 2007 - Petr Sobotka sobotkap@centum.cz
- Fix typo in changelog
* Wed Aug 29 2007 - trisk@acm.jhu.edu
- Bump to 0.81, add workaround for broken tarball
* Mon Aug 20 2007 - trisk@acm.jhu.edu
- Clean up, allow building with Studio
* Sun Aug 19 2007 - Petr Sobotka sobotkap@centrum.cz
- Initial spec
