#
# spec file for package SFEliborcus-010-gpp
#
# includes module: liborcus-010-gpp
#
## TODO ##

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name liborcus
%define src_url  http://kohei.us/files/orcus/src

%define major_version 0
%define minor_version 9
%define micro_version 2

Name:			SFEliborcus-010-gpp
IPS_Package_Name:	sfe/library/g++/liborcus-010
Summary:		Standalone file import filter library for spreadsheet documents (/usr/g++)
Group:			System/Libraries
URL:			https://gitlab.com/orcus/orcus
Version:		%{major_version}.%{minor_version}.%{micro_version}
License:		MPL2.0
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

# BuildRequires aclocal-1.14 (part of automake)

BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:	%{pnm_buildrequires_icu_gpp_default}
Requires:	%{pnm_requires_icu_gpp_default}

##TODO## check this dependency. Is it a hard 2.7 or just a default module needed for 2.6?
# probably a fib but 0.9.2 requires python >= 2.7.1
##BuildRequires:	runtime/python-27 >= 2.7.1
##Requires:	runtime/python-27 >= 2.7.1
BuildRequires: %{pnm_buildrequires_python_default}
Requires:      %{pnm_requires_python_default}

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}


BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

%if %( expr %{solaris11} '+' %{solaris12}  '+' %{openindiana} '>=' 1 )
#S11 S12 openindiana need zlib.pc (should not bother oihipster, which probably already has a propper zlib.pc)
# Confirmed: hipster circa 201605 has /usr/lib/amd64/pkgconfig/zlib.pc
BuildRequires:  SFEzlib-pkgconfig 
#for pkgtool's dependency resoultion
Requires:       SFEzlib-pkgconfig 
%endif

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
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}



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

##TODO## oh, this might need a review, if it is still needed. Check with visibility fixes for the SFEgcc on OmniOS, might apply for S12 too
#S12
%if %{solaris12}
   gsed -i.bak0 -e '/^CXXFLAGS=/ s/-fvisibility=hidden//' \
   configure.ac \
   ;
%endif

#debug [ -f configure.ac.bak0 ] && (diff -u configure.ac.bak0 configure.ac; exit 0)


./configure	\
	--prefix=%{_prefix}	\
	--program-suffix="-%{major_version}.%{minor_version}"	\
        --with-boost=%{boost_gpp_default_prefix} \
	;


#I can't help, that super smart Makefile immediately re-creates everything by running: 
#/bin/bash ./config.status --recheck
#you'll see in "make" for the second time a configure run. Only costs a bit of time, so stop fixing an overly sensitive Makefile.
make V=2 -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.*a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/orcus-*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/%{src_name}-*.so*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%{src_name}-*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %{_includedir}/%{src_name}-0.10
%{_includedir}/%{src_name}-0.10/orcus


%changelog
* Mon Sep 18 2016 - pjama
- Initial spec of version 0.9.2 which is really orcus API 0.10 because LO4 requires old API, LO5+ requires this version
- Variations from  SFEliborcus.spec below
- add links to libs etc from old version to new version to maintain compatability for LO4
- remove all fancy injection of -pthreads and put in CXXFLAGS because that works now.... future hindsight may prove me wrong.
- enclose %vars in {} for readability
- pnm a few dependancies
- See SFEliborcus.spec for earlier changelog.
