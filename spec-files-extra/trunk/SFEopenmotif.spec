#
# spec file for package SFEopenmotif
#

# Build with gcc since Solaris has no need for this package, since Solaris can use the commercial version
# Install in /usr instead of /usr/g++, not observing the SFE convention, since this spec is intended especially
# for OpenIndiana, which does not follow it.
# This package is NOT intended for deployment on Oracle Solaris (although it does build there).

# A list of Motif applications can be found here: http://motif.ics.com/book/export/html/31

## This package does not currently build on OI hipster:
##
## In file included from XmRenderTI.h:33:0,
##                  from Label.c:82:
## /usr/include/X11/Xft/Xft.h:39:22: fatal error: ft2build.h: No such file or directory
##  #include <ft2build.h>
##
## This is even though ft2build.h is in /usr/include/freetype2
## Explicitly supplying that path to ./configure does not work.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define src_name        motif
%define X11_DIR %{_prefix}/X11

Name:                    SFEopenmotif
IPS_package_name:	 sfe/library/motif
Summary:                 Publicly licensed version of Motif, the industry standard user interface toolkit for UNIX systems.
Version:                 2.3.4
Source:                  %sf_download/%src_name/%src_name-%version-src.tgz
URL:                     http://motif.ics.com/motif
License:                 LGPL
#Patch0:                  %{src_name}-01-%{version}.diff
#Patch1:                  %{src_name}-02-compatibility.diff
#Source1:                 XmStrDefs21.ht

%include default-depend.inc

Requires: SUNWcsu
Requires: SUNWxwxft
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
BuildRequires: image/library/libpng
Requires: SUNWfontconfig
BuildRequires: system/library/freetype-2
Conflicts: SUNWmfrun
Conflicts: SUNWmfdev

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
Conflicts: SUNWmfdev

%prep
%setup -q -n %src_name-%version
#%patch0 -p1

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./autogen.sh
./configure --prefix=%{X11_DIR} \
            --mandir=%{X11_DIR}/share/man \
            --sysconfdir=%{_sysconfdir} \
            --enable-xft \
            --enable-jpeg \
            --enable-png \
	    --disable-static

#cat %{PATCH1} | gpatch -p1 --fuzz=0
#cp %{SOURCE1} lib/Xm

make

%install
rm -rf %buildroot
make install DESTDIR=$RPM_BUILD_ROOT

rm %buildroot%X11_DIR/lib/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{X11_DIR}
%dir %attr (0755, root, bin) %{X11_DIR}/bin
%{X11_DIR}/bin/*
%dir %attr (0755, root, bin) %{X11_DIR}/lib
%{X11_DIR}/lib/lib*.so*
%X11_DIR/lib/X11
%dir %attr(0755, root, bin) %{X11_DIR}/share
%dir %attr(0755, root, bin) %{X11_DIR}/share/man
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man1
%{X11_DIR}/share/man/man1/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man3
%{X11_DIR}/share/man/man3/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man4
%{X11_DIR}/share/man/man4/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man5
%{X11_DIR}/share/man/man5/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/manm
%{X11_DIR}/share/man/manm/*

%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/pixmaps
%{X11_DIR}/share/Xm/pixmaps/*
%X11_DIR/share/Xm/drag_and_drop

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{X11_DIR}
%dir %attr (0755, root, bin) %{X11_DIR}/include
%{X11_DIR}/include/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/ButtonBox/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Color/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Column/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Exm
%{X11_DIR}/share/Xm/Exm/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Ext18list
%{X11_DIR}/share/Xm/Ext18list/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Icon/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Outline/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Paned2/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Tabstack/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Tree/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/airport/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/animate/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/autopopups/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/combo2/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/draw/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/earth/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/filemanager/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/fileview/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/fontsel/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/getsubres/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/helloint/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/hellomotif/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/i18ninput/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/panner/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/periodic/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/piano/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/sampler2_0/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/setDate/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/todo/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/tooltips/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/wsm/*

%changelog
* Fri Dec 18 2015 - Alex Viskovatoff
- Update to 2.3.4; add IPS package name
* Thu Feb 07 2008 - moinak.ghosh@sun.com
- Rework to add compatibility with Solaris Motif.
- Add devel package.
- Change install prefix to /usr/X11
- Update dependencies.
- Thu Feb 07 2008 - pradhap (at) gmail.com
- Initial openmotif spec file.

