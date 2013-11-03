#
# spec file for package SFEsigcpp-gpp
#
# includes module(s): libsigc++
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use sigcpp_64 = sigcpp.spec
%endif
%include base.inc

%use sigcpp = sigcpp.spec

Name:                    SFEsigcpp-gpp
IPS_Package_Name:	 library/g++/sigcpp
Summary:                 %{sigcpp.summary} (/usr/g++)
Group:                   Development/C++
URL:                     %{sigcpp.url}
License:                 LGPLv2
SUNW_Copyright:          sigcpp.copyright
Version:                 %{sigcpp.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:  %{pnm_buildrequires_SFExz_gnu}
BuildRequires:  SFEgcc
Requires: 	SFEgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}

%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%{_arch64}
%sigcpp_64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir -p %{name}-%{version}/%{base_arch}
%sigcpp.prep -d %{name}-%{version}/%{base_arch}



%build
%ifarch amd64 sparcv9
%sigcpp_64.build -d %{name}-%{version}/%{_arch64}
%endif

%sigcpp.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%sigcpp_64.install -d %{name}-%{version}/%{_arch64}
%endif

%sigcpp.install -d %{name}-%{version}/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
#unusual place for an include file...
%{_libdir}/sigc*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
#unusual place for an include file...
%{_libdir}/%{_arch64}/sigc*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, other)
%{_datadir}/doc
%{_datadir}/devhelp

%changelog
* Sun Nov  3 2013 - Thomas Wagner
- %use usr-g++.inc
- add BuildRequires: %{pnm_buildrequires_SFExz_gnu}, %include packagenamemacros.inc
- use manual xz unpacking for older pkgbuild versions
- use %{gnu_lib_path}
- make it 32/64-bit
* Wed Oct 30 2013 - Alex Viskovatoff
- Bump to 2.3.1
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Thu Jun 26 2008 - river@wikimedia.org
- need to use SFW gcc, not SFE because flags depend on Sun ld
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWsigcpp.spec to build with g++
