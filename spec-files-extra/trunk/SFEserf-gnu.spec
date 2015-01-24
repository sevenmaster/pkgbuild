#
# spec file for package SFEserf
#
#
%include Solaris.inc
%include usr-gnu.inc
%include base.inc

%include packagenamemacros.inc

##TODO## make 32/64-bit package

Name:			SFEserf-gnu
License:		Apache
IPS_Package_Name:	library/gnu/serf
Group:			System/Libraries
Version:		1.3.8
Summary:		High-performance asynchronous HTTP client library (/usr/gnu)
Source:			http://serf.googlecode.com/svn/src_releases/serf-%{version}.tar.bz2
Patch1:			serf-01-SConstruct.diff
URL:			https://code.google.com/p/serf/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:		%{license}.copyright

BuildRequires: %{pnm_buildrequires_apr_default}
Requires:      %{pnm_requires_apr_default}
BuildRequires: %{pnm_buildrequires_apr_util_default}
Requires:      %{pnm_requires_apr_util_default}

BuildRequires: SFEscons

%description
The serf library is a high performance C-based HTTP client library built upon the Apache Portable Runtime (APR) library.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n serf-%{version}

%patch1 -p0

%build

##TODO## for 32/64-bit builds, see the README
scons APR=%{_basedir}/%{apr_default_basedir} APU=%{_basedir}/%{apr_util_default_basedir} PREFIX=/usr/gnu CC=$CC

%install
rm -rf $RPM_BUILD_ROOT

scons install --install-sandbox=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';' -print


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Jan 18 2015 - Thomas Wagner
- Initial spec version 1.3.8.
- need patch1 or 
