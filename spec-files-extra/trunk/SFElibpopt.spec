#
# spec file for package SFElibpopt
#
#
%include Solaris.inc

##NOTE## Only needed on Omnios. Solaris 11 / 12 / OpenIndiana has its own libpopt

%ifarch amd64 sparcv9
%include arch64.inc
%use popt64 = popt.spec
%endif

%include base.inc

%use popt = popt.spec

Name:                    SFElibpopt
IPS_package_name:        library/popt
Meta(info.classification): %{classification_prefix}:System/Libraries
Summary:                 Command line parsing library
License:                 MIT X
Version:                 %{popt.version}
Source:                  http://rpm5.org/files/popt/popt-%{version}.tar.gz
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

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
%popt64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%popt.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%popt64.build -d %name-%version/%_arch64
%endif

%popt.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%popt64.install -d %name-%version/%_arch64
#popt.pc for %_arch64 is wrong in /usr/lib
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig $RPM_BUILD_ROOT//usr/lib/%_arch64/
%endif

%popt.install -d %name-%version/%{base_arch}

find $RPM_BUILD_ROOT/%{_libdir} -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Thu Jul 25 2015 - Thomas Wagner
- initial spec, based on spec-files/specs/SUNWlibpopt.spec .. Omnios lost libpopt
