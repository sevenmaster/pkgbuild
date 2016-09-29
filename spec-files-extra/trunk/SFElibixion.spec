#
# spec file for package SFElibixion
#
# includes module: libixion
#
## TODO ##
## Where should pyton bindings go? Currently get installed in /usr/g++/lib/python2.6/site-packages but might be better under real site-packages?

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libixion
%define src_url  http://kohei.us/files/ixion/src

%define major_version 0
%define minor_version 9
%define micro_version 1


Name:			SFElibixion
IPS_Package_Name:	sfe/library/g++/libixion
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

# For ixion 0.9.1 python >= 0.27.1 required
# Hacks below for those osdistos where *default* python version falls short
BuildRequires: %{pnm_buildrequires_python_default}
Requires:      %{pnm_requires_python_default}

BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

BuildRequires:  SFEmdds
#no runtime dependency, but pkgtool can't resolve that depenency
Requires:       SFEmdds

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








export PKG_CONFIG_PATH=%{gnu_lib}/pkgconfig:%{gpp_lib}/pkgconfig


# Edit configure so pkg-config uses python-%{python_version}.pc (rather than look for, and not find, python.pc)
%if %( expr %{python_version} '>=' 2.7 )
gsed -i.pre_pkgconfig-python-fix \
	-e '/PKG_CONFIG/s/python >=/python-%{python_version} >=/'	\
	configure	\
	;
%endif

### Special fix for 2.6 python on OI 151a9
%if %( expr %{python_version} '=' 2.6 )
# Gratuitously hack configure to pretend python 2.6 is ok
gsed -i.pre_hack_to_accept_python2.6 \
	-e 's|checking whether $PYTHON version is >= 2.7.0|checking whether $PYTHON version is >= %{python_version}|g'	\
	-e 's|checking for a Python interpreter with version >= 2.7.0"|checking for a Python interpreter with version >= %{python_version}"|g'	\
	-e 's|minver = list(map(int, '\''2.7.0'\''|minver = list(map(int, '\''%{python_version}'\''|g'	\
	-e 's|LDFLAGS="-L/usr/local/lib"|LDFLAGS="$LDFLAGS -L/usr/local/lib"|'  \
	configure	\
	;

# Set variables because there's no pkg-config .pc file for Python 2.6
export PYTHON=python%{python_version}
export PYTHON_LIBS=-lpython%{python_version}
export PYTHON_CFLAGS=-I/usr/include/python%{python_version}

%endif


./configure	\
	--prefix=%{_prefix}	\
	--program-suffix="-%{major_version}%{minor_version}"	\
	--with-boost=%{boost_gpp_default_prefix} \
	;



make -j$CPUS


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
%{_libdir}/python*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%{src_name}-*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %{_includedir}/%{src_name}-*
%{_includedir}/%{src_name}-*/ixion


%changelog
* Mon Sep 19 2016 - pjama
- fix "configure: WARNING: boost/thread.hpp: accepted by the compiler, rejected by the preprocessor!" by adding -pthreads to CPPFLAGS
- suffix the bin binaries with version number to allow parallel install of versions. All other files already in versioned.
- modified versioning into major, minor and micro
- enclosed a lot of %vars in {} for readability
- Messed with python in configure to hopefully improve future supportability if/when osdistro python versions advance
* Fri Apr 22 2016 - Thomas Wagner
- remove -D_GLIBCXX_USE_C99_MATH for (S12) or get /usr/gcc/4.8/include/c++/4.8.5/cmath: error: redefinition of 'constexpr int std::fpclassify(float)'
* Mon Jan  4 2016 - Thomas Wagner
- add to CXXFLAGS -D_GLIBCXX_USE_C99_MATH to avoid std::isnan and isnan conflicting (all, needed S11 S12)
* Fri Oct 23 2015 - Thomas Wagner
- merge in pjama's changes
##TODO## see if python version can be set with pnm macro
* Sun Sep 20 2015 - pjama
- %include usr-g++.inc
- add (Build)Requires SFEgcc
- some python version edits to make Openindiana a9 friendly
- add --std=c++0x  to CXXFLAGS... can't remember why
- set PKG_CONFIG_PATH so we can find stuff hiding in /usr/g++ and /usr/gnu
* Mon Aug 10 2015 - Thomas Wagner
- add BuildRequires SFEmdds
- workaround to find python on platform without "python.pc" file, pythong-2.7.pc instead. set PYTHON_LIBS and PYTHON_CFLAGS for configure
* Sat Aug  8 2015 - Thomas Wagner
- initial commit to svn for pjama
- unpack with xz
- change to %{pnm_buildrequires_boost_gpp_default}, library_math_header_math, SFExz_gnu
- disable _use_internal_dependency_generator
* Sun Jun 14 2015 - pjama
- initial spec
