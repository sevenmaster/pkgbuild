#
# spec file for package SFEqupzilla
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
Version:	1.8.9
Source:		http://github.com/QupZilla/%srcname/releases/download/v%version/QupZilla-%version.tar.xz
Patch0:		qupzilla-01-d_type.patch
SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires:	SFEqt-gpp
# Let pkgdepend take care of runtime dependencies

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n QupZilla-%version
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
%_datadir/appdata/%srcname.appdata.xml

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/%srcname/locale
%endif


%changelog
* Sun Jan 31 2016 - Alex Viskovatoff <herzen@imap.cc>
- bump to 1.8.9
* Sat Feb  1 2014 - Alex Viskovatoff <herzen@imapmail.org>
- update to 1.6.1, deleting patch added in previous commit
* Tue Jan 14 2014 - Alex Viskovatoff <herzen@imapmail.org>
- update to 1.6.0, adding one patch
* Thu Oct 31 2013 - Alex Viskovatoff <herzen@imapmail.org>
- add copyright file
* Sun Oct 27 2013 - Alex Viskovatoff <herzen@imapmail.org>
- initial spec
