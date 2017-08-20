#
# spec file for package SFElibtasn1-gnu
#
# includes module(s): libtasn1
#

%define _use_internal_dependency_generator 0

%include Solaris.inc

%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libtasn164 = libtasn1.spec
%endif

%include base.inc

%define	src_name libtasn1
%use libtasn1 = libtasn1.spec

Name:                SFElibtasn1-gnu
IPS_Package_Name:    library/gnu/libtasn1
Summary:             Tiny ASN.1 library (/usr/gnu)
Version:             %{libtasn1.version}
SUNW_BaseDir:        %{_prefix}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libtasn164.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libtasn1.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libtasn164.build -d %name-%version/%_arch64
%endif

%libtasn1.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libtasn164.install -d %name-%version/%_arch64
%endif

%libtasn1.install -d %name-%version/%{base_arch}
##TODO## find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;

[ -d "$RPM_BUILD_ROOT%{_datadir}" ] && rmdir $RPM_BUILD_ROOT%{_datadir}
[ -d "$RPM_BUILD_ROOT%{_std_datadir}" ] && rmdir $RPM_BUILD_ROOT%{_std_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif


%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/aclocal
#%{_datadir}/aclocal/*


%changelog
* Sun Aug 20 2017 - Thomas Wagner
- disable dependency generator
* Tue Jun  6 2017 - Thomas Wagner
- bump to 4.12
* Sun Oct 11 2015 - Thomas Wagner
- bump to 4.5
- add IPS_Package_Name, relocate to usr-gnu.inc
- make it 32/64-bit
- fix %files
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
* Wed May 28 2008 - jeff.cai@sun.com
- Split to two spec files
