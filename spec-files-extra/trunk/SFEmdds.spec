#
# spec file for package SFEmdds
#
# includes module: mdds
#
## TODO ##

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name mdds
%define src_url  http://kohei.us/files/mdds/src/

#%define major_version 0.11
#%define minor_version 2

%define major_version 0.12
%define minor_version 1

Name:			SFEmdds
IPS_Package_Name:	sfe/library/mdds
Summary:		A collection of multi-dimensional data structure and indexing algorithm.
Group:			System/Libraries
URL:			https://gitlab.com/mdds/mdds
Version:		%major_version.%minor_version
##TODO## check license SFEmggs.spec MIT/X11 - license tag and file
License:		MIT/X11
#SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}_%{version}.tar.bz2
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

##TODO## check build and runtime dependencies
# REqs
# boost-devel, pkg-config, 

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
#no runtime present Requires:	%{pnm_requires_boost_gpp_default}



%description
This library provides a collection of multi-dimensional data structure and indexing
algorithm. All data structures are available as C++ templates, hence this is a
header-only library, with no shared library to link against.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
%setup -q -n %{src_name}_%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

./configure	\
	--prefix=%_prefix	\
	;

#make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%src_name
%dir %attr (0755, root, bin) %_datadir/pkgconfig
%_datadir/pkgconfig/%src_name.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/%src_name


%changelog
* Sun Sep 20 2015 - pjama
- add (BUILD)Requires SFEgcc
* Mon Aug 10 2015 - Thomas Wagner
* Sat Aug  8 2015 - Thomas Wagner
- initial commit to svn for pjama
- change to (Build)Requires %{pnm_buildrequires_boost_gpp_default}
- disable _use_internal_dependency_generator
* Sun Jun 14 2015 - pjama
- initial spec
