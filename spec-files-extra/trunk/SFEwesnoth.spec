#
# spec file for package SFEwesnoth.spec
#
%include Solaris.inc

# For binary packages on wesnoth.org
#%define _basedir /opt/games

%define wesnoth_datadir %{_datadir}/wesnoth

# Relative path on prefix 
%define pythonlibdir lib/python2.6/site-packages/wesnoth
%define abs_pythonlibdir %{_basedir}/%{pythonlibdir}

%define src_version 1.10.5

#
# Wesnoth 1.10.5 builds with CMake/GCC 4.6.2 with minimal patches. - Ken Mays
#

Name:                    	SFEwesnoth
IPS_Package_Name:	games/wesnoth
Summary:                 	Battle for Wesnoth is a fantasy turn-based strategy game
Version:                 	1.10.5
License:			GPLv2
URL:				http://www.wesnoth.org
Meta(info.upstream):            David White
Meta(info.repository_url):      http://svn.gna.org/svn/wesnoth 
Meta(pkg.detailed_url):         http://www.wesnoth.org
Meta(info.maintainer):		Petr Sobotka sobotkap@gmail.com
SUNW_BaseDir:			%{_basedir}
SUNW_Copyright:			wesnoth.copyright
Source:                  	%{sf_download}/wesnoth/wesnoth-%{src_version}.tar.bz2

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires:		SFEsdl-mixer-devel
BuildRequires:		SFEsdl-ttf-devel
BuildRequires:		SFEsdl-net-devel
BuildRequires:		SFEsdl-image-devel
BuildRequires:		SFEcmake
BuildRequires:          SUNWgnome-common-devel
BuildRequires:          SUNWgnu-gettext
Requires:	        SFEsdl-mixer
Requires:	        SFEsdl-ttf
Requires:	        SFEsdl-net
Requires:	        SFEsdl-image
Requires:   	        SFEboost
Requires:	        SUNWPython26

%prep
%setup -q -n wesnoth-%{src_version}
# Setup G++ for Solaris
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
mkdir build

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export MSGFMT=/usr/gnu/bin/msgfmt
cd build
cmake ..
gmake -j $CPUS


%install
rm -rf %{buildroot}

cd build
gmake install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"


%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/wesnoth
%{_mandir}
%{wesnoth_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{abs_pythonlibdir}
%{abs_pythonlibdir}/*

%changelog
* Tue Dec 11 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 1.10.5, converted to cmake/GCC4 build
* Mon Feb 21 2011 - Milan Jurik
- fix packaging
* Sat Sep 12 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to version 1.6.5
* Fri Aug 07 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to version 1.6.4
* Sat Apr 18 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to 1.6.1 (merged from SFEwesnoth-dev)
* Sat Mar 14 2009 - Milan Jurik
- Bump to 1.4.7
* Sun Oct 12 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.5
* Mon Jul 28 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.4
* Sun Jun 22 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.3 version
* Wed May 07 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.4.2 version
* Mon Mar 10 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.4 stable version.
- Changed preferences dir to ~/.wesnoth from ~/.wesnoth-dev which will 
	be used for development releases in future.
* Sun Feb 24 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.19 (last rc release before 1.4)
* Tue Feb 19 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.18
* Thu Feb 14 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.16
* Tue Jan 29 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.15
* Wed Jan 16 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.14
* Sat Jan 05 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Removed --enable-dummy-locales option from configure as it cause warning 
* Tue Jan 01 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.13
- Introduced new dependency SFEboost
- Changed compiler from gcc to sun studio + stlport4 (need to be same as for boost)
* Sat Dec 01 2007 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.12
* Mon Nov 19 2007 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.11
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Nov 11 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.10
* Fri Oct 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.9
- add html documentation
* Wed Sep 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.8
* Thu Sep 6 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
