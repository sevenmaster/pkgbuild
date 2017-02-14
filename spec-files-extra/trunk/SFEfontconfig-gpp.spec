#
# spec file for package SFEfontconfig-gpp
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc
%define srcname fontconfig

#we don't want OS's gcc runtime as a dependency listed!
%define _use_internal_dependency_generator 0


Name:		SFEfontconfig-gpp
IPS_Package_Name: system/library/g++/fontconfig
Summary:	Library for configuring and customizing font access
URL:		http://www.freedesktop.org/wiki/Software/fontconfig/
License:	GPLv2
SUNW_Copyright:	GPLv2.copyright
Group:		System/Libraries
Version:	2.12.1
Source:		http://www.freedesktop.org/software/%srcname/release/%srcname-%version.tar.bz2
%include	default-depend.inc

BuildRequires:	SFEgcc-runtime
Requires:	SFEgcc

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix --sysconfdir=%_std_sysconfdir --disable-static

gmake -j$CPUS

%install
rm -rf %buildroot
gmake install DESTDIR=%buildroot
rm -r %buildroot%_std_sysconfdir %buildroot%_libdir/*.la

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/fc-*
%dir %attr (0755, root, bin) %dir %_libdir
%_libdir/lib%srcname.so*
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*
%dir %attr (0755, root, bin) %dir %_includedir
%_includedir/*
%dir %attr (0755, root, sys) %_prefix/var
%_prefix/var/cache/fontconfig
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_docdir
%_docdir/%srcname
%_datadir/%srcname
%_mandir
%_datadir/xml

%changelog
* Thu Jan  6 2016 - Thomas Wagner
- bump to 2.12.1 - get new symbols  FcWeightFromOpenType FcWeightToOpenType  
- disable _use_internal_dependency_generator 0 - we don't want OS's gcc runtime listed as a dependency
* Tue Dec 29 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
