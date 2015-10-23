#
# spec file for package SFElibodfgen
#
# includes module: libodfgen
#
## TODO ##
# Lots: only started basic info 

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libodfgen
%define src_url  http://downloads.sourceforge.net/libwpd

%define major_version 0.1
%define minor_version 4

Name:			SFElibodfgen
IPS_Package_Name:	sfe/library/g++/libodfgen
Summary:		libodfgen is an ODF export library for projects using librevenge. (/usr/g++)
Group:			System/Libraries
URL:			http://sourceforge.net/p/libwpd/wiki/libodfgen
Version:		%major_version.%minor_version
License:		LGPL and MPL
#SUNW_Copyright:	libodfgen.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:  %{pnm_buildrequires_developer_cppunit}
Requires:       %{pnm_requires_developer_cppunit}

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}

BuildRequires:  SFElibrevenge
Requires:       SFElibrevenge

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

%description
Library that handles Open Document Files.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
#don't unpack please
%setup -q -c -T -n %src_name-%version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/lib/pkgconfig

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

./configure	\
	--prefix=%_prefix	\
        --disable-weffc         \
	;

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_libdir
%_libdir/%src_name-%major_version.so*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%src_name-%major_version.pc

%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%src_name

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name-%major_version
%_includedir/%src_name-%major_version/%src_name


%changelog
* Sun Sep 20 2015 - pjama
- %include usr-g++.inc
- set (Build)Requires SFEgcc
* Sat Aug 11 2015 - Thomas Wagner
- disable warnings with --disable-weffc (Disable -Weffc++ warnings in configure to avoid "Could not find Boost implementation of shared_ptr")
* Mon Aug 10 2015 - Thomas Wagner
- rename IPS_Package_Name to propperly reflect g++ compiler
##TODO## relocation to /usr/g++ (depends on LO package)
* Sat Aug  8 2015 - Thomas Wagner
- initial commit to svn for pjama
- unpack with xz
- change to (Build)Requires %{pnm_buildrequires_boost_gpp_default}, %{pnm_buildrequires_developer_cppunit}, library_math_header_math, add SFExz_gnu
* Sun Jun 14 2015 - pjama
- initial spec
