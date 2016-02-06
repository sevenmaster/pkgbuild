#
# spec file for package SFExplore
#

%include Solaris.inc
%define srcname xplore

Name:		SFExplore
IPS_Package_Name:	motif/file-manager/xplore
Summary:	A configurable Motif file manager with an Explorer-like user interface
Group:		Desktop (GNOME)/File Managers
Version:	1.2
URL:		http://www.musikwissenschaft.uni-mainz.de/~ag/xplore/xplore.php
Source:		http://www.musikwissenschaft.uni-mainz.de/~ag/xplore/%srcname-%{version}a.tar.bz2

BuildRequires:	library/motif

%prep
%setup -q -n %srcname-%{version}a

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
xmkmf -a
make

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/xplore*
%_libdir
