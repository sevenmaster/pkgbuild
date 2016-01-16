#
# spec file for package SFElibrevenge
#
# includes module: librevenge
#
## TODO ##
# Lots: only started basic info 
# see http://sourceforge.net/p/libwpd/librevenge/ci/1e440fcbcb78a29e76562bf5e87cbd927afe5a36/tree/librevenge.spec.in

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0


%define src_name librevenge
%define src_url  http://downloads.sourceforge.net/libwpd

%define major_version 0.0
%define minor_version 3

Name:			SFElibrevenge
IPS_Package_Name:	sfe/library/g++/librevenge
Summary:		Library for reading and converting WordPerfect(tm) documents (/usr/g++)
Group:			System/Libraries
URL:			http://sourceforge.net/p/libwpd/wiki/librevenge/
Version:		%major_version.%minor_version
License:		LGPLv2 and MPL
SUNW_Copyright:		LGPLv2.copyright
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
BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

BuildRequires:	%{pnm_buildrequires_developer_documentation_tool_doxygen}

# Copied from Wikipedia
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
export CXXFLAGS="%cxx_optflags -pthreads -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/lib/pkgconfig

./configure	\
	--prefix=%_prefix	\
	--disable-werror	\
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
%_libdir/%src_name-generators-%major_version.so*
%_libdir/%src_name-stream-%major_version.so*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%src_name-%major_version.pc
%{_libdir}/pkgconfig/%src_name-generators-%major_version.pc
%{_libdir}/pkgconfig/%src_name-stream-%major_version.pc

%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%src_name

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name-%major_version
%_includedir/%src_name-%major_version/%src_name
%_includedir/%src_name-%major_version/%src_name-generators
%_includedir/%src_name-%major_version/%src_name-stream


%changelog
* Sat Jan  2 2016 - Thomas Wagner
- bump to version 0.0.3
- add -pthreads (or get configure on boost classic.hpp fail the test)
- find cppunit by PKG_CONFIG_PATH point to /usr/g++ first
* Sun Sep 20 2015 - pjama
- %include usr-g++.inc
- add (Build)Requires SFEgcc
- add (Build)Requires doxygen
* Mon Aug 10 2015 - Thomas Wagner
- rename IPS_Package_Name to propperly reflect g++ compiler
* Wed Aug  5 2015 - Thomas Wagner
- initial commit to svn for pjama
- unpack with xz
- add (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, %{pnm_buildrequires_developer_cppunit}
- disable _use_internal_dependency_generator to stop wasting time.
* Sun Jun 14 2015 - pjama
- initial spec
