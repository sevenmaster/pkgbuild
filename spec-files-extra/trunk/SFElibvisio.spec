#
# spec file for package SFElibvisio
#
# includes module: libvisio
#
## TODO ##
# It would be nice if libs linked to libicuuc.so instead of libicuuc.so.<version_no_at_compile_time> and friends

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libvisio
%define src_url  http://dev-www.libreoffice.org/src/libvisio

%define major_version 0.1
%define minor_version 1

Name:			SFElibvisio
IPS_Package_Name:	sfe/library/g++/libvisio
Summary:		Libvisio is a library that parses the file format of Microsoft Visio documents of all versions.
Group:			System/Libraries
URL:			https://wiki.documentfoundation.org/DLP/Libraries/libvisio
Version:		%major_version.%minor_version
License:		MPL2.0
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
Patch1:			libvisio-01-pow.diff
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

BuildRequires:  %{pnm_buildrequires_developer_gperf}
Requires:       %{pnm_requires_developer_gperf}

BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

BuildRequires:  %{pnm_buildrequires_SUNWlxml_devel}
Requires:       %{pnm_requires_SUNWlxml}

BuildRequires:	SFElibrevenge
Requires:	SFElibrevenge

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

%description
libvisio is an import filter library for Microsoft Visio files, based on librevenge.
It can import .vsd and .vss files of all versions.
It is a part of the Document Liberation Project.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
#don't unpack please
%setup -q -c -T -n %src_name-%version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)

%patch1 -p0


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

#from studio compiled icu.pc
#g++: error: unrecognized command line option '-compat=5'
#./Makefile:ICU_CFLAGS =   -compat=5
#./Makefile:LIBVISIO_CXXFLAGS = -I/usr/include/librevenge-0.0   -I/usr/include/libxml2      -compat=5
perl -w -pi -e "s,-compat=5,," Makefile src/test/Makefile src/conv/text/Makefile src/conv/Makefile src/conv/raw/Makefile src/conv/svg/Makefile src/Makefile src/lib/Makefile inc/libvisio/Makefile inc/Makefile build/Makefile 


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
%_bindir/vsd2*
%_bindir/vss2*

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
- rename IPS_Package_Name to propperly reflect g++ compiler
##TODO## relocation to /usr/g++ (depends on LO package)
* Sat Aug  8 2015 - Thomas Wagner
- edit out -compat=5 from all files, comes from studio compiles icu libraries but g++ doesn't know that switch
- initial commit to svn for pjama
- unpack with xz
- change to (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, developer_icu, library_math_header_math, SUNWlxml_devel, add SFExz_gnu
- add (Build)Requires developer_gperf
- disable _use_internal_dependency_generator
* Sun Jun 14 2015 - pjama
- initial spec
- Thanks to Peter Tribble for sharing http://ptribble.blogspot.co.uk/2015/06/building-libreoffice-on-tribblix.html
