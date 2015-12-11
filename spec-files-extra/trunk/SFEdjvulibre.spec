#
# spec file for package SFEdjvulibre
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _cxx_libdir /usr/g++/lib
%define srcname djvulibre

Name:		SFEdjvulibre
IPS_Package_Name:	library/desktop/djvulibre
Summary:	Open source implementation of DjVu
URL:		http://djvu.sourceforge.net
Vendor:		The original inventors of DjVu
License:	GPLv2+
Group:		Desktop (GNOME)/Libraries
SUNW_Copyright:	djvulibre.copyright
Version:	3.5.27
Source:		%sf_download/project/djvu/DjVuLibre/%version/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name


%prep
%setup -q -n %srcname-%version

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

# The developers of djvulibre recommend using gcc, so don't even try CC
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix --libdir=%_cxx_libdir

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_cxx_libdir/*.la

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/*
%dir /usr/g++
%dir %attr (0755, root, bin) %_cxx_libdir
%_cxx_libdir/lib*.so*
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, bin) %_datadir/man
%_mandir/man1
%defattr (-, root, other)
%_datadir/djvu
%_datadir/icons/hicolor
%dir %attr (-, root, root) %_datadir/mime
%dir %attr (-, root, root) %_datadir/mime/packages
%_datadir/mime/packages/djvulibre-mime.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %attr (0755, root, other) %_includedir/libdjvu
%_includedir/libdjvu/*
%dir %attr (0755, root, other) %_cxx_libdir/pkgconfig
%_cxx_libdir/pkgconfig/ddjvuapi.pc


%changelog
* Thu Dec 10 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 3.5.27
* Mon Aug 27 2012 - Milan Jurik
- bump to 3.5.25
* Sat Feb 04 2012 - Milan Jurik
- fix build with the latest GCC
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jun 12 2011 - Alex Viskovatoff
- Qt gcc libs are now in their own place
* Tue Apr 12 2011 - Alex Viskovatoff
- Bump to 3.5.24
* Tue Feb  8 2011 - Alex Viskovatoff
- Use /usr/stdcxx as basedir
* Mon Jan 31 2011 - Alex Viskovatoff
- Initial spec
