#
# spec file for package SFEboost-gpp
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc
%include usr-g++.inc
%include packagenamemacros.inc
%include buildparameter.inc
%define cc_is_gcc 1
%include base.inc
# Build multithreaded libs: no need for non-multithreaded libs
%define boost_with_mt 1

##REMEMBER## to update this version number in include/packagenamemacros.inc accordingly
%define        major      1
%define        minor      58
%define        patchlevel 0
%define        ver_boost  %{major}_%{minor}_%{patchlevel}

%ifarch amd64 sparcv9
%include arch64.inc
%use boost_64 = boost.spec
%endif

%include usr-g++.inc
%include base.inc
%use boost = boost.spec

Name:		SFEboost-gpp
IPS_Package_Name:	system/library/g++/boost
Summary:	Free peer-reviewed portable C++ libraries (g++-built)
License:	Boost License Version
Group:		System/Libraries
URL:		http://www.boost.org/
#Source:		%{sf_download}/boost/boost_%{ver_boost}.tar.bz2
SUNW_Copyright:	boost.copyright
Version:	%{boost.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: %{pnm_buildrequires_python_default}

#currently suspended, *may* be tested later if osdistro fits *and* changes in version can be managed good enough
#need icu compiled with GXX/gpp/g++ and only oihipster has it in osdistro
#%if %{oihipster}
#BuildRequires:  developer/icu
#Requires:       library/icu
#%else
BuildRequires:	SFEicu-gpp-devel
Requires:	SFEicu-gpp
#%endif

%package -n %name-devel
IPS_package_name:	system/library/g++/boost/header-boost
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package -n %name-doc
IPS_package_name:	system/library/g++/boost/documentation
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%boost_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%boost.prep -d %name-%version/%{base_arch}

%build
PKG_CONFIG_PATH_ORIG=$PKG_CONFIG_PATH

%ifarch amd64 sparcv9
#+ openindiana?
%if %( expr %{solaris11} '+' %{solaris12} )
export PKG_CONFIG_PATH=/usr/g++/lib/%_arch64/pkgconfig:$PKG_CONFIG_PATH_ORIG
%endif
%define BITS 64
%define additional_bjam_cxxflags
export GPP_LIB="-L/usr/g++/lib/%{_arch64} -R/usr/g++/lib/%{_arch64}"
%boost_64.build -d %name-%version/%_arch64
%endif

#+ openindiana?
%if %( expr %{solaris11} '+' %{solaris12} )
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:$PKG_CONFIG_PATH_ORIG
%endif


#%define BITS 32
#%if %{omnios}
##%define additional_bjam_cxxflags %( echo 'cxxflags="-fvisibility=hidden"' )
##alternative would be to patch-in LD_ALTEXEC=/usr/bin/gld
#%define additional_bjam_cxxflags %( echo 'cxxflags="-fvisibility=default"' )
#%endif
%define additional_bjam_cxxflags

export GPP_LIB="-L/usr/g++/lib -R/usr/g++/lib"
%boost.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%define BITS 64
%boost_64.install -d %name-%version/%_arch64
%endif

%define BITS 32
%boost.install -d %name-%version/%base_arch

find $RPM_BUILD_ROOT \( -name \*.la -o -name \*.a \) -exec rm {} \;

mkdir -p %{buildroot}%{_docdir}/boost-%{version}

cd %{_builddir}/%{name}-%{version}/%{base_arch}/boost_%{boost.ver_boost}

cd "doc/html"
for i in `find . -type d`; do
  mkdir -p %{buildroot}%{_docdir}/boost-%{version}/$i
done
for i in `find . -type f`; do
  cp $i %{buildroot}%{_docdir}/boost-%{version}/$i
done

#Test case for RUNPATH:
# boost locale and boost regex need to have the icu library path in RPATH
# test command: ldd boost_locale.so -->> prints the correct icu, e.g. /usr/g++/lib/libuu*so* and *not* /usr/lib/libuu*so* ...
#note: /usr/g++/bin in RPATH is a flaw, will be corrected later
#
# cd /usr/g++;  find . -name libboost_locale.so.\* -exec file {} \; -exec ldd {} \; -exec elfdump -d {} \; -print | egrep "RPATH|/libicui18n|bit"
#
#./lib/amd64/libboost_locale.so.1.58.0: ELF 64-bit LSB shared object, x86-64, version 1, dynamically linked, not stripped
#        libicui18n.so.55 =>      /usr/g++/lib/amd64/libicui18n.so.55
#     [17]  RPATH           0x21de2   /usr/g++/lib/amd64:/usr/gcc/4.8/lib/amd64:/usr/gcc/lib/amd64:/usr/g++/bin
#
#./lib/libboost_locale.so.1.58.0: ELF 32-bit LSB shared object, Intel 80386, version 1, dynamically linked, not stripped
#        libicui18n.so.55 =>      /usr/g++/lib/libicui18n.so.55
#     [17]  RPATH           0x20c25  /usr/g++/lib:/usr/gcc/4.8/lib:/usr/gcc/lib:/usr/g++/bin




%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%_libdir/%_arch64
%endif

%files -n %name-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/boost

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/boost-%{version}

%changelog
- Wed Oct 28 2015 - Thomas Wagner
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
* Thu Jan  1 2015 - Thomas Wagner
- bump to 1.55.0
* Sat Apr  6 2013 - Thomas Wagner
- align SFEboost-gpp.spec and SFEboost-stdcxx.spec
- pause patch5 boost-05-remove-fchmodat.diff for version 1.53.0
* Wed Feb  6 2013 - Thomas Wagner
- add patch5 for S10, SXCE to remove fchmodat
- include packagenamemacros.inc earlier
* Sun Apr 29 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_python_default}, %include packagenamacros.inc
* Thu Jan 12 2012 - Milan Jurik
- package restructuralization, static libs re-added
* Sun Jun 31 2011 - Alex Viskovatoff
- set correct runpath for some more shared libraries
* Fri Jul 29 2011 - Alex Viskovatoff
- add License and SUNW_Copyright tags
* Thu Jun 23 2011 - Alex Viskovatoff
- set correct runpath for libboost_regex, so it finds ICU libraries
* Sun Apr  3 2011 - Alex Viskovatoff
- use new g++ libs pathname; build multithreaded libs
* Fri Jan 11 2011 - Milan Jurik
- do not deliver static libs
* Mon May 17 2010 - Albert Lee <trisk@opensolaris.org>
- Remove SUNWicu* dependencies added in error
* Sat Jan 30 2010 - Brian Cameron <brian.cameron@sun.com>
- Install header files, so it isn't necessary to install the Sun Studio
  version of boost to access these.
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Re-add SUNWicud
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- changed %builddir, created base-specs/boost.spec
* Wed Apr 23 2008 - laca@sun.com
- create, based on SFEboost.spec
- force building with g++ and install the libs to /usr/lib/g++/<version>
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
