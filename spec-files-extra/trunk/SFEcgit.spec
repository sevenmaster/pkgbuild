#
# spec file for package SFEcgit
#
%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%define sname cgit

Name:		SFEcgit
IPS_Package_Name:	web/cgit
Version:	1.1
Summary:	A web interface for git written in plain C
Source:		https://git.zx2c4.com/%{sname}/snapshot/%{sname}-%{version}.tar.xz
Patch1:		cgit-timegm.patch
URL:		https://git.zx2c4.com/cgit/
Group:		System/Services
License:	GPLv2
SUNW_Copyright:	%{license}.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p1

gsed -i -e 's/\/usr\/local/\/usr/g' -e 's/\/var\/www\/htdocs/\/usr\/share/g' Makefile
gsed -i -e 's/\/bin\/sh/\/bin\/bash/g' gen-version.sh

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++

make get-git

gsed -i -e 's/CC\ \=\ cc/CC\ \=\ gcc/g' git/Makefile
gsed -i -e '/\/usr\/ucb\/install/d' git/config.mak.uname

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %{_libdir}/cgit/filters
%{_libdir}/cgit/filters/*
%dir %attr (0755, root, sys) /usr/share
%dir /usr/share/cgit
/usr/share/cgit/*

%changelog
* Mon May 01 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial version 1.1
