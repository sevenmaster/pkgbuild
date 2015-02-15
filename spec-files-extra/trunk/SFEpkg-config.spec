#
# spec file for package pkg-config
#

%include Solaris.inc

Name:			SFEpkg-config
IPS_Package_Name:	developer/build/pkg-config
License:		GPLv2
Group:			Development/System
Version:		0.23
Summary:		A tool to query library build-time information
Source:			http://pkgconfig.freedesktop.org/releases/pkg-config-%{version}.tar.gz
URL:			http://www.freedesktop.org/wiki/Software/pkg-config/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%description
pkg-config(1) is used to determine what compile and link flags should be used when building against a library that supports pkg-config, as well as additional required dependencies, and their versions.

%prep
%setup -q -n pkg-config-%{version}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

CFLAGS="%{optflags}" \
   ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
               --with-internal-glib

gmake -j$CPUS

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*


%changelog
* Sun Feb 15 2015 - Thomas Wagner
- initial spec modeled after userland gate and old JDS pkg-config.spec
