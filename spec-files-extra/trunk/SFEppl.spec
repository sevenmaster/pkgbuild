#
# spec file for package SFEppl
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-gnu.inc

%define cc_is_gcc 1
%include base.inc

%define src_name   ppl

Name:                SFEppl
IPS_Package_Name:    library/ppl
Summary:             PPL - Parma Polyhedra Library
Version:             0.12.1
URL:                 http://www.cs.unipr.it/ppl/
Source:              http://bugseng.com/products/ppl/download/ftp/releases/%{version}/ppl-%{version}.tar.bz2
Patch1:        	     ppl-01-numeric_limits.diff
License:      	     GPL
SUNW_Copyright:      SFEppl.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:       SFEgcc
Requires:            SFEgccruntime
BuildRequires:       SFEgmp-gpp-devel
Requires:            SFEgmp-gpp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description
This is the release 0.11 of the Parma Polyhedra Library:
a C++ library for (not necessarily closed) convex polyhedra
and other numerical abstractions.

To be more precise, the Parma Polyhedra Library (PPL) can handle:

  + all the convex polyhedra that can be defined as the intersection
    of a finite number of (open or closed) hyperspaces, each described
    by an equality or a (strict or non-strict) inequality with rational
    coefficients;

  + convex polyhedra defined by systems of bounded differences with
    a wide choice of integer, rational or floating point coefficients;

  + all grids (or, equivalently, lattices); a grid is defined by a set
    of congruence relations with rational coefficients and consists of
    the set of all points that satisfy these relations;

  + finite powersets of the above;

  + linear programming problems, solved with an implementation of the
    primal simplex algorithm using exact arithmetic.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/lib/pkgconfig

./configure --prefix=%{_prefix} \
            --with-gmp-prefix=/usr/g++

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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Thu Mar  7 2013 - Logan Bruns <logan@gedanken.org>
- initial version
