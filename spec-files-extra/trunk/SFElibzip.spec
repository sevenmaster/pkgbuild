#
# spec file for package SFElibzip
#
# includes module(s): libzip
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libzip_64 = libzip.spec
%endif

%include base.inc
%use libzip = libzip.spec

Name:		SFElibzip
IPS_Package_Name:	library/libzip
Summary:        C library for reading, creating, and modifying zip archives
Group:		Applications/System Utilities
Version:	%{libzip.version}
URL:            http://www.nih.at/libzip/index.html
Source:         http://www.nih.at/libzip/libzip-%{version}.tar.xz
License:        BSD
SUNW_Copyright:	BSDlicense.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libzip_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libzip.prep -d %name-%version/%{base_arch}

%build

%ifarch amd64 sparcv9
%libzip_64.build -d %name-%version/%_arch64
%endif

%libzip.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libzip_64.install -d %name-%version/%_arch64
%endif

%libzip.install -d %name-%version/%{base_arch}

mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
for binary in `cd %{buildroot}/%{_bindir}; ls -1d zip*`
  do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  ln -f -s /usr/lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%ifarch amd64 sparcv9
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%hard %{_bindir}/zipmerge
%hard %{_bindir}/zipcmp
#those are symlinks to the binaries above
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man*/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libzip.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/libzip.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%{_libdir}/libzip/include/*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/libzip/include/*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libzip.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/libzip.pc
%endif

%changelog
* Fri Dec 11 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 1.0.1
* Sun Feb 10 2013 - Thomas Wagner
- initial spec
