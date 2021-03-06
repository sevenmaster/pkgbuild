#
# spec file for package SFElibmp4v2
#
# includes module(s): libmp4v2
#
%include Solaris.inc
%define cc_is_gcc 1
%include osdistro.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libmp4v2_64 = libmp4v2.spec
%endif

%include base.inc
%use libmp4v2 = libmp4v2.spec

Name:                    SFElibmp4v2
IPS_Package_Name:	library/video/libmp4v2
Summary:                 %{libmp4v2.summary}
License:                 GPLv2
SUNW_Copyright:          libmp4v2.copyright
Version:                 %{libmp4v2.version}
URL:			https://code.google.com/p/mp4v2/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libmp4v2_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libmp4v2.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libmp4v2_64.build -d %name-%version/%_arch64
%endif

%libmp4v2.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libmp4v2_64.install -d %name-%version/%_arch64
%endif

%libmp4v2.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun May 15 2015 - Thomas Wagner
- disable script autoaux/missing on omnios and openindiana
* Wed Mar  4 2015 - Thomas Wagner
- %include osdistro.inc, exclude aclocal on %{omnios}
* Sun Aug 19 2012 - Milan Jurik
- use GCC
* Sun Oct 16 2011 - Milan Jurik
- add IPS package name
* Fri Aug 21 2009 - Milan Jurik
- Initial version
