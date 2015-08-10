#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc
# Build multithreaded libs: no need for non-multithreaded libs
%define boost_with_mt 1


%define        major      1
%define        minor      58
%define        patchlevel 0
%define        ver_boost  %{major}_%{minor}_%{patchlevel}
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

%if %{solaris12}
BuildRequires:  developer/icu
Requires:       developer/icu
%else
BuildRequires:	SFEicu-gpp-devel
Requires:	SFEicu-gpp
%endif

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
%boost.prep -d %name-%version


%build
%boost.build -d %name-%version


%install
rm -rf %buildroot
%boost.install -d %name-%version

cd %_builddir/%name-%version/boost_%boost.ver_boost

mkdir -p %buildroot%_docdir/boost-%version
cd "doc/html"
for i in `find . -type d`; do
  mkdir -p %buildroot%_docdir/boost-%version/$i
done
for i in `find . -type f`; do
  cp $i %buildroot%_docdir/boost-%version/$i
done

# It's not worth figuring out how to get the Boost build system
# to set the runpath correctly
%define rpath 'dyn:runpath /usr/g++/lib:/usr/gnu/lib'
pushd %buildroot%_libdir
for i in *.so.*; do
  /usr/bin/elfedit -e %rpath $i
done
popd

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files -n %name-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/boost
%{_libdir}/lib*.a

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/boost-%{version}

%changelog
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
