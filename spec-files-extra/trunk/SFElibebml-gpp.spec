#
# spec file for package SFElibebml
#

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%define srcname libebml

Name:		SFElibebml-gpp
IPS_package_name: library/g++/libebml
License:	LGPL
Summary:	Extensible Binary Meta Language
Group:		System Environment/Libraries
URL:		http://ebml.sourceforge.net
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.3.1
Source:		http://dl.matroska.org/downloads/%srcname/%srcname-%version.tar.bz2
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWgnu_coreutils}
BuildRequires:	SUNWloc

BuildRequires:	SFEgcc
# Specifying runtime dependencies is deprecated: pkgdepend finds them
#Requires:	SFEgccruntime

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
export CFLAGS="%_optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT=/usr/bin/msgfmt

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
- update to 1.3.1 (the build system is more conventional now)
* Fri Aug 14 2015 - Thomas Wagner
- set normal CFLAGS, LDFLAGS
##TODO## revisit AR=CC
- AR=/usr/gnu/bin/ar in case cc_is_gcc is true
* Sun May 17 2015 - Thomas Wagner
- rework patch libebml-01-makefile.diff
* Sun Feb  9 2014 - Alex Viskovatoff
- update to 1.3.0; restore correct IPS package name
* Thu Jul 11 2013 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWgnu_coreutils}, %include packagenamemacros.inc
- %include usr-g++.inc
* Sun Jul 24 2012 - Thomas Wagner
- change IPS_package_name: library/g++/ebml
* Sun Jul 29 2012 - Milan Jurik
- bump to 1.2.2
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- Accept either SFEcoreutils or SUNWgnu-coreutils for buildrequires.
* Fri Dec  2 2011 - Thomas Wagner 
- Add IPS package name
- fork SFElibebml.spec to SFElibebml-gpp.spec
- move to gcc/g++ and relocate to prefix /usr/g++
* Sat Feb  5 2011 - Alex Viskovatoff
- Update to 1.2.0, adding one patch
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4
* Tue Nov 23 2010 - Alex Viskovatoff
- Use stdcxx.inc instead of -library=stdcxx4; install in /usr/stdcxx
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12u1)
- Patch linux Makefile so that it works with Linux and Solaris
  instead of creating a new Makefile for Solaris.
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
