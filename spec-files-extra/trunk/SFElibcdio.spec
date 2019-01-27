#
# spec file for package SUNWlibcdio
#
# includes module(s): libcdio
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Currently, libcdio doesn't work well on Solaris SPARC 
# because of endianess differences. A bug has been filed for it 
# at http://bugzilla.gnome.org/show_bug.cgi?id=377280. Patch
# has been provided as an workaround (please note that this
# is not a final solution). To make libcdio work on Solaris SPARC
# we suggest you applying the patch above.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc


%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use libcdio = libcdio.spec

Name:		SFElibcdio
IPS_Package_Name:	library/audio/libcdio 
Summary:	GNU Compact Disc Input and Control Library
Group:		System/Libraries
License:	GPLv3
SUNW_Copyright:	libcdio.copyright
URL:		http://www.gnu.org/software/libcdio/
Version:	%{libcdio.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: %{pnm_requires_library_expat}
BuildRequires: %{pnm_buildrequires_SUNWlibC}
Requires: %{pnm_buildrequires_SUNWlibC}
BuildRequires: SUNWlibms
Requires: SUNWlibms
Requires:      %{pnm_requires_SUNWdbus}
Requires: SFElibcddb
BuildRequires: SFElibcddb
Requires: SFElibiconv

BuildRequires: %{pnm_buildrequires_SUNWncurses_devel}
Requires:      %{pnm_requires_SUNWncurses}

%if %with_hal
Requires: SUNWhal
%endif
BuildRequires:	%{pnm_buildrequires_library_expat}
BuildRequires:	%{pnm_buildrequires_SUNWdbus_devel}
BuildRequires:	%{pnm_buildrequires_SUNWgnome_common_devel}
BuildRequires:	SFElibcddb-devel
BuildRequires:	SFElibiconv-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libcdio.prep -d %name-%version

%build
export CC=gcc
export CXX=g++

export CFLAGS="%optflags -I/usr/gnu/include -I/usr/gnu/include/ncurses"
%if %with_hal
export CFLAGS="$CFLAGS -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include"
export LDFLAGS="%_ldflags -lhal -ldbus-1 -R/usr/gnu/lib -L/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags -R/usr/gnu/lib -L/usr/gnu/lib"
%endif

%libcdio.build -d %name-%version

%install
%libcdio.install -d %name-%version

#rm -rf $RPM_BUILD_ROOT%{_mandir}
#rm -rf $RPM_BUILD_ROOT%{_prefix}/share
#rm -rf $RPM_BUILD_ROOT%{_prefix}/info
rm -f $RPM_BUILD_ROOT%{_prefix}/share/info/dir

#%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
#%dir %attr (0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
#%dir %attr (0755, root, bin) %{_mandir}/jp
#%dir %attr (0755, root, bin) %{_mandir}/jp/man1
#%{_mandir}/jp/man1/*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/cdio

%changelog
* Thu Jan 24 2018 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWncurses_devel} (S11.4 S12)
* Mon Mar 26 2018 - Thomas Wagner
- bump to 2.0.0
* Wed Feb  1 2017 - Thomas Wagner
- bump to 0.92
- change to cc_is_gcc 1
- update patches libcdio-01-usehal.diff libcdio-02-stdint.diff
* Fri Oct 23 2015 - Thomas Wagner
- merge with pjama's changes
* Sat May 23 2013 - pjama
- more packagenamemacros to make hipster compatable
* Sun Oct 28 2013 - Thomas Wagner
- cleanup target dir in %install
* Fri Jul  5 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibC}, %{pnm_buildrequires_SUNWncurses_devel}, %include packagenamemacros.inc
* Thu Oct 06 2011 - Milan Jurik
- clean up, add IPS package name
* Thu Jul 21 2011 - Milan Jurik
- de-gcc spec, leave decision about compiler to environment
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Jul 10 2011 - Alex Viskovatoff
- Build with SFEgcc
* Sun Apr 11 2010 - Milan Jurik
- adding missing build dependency
* Thu Apr 08 2010 - Milan Jurik
- adding missing dependency and dbus-1.0 header files path
* Sat Aug 15 2009 - Thomas Wagner
- add (Build)Requires: SUNWgcc/SUNWgccruntime SUNWlibms/SUNWlibms
* Wed Mar 18 2009 - Thomas Wagner
- add os build conditional SUNWncurses/SFEncurses to re-enable build on old OS < snv_100
* Sat Nov 29 2008 - dauphin@enst.fr
- s/SFEncurses/SUNWncurses is available in build 101
* date unknow
- fix my error on mandir Gilles Dauphin
* Wed Oct 22 2008 - dick@nagual.nl
- s/SUNWncurses/SFEncurses since the SUNpkg is not available
* Tue Sep 02 2008 - halton.huo@sun.com
- s/SFEncurses/SUNWncurses since it goes into vermillion
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Add Requires/BuildRequires to SFEncurses and SFEncurses-devel
- Add -I/usr/gnu/include/ncurses in CFLAGS to fix build issue
- Move patches to libcdio.spec
* Fri Jul 11 2008 - andras.barna@gmail.com
- Add ACLOCAL_FLAGS, SFElibiconv dep, adjust ld+cflags
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- fix to manpath ownership
* Sat Jan 19 2008 - moinak.ghosh@sun.com
- Set g++ as cpp compiler
- Added back man and info files
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Changed reference to non-existent gcc_ldflags
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 0.79.  Add libcdio-02-stdint.diff.
* Thu Oct 18 2007 - laca@sun.com
- use gcc specific compiler/linker flags
* Mon Jun 23 - irene.huang@sun.com
- created.
