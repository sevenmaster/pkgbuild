#
# spec file for package SFEclucene-gpp
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-g++.inc
%include base.inc

%define cc_is_gcc 1
%include base.inc

Name:                SFEclucene-gpp
IPS_Package_Name:    text/library/g++/clucene
Summary:             CLucene - a C++ search engine (g++)
Version:             2.3.3.4
URL:                 http://clucene.sourceforge.net
Source:              http://downloads.sourceforge.net/project/clucene/clucene-core-unstable/2.3/clucene-core-%{version}.tar.gz
License:      	     dual licensed Apache 2 and LGPL
SUNW_Copyright:      SFEclucene-gpp.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:      SFEcmake
BuildRequires:      SFEgcc
Requires:           SFEgccruntime
BuildRequires:	    SFEboost-gpp-devel
Requires:	    SFEboost-gpp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description
CLucene is a high-performance, scalable, cross platform,
full-featured, open-source indexing and searching API. Specifically,
CLucene is the guts of a search engine, the hard stuff. You write the
easy stuff: the UI and the process of selecting and parsing your data
files to pump them into the search engine yourself, and any
specialized queries to pull it back for display or further processing.

CLucene is a port of the very popular Java Lucene text search engine
API. CLucene aims to be a good alternative to Java Lucene when
performance really matters or if you want to stick to good old
C++. CLucene is faster than Lucene as it is written in C++, meaning it
is being compiled into machine code, has no background GC operations,
and requires no any extra setup procedures.

%prep
%setup -q -n clucene-core-%version

# To be safe exclude bundled boost so it has to use SFEboost-gpp (or fail)
gsed -i 's|ADD_SUBDIRECTORY (src/ext)|# ADD_SUBDIRECTORY (src/ext)|g' CMakeLists.txt

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags  -L/usr/g++/lib"
echo "DEBUG: CFLAGS =$CFLAGS"
echo "DEBUG: LDFLAGS=$LDFLAGS"

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -G "Unix Makefiles" ..

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd build
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/CLuceneConfig.cmake
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Apr  7 2013 - Thomas Wagner
- relocate to usr-gnu.inc
* Tue Feb 5 2013 - Logan Bruns <logan@gedanken.org>
- initial version
