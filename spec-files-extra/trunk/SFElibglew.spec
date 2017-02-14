#
# spec file for package SFElibglew
#
# includes module: glew
#
## TODO ##
#
##


%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%include base.inc
%include packagenamemacros.inc

#%define major_version 1.12
#%define major_version 1.10
%define major_version 1.13
%define minor_version 0

%define src_name glew
%define src_url  http://downloads.sourceforge.net/%src_name/%major_version.%minor_version

Name:		SFElibglew
IPS_Package_Name:	sfe/library/libglew
Summary:	OpenGL Extension Wrangler Library (/usr/gnu/)
Group:		System/Libraries
URL:		http://glew.sourceforge.net/
Version:	%major_version.%minor_version
License:	LGPLv2.1+
Source:		%{src_url}/%src_name-%{version}.tgz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

# Requirements
#     GNU make
#     perl
#     wget
#     GNU sed
#     gcc compiler
#     git

BuildRequires:  SFEgcc
Requires:       SFEgccruntime

# Requires glu
# which Hipster has /x11/library/glu
# and OI has in x11/library/mesa

# # Warning, on hipster, glew.pc, requires glu.pc which requires something, which requires xcb.pc, which requires
# x11/library/libpthread-stubs which isn't installed by default. But LibreOffice configure tells you glew failed.
%if %{oihipster}
BuildRequires:	x11/library/libpthread-stubs
Requires:	x11/library/libpthread-stubs
%endif

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform
open-source C/C++ extension loading library. GLEW provides efficient
run-time mechanisms for determining which OpenGL extensions are
supported on the target platform. OpenGL core and extension
functionality is exposed in a single header file.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
%setup -q -n glew-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

export SYSTEM="solaris-gcc"
export GLEW_DEST="%{_prefix}"

export LD=`which ld-wrapper`
[ -z "$LD" ] && LD=/usr/bin/ld

make LD="$LD" all


%install
rm -rf $RPM_BUILD_ROOT
SYSTEM="solaris-gcc" make install.all DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT SYSTEM="solaris-gcc" install.all
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/visualinfo
%{_bindir}/glewinfo

%dir %attr (0755, root, bin) %_libdir
%_libdir/libGLEW.so*
%_libdir/libGLEWmx.so*

%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/glew.pc
%_libdir/pkgconfig/glewmx.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/GL


%changelog
* Sun Nov  6 2016 - Thomas Wagner
- relocate to /usr/gnu/ because (OIH) has its own libglew starting with 2016
  export GLEW_DEST="%{_prefix}"
* Fri Oct 23 2015 - Thomas Wagner
- merge in pjama's changes. Help finding LD on various build environments
* Sun Jun 14 2015 - pjama
- initial spec
#historic log, this looks like a major rewrite
* Sun Feb 12 2012 - Milan Jurik
- bump to 1.7.0
* Sat Mar 05 2011 - Milan Jurik
- bump to 1.5.8
* Sun Dec 19 2010 - Milan Jurik
- bump to 1.5.7
* Sat May 15 2010 - Milan Jurik
- Initial package
