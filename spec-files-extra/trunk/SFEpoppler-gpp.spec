
#Building poppler with support for:
#  font configuration: fontconfig
#  splash output:      yes
#  cairo output:       yes
#  qt4 wrapper:        yes
#  qt5 wrapper:        no
#  glib wrapper:       yes
#    introspection:    yes
#  cpp wrapper:        yes
#  use gtk-doc:        no
#  use libjpeg:        yes
#  use libpng:         yes
#  use libtiff:        yes
#  use zlib:           yes
#  use libcurl:        no
#  use libopenjpeg:    yes
#      with openjpeg1
#  use cms:            yes
#      with lcms1
#  command line utils: yes
#  test data dir:      /localhomes/sfe/packages/BUILD/SFEpoppler-gpp-0.35.0/poppler-0.35.0/./../test


#
# spec file for package SFEpoppler-gpp
#
# includes module(s): poppler
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc

%use poppler = poppler.spec

Name:                    SFEpoppler-gpp
IPS_Package_Name:	 library/g++/poppler
Summary:                 PDF rendering library (g++-built)
URL:                     http://poppler.freedesktop.org
License:                 GPLv2
SUNW_Copyright:          poppler.copyright
Version:                 %{poppler.version}
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
Requires:      SUNWgnome-base-libs
BuildRequires: %{pnm_buildrequires_SUNWgtk2_devel}
Requires:      %{pnm_requires_SUNWgtk2}
BuildRequires: %{pnm_buildrequires_SUNWcairo_devel}
Requires:      %{pnm_requires_SUNWcairo}
BuildRequires: %{pnm_buildrequires_SFExz_gnu}

BuildRequires: SFEsigcpp-gpp
Requires:      SFEsigcpp-gpp

BuildRequires: SFEopenjpeg
Requires:      SFEopenjpeg

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%poppler.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%cxx_optflags -fpermissive"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
export PATH=/usr/g++/bin:$PATH
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export PERL_PATH=/usr/perl5/bin/perl
%poppler.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%poppler.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# RUNPATH ends up getting incorrectly set, with /usr/g++/lib behind /usr/lib
%define rpath 'dyn:runpath /usr/g++/lib:/usr/gnu/lib'
# pushd %buildroot%_libdir
# elfedit -e %rpath libpoppler-cpp.so.0.1.0
# elfedit -e %rpath libpoppler-glib.so.5.0.0
# elfedit -e %rpath libpoppler.so.7.0.0
# popd

# REMOVE l10n FILES - included in Solaris
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# remove files included in SUNWgnome-pdf-viewer[-devel]:
rm -r $RPM_BUILD_ROOT%{_mandir}
#rm -r $RPM_BUILD_ROOT%{_includedir}
rm -r $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%_libdir/girepository-1.0

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%_includedir
%dir %attr (0755, root, sys) %{_datadir}
%_datadir/gtk-doc
%_datadir/gir-1.0

%changelog
* Mon Aug 24 2015 - Thomas Wagner
- add (Build)Requires SFEsigcpp-gpp SFEopenjpeg
- switch possible version depending on osdistro version for "cairo"
- bump to 0.24.3, 0.14.5, 0.32.0 (osdistro OM, S11, S12)
- unpack with xz or gzip
- CXXFLAGS -std=gnu++11 and find  LIBOPENJPEG includes by libopenjpeg1
- workaround to find strcpy_s, strcat_s (just use them)
* Mon Feb  3 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWcairo_devel}, %{pnm_buildrequires_SUNWgtk2_devel}
- remove Requires: SUNWsigcpp-devel (SFEsigcpp-gpp-devel is found first in /usr/g++)
- fix unpacking directories (base-specs/poppler.spec)
* Mon Jan 13 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SFExz}, %include packagenamemacros.inc
- use manual call to xz (older pkgbuild can't)
- include usr-g++.inc
* Wed Oct 30 2013 - Alex Viskovatoff
- adapt to updated base spec
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Wed Apr 23 2008 - laca@sun.com
- create
Index: base-specs/poppler.spec
===================================================================
--- base-specs/poppler.spec	(revision 6061)
+++ base-specs/poppler.spec	(working copy)
@@ -1,22 +1,26 @@
 #
-# spec file for package poppler
 #
-# Copyright (c) 2005 Sun Microsystems, Inc.
-# This file and all modifications and additions to the pristine
-# package are under the same license as the package itself.
-#
-# Owner: mattman
-# bugdb: bugzilla.freedesktop.org
-#
 Name:         poppler
 License:      GPL
 Group:        System/Libraries
+%if %{omnios}
 Version:      0.24.3
-Release:      1 
-Distribution: Java Desktop System
-Vendor:       Sun Microsystems, Inc.
+Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
+%endif
+#%if %{oihipster}
+#Version:      0.00.0
+#Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
+#%endif
+%if %{solaris11}
+Version:      0.14.5
+Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.gz
+%endif
+%if %{solaris12}
+#Version:      0.35.0
+Version:      0.32.0
+Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
+%endif
 Summary:      PDF Rendering Library
-Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
 # date:2005-11-29 type:feature owner:laca bugzilla:9730
 Patch1:       poppler-01-uninstalled.pc.diff
 URL:          http://poppler.freedesktop.org/
@@ -98,22 +102,27 @@
 %prep
 #don't unpack please
 %setup -q -c -T
-xz -dc %SOURCE0 | (cd ..; tar xf -)
+echo %SOURCE0 | grep "xz$" && xz -dc %SOURCE0 | (cd ..; tar xf -)
+echo %SOURCE0 | grep "bz$" && gzip -d < %SOURCE0 | (cd ..; tar xf -)
 
 #%patch1 -p1
 
 %build
-%ifos linux
-if [ -x /usr/bin/getconf ]; then
-  CPUS=`getconf _NPROCESSORS_ONLN`
-fi
-%else
-  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
-%endif
-if test "x$CPUS" = "x" -o $CPUS = 0; then
-  CPUS=1
-fi
+CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
 
+export CFLAGS="%optflags -std=gnu++11"
+export CXXFLAGS="%cxx_optflags -std=gnu++11"
+export LDFLAGS="%{_ldflags}"
+
+#configure doen't handle the "1" version libopenjpeg1 ...
+export LIBOPENJPEG_CFLAGS=$( pkg-config --cflags "libopenjpeg1" )
+export LIBOPENJPEG_LIBS="-lopenjpeg"
+ 
+
+echo "Note: editing out AC_CHECK_FUNCS(strcpy_s, strcat_s) from configure.ac. Else this fails with not switching on defines in std include files."
+gsed -i.bak '/AC_CHECK_FUNCS.*strcpy_s/ s/^dnl //' configure.ac
+autoconf
+
 # Building documentation currently breaks build
 ./configure --prefix=%{_prefix}		\
 	    --datadir=%{_datadir}       \
Index: SFEpoppler-gpp.spec
===================================================================
--- SFEpoppler-gpp.spec	(revision 6061)
+++ SFEpoppler-gpp.spec	(working copy)
@@ -1,3 +1,27 @@
+
+#Building poppler with support for:
+#  font configuration: fontconfig
+#  splash output:      yes
+#  cairo output:       yes
+#  qt4 wrapper:        yes
+#  qt5 wrapper:        no
+#  glib wrapper:       yes
+#    introspection:    yes
+#  cpp wrapper:        yes
+#  use gtk-doc:        no
+#  use libjpeg:        yes
+#  use libpng:         yes
+#  use libtiff:        yes
+#  use zlib:           yes
+#  use libcurl:        no
+#  use libopenjpeg:    yes
+#      with openjpeg1
+#  use cms:            yes
+#      with lcms1
+#  command line utils: yes
+#  test data dir:      /localhomes/sfe/packages/BUILD/SFEpoppler-gpp-0.35.0/poppler-0.35.0/./../test
+
+
 #
 # spec file for package SFEpoppler-gpp
 #
@@ -33,8 +57,13 @@
 BuildRequires: %{pnm_buildrequires_SUNWcairo_devel}
 Requires:      %{pnm_requires_SUNWcairo}
 BuildRequires: %{pnm_buildrequires_SFExz_gnu}
-Requires:      SFEsigcpp-gpp-devel
 
+BuildRequires: SFEsigcpp-gpp
+Requires:      SFEsigcpp-gpp
+
+BuildRequires: SFEopenjpeg
+Requires:      SFEopenjpeg
+
 %package devel
 Summary:                 %{summary} - development files
 SUNW_BaseDir:            %{_basedir}
@@ -101,6 +130,8 @@
 %_datadir/gir-1.0
 
 %changelog
+Requires:      SFEsigcpp-gpp
+make version dependent of the actual OS
 * Mon Feb  3 2014 - Thomas Wagner
 - change (Build)Requires to %{pnm_buildrequires_SUNWcairo_devel}, %{pnm_buildrequires_SUNWgtk2_devel}
 - remove Requires: SUNWsigcpp-devel (SFEsigcpp-gpp-devel is found first in /usr/g++)
