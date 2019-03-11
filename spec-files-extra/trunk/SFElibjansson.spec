#
# spec file for package SUNWlibjansson
#
# includes module(s): libjansson
#
%include Solaris.inc
%include packagenamemacros.inc

#%if %{solaris11}%{s110400}
#exit 1
#%endif

%ifarch amd64 sparcv9
%include arch64.inc
%use libjansson64 = libjansson.spec
%endif

%include base.inc
%use libjansson = libjansson.spec

Name:		SFElibjansson
IPS_Package_Name:	library/jansson 
Summary:	libjansson is a C library for encoding, decoding and manipulating JSON data
Group:		System/Libraries
License:	MIT
Copyright:	libjansson.copyright
URL:		http://www.digip.org/jansson
Version:	%{libjansson.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%libjansson64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir -p %{name}-%{version}/%{base_arch}
%libjansson.prep -d %{name}-%{version}/%{base_arch}

%build
%ifarch amd64 sparcv9
%libjansson64.build -d %{name}-%{version}/%{_arch64}
%endif

%libjansson.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libjansson64.install -d %{name}-%{version}/%{_arch64}
%endif

%libjansson.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, bin) %{_mandir}
#%{_mandir}/*
#%dir %attr (0755, root, bin) %{_mandir}/man*
#%{_mandir}/man*/*
#%dir %attr (0755, root, bin) %{_infodir}
#%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/jansson

%changelog
* Sun Mar  3 2019 - Thomas Wagner
- initial spec version 2.12 based on Solaris Userland library/jasson
