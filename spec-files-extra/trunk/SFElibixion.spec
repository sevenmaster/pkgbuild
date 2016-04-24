#
# spec file for package SFElibixion
#
# includes module: libixion
#
## TODO ##
# move to 0.9.0 ? but may need python 2.7

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libixion
%define src_url  http://kohei.us/files/ixion/src

# althoug it's labeled 0.7.0 it builds as 0.8.0
#%define major_version 0.8
#%define minor_version 0
%define major_version 0.9
%define minor_version 1

Name:			SFElibixion
IPS_Package_Name:	sfe/library/g++/libixion
Summary:		A general purpose formula parser and interpreter that can calculate multiple named targets, or "cells" (/usr/g++)
Group:			System/Libraries
#URL:			https://gitorious.org/ixion/pages/Home
URL:			https://gitlab.com/ixion/ixion
Version:		%major_version.%minor_version
License:                MPL2.0
SUNW_Copyright:         %{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

# Python interpreter with version >= 2.7.0 required for v0.9.0
# TODO ##
# Fix python pkges to link .pc files a bit better, many config scripts look for:
# python python2 python3 python3.3 python3.2 python3.1 python3.0 python2.7  python2.6 python2.5 python2.4 python2.3 python2.2 python2.1 python2.0
# We have:
# $ ls /usr/lib/pkgconfig/python*
# /usr/lib/pkgconfig/python-2.7.pc  /usr/lib/pkgconfig/python-3.3.pc  /usr/lib/pkgconfig/python-3.3m.pc  /usr/lib/pkgconfig/python3.pc
# manually linked python.pc and python2.pc to python-2.7.pc 
# Update fresh install of OIH circa 20150919 only has python-2.7.pc

#notes/findings
#pkg-config --print-errors --cflags --libs "python-2.7 >= 0.27.1"
#-I/usr/include/python2.7 -lpython2.7 
#
#but configure asks for "python >= 0.27.1" which is not found.
#workaround, set PYTHON_CFLAGS and PYTHON_LIBS in the environment

#this workaround is used below in block %build
#PYTHON_LIBS=`$PKG_CONFIG --libs "python-2.7 >= 0.27.1" 2>/dev/null`
#PYTHON_CFLAGS=`$PKG_CONFIG --cflags "python-2.7 >= 0.27.1" 2>/dev/null`



##TODO## is this better a pnm_macro in the future?
# probably a fib but 0.9.1 requires python >= 2.7.0
#BuildRequires:  runtime/python-27 >= 2.7.0
#BuildRequires:  runtime/python-26 >= 2.6.0
#try pnm macro BuildRequires:  runtime/python-26
##TODO## OI requires python 2.6
BuildRequires: %{pnm_buildrequires_python_default}
Requires:      %{pnm_requires_python_default}


##TODO## check dependency
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
#export CXXFLAGS="%cxx_optflags -pthreads -I/usr/g++/include"
##paused##%if %{solaris12}
##paused##export CXXFLAGS="%cxx_optflags -pthreads -I/usr/g++/include"
##paused##%else
%if %{solaris11}
export CXXFLAGS="%cxx_optflags -D_GLIBCXX_USE_C99_MATH -pthreads --std=c++0x -I/usr/g++/include"
%endif
%if %{solaris12}
export CXXFLAGS="%cxx_optflags -pthreads --std=c++0x -I/usr/g++/include"
%endif
##paused##%endif
##TODO## if g++ runtime makes troubles, try entering a runpath which takes g++ runtime from SFEgcc instead of using the osdistro /usr/lib/libstdc++.so.6
export LDFLAGS="%_ldflags -pthreads -L/usr/g++/lib -R/usr/g++/lib"

##TODO## below needed or does it work in CXXFLAGS?
export CPPFLAGS="-I/usr/g++/include"
##TODO##
# Fix this
#checking boost/thread.hpp presence... no
#checking boost/thread.hpp usability... yes
#checking boost/thread.hpp presence... no
#configure: WARNING: boost/thread.hpp: accepted by the compiler, rejected by the preprocessor!
#configure: WARNING: boost/thread.hpp: proceeding with the compiler's result
#checking for boost/thread.hpp... yes
#checking for the Boost thread library... (cached) yes


#NOTE: python version is contained int he python-2.7.pc file name!
[ -z ${PKG_CONFIG} ] && PKG_CONFIG="pkg-config"
echo "PKG_CONFIG: ${PKG_CONFIG}"
export PYTHON_LIBS=`$PKG_CONFIG --libs "python-2.7 >= 0.27.1" 2>/dev/null`
export PYTHON_CFLAGS=`$PKG_CONFIG --cflags "python-2.7 >= 0.27.1" 2>/dev/null`

export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig:/usr/g++/lib/pkgconfig


##TODO## find a way to patch in the osdistro default perl version so we can be sure to have it available as package
%if %{openindiana}
##TODO## Fix for 2.6 python on OI
gsed -i -e 's|checking whether $PYTHON version is >= 2.7.0"|checking whether $PYTHON version is >= 2.6.0"|g'	\
	-e 's|checking for a Python interpreter with version >= 2.7.0"|checking for a Python interpreter with version >= 2.6.0"|g'	\
	-e 's|minver = list(map(int, '\''2.7.0'\''|minver = list(map(int, '\''2.6.0'\''|g'	\
	configure	\
	;

export PYTHON_LIBS=-lpython2.6
export PYTHON_CFLAGS=-I/usr/include/python2.6
PYTHON_CFLAGS=-I/usr/include/python2.6
%endif


./configure	\
	--prefix=%_prefix	\
	;

#make -j$CPUS
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_bindir
%_bindir/ixion-*

%dir %attr (0755, root, bin) %_libdir
#%_libdir/%src_name-%major_version.so*
%_libdir/%src_name-*.so*
%_libdir/python*

%dir %attr (0755, root, other) %_libdir/pkgconfig
#%_libdir/pkgconfig/%src_name-%major_version.pc
%_libdir/pkgconfig/%src_name-*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
#%dir %_includedir/%src_name-%major_version
#%_includedir/%src_name-%major_version/ixion
%dir %_includedir/%src_name-*
%_includedir/%src_name-*/ixion


%changelog
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
