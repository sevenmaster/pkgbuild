#
# spec file for package SFEatlas
#
# includes module(s): atlas
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define srcname atlas
%define builddirname ATLAS-bin
%define lapack_version 3.4.2

%if %{opt_arch64}
%define bitwidth 64
%else
%define bitwidth 32
%endif

Name:					atlas
Version:                3.10.0
Source:		         	%{sf_download}/project/math-atlas/Stable/%{version}/%{srcname}%{version}.tar.bz2
Source1:                http://www.netlib.org/lapack/lapack-%{lapack_version}.tgz

%define libdir %{_libdir}/atlas

%prep
%setup -q -c -n %{srcname}-%{version}
cp %SOURCE1 .


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

mkdir %{builddirname}
cd %{builddirname}

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
#export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

../ATLAS/configure --prefix=%{_prefix} \
                   --incdir=%{_includedir} \
                   --libdir=%{libdir} \
                   --with-netlib-lapack-tarfile=../lapack-%{lapack_version}.tgz \
                   -b %{bitwidth} --shared

# Don't use a top level parallel build. Atlas will invoke a parallel
# build for portions as appropriate
make


%install
cd %{builddirname}
make install DESTDIR=$RPM_BUILD_ROOT \
             INCINSTdir=$RPM_BUILD_ROOT%{_includedir} \
             LIBINSTdir=$RPM_BUILD_ROOT%{_libdir}/atlas

# Move CBLAS/CLAPACK headers to include/atlas
mv $RPM_BUILD_ROOT%{_includedir}/cblas.h $RPM_BUILD_ROOT%{_includedir}/atlas/cblas.h
mv $RPM_BUILD_ROOT%{_includedir}/clapack.h $RPM_BUILD_ROOT%{_includedir}/atlas/cblapack.h


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Nov 15 2012 - Aurélien Larcher <aurelien.larcher@gmail.com>
- Add support for 32/64 build and move cblas.h, clapack.h to include/atlas to avoid conflict.
* Mon Oct 29 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 3.10.0, include lapack at build time only and add shared libraries.
* Fri Apr 13 2012 - Logan Bruns <logan@gedanken.org>
- Force 32 bit build to match lapack sfe build.
* Thu Apr 12 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
