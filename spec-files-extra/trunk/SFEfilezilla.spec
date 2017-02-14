#checking for wxWidgets version >= 3.0.2 (--unicode=yes --universal=no)... no (version 2.8.12 is not new enough)
#configure: error: 
#    The requested wxWidgets build couldn't be found.
#    
#    The configuration you asked for FileZilla requires a wxWidgets
#    build with the following settings:
#        --unicode=yes --universal=no
#    but such build is not available.
#
#    To see the wxWidgets builds available on this system, please use
#    'wx-config --list' command. To use the default build, returned by
#    'wx-config --selected-config', use the options with their 'auto'
#    default values.
#
#    If you still get this error, then check that 'wx-config' is
#    in path, the directory where wxWidgets libraries are installed
#    (returned by 'wx-config --libs' command) is in LD_LIBRARY_PATH
#    or equivalent variable and wxWidgets version is 3.0.2 or above.


#
# spec file for package SFEfilezilla
#
# includes module(s): filezilla
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc
%use filezilla = filezilla.spec

Name:               SFEfilezilla
IPS_package_name:   desktop/network/filezilla
Group:	            Desktop/Applications/File Managers
Summary:            FileZilla FTP client (FTP and SFTP)
Version:            %{filezilla.version}
SUNW_Copyright:     %{name}.copyright
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

#fresh filezilla requires -std=c++14 features
BuildRequires: SFEgcc-49
BuildRequires: SFEgccruntime-49
Requires: SFEgccruntime-49

Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnutls
Requires:      %{pnm_buildrequires_SUNWgnu_idn}
Requires: SFEwxwidgets-gpp
Requires: SUNWxdg-utils
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnutls-devel
BuildRequires: %{pnm_buildrequires_SUNWgnu_idn}
BuildRequires: SFEwxwidgets-gpp-devel
BuildRequires: SUNWxdg-utils

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%filezilla.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=/usr/gcc/4.9/bin/gcc
export CXX=/usr/gcc/4.9/bin/g++
export CPP=/usr/gcc/4.9/bin/cpp
export CPPFLAGS="-I/usr/g++/include -I%{_includedir}/idn"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -fpermissive -L/usr/g++/lib -R/usr/g++/lib"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

export PATH=/usr/g++/bin:$PATH
%filezilla.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%filezilla.install -d %name-%version

#temporary until SFEgcc defaults to a -std=c++14 gcc compiler
RUNPATHFILEZILLA="/usr/gcc/4.9/lib:/usr/gcc/lib:/usr/g++/lib:/usr/lib"
/usr/bin/elfedit -e 'dyn:runpath '$RUNPATHFILEZILLA'' $RPM_BUILD_ROOT/%{_bindir}/filezilla

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%doc(bzip2) -d filezilla-%{filezilla.version} COPYING GPL.html NEWS AUTHORS README
%doc -d filezilla-%{filezilla.version} ChangeLog
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/filezilla
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Sun Nov 13 2016 - Thomas Wagner
- set Requires: SFEgccruntime-49 to workaround pkgtool flaw to now check buildtime-requires and fail is missing
* Sun Jan 17 2016 - Thomas Wagner
- bump to 3.14.1
- set BuildRequires to SFEgcc-4.9 and set CC/CXX/CPP for -std=c++14 compiler
- elfedit to find libstdc++.so.6.0.20 in /usr/gcc/4.9/lib
* Fri Oct 25 2013 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNEgnu_idn}, %include packagenamacros.inc
- requires -std=c++14 features, for transitioning requires SFEgcc-49 and SFEgccruntime-49, set CC CXX CPP variables to exact path
* Fri Jun 29 2012 - Thomas Wagner
- change (Build)Requires to SFEwxwidgets-gpp(-devel) (g++)
- adapt to new usr-g++.inc -> CPPFLAGS change g++ include location,
  CXXFLAGS add -L|-R/usr/g++/lib, LDFLAGS use -L|-R/usr/g++/lib
- add IPS_Package_Name and Group:
* Sat Apr 28 2012 - Thomas Wagner
- remove double %% from %use
* Aug 2009 - Gilles Dauphin
- back to libCstd, wx was compiled with it
* Aug 2009 - Gilles Dauphin
- use stlport4
* Thu Nov 13 2008 - alfred.peng@sun.com
- Depends on SUNWwxwigets and SUNWwxwigets-devel instead.
  Update the group bit.
* Sat Sep 27 2008 - alfred.peng@sun.com
- Add %doc to %files for copyright.
* Fri Aug 29 2008 - alfred.peng@sun.com
- Update %files to include icons.
* Thu Mar 06 2008 - nonsea@users.sourceforge.net
- Update %files cause version upgrade.
- Add pkg -l10n
- Repleace Requires/BuildRequires from SFElibidn to SUNWgnu-idn
* Mon Aug 06 2007 - nonsea@users.sourceforge.net
- initial version created
