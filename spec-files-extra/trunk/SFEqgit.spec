#
# spec file for package SFEqgit
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname qgit

Name:		SFEqgit
IPS_Package_Name: developer/versioning/qgit
Summary:	Git GUI viewer based on Qt4
URL:		http://sourceforge.net/projects/qgit/
License:	GPLv2
SUNW_Copyright:	GPLv2.copyright
Group:		Development/Source Code Management
Version:	2.3
Source:		%sf_download/%srcname/%srcname-%version.tar.bz2
# The following two files were obtained from the ABS tree
# http://wiki.archlinux.org/index.php/Arch_Build_System
Source1:	qgit.desktop
Source2:	qgit.png
Patch1:		qgit-01-git_config.patch
%include	default-depend.inc

BuildRequires:	SFEqt-gpp
Requires:	developer/versioning/git

%prep
%setup -q -n %srcname
%patch1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads"
export LDFLAGS="%_ldflags -pthreads"

/usr/g++/bin/qmake
make -j$CPUS

%install
rm -rf %buildroot
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_datadir/applications
mkdir %buildroot%_datadir/pixmaps
cp bin/%srcname %buildroot%_bindir
cp %SOURCE1 %buildroot%_datadir/applications
cp %SOURCE2 %buildroot%_datadir/pixmaps

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
* Fri Dec  5 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
