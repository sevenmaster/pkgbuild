#
# spec file for package SFEcloog
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-gnu.inc

%define src_name   cloog

Name:                SFEcloog
IPS_Package_Name:    sfe/library/cloog
Summary:             CLooG - The Chunky Loop Generator
Version:             0.18.0
URL:                 http://www.cloog.org
Source:              ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{version}.tar.gz
License:      	     LGPL
SUNW_Copyright:      SFEcloog.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgmp-devel
Requires: SFEgmp
BuildRequires: SFEisl-devel
Requires: SFEisl

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description
CLooG is a software which generates loops for scanning Z-polyhedra. That is,
CLooG finds the code or pseudo-code where each integral point of one or more
parametrized polyhedron or parametrized polyhedra union is reached. CLooG is
designed to avoid control overhead and to produce a very efficient code.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix} \
            --with-gmp=system \
            --with-isl=system

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Feb 21 2013 - Logan Bruns <logan@gedanken.org>
- initial version
