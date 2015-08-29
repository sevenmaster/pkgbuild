#
# spec file for package SFElibmatroska
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _prefix %_basedir/g++
%define srcname libmatroska

Name:		SFElibmatroska-gpp
IPS_package_name: library/video/g++/libmatroska
License:	LGPL
Summary:	Matroska Video Container
Group:		System Environment/Libraries
URL:		http://www.matroska.org
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.4.2
Source:		http://dl.matroska.org/downloads/%srcname/%srcname-%version.tar.bz2

SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

BuildRequires:	SFElibebml-gpp-devel
Requires:	SFElibebml-gpp

%description
Matroska aims to become THE Standard of Multimedia Container Formats.
It was derived from a project called MCF, but differentiates from it
significantly because it is based on  EBML (Extensible Binary Meta
Language), a binary derivative of XML. EBML enables the Matroska
Development Team to gain significant advantages in terms of future
format extensibility, without breaking file support in old parsers.
These libraries are used by mkvtoolnix.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CXXFLAGS="%cxx_optflags -I%/usr/g++/include"
export ACLOCAL_FLAGS="-I/usr/share/aclocal -I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig

./configure --prefix=%_prefix
make -j$CPUS

%install

rm -rf %buildroot
make install DESTDIR=%buildroot
rm %buildroot%_libdir/%srcname.*a

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_libdir/%srcname.so*

%files devel
%defattr (-, root, bin)
%_includedir
%dir %attr (-, root, other) %_pkg_config_path
%_pkg_config_path/%srcname.pc

%changelog
* Thu Aug 27 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 1.4.2 (the build system is more conventional now)
* Sun Feb  9 2014 - Alex Viskovatoff
- update to 1.4.1
* Sun Aug 05 2012 - Milan Jurik
- bump to 1.3.0
* Sun Jun 17 2012 - Thomas Wagner
- fix (Build)Requires on SFElibebml-gpp(-devel)
* Fri Dec  2 2011 - Thomas Wagner
- Add IPS package name
- copy SFElibmatroska.spec to SFElibmatroska-gpp.spec
- move to gcc/g++ and relocate to prefix /usr/g++
- add (Build)Requires on SFElibebml-gpp
- remove (Build)Requires on SUNWstdcxx 
* Sat Feb  5 2011 - Alex Viskovatoff
- Bump to 1.1.0
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4
* Tue Nov 23 2010 - Alex Viskovatoff
- Use stdcxx.inc instead of -library=stdcxx4; install in /usr/stdcxx
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12.2)
- Patch linux Makefile so that it works with Linux and Solaris
  instead of creating a new Makefile for Solaris.
* Mar 2010  - Gilles Dauphin
- look at install dir. Example search for /usr/SFE/include
- idem for _libdir
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
