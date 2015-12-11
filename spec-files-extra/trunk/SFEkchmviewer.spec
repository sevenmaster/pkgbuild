#
# spec file for package SFEkchmviewer
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname kchmviewer

Name:		SFEkchmviewer
IPS_package_name: desktop/kchmviewer
Summary:	CHM help file viewer based on Qt
URL:		http://www.ulduzsoft.com/linux/kchmviewer/
Group:		Applications/Office
Vendor:		George Yunaev
Version:	7.5
License:	GPLv3+
SUNW_Copyright:	kchmviewer.copyright
Source:		http://downloads.sourceforge.net/%srcname/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires: SFEqt-gpp-devel
BuildRequires: SFEchmlib
BuildRequires: SFElibzip

Requires: SFEqt-gpp
Requires: SFEchmlib
Requires: SUNWzlib


%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

echo "INCLUDEPATH += /usr/lib/libzip/include" >> lib/libebook/libebook.pro
gsed -i 's/linux-g++\*:/solaris-g++\*:/' src/src.pro
export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++
qmake
# Parallelism breaks with 16 cpus, so don't use more than 4
gmake -j$(test $CPUS -ge 4 && echo 4 || echo $CPUS) PREFIX=%_basedir

%install
rm -rf %buildroot

ginstall -d %buildroot%_bindir \
	    %buildroot%_datadir/applications %buildroot%_datadir/pixmaps
ginstall -t %buildroot%_bindir bin/%srcname
ginstall -t %buildroot%_datadir/applications packages/%srcname.desktop
ginstall -t %buildroot%_datadir/pixmaps packages/%srcname.png

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (0755, root, sys) %_datadir
%defattr (-, root, other)
%_datadir/applications/%srcname.desktop
%_datadir/pixmaps/%srcname.png


%changelog
* Fri Dec 11 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 7.5 (now reads epubs)
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Wed Apr 13 2011 - Alex Viskovatoff
- Use only 2 cpus: using 16 cpus breaks build
* Sat Mar 12 2011 - Alex Viskovatoff
- Place /usr/stdcxx/bin at front of PATH
* Fri Jan 28 2011 - Alex Viskovatoff
- Accommodate to Qt being in /usr/stdcxx
* Mon Jan 24 2011 - Alex Viskovatoff
- Define QMAKESPEC
* Sat Dec 11 2010 - Alex Viskovatoff
- Initial spec
