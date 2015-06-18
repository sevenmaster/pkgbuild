##TODO## optional dependency: service/network/dns/unbound to get DNSSEC test 
#  DNSSEC root key file: /etc/unbound/root.key
#configure: WARNING:
#***
#*** The DNSSEC root key file in /etc/unbound/root.key was not found.
#*** This file is needed for the verification of DNSSEC responses.
#*** Use the command: unbound-anchor -a "/etc/unbound/root.key"
#*** to generate or update it.
#***


#
# gnutls
#
%include Solaris.inc

%include packagenamemacros.inc
%include usr-gnu.inc

%define _use_internal_dependency_generator 0

%ifarch amd64 sparcv9
%include arch64.inc
%use gnutls64 = gnutls.spec
%endif

%include base.inc
%use gnutls = gnutls.spec

Name:          SFEgnutls
IPS_package_name: library/gnu/gnutls
Group:         System/Libraries
Summary:       GNU transport layer security library (/usr/gnu)
Version:       %{gnutls.version}
%define        major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:        ftp://ftp.gnutls.org/gcrypt/gnutls/v%{major_minor_version}/gnutls-%{version}.tar.xz
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFEnettle-gnu-devel
Requires:	SFEnettle-gnu

BuildRequires:           %{pnm_buildrequires_SUNWlibgcrypt_devel}
Requires:                %{pnm_buildrequires_SUNWlibgcrypt}

BuildRequires:           %{pnm_buildrequires_SUNWzlib_devel}
Requires:                %{pnm_buildrequires_SUNWzlib}


%package devel
%include default-depend.inc
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires: SUNWgnutls


%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%gnutls64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%gnutls.prep -d %name-%version/%base_arch

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

%ifarch amd64 sparcv9
%gnutls64.build -d %name-%version/%_arch64
%endif

%gnutls.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gnutls64.install -d %name-%version/%_arch64
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/psktool
%endif

%gnutls.install -d %name-%version/%base_arch
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
rm -rf $RPM_BUILD_ROOT%{_bindir}/psktool



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/certtool
%{_bindir}/srptool
%{_bindir}/gnutls-serv
%{_bindir}/ocsptool
%{_bindir}/tpmtool
%{_bindir}/gnutls-cli-debug
%{_bindir}/gnutls-cli
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/locale
%{_datadir}/locale/*

%changelog
* Thu Jun 18 2015 - Thomas Wagner
- unarchvied
- relocate to /usr/gnu, add IPS_Package_Name
- bump to 3.3.15
