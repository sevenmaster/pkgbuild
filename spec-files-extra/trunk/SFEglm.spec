#
# spec file for package SFEglm
#
# includes module: glm
#
## TODO ##
# include docs?

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name glm
#%define src_url  http://downloads.sourceforge.net/glm
%define src_url  http://downloads.sourceforge.net/ogl-math

%define major_version 0.9.6
%define minor_version 3

Name:			SFEglm
IPS_Package_Name:	sfe/library/glm
Summary:		Header only C++ mathematics library for graphics
Group:			System/Libraries
URL:			http://glm.g-truc.net
Version:		%major_version.%minor_version
##TODO## check license SFEmggs.spec MIT/X11 - license tag and file
License:		MIT and GPL-2.0+`
#SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.zip
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc



%description
OpenGL Mathematics (GLM) is a header only C++ mathematics library for graphics
software based on the OpenGL Shading Language (GLSL) specification.

GLM provides classes and functions designed and implemented with the same naming
conventions and functionalities than GLSL so that when a programmer knows GLSL,
he knows GLM as well which makes it really easy to use.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

BuildRequires: %{pnm_buildrequires_developer_build_cmake}
#to auto-resolve by pkgtool
Requires:      %{pnm_requires_developer_build_cmake}


%prep
%setup -q -n %src_name


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

#./configure	\
#	--prefix=%_prefix	\
#	;


#cmake\\
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_libdir
#%_libdir/%src_name-%major_version.so*
%_libdir/cmake/FindGLM.cmake

#%dir %attr (0755, root, other) %_datadir/doc
#%_datadir/doc/%src_name

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/%src_name

%changelog
* Mon Aug 10 2015 - Thomas Wagner
- initial commit to svn for pjama
- add (Build)Requires cmake %{pnm_buildrequires_developer_build_cmake}
- disable _use_internal_dependency_generator
* Sun Jun 14 2015 - pjama
- initial spec
