#
# spec file for package SFElibsodium
#
# includes module(s): libsodium
#

%include Solaris.inc
%include osdistro.inc
%define cc_is_gcc 1
%include base.inc

##TODO## not on Openindiana
##TODO## pnm_macro to get os provided or SFE libsodium

%ifarch amd64 sparcv9
%include arch64.inc
%use libsodium_64 = libsodium.spec
%endif

%include base.inc
%use libsodium = libsodium.spec


Name:                    %{libsodium.name}
IPS_Package_Name:	 components/library/libsodium
Summary:    	         %{libsodium.summary}
Version:                 %{libsodium.version}
URL:			 %{libsodium.url}
Source:         https://github.com/jedisct1/libsodium/releases/download/%{version}/libsodium-%{version}.tar.gz
SUNW_Copyright: libsodium.copyright
Group:		Applications/Archivers
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name



%description
It is a portable, cross-compilable, installable, packageable fork of NaCl, with a compatible API, and an extended API to improve usability even further.


%prep
rm -rf %{name}-%{version}
%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%{_arch64}
%libsodium_64.prep -d %{name}-%{version}/%{_arch64}
%endif

%libsodium.prep -d %{name}-%{version}/%{base_arch}


%build
%ifarch amd64 sparcv9
%libsodium_64.build -d %{name}-%{version}/%{_arch64}
%endif

%libsodium.build -d %{name}-%{version}/%{base_arch}}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libsodium_64.install -d %{name}-%{version}/%{_arch64}
%endif

%libsodium.install -d %{name}-%{version}/%{base_arch}

find $RPM_BUILD_ROOT%{_libdir}/ -name "*.a" -exec rm {} \; -print -o -name  "*.la" -exec rm {} \; -print

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
#%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*
#%dir %attr (0755, root, other) %{_datadir}/doc
#%{_datadir}/doc/*

%changelog
* Fri Jul 26 2019 - Thomas Wagner
- fix i386 compile with bash_arch
* Mon Jul  2 2018 - Thomas Wagner
- initial spec 1.0.13
