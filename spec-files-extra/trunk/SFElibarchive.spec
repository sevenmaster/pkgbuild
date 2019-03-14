#
# spec file for package SUNWlibarchive
#
# includes module(s): libarchive
#
%include Solaris.inc
%include packagenamemacros.inc

%if %( expr %{solaris11} '|' %{s110400} '|' %{oihipster} )
exit 1
%endif

%ifarch amd64 sparcv9
%include arch64.inc
%use libarchive64 = libarchive.spec
%endif

%include base.inc
%use libarchive = libarchive.spec

Name:		SFElibarchive
IPS_Package_Name:	library/archive 
Summary:	Multi-format archive and compression library
Group:		System/Libraries
License:	New BSD License
Copyright:	libarchive.copyright
URL:		http://www.digip.org/archive
Version:	%{libarchive.version}
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
%libarchive64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir -p %{name}-%{version}/%{base_arch}
%libarchive.prep -d %{name}-%{version}/%{base_arch}

%build
%ifarch amd64 sparcv9
%libarchive64.build -d %{name}-%{version}/%{_arch64}
%endif

%libarchive.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libarchive64.install -d %{name}-%{version}/%{_arch64}
%endif

%libarchive.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
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
%{_includedir}/*


%changelog
* Thu Mar 14 2019 - Thomas Wagner
- initial spec version 3.3.3 based on Solaris Userland library/libarchive
