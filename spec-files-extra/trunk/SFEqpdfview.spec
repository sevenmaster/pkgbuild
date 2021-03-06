#
# spec file for package SFEqpdfview
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname qpdfview
%define _pkg_docdir %_docdir/%srcname

Name:		SFEqpdfview
IPS_Package_Name: desktop/pdf-viewer/qpdfview
Summary:	Tabbed document viewer using the poppler library and Qt
URL:		https://launchpad.net/qpdfview
License:	GPLv2
SUNW_Copyright:	GPLv2.copyright
Group:		Applications/Office
Version:	0.4.16
Source:		http://launchpad.net/%srcname/trunk/%version/+download/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires:	SFEqt-gpp-devel
Requires:	SFEqt-gpp
BuildRequires:	SFEpoppler-gpp-devel
Requires:	SFEpoppler-gpp
BuildRequires:	SFEdjvulibre-devel
Requires:	SFEdjvulibre
BuildRequires:	SFEfile
Requires:	SFEfile
# desktop/pdf-viewer/evince delivers libspectre, used for rendering PostScript
BuildRequires:	evince
Requires:	evince

%description
qpdfview uses Poppler for PDF support, libspectre for PS support, DjVuLibre
for DjVu support, CUPS for printing support and the Qt toolkit for its
interface.

Current features include:
● Outline, properties and thumbnail panes  ● Scale, rotate and fit
● Fullscreen and presentation views  ● Continuous and multiple-page layouts
● Search for text  ● Configurable tool bars  ● Configurable keyboard shortcuts
● Persistent per-file settings  ● SyncTeX support
● Rudimentary annotation support (with Poppler version 0.20.1 or higher)
● Rudimentary form support  ● Support for PostScript and DjVu documents


%prep
%setup -q -n %srcname-%version

# Not clear why qmake doesn't use QMAKE_LIBS_NETWORK from qmake.conf
echo '\nINCLUDEPATH += /usr/gnu/include\nLIBS += -L/usr/gnu/lib -R/usr/gnu/lib -lsocket' \
  >> application.pro

/usr/g++/bin/qmake qpdfview.pro


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig

make -j$CPUS


%install
rm -rf %buildroot

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
make INSTALL_ROOT=%buildroot install


%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%doc CONTRIBUTORS CHANGES README TODO
%_bindir/%srcname
%_libdir/%srcname/libqpdfview_*.so
%dir %attr (-, root, sys) %_datadir
%_mandir
%defattr (-, root, other)
%_datadir/applications/%srcname.desktop
%_datadir/icons
%_datadir/%srcname
%_datadir/appdata/qpdfview.appdata.xml


%changelog
* Tue Jan  5 2016 - Alex Viskovatoff <herzen@imap.cc>
- update to 0.4.16
* Tue Jan 14 2014 - Alex Viskovatoff <herzen@imap.cc>
- bump to 0.4.7
* Thu Oct 31 2013 - Alex Viskovatoff <herzen@imap.cc>
- initial spec
