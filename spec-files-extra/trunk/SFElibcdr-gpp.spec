#
# spec file for package SFElibcdr
#
# includes module: libcdr
#
## Status ##
# compiles, nees to be integrated into LO
#
## TODO ##
# a few more requires
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0


%define src_name libcdr
%define src_url  http://dev-www.libreoffice.org/src/libcdr/

%define major_version 0
%define minor_version 1
%define micro_version 3

Name:			SFElibcdr-gpp
IPS_Package_Name:	sfe/library/g++/libcdr
Summary:		Library for parsing the Corel Draw file format structure
Group:			System/Libraries
URL:			https://wiki.documentfoundation.org/DLP/Libraries/libcdr
Version:		%{major_version}.%{minor_version}.%{micro_version}
License:		MPL2.0
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

# Requires boost as well ...or does it. Maybe it does but via an already required pkg (librevenge?)
# config looks for icu.. and boost, cppunit

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

BuildRequires:	SFElibrevenge
Requires:	SFElibrevenge

BuildRequires:  SFElcms2-gnu
Requires:       SFElcms2-gnu

BuildRequires:  %{pnm_buildrequires_library_libxml2}
Requires:       %{pnm_requires_library_libxml2}

BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

%description
libcdr is a library for parsing the Corel Draw file format structure. It is
cross-platform, at the moment it can be build on Microsoft Windows and Linux and Solarish

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}

%description devel
libcdr is a library for parsing the Corel Draw file format structure. It is
cross-platform, at the moment it can be build on Microsoft Windows and Linux and Solarish

%prep
#don't unpack please
%setup -q -c -T -n %{src_name}-%{version}
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)



%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -I/usr/g++/include"
export CXXFLAGS="%{cxx_optflags} -pthreads -I/usr/g++/include"
export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib"

export PKG_CONFIG_PATH=%{gpp_lib}/pkgconfig:%{gnu_lib}/pkgconfig

./configure	\
	--prefix=%{_prefix}	\
	--disable-werror	\
	;

make -j$CPUS
#make V=2


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/%{src_name}-%{major_version}.%{minor_version}.so*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%{src_name}-%{major_version}.%{minor_version}.pc

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/%{src_name}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %{_includedir}/%{src_name}-%{major_version}.%{minor_version}
%{_includedir}/%{src_name}-%{major_version}.%{minor_version}/%{src_name}/*.h


%changelog
* Tue Sep 2016 - pjama
- initial spec
