#
# spec file for package SFElibffi
#
# includes module(s): libffi
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libffi_64 = libffi.spec
%endif

%include base.inc
%use libffi = libffi.spec

Name:		SFElibffi-gpp
IPS_Package_Name:	library/g++/libffi
Summary:	A Portable Foreign Function Interface Library (/usr/g++)
Group:		System/Multimedia Libraries
Version:	%{libffi.version}
URL:		https://sourceware.org/libffi/
License:        MIT
SUNW_Copyright:	%{name}.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEgcc
Requires:      SFEgccruntime

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libffi_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libffi.prep -d %name-%version/%{base_arch}

%build
export CC=gcc

%ifarch amd64 sparcv9
%libffi_64.build -d %name-%version/%_arch64
%endif

%libffi.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libffi_64.install -d %name-%version/%_arch64
%endif

%libffi.install -d %name-%version/%{base_arch}

rm -r $RPM_BUILD_ROOT/%{_datadir}/info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_libdir/libffi.so*
%ifarch amd64 sparcv9
%_libdir/%_arch64/libffi.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/info/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/libffi.pc
%_libdir/libffi-*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %_libdir/%_arch64/pkgconfig
%_libdir/%_arch64/pkgconfig/libffi.pc
%_libdir/%_arch64/libffi-*
%endif

%changelog
* Thu Dec 23 2016 - Thomas Wagner
- initial spec version 3.2.1
- relocate to /usr/g++ to make it easier for SFEglib2-gpp to propperly set RUNPATH and have libtool copy files to correct $(libdir)
