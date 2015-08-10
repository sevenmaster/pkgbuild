
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
%patch4 -p1 
%patch5 -p1 
%endif
#cc_is_gcc AND minor >= 58


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
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

BOOST_ROOT=`pwd`

export CFLAGS="%optflags -D_XPG6"
export CXXFLAGS="%cxx_optflags -D_XPG6"

%if %cc_is_gcc
export CC=gcc
export CXX=g++
export LDFLAGS="%_ldflags"
%else
export LDFLAGS="%_ldflags"
%endif

%if %cc_is_gcc
./bootstrap.sh --prefix=%{_prefix} --with-toolset=gcc --with-icu=/usr/g++
%else
./bootstrap.sh --prefix=%{_prefix} --with-toolset=sun --with-icu
%endif

./bjam --v2 -d+2 -q -j$CPUS -sBUILD="release <threading>single/multi" \
  release stage

%install
./bjam install --prefix=$RPM_BUILD_ROOT%{_prefix}

%changelog
* Mon Aug 10 2015 - Thomas Wagner
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
