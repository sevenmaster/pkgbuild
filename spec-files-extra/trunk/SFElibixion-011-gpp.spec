#
# spec file for package SFElibixion-011-gpp
#
# includes module: libixion-011-gpp
#
## TODO ##
## Separate packages for bin and libs to suit future versions?

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libixion
%define src_url  http://kohei.us/files/ixion/src

%define major_version 0
%define minor_version 11
%define micro_version 1


#Name:			SFElibixion-%{major_version}%{minor_version}-gpp
#to have pkgtool-uninstall-recoursive really find this package we need the real name here, without any eval
Name:			SFElibixion-011-gpp
#IPS_Package_Name:	sfe/library/g++/libixion-%{major_version}%{minor_version}
IPS_Package_Name:	sfe/library/g++/libixion-011
Summary:		A general purpose formula parser and interpreter that can calculate multiple named targets, or "cells" (/usr/g++)
Group:			System/Libraries
URL:			https://gitlab.com/ixion/ixion
Version:		%{major_version}.%{minor_version}.%{micro_version}
License:                MPL2.0
SUNW_Copyright:         %{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime






BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

BuildRequires:  SFEmdds-12
#no runtime dependency, but pkgtool can't resolve that depenency
Requires:       SFEmdds-12

%description
Ixion is a general purpose formula parser & interpreter that can calculate multiple named targets, or "cell".

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

%if %{openindiana}
export CXXFLAGS="%{cxx_optflags} -pthreads -I/usr/g++/include"
%endif

%if %{oihipster}
export CXXFLAGS="%{cxx_optflags} -pthreads -I/usr/g++/include"
%endif

%if %{solaris11}
export CXXFLAGS="%{cxx_optflags} -D_GLIBCXX_USE_C99_MATH -pthreads --std=c++0x -I/usr/g++/include"
%endif

%if %{solaris12}
export CXXFLAGS="%{cxx_optflags} -pthreads --std=c++0x -I/usr/g++/include"
%endif

##TODO## if g++ runtime makes troubles, try entering a runpath which takes g++ runtime from SFEgcc instead of using the osdistro /usr/lib/libstdc++.so.6

export LDFLAGS="%{_ldflags} -pthreads -L/usr/g++/lib -R/usr/g++/lib"
export CPPFLAGS="-pthreads -I/usr/g++/include"

# Change cruddy last resort, default LDDFLAGS and CPPFLAGS in configure
gsed -i.FixFlags \
	-e 's|CPPFLAGS="$CPPFLAGS -g -O2 -fvisibility=hidden -I/usr/local/include"|CPPFLAGS="$CPPFLAGS"|'	\
        -e 's|LDFLAGS="-L/usr/local/lib"|LDFLAGS="$LDFLAGS"|'  \
        configure       \
        ;

export PKG_CONFIG_PATH=%{gnu_lib}/pkgconfig:%{gpp_lib}/pkgconfig


./configure	\
	--prefix=%{_prefix}	\
	--program-suffix="-%{major_version}.%{minor_version}"	\
	--with-boost=%{boost_gpp_default_prefix} \
	--disable-python	\
	;


make -j$CPUS V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ixion-*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/%{src_name}-*.so*


%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%{src_name}-*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %{_includedir}/%{src_name}-*
%{_includedir}/%{src_name}-*/ixion


%changelog
* Wed Nov 15 2017 - Thomas Wagner
- remove macro variables vom package names -> help pkgtool resolve dependency chains
* Sep 2016 - pjama
- initial spec: Copy SFElibixion.spec to SFElibixion-011-gpp.spec because the different versions (0.9.1 vs 0.11.x) have a different API versions, install in differnent paths and have different pkg-config .pc files. They can co-install
- remove all python config and requirements becuase ixion >= 0.11.1 requires python 3 and we don't have such fancy pants versions around these parts. disabling python with 
- refer SFElibixion.spec for earlier history.
