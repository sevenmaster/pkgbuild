#
# spec file for package SFElibwpd
#
# includes module: libwpd
#
## TODO ##
# Lots: only started basic info 

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libwpd
%define src_url  http://downloads.sourceforge.net/libwpd

%define major_version 0.10
%define minor_version 0

Name:			SFElibwpd
IPS_Package_Name:	sfe/library/g++/libwpd
Summary:		Library for reading and converting WordPerfect(tm) documents
Group:			System/Libraries
URL:			http://libwpd.sf.net/
Version:		%major_version.%minor_version
License:		LGPLv2
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

##TODO## BuildRequires:	SFEgcc
##TODO## Requires:	SFEgccruntime
BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:  %{pnm_buildrequires_developer_icu}
BuildRequires:  %{pnm_requires_developer_icu}

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}

BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

BuildRequires:  SFElibrevenge
Requires:       SFElibrevenge


%description
Library that handles Word Perfect documents.

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

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

./configure	\
	--prefix=%_prefix	\
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

%dir %attr (0755, root, bin) %_bindir
%_bindir/wpd2*

%dir %attr (0755, root, bin) %_libdir
%_libdir/%src_name-%major_version.so*

%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%src_name-%major_version.pc

%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%src_name

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name-%major_version
%_includedir/%src_name-%major_version/%src_name


%changelog
* Mon Aug 10 2015 - Thomas Wagner
- disable _use_internal_dependency_generator
- rename IPS_Package_Name to propperly reflect g++ compiler
##TODO## relocation to /usr/g++ (depends on LO package)
- initial commit to svn for pjama
- unpack with xz
- change to (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, developer_icu, library_math_header_math, add SFExz_gnu
- disable _use_internal_dependency_generator
* Sun Jun 14 2015 - pjama
- initial spec
