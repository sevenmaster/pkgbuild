
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
Summary:                 PDF rendering library (/usr/g++)
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
BuildRequires: %{pnm_buildrequires_SFExz_gnu}

BuildRequires: SFEsigcpp-gpp
Requires:      SFEsigcpp-gpp

BuildRequires: SFEopenjpeg
Requires:      SFEopenjpeg

BuildRequires: SFEpoppler-data-gpp
Requires:      SFEpoppler-data-gpp

#note: Solaris 11 cairo is too old to build more fresh poppler
%if %{solaris11}
#can be built with studio or gcc (on gcc_only distros like OIHipster)
BuildRequires: SFEcairo-gpp
Requires:      SFEcairo-gpp
%endif

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
export PATH=/usr/g++/bin:$PATH
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
* Fri Nov 13 2015 - Thomas Wagner
- find cairo cflags/includes by pkg-config --cflags 
- add to PKG_CONFIG_PATH /usr/g++/share/pkgconfig
- add to CXXFLAGS -D_STDC_C11
- add to CXXFLAGS -D_STDC_C11_BCI (else strcpy_s is not enabled on S12)
- fix unpacking gz / gzip
- change BuildRequires to SFEcairo-gpp in all cases, cairo is now in /usr/g++, remove pnm_macro for SUNWcairo
- add BuildRequires SFEpoppler-data-gpp
* Sun Oct 25 2015 - Thomas Wagner
- bump version to 0.32.0 (S11 only!)
- add (Build)Requires SFEpoppler-gpp.spec (S11 only!)
- add workaround for g-ir-scanner not honouring CFLAGS when searching for cairo.h
- to get GfxState.h --enable-xpdf-headers
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
