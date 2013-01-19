#
# spec file for package SFEerlang 
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%define is64 1
%use erlang_64 = erlang.spec
%endif

%include base.inc
%define is64 0
%use erlang = erlang.spec

%define pkg_src_name     otp_src
%define src_name         erlang
%define src_ver          R15B03
%define major            15
%define minor            3

Name:                    SFEerlang
IPS_package_name:	 sfe/runtime/erlang
Summary:                 erlang - Erlang programming language and OTP libraries (g++-built)
Version:                 %{major}.%{minor}
Release:                 1
License:                 ERLANG PUBLIC LICENSE
Group:                   Development/Languages/Erlang
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.erlang.org
Source:                  http://erlang.org/download/%{pkg_src_name}_%{src_ver}-1.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%define SFEgd            %(/usr/bin/pkginfo -q SUNWgd2 && echo 0 || echo 1)
%define SFEunixodbc      %(/usr/bin/pkginfo -q SUNWunixodbc && echo 0 || echo 1)

%include default-depend.inc

BuildRequires: 	SFEgcc
Requires: 	SFEgccruntime

BuildRequires:  SFEwxwidgets-gnu-devel
Requires:       SFEwxwidgets-gnu

%if %SFEgd
BuildRequires: SFEgd-devel
Requires: SFEgd
%else
BuildRequires: SUNWgd2
Requires: SUNWgd2
%endif

%if %SFEunixodbc
BuildRequires: SFEunixodbc-devel
Requires: SFEunixodbc
%else
BuildRequires: SUNWunixodbc
Requires: SUNWunixodbc
%endif

BuildRequires: SUNWgtar
BuildRequires: SUNWesu

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%define is64 1
%erlang_64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir %{name}-%{version}/%{base_arch}
%define is64 0
%erlang.prep -d %{name}-%{version}/%{base_arch}


%build
%ifarch amd64 sparcv9
%define is64 1
%erlang_64.build -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%erlang.build -d %{name}-%{version}/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%define is64 1
%erlang_64.install -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%erlang.install -d %{name}-%{version}/%{base_arch}


# Prepare lists of files for packaging
cd %{_builddir}/%{name}-%{version}
touch SFEerlang-all.files

%clean
%ifarch amd64 sparcv9
%define is64 1
%erlang_64.clean -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%erlang.clean -d %{name}-%{version}/%{base_arch}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ct_run
%{_bindir}/dialyzer
%{_bindir}/epmd
%{_bindir}/*erl*
%{_bindir}/escript
%{_bindir}/run_test
%{_bindir}/typer

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%endif

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang
%{_libdir}/%{_arch64}/erlang/*
%endif

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/erlang
%{_libdir}/erlang/*

%changelog
* Fri Jan 18 2013- Logan Bruns <logan@gedanken.org>
- Updated to R15B03
- Added IPS name
* Sun Jun 6 2010 - markwright@internode.on.net
- Initial spec
