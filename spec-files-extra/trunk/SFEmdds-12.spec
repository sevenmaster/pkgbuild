#
# spec file for package SFEmdds-12
#
# includes module: mdds-12
#
# Note: this is a different beast to mdds as it has API version 1.2 as opposed to 0.12.1 which has no api version
#
## TODO ##

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name mdds
%define src_url  http://kohei.us/files/mdds/src

%define major_version 1
%define minor_version 2
%define micro_version 2

Name:			SFEmdds-%{major_version}%{minor_version}
IPS_Package_Name:	sfe/library/mdds-%{major_version}%{minor_version}
Summary:		A collection of multi-dimensional data structure and indexing algorithm.
Group:			System/Libraries
URL:			https://gitlab.com/mdds/mdds
Version:		%{major_version}.%{minor_version}.%{micro_version}
License:		MIT/X11
SUNW_Copyright:		%{src_name}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

BuildRequires:	%{pnm_buildrequires_boost_gpp_default}


%description
This library provides a collection of multi-dimensional data structure and indexing
algorithm. All data structures are available as C++ templates, hence this is a
header-only library, with no shared library to link against.

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}



%prep
%setup -q -n %{src_name}-%{version}


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -I/usr/g++/include"
export CXXFLAGS="%{cxx_optflags} -I/usr/g++/include"
export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib"

./configure	\
	--prefix=%{_prefix}	\
	;

#make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/%{src_name}-%{major_version}.%{minor_version}

%dir %attr (0755, root, bin) %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/%{src_name}-%{major_version}.%{minor_version}.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/%{src_name}-%{major_version}.%{minor_version}/%{src_name}


%changelog
* Mon Sep 19 2016 - pjama
- tidy up cruft
* Thu Aug 04 2016 - pjama
- bump version from 1.2.0 to 1.2.1
- enclose %vars in {} for readability
* Wed May 12 2016 - pjama
- bump version from 0.12.1 to 1.2.0 because latest liborcus requires at least v1.0. update but LO5.1 barfs
- and change pkg name to co-exist with mdds. 
- change "_" to "-" in sourcefile names to suit new source file format
- append "%{major_version}" to files in doc and pkgconfig.
* Sun Sep 20 2015 - pjama
- add (BUILD)Requires SFEgcc
- initial spec clone of SFEmdds because different API and install directeries and .pc file.
