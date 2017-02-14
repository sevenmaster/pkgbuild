#
#
Name:         poppler
License:      GPL
Group:        System/Libraries

%if %{openindiana}
#Version:      0.35.0 # Have used this previously and it works
Version:      0.32.0
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
#osdistro has 1.10.2
%define cairo_version 1.10.2
%endif

%if %{omnios}
Version:      0.24.3
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
%endif

%if %{oihipster}
#stop using bcs gcc5 runtime libs - #use poppler from osdistro for now, so we don't build this spec file base-specs/poppler.spec you are looking at
Version:      0.32.0
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
%define cairo_version 1.14.6
%endif

%if %{solaris11}
# might be bumped to Version:      0.39.0
Version:      0.32.0
#Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.gz
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
#%define cairo_version 1.14.2
#1.12.2 or 1.14.2 from SFE
%define cairo_version 1.12.2
%endif

%if %{solaris12}
#Version:      0.35.0
Version:      0.32.0
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
#osdistro has 1.12.2
%define cairo_version 1.12.2
%endif

Summary:      PDF Rendering Library
# date:2005-11-29 type:feature owner:laca bugzilla:9730
#Patch1:       poppler-01-uninstalled.pc.diff
URL:          http://poppler.freedesktop.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.20.1

Requires:      cairo >= %{cairo_version}
Requires:      gtk2 >= %{gtk2_version}

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: gtk2-devel >= %{gtk2_version}

%description
Poppler is a fork of the xpdf PDF viewer developed by Derek Noonburg
of Glyph and Cog, LLC.  The purpose of forking xpdf is twofold.
First, we want to provide PDF rendering functionality as a shared
library, to centralize the maintenence effort.  Today a number of
applications incorporate the xpdf code base, and whenever a security
issue is discovered, all these applications exchange patches and put
out new releases.  In turn, all distributions must package and release
new version of these xpdf based viewers.  It's safe to say that
there's a lot of duplicated effort with the current situaion.  Even if
poppler in the short term introduces yet another xpdf derived code
base to the world, we hope that over time these applications will
adopt poppler.  After all, we only need one application to use poppler
to break even.

Second, we would like to move libpoppler forward in a number of areas
that doesn't fit within the goals of xpdf.  By design, xpdf depends on
very few libraries and runs a wide range of X based platforms.  This
is a strong feature and reasonable design goal.  However, with poppler
we would like to replace parts of xpdf that are now available as
standard components of modern Unix desktop environments.  One such
example is fontconfig, which solves the problem of matching and
locating fonts on the system, in a standardized and well understood
way.  Another example is cairo, which provides high quality 2D
rendering.

%package devel
Summary:      PDF Rendering Library
Group:        Development/Libraries
Requires:     %{name} = %{version}
Requires:     cairo-devel >= %{cairo_version}
Requires:     gtk2-devel >= %{gtk2_version}

%description devel
Poppler is a fork of the xpdf PDF viewer developed by Derek Noonburg
of Glyph and Cog, LLC.  The purpose of forking xpdf is twofold.
First, we want to provide PDF rendering functionality as a shared
library, to centralize the maintenence effort.  Today a number of
applications incorporate the xpdf code base, and whenever a security
issue is discovered, all these applications exchange patches and put
out new releases.  In turn, all distributions must package and release
new version of these xpdf based viewers.  It's safe to say that
there's a lot of duplicated effort with the current situaion.  Even if
poppler in the short term introduces yet another xpdf derived code
base to the world, we hope that over time these applications will
adopt poppler.  After all, we only need one application to use poppler
to break even.

Second, we would like to move libpoppler forward in a number of areas
that doesn't fit within the goals of xpdf.  By design, xpdf depends on
very few libraries and runs a wide range of X based platforms.  This
is a strong feature and reasonable design goal.  However, with poppler
we would like to replace parts of xpdf that are now available as
standard components of modern Unix desktop environments.  One such
example is fontconfig, which solves the problem of matching and
locating fonts on the system, in a standardized and well understood
way.  Another example is cairo, which provides high quality 2D
rendering.

%prep
#don't unpack please
%setup -q -c -T
echo %SOURCE0 | grep "xz$" && xz -dc %SOURCE0 | (cd ..; tar xf -)
echo %SOURCE0 | grep "gz$" && gzip -d < %SOURCE0 | (cd ..; tar xf -)

#%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

#paused #need to know 64-bit path as well %if opt_arch -> sed -e 's?/pkgconfig?%{_arch64}/pkgconfig?g'
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/g++/share/pkgconfig

export CFLAGS="%optflags `pkg-config --cflags-only-I cairo`"
export CXXFLAGS="%cxx_optflags `pkg-config --cflags-only-I cairo`"
#export CXXFLAGS="%cxx_optflags -D_STDC_C11 `pkg-config --cflags-only-I cairo`"
%if %( expr %{solaris11} '|' %{solaris12} )
#-D_STDC_C11_BCI solves perf-test.cc:525:44: error: 'strcpy_s' was not declared in this scope
export CXXFLAGS="$CXXFLAGS -std=c++11 -D_STDC_C11_BCI"
%endif
%if %{openindiana}
# Overwrite FLAGS for OI to include /usr/gnu/include where we keep SFE libiconv includes
export CFLAGS="%optflags -I/usr/gnu/include `pkg-config --cflags-only-I cairo`"
export CXXFLAGS="%cxx_optflags -I/usr/gnu/include `pkg-config --cflags-only-I cairo`"
%endif
export LDFLAGS="%{_ldflags}"

#configure doen't handle the "1" version libopenjpeg1 ...
export LIBOPENJPEG_CFLAGS=$( pkg-config --cflags "libopenjpeg1" )
export LIBOPENJPEG_LIBS="-lopenjpeg"

export CAIRO_CFLAGS="`pkg-config --cflags cairo`"
export CAIRO_LIBS="`pkg-config --libs cairo`"
 
echo "Debug:
PKG_CONFIG_PATH    $PKG_CONFIG_PATH
LIBOPENJPEG_CFLAGS $LIBOPENJPEG_CFLAGS
LIBOPENJPEG_LIBS   $LIBOPENJPEG_LIBS
CAIRO_CFLAGS       $CAIRO_CFLAGS
CAIRO_LIBS         $CAIRO_LIBS
CFLAGS             $CFLAGS
CXXFLAGS           $CXXFLAGS
LDFLAGS            $LDFLAGS
PATH               $PATH
_arch64            %_arch64
bld_arch           %bld_arch
base_isa           %base_isa
"

echo "Note: editing out AC_CHECK_FUNCS(strcpy_s, strcat_s) from configure.ac. Else this fails with not switching on defines in std include files."
gsed -i.bak '/AC_CHECK_FUNCS.*strcpy_s/ s/^dnl //' configure.ac
autoconf

# Building documentation currently breaks build
./configure --prefix=%{_prefix}		\
	    --datadir=%{_datadir}       \
            --libdir=%{_libdir}         \
	    --sysconfdir=%{_sysconfdir} \
	    --enable-poppler-glib	\
            --enable-poppler-qt4       \
            --disable-poppler-qt5       \
            --disable-static            \
	    --mandir=%{_mandir}	        \
            --enable-zlib               \
	    --disable-gtk-doc           \
            --enable-xpdf-headers       \
#            %{gtk_doc_option}

#stupid g-ir-scanner doesn't follow ENV variables nor what configure found.
#push it a but to make it stuble over cairo.h in /usr/gnu/include/cairo
gsed -i.bak -e '/INTROSPECTION_SCANNER_ARGS/ s?$? `pkg-config --cflags cairo` ?' glib/Makefile.am

gmake V=2 -j$CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_includedir}/poppler/
%{_libdir}/*.so
%{_libdir}/pkgconfig/
%{_datadir}/gtk-doc

%changelog
* Tue Nov  1 2016 - Thomas Wagner
- re-enable SFEpoppler-gpp 0.32.0 on OIH 2016, as GCC5 runtime libs are not matching when building LO4
* Fri Sep 30 2016 - pjama
- Add config to define Version and cairo_version for openindiana
- include /usr/gnu/include in CFLAGS path to find SFElibiconv headers for openindiana
* Sat Apr 23 2016 - Thomas Wagner
- revert commit 6199 as it broke compile on most osdistro by removing code switching the version based on osdistro
- merge in only selected changes from commit 6199
* Fri Feb  2 2016 - Alex Viskovatoff rev 6199
- bump to version 0.39.0 for all osdistro
* Mon Jan  4 2016 - Thomas Wagner
- change (Build)Requires to pnm_buildrequires_SFEopenjpeg
- add -D_STDC_C11_BCI -std=c++11 as well (S11.3)
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
- Update to 0.24.3; build poppler-qt4
* Fri Aug  5 2011 - Alex Viskovatoff
- Update to 0.14.5
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 0.6.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 0.6.1. Remove upstream patch, 02-fixcast.
* Mon Sep 03 2007 - brian.cameron@sun.com
- Bump to 0.6.0
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 0.5.91. Remove upstream patch, 02-c++issues.
* Wed Jul 04 2007 - darren.kenny@sun.com
- Remove poppler-02-glib-2.diff since it appears to be already in 0.5.9.
- Add new poppler-02-c++issues.diff patch to fix some C++ Compilation issues
  in 0.5.9.
* Fri May 18 2007 - laca@sun.com
- explicitely disable qt/qt4 support
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Sun Jun 11 2006 - laca@sun.com
- Bump to 0.5.3 to fix the build of evince
- Add patch, 03-glib-2, so that configure looks for glib-2.0, not the old glib.
  Freedesktop bugzilla #8600.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 0.5.1 as required by evince 0.5.2.
* Sun Jan 22 2006 - damien.carbery@sun.com
- Bump to 0.5.0, as required by evince 0.5.0.
- Point to 'm4' dir in aclocal call.
- Remove upstream patch, 01-freetype. Renumber others.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.4.4.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Remove upstream patch, 02-macrofix.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 0.4.3
* Tue Nov 29 2005 - laca@sun.com
- add uninstalled.pc.diff patch so that poppler can be in the same Solaris
  pkg as evince
* Thu Oct 13 2005 - damien.carbery@sun.com
- Enable poppler-glib as it is required by evince.
* Fri Sep 30 2005 - brian.cameron@sun.com
- Bump to 0.4.2
* Tue Sep 20 2005 - laca@sun.com
- add FREETYPE_CFLAGS to CFLAGS where needed
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 0.4.0.
* Tue Aug 16 2005 - glynn.foster@sun.com
- Initial spec file for poppler
