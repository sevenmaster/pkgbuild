# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

#examples:
#%define src_version 0.8.4
#just in case, use for 0.8.4-1 -> 0.8.4.1
#%define ips_version 0.8.4

%define src_version 0.9.0
#just in case, use for 0.9.0-1 -> 0.9.0.1
%define ips_version 0.9.0

%define src_name libdbi

Name:		SFElibdbi
IPS_Package_Name:	library/dbi
Summary:	database-independent abstraction layer (libdbi)
Version:	%{src_version}
IPS_component_version: %{ips_version}
URL:		http://libdbi.sourceforge.net
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Group:		System/Libraries
License:	LGPL
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
##TODO## SUNW_Copyright: %{name}.copyright

%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%description
libdbi implements a database-independent abstraction layer in C, similar to the DBI/DBD layer in Perl. Writing one generic set of code, programmers can leverage the power of multiple databases and multiple simultaneous database connections by using this framework.

In order to utilize the libdbi framework, you need to install drivers for a particular type of database. See libdbi-drivers (dbi-drivers).

%prep
%setup -q -n %{src_name}-%{version}

%build

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} --disable-static
gmake

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir} 
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%changelog
* Sat Jan  6 2018 - Thomas Wagner
- fix permissions for /usr/lib/pkgconfig
* Fri Mar 15 2013 - Thomas Wagner
- bump to 0.9.0
* Sat Aug 11 2012 - Thomas Wagner
- initial spec
