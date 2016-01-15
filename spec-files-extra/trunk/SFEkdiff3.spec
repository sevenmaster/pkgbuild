#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                SFEkdiff3
IPS_package_name:    text/kdiff3
Group:		     Applications/System Utilities
URL:		     http://kdiff3.sourceforge.net/
Summary:             Qt based diff - compares or merges 2 or 3 files or directories
Version:             0.9.98
Source:              %{sf_download}/kdiff3/kdiff3-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc

Requires: SFEqt-gpp
BuildRequires: SFEqt-gpp-devel

%prep
%setup -q -n kdiff3-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

cd src-QT4

gsed -i -e 's|/usr/local/|/usr/|g' kdiff3.pro

/usr/g++/bin/qmake kdiff3.pro -o Makefile.qt
make -f Makefile.qt

%install
rm -rf $RPM_BUILD_ROOT

cd src-QT4
make -f Makefile.qt install INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kdiff3
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Fri Jan 15 2016 - Alex Viskovatoff <herzen@imap.cc>
- Update to 0.9.98; use new directory layout
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Fri Dec 07 2006 - Eric Boutilier
- Initial spec
