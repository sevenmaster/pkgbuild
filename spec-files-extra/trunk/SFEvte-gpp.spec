#
# spec file for package SFEvte-gpp
#

# There is never going to be a system vte, since vte comes with gnome-terminal,
# but use the g++ designation in the name of this package anyway.

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc
%define srcname vte

Name:		SFEvte-gpp
IPS_Package_Name: system/library/g++/vte
Summary:	Library providing a virtual terminal emulator widget
URL:		https://wiki.gnome.org/action/show/Apps/Terminal/VTE
License:	LGPLv2+
SUNW_Copyright:	GPLv2.copyright
Group:		System/Libraries
Version:	0.42.2
Source:		http://git.gnome.org/browse/%srcname/snapshot/%srcname-%version.tar.xz
%include	default-depend.inc
BuildRequires:	library/desktop/g++/gtk3
BuildRequires:	SFEgnutls
BuildRequires:	SFEzlib-pkgconfig
BuildRequires:	SFElibtool
BuildRequires:	SFEvala

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -R/usr/g++/lib -R/usr/gnu/lib"
export PKG_CONFIG_PATH="%_pkg_config_path:/usr/gnu/lib/pkgconfig"
export PATH=/usr/g++/bin:$PATH

./autogen.sh --disable-Bsymbolic
./configure --prefix=%_prefix --libexecdir=%_libdir \
	    --disable-Bsymbolic --disable-static

gmake -j$CPUS

%install
rm -rf %buildroot
gmake install DESTDIR=%buildroot
# Don't bother with locale data
rm -r %buildroot%_datadir
rm %Buildroot%_libdir/libvte2_90.la

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/vte2_90
%dir %attr (0755, root, bin) %dir %_libdir
%_libdir/libvte2_90.so*
%_libdir/gnome-pty-helper
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*
%dir %attr (0755, root, bin) %dir %_includedir
%_includedir/*
%dir %attr (0755, root, sys) %_prefix/etc
%attr (0755, root, other) %_prefix/etc/profile.d/vte.sh

%changelog
* Wed Jan  6 2016 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
