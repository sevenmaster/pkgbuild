#
# spec file for package boost
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%{!?boost_with_mt: %define boost_with_mt 0}

Name:         boost
License:      Boost License Version
Group:        System/Libraries
Version:      %{major}.%{minor}.%{patchlevel}
Summary:      boost - free peer-reviewed portable C++ source libraries
Source:       %{sf_download}/boost/boost_%{ver_boost}.tar.bz2
URL:          http://www.boost.org/

#note: below patch resources can be overwritten by new definitions for newer boost
# older boost (< 58, around 55)
# Ticket #6161
Patch1:       boost-01-putenv.diff
Patch2:       boost-gpp-01-cstdint.diff
# stlport4/stdcxx4
Patch3:       boost-stdcxx-01-stl.diff
Patch4:       boost-stdcxx-02-wchar.diff

#NOTE# patches start counting with "1"
#use new patches boost >= 1.58.0 (imported thankfully from openindiana source repo)
#https://github.com/OpenIndiana/oi-userland/tree/oi/hipster/components/boost/patches
#note: patch4 will no longer be applied, only to be applied to minor = 58
#note: patch5 will no longer be applied, only to be applied if minor = 58
%if %(expr %cc_is_gcc '&' %{minor} '>=' 58)
Patch1: boost-gpp-01-cstdint.patch
Patch2: boost-gpp-02-usr-include.patch
Patch3: boost-gpp-03-log-xopensource.patch
Patch4: boost-gpp-04-0001-Fix-exec_file-for-Python-3-3.4.patch
Patch5: boost-gpp-05-0002-Fix-a-regression-with-non-constexpr-types.patch
%endif
#minor >= 58

BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}_%{major}_%{minor}_%{patchlevel}

%if %(expr %cc_is_gcc '&' %{minor} '>=' 58)
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
#only for = 58 %patch4 -p1 
#only for = 58 %patch5 -p1 
%endif
#cc_is_gcc AND minor >= 58

#
%if %(expr %cc_is_gcc '&' %{minor} '=' 58)
%patch4 -p1 
%patch5 -p1 
%endif
#cc_is_gcc AND minor = 58

##below older patch stuff, might be removed once 0.55 is eliminated in every SFEboost-<somehting>.spec

#is it studio?
%if %cc_is_gcc
#nothing here
%else
#studio
%patch1 -p0
%endif 

#separate for readbility
#cc_is_gcc and old minor < 53
%if %(expr %cc_is_gcc '&' %{minor} '<' 58)
%patch2 -p0
%endif

#paused# %if %( expr %cc_is_gcc '&' 0%stl_is_stdcxx )
#paused# %patch3 -p0
#paused# %patch4 -p0
#paused# %endif


%build

#variable BITS=<32|64> comes from calling spec file, e.g SFEboost-gpp.spec
##TODO## add BITS to other spec files then SFEboost-gpp.spec

CPUS=%{_cpus_memory}

BOOST_ROOT=`pwd`

##TODO## check if Solaris 11.2 need this as well
#on Solaris 12 with patched SFEgcc.spec (userland Sol gcc 4.8 patches for new C++ standards present in system headers)
#else: /usr/include/sys/feature_tests.h:392:2: error: #error "Compiler or options invalid; UNIX 03 and POSIX.1-2001 applications       require the use of c99"
# #error "Compiler or options invalid; UNIX 03 and POSIX.1-2001 applications \
#-D_GLIBCXX_USE_C99_MATH or get on S11.3+SFEgcc 4.8.5 this: ./boost/math/special_functions/fpclassify.hpp:525:17: error: 'isnan' is not a member of 'std'
%if %( expr %{solaris11} '|' %{solaris12} )
export CFLAGS="%optflags -D_XPG6"
export CXXFLAGS="%cxx_optflags -D_XPG6 -std=c++11 -D_GLIBCXX_USE_C99_MATH"
%else
export CFLAGS="%optflags -D_XPG6"
export CXXFLAGS="%cxx_optflags -D_XPG6"
%endif

%if %cc_is_gcc
export CC=gcc
export CXX=g++
%endif

export LDFLAGS="%_ldflags ${GPP_LIB}"

#we have a problem on OmniOS, the Solaris linker there fails with
#ld: fatal: relocation error: R_386_GOTOFF: file bin.v2/libs/log/build/gcc-4.8.5/release/log-api-unix/threading-multi/text_file_backend.o: symbol construction vtable for std::basic_ofstream<char, std::char_traits<char> >-in-boost::filesystem::basic_ofstream<char, std::char_traits<char> >: a GOT relative relocation must reference a local symbol
#so we use the Gnu linker until the link error with the Solaris linker is fixed
#%if %(expr %{BITS} '=' 32 '&' %{omnios} )
##PAUSED##%if %( expr %{omnios} '&' %{BITS} '=' 32 )
##PAUSED##echo "OmniOS fix in place. BITS=%{BITS} and we set LD_ALTEXEC to the gnu linker /usr/bin/gld"
##PAUSED##export LD_ALTEXEC=/usr/bin/gld
##PAUSED##%endif

#prepare a user config
echo 'using mpi ;' > `pwd`/user-config.jam

%if %cc_is_gcc
./bootstrap.sh --prefix=%{_prefix} --libdir=%{_libdir} --with-toolset=gcc --with-icu=/usr/g++
%define ICU_ROOT /usr/g++
%define ICU_PATH /usr/g++
%define ICU_LINK '-L%{_libdir} -R%{_libdir}  -licudata -licui18n -licuuc '
%else
./bootstrap.sh --prefix=%{_prefix} --libdir=%{_libdir} --with-toolset=sun --with-icu
%define ICU_ROOT /usr
%define ICU_PATH /usr
#e.g. -L/usr/g++/lib       -R/usr/g++/lib       -licudata -licui18n -licuuc
#e.g. -L/usr/g++/lib/amd64 -R/usr/g++/lib/amd64 -licudata -licui18n -licuuc
%define ICU_LINK '-L%{_libdir} -R%{_libdir}  -licudata -licui18n -licuuc '
%endif

#with ICU_LINK set, then the configure test gcc.link bin.v2/libs/regex/build/gcc-4.8.5/debug/address-model-64/has_icu
# succeeds, see in /amd64/boost_1_58_0/bin.v2/config.log
# the build system looks like not honouring LDFLAGS to find icu libs in /usr/g++/lib

echo "debug: BITS     is %{BITS}"
echo "debug: _libdir  is %{_libdir}"
echo "debug: ICU_LINK is %{ICU_LINK}"
echo "debug: CPUS     is ${CPUS}"
echo "debug: CXXFLAGS is ${CXXFLAGS}"
echo "debug: additional_bjam_cxxflags is %{additional_bjam_cxxflags}"
echo "debug: LD_FLAGS is is ${LD_FLAGS}"
echo "may be empty:"
echo "debug: LD_ALTEXEC is ${LD_ALTEXEC}"

./bjam --v2 -d+2 -q address-model=%{BITS}   \
  -j$CPUS \
  -sBUILD="release <threading>single/multi" \
  -sICU_ROOT=%{ICU_ROOT} \
  -sICU_PATH=%{ICU_PATH} \
  -sICU_LINK=%{ICU_LINK} \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --includedir=/usr/g++/include \
  --user-config=`pwd`/user-config.jam \
  cxxflags="$CXXFLAGS" cflags="$CFLAGS" \
  %{additional_bjam_cxxflags}



%install

#looks like install can use more cpus as well. cc1plus running...even with "bjam install"
#CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
CPUS=%{_cpus_memory}

./bjam --v2 -d+2 -q address-model=%{BITS}   \
  -j$CPUS \
  -sBUILD="release <threading>single/multi" \
  -sICU_ROOT=%{ICU_ROOT} \
  -sICU_PATH=%{ICU_PATH} \
  -sICU_LINK=%{ICU_LINK} \
  --prefix=$RPM_BUILD_ROOT%{_prefix} \
  --libdir=$RPM_BUILD_ROOT%{_libdir} \
  --user-config=`pwd`/user-config.jam \
  install


%changelog
* Fri Jan  8 2016 - Thomas Wagner
- bump version to 0.59.0 on (OIH)
* Mon Jan  4 2016 - Thomas Wagner
- add to CXXFLAGS -D_GLIBCXX_USE_C99_MATH to avoid std::isnan and isnan conflicting (S11 S12)
- fix typo --stdc=c++11 -> -stdc=c++11
* Sun Jan  3 2016 - Thomas Wagner
- need -std=c++11 as well (S11)
* Tue Nov 17 2015 - Thomas Wagner
- fix the 32-bit BUILD be really 32-bit
- bump version to 0.59.0 or get c++ redefinition with updates system headers (S11 S12)
- really use cxxflags and cflags with bjam
* Wed Oct 28 2015 - Thomas Wagner
- make build work on low memory machines %include buildparameter.inc, use CPUS=%{_cpus_memory}
- for now, use SFEicu-gpp on all osdistro (OIH)
- for 32 / 64-bit by adding GPP_LIB point to /usr/g++/lib or /usr/g++/lib/%{_arch64}
- make install work in parallel as well
* Sat Sep 19 2015 - Thomas Wagner
- make it 32/64-bit
- fix finding correct icu libs in /usr/g++/lib (ICU_LINK)
- remove elfedit, RPATH might be edited in a later spec version and have /usr/g++/bin removed from RPATH
- add mpi (as in boost from OI userland)
* Wed Sep 16 2015 - Thomas Wagner
- add --with-locale (spits Boost.Locale needs either iconv or ICU library to be built, see next changelog line)
- add dirty hack to change config cache to have icu set to true (the change is not yet 32/64-bit safe, remove once bjam detecting icu is fixed!)
- add echo 'using mpi ;' > ./user-config.jam; (adopted from OI userland)
* Sat Aug 15 2015 - Thomas Wagner
- use BuildRequires:  developer/icu (OIH)  else use BuildRequires  SFEicu-gpp-devel (all other)
* Mon Aug 10 2015 - Thomas Wagner
- contionally use BuildRequires developer/icu on S12 instead of SFEicu-gpp
- patch1 .. patch5 thankfully imported patches for boost 0.58 from openindiana source repo
- temporarily comment stdcxx patches, check once needed
- try keeping older patches, may be phased out once other uses are updated or have ended
##TODO## work on studio compiled boost once it is needed
- bump to 1.58.0
* Sat Apr  6 2013 - Thomas Wagner
- align SFEboost-gpp.spec and SFEboost-stdcxx.spec
- pause patch fchmod for version 1.53.0
* Sat Dec 14 2013 - Ken Mays <kmays2000@gmail.com>
- bump to 1.55.0
* Thu Feb 21 2013 - Ken Mays <kmays2000@gmail.com>
- bump to 1.53.0
* Wed Feb  6 2013 - Thomas Wagner
- add patch5 for S10, SXCE to remove fchmodat
* Sat May 19 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.49.0 and removed a patch that is no longer needed.
* Sat Jan 14 2012 - Milan Jurik
- add support for stdcxx
* Thu Jan 12 2012 - Milan Jurik
- bump to 1.48.0
* Sat Jul 30 2011 - Milan Jurik
- bump to 1.47.0
* Thu Jun 23 2011 - Alex Viskovatoff
- enable ICU when building with gcc
* Sat Mar 19 2011 - Milan Jurik
- bump to 1.46.1 but disable graph lib for Sun Studio build
* Thu Aug 26 2010 - Brian Cameron <brian.cameron@oracle.com
- Bump to 1.44.
* Wed Aug 04 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 1.43.
* Fri Mar 05 2010 - Brian Cameron <brian.cameron@sun.com>
- Bump to 1.42.
* Fri Jan 29 2010 - Brian Cameron <brian.cameron@sun.com>
- Add boost-with-mt option to build the mt version of the libraries.
  Do not build with ICU support if building the GCC version, otherwise the
  boost regex library is not usable.
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Add patch4 from upstream for #2602
- Update URL
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- Bump to 1.40.0, updated boost-01-studio patch
- Initial base spec
