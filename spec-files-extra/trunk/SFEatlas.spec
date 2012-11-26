#
# spec file for package SFEatlas
#
# includes module(s): atlas
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%use atlas_64 = atlas.spec
%endif

%include base.inc
%use atlas = atlas.spec

Name:                   SFEatlas
IPS_Package_Name:	math/atlas
Summary:                ATLAS - Automatically Tuned Linear Algebra Software
Group:                  Utility
Version:                %{atlas.version}
URL:		        http://math-atlas.sourceforge.net
License: 		BSD
SUNW_Copyright: 	%{name}.copyright
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%define builddir	%{name}-%{version}
%include default-depend.inc

BuildRequires: SFEgcc
Requires: SFEgccruntime


%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

%prep
rm -rf %{builddir}
%ifarch amd64 sparcv9
mkdir -p %{builddir}/%_arch64
%atlas_64.prep -d %{builddir}/%_arch64
%endif

mkdir -p %{builddir}/%base_arch
%atlas.prep -d %{builddir}/%base_arch

%build
%ifarch amd64 sparcv9
%atlas_64.build -d %{builddir}/%_arch64
%endif

%atlas.build -d %{builddir}/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%atlas_64.install -d %{builddir}/%_arch64
%endif

%atlas.install -d %{builddir}/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/atlas
%{_includedir}/atlas/*
%dir %attr (0755, root, bin) %{_libdir}/atlas
%{_libdir}/atlas/*.so
%{_libdir}/atlas/*.a
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/atlas
%{_libdir}/%{_arch64}/atlas/*.so
%{_libdir}/%{_arch64}/atlas/*.a
%endif

%changelog
* Thu Nov 15 2012 - Aurélien Larcher <aurelien.larcher@gmail.com>
- Add support for 32/64 build and move cblas.h, clapack.h to include/atlas to avoid conflict.
* Mon Oct 29 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 3.10.0, include lapack at build time only and add shared libraries.
* Fri Apr 13 2012 - Logan Bruns <logan@gedanken.org>
- Force 32 bit build to match lapack sfe build.
* Thu Apr 12 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
