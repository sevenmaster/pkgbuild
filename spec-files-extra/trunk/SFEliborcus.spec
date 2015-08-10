#
# spec file for package SFEliborcus
#
# includes module: liborcus
#
## TODO ##

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name liborcus
%define src_url  http://kohei.us/files/orcus/src

# Dunno what it is with people putting 0.8.0 config in a download file with 0.7.0 in it
%define major_version 0.7
%define minor_version 1
#%define major_version 0.8
#%define minor_version 0
#%define major_version 0.9
#%define minor_version 2

Name:			SFEliborcus
IPS_Package_Name:	sfe/library/g++/liborcus
Summary:		Standalone file import filter library for spreadsheet documents
Group:			System/Libraries
URL:			https://gitlab.com/orcus/orcus
Version:		%major_version.%minor_version
License:		MPL2.0
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
#Source:		%{src_url}/%{src_name}-0.7.0.tar.bz2
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

##TODO## BuildRequires:	SFEgcc
##TODO## Requires:	SFEgccruntime
BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:  %{pnm_buildrequires_developer_icu}
BuildRequires:  %{pnm_requires_developer_icu}

##TODO## check this dependency. Is it a hard 2.7 or just a default module needed for 2.6Ã6?
# probably a fib but 0.9.2 requires python >= 2.7.1
BuildRequires:	runtime/python-27 >= 2.7.1

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}


BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

BuildRequires:  SFElibrevenge
Requires:       SFElibrevenge

BuildRequires:	SFElibixion
Requires:	SFElibixion

BuildRequires:	SFEmdds
Requires:	SFEmdds

%description
liborcus is a standalone file import filter library for spreadsheet
documents. Currently under development are ODS, XLSX and CSV import
filters.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
%setup -q -n %src_name-%version
#%setup -q -n %src_name-0.7.0


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

## TODO ##
# Fix this
#checking boost/thread.hpp presence... no
#checking boost/thread.hpp usability... yes
#checking boost/thread.hpp presence... no
#configure: WARNING: boost/thread.hpp: accepted by the compiler, rejected by the preprocessor!
#configure: WARNING: boost/thread.hpp: proceeding with the compiler's result
#checking for boost/thread.hpp... yes
#checking for the Boost thread library... (cached) yes

# boost/iostreams/device/file_descriptor.hpp
# above doesn't like -pthreads


./configure	\
	--prefix=%_prefix	\
	;

## TODO ##
#  Peter Tribbles' sneaky hack to insert -pthreads in all the Makefiles at:
#For liborcus, run the following against all the Makefiles that the configure step generates:
#gsed -i 's:-DMDDS_HASH_CONTAINER_BOOST:-pthreads -DMDDS_HASH_CONTAINER_BOOST:'

gsed -i -e 's/-DMDDS_HASH_CONTAINER_BOOST/-pthreads -DMDDS_HASH_CONTAINER_BOOST/' \
    `find . -name Makefile`

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
%_bindir/orcus-*

%dir %attr (0755, root, bin) %_libdir
%_libdir/%src_name-*.so*
#%_libdir/%src_name-mso-*.so*
#%_libdir/%src_name-parser-*.so*
#%_libdir/%src_name-spreadsheet-model-*.so*

%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%src_name-*.pc
#%_libdir/pkgconfig/%src_name-spreadsheet-model-*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name-*
%_includedir/%src_name-*/orcus


%changelog
* Mon Aug 10 2015 - Thomas Wagner
- rename IPS_Package_Name to propperly reflect g++ compiler
##TODO## relocation to /usr/g++ (depends on LO package)
- initial commit to svn for pjama
- unpack with xz
##TODO## check python 2.7 only, or is python 2.6 plus modules enough?
- change to (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, developer_icu, library_math_header_math, SUNWlxml_devel, add SFExz_gnu, library_math_header_math, add SFExz_gnu
* Sun Jun 14 2015 - pjama
- initial spec
