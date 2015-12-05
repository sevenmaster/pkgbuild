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
%include	default-depend.inc

BuildRequires:	SFEqt

%prep
%setup -q -n %srcname

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
cp bin/%srcname %buildroot%_bindir

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/%srcname

%changelog
* Fri Dec  5 2015 - Alex Viskovatoff <viskov@imap.cc>
- Initial spec
