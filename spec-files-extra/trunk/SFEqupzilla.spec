#
# spec file for package SFEqupzilla
#
# includes module: qupzilla
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname qupzilla
%define _pkg_docdir %_docdir/%srcname

Name:		SFEqupzilla
IPS_Package_Name: web/browser/qupzilla
Summary:	Lightweight multiplatform QtWebKit browser
URL:		http://www.qupzilla.com/
License:	GPLv3
SUNW_Copyright:	%srcname.copyright
Group:		Applications/Internet
Version:	1.4.4
Source:		http://github.com/QupZilla/%srcname/archive/v%version.tar.gz
Patch0:		qupzilla-01-d_type.patch
SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires:	SFEqt-gpp
Requires:	SFEqt-gpp

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version
%patch0 -p 1

# enable webgl support
export USE_WEBGL=true
# build with debugging symbols
echo "\nCONFIG += debug" >> src/defines.pri
/usr/g++/bin/qmake


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/g++/include -I/usr/g++/include/qt"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads"
export LDFLAGS="%_ldflags -pthreads -L/usr/g++/lib -R/usr/g++/lib"

make -j$CPUS


%install
rm -rf %buildroot

make INSTALL_ROOT=%buildroot install

%if %build_l10n
%else
rm -r %buildroot%_datadir/%srcname/locale
%endif


%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%doc AUTHORS CHANGELOG README.md
%_bindir/%srcname
%_libdir/libQupZilla.so*
%_libdir/%srcname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/%srcname.desktop
%_datadir/bash-completion
%defattr (-, root, other)
%_datadir/icons
%_datadir/pixmaps
%_datadir/%srcname/themes

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/%srcname/locale
%endif


%changelog
* Thu Oct 31 2013 - Alex Viskovatoff <herzen@imapmail.org>
- add copyright file
* Sun Oct 27 2013 - Alex Viskovatoff <herzen@imapmail.org>
- initial spec
