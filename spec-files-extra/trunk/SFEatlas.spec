#
# spec file for package SFEatlas
#
# includes module(s): atlas
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define srcname atlas

Name:                    SFEatlas
IPS_Package_Name:	 math/atlas
Summary:                 ATLAS - Automatically Tuned Linear Algebra Software
Group:                   Utility
Version:                 3.8.4
URL:		         http://math-atlas.sourceforge.net
Source:		         %{sf_download}/project/math-atlas/Stable/%{version}/%{srcname}%{version}.tar.bz2
License: 		 BSD
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: library/lapack

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

%prep
rm -rf %name-%version
%setup -q -c -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

mkdir atlas
cd atlas

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
../ATLAS/configure --prefix=%{_prefix}			\
                   --incdir=%{_includedir}              \
                   --libdir=%{_libdir}/atlas            \
                   --with-netlib-lapack=/usr/lib/liblapack.a 

# Don't use a top level parallel build. Atlas will invoke a parallel
# build for portions as appropriate
make

%install
cd atlas
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT \
             INCINSTdir=$RPM_BUILD_ROOT/usr/include \
             LIBINSTdir=$RPM_BUILD_ROOT/usr/lib/atlas

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}/cblas.h
%{_includedir}/clapack.h
%dir %attr (0755, root, bin) %{_includedir}/atlas
%{_includedir}/atlas/*
%dir %attr (0755, root, bin) %{_libdir}/atlas
%{_libdir}/atlas/*

%changelog
* Thu Apr 12 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
