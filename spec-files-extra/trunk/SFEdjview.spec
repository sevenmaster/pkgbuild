#
# spec file for package SFEdjview
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define  _cxx_libdir /usr/g++/lib
%define srcname djview

Name:		SFEdjview
IPS_Package_Name:	desktop/djview
Summary:	DjVu file viewer
URL:		http://djvu.sourceforge
Group:		Applications/Office
Vendor:		Léon Bottou
License:	GPLv2+
SUNW_Copyright:	djview.copyright
Version:	4.10
Source:		%sf_download/project/djvu/DjView/%version/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt-gpp-devel
BuildRequires:	SFEdjvulibre-devel

Requires:	SFEgccruntime
Requires:	SFEqt-gpp
Requires:	SFEdjvulibre


%prep
%setup -q -n %srcname-%version
gsed -i -e 's/DjView4/DjView/' -e 's/djview4 %f/djview %f/' \
     desktopfiles/djvulibre-djview4.desktop

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -L%_cxx_libdir"
export LDFLAGS="%_ldflags -pthreads -L%_cxx_libdir -R%_cxx_libdir"
export QMAKE=/usr/g++/bin/qmake
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++
export PKG_CONFIG_PATH="%_cxx_libdir/pkgconfig"

./configure --prefix=%_prefix

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/djview
%dir %attr (-, root, sys) %_datadir
%_mandir
%_datadir/applications/djvulibre-djview4.desktop
%_libdir/mozilla/plugins
%defattr (-, root, other)
%_datadir/djvu
%_datadir/icons/hicolor

%changelog
* Thu Dec 10 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 4.10
* Mon Aug 27 2012 - Milan Jurik
- bump to 4.9
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jun 12 2011 - Alex Viskovatoff
- Qt gcc libs are now in their own place
* Tue Apr 12 2011 - Alex Viskovatoff
- Update to 4.7
* Tue Feb  8 2011 - Alex Viskovatoff
- Adapt to Qt gcc libs now being in /usr/stdcxx
* Mon Jan 31 2011 - Alex Viskovatoff
- Initial spec
