#
# spec file for package SUNWcairo
#
# includes module(s): cairo
#
# Copyright (c) 2009, 2014, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use cairo_64 = cairo.spec
%endif

%include base.inc

%use cairo = cairo.spec

Name:                    SFEcairo-gnu
IPS_package_name:        library/desktop/gnu/cairo
Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Meta(com.oracle.info.name): %{cairo.name}
Meta(com.oracle.info.version): %{cairo.version}
Meta(com.oracle.info.description): %{cairo.summary} (/usr/gnu)
#Meta(com.oracle.info.tpno): 7377
Summary:                 Vector graphics library
Version:                 %{cairo.version}
License:                 %{cairo.license}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
##TODO## SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: library/glib2
BuildRequires: library/graphics/pixman
BuildRequires: library/zlib
BuildRequires: system/library/freetype-2
BuildRequires: system/library/fontconfig
BuildRequires: image/library/libpng
BuildRequires: x11/compatibility/links-svid
BuildRequires: x11/server/xorg
#relax dependency
#BuildRequires: developer/build/automake-111
#need minimum 1.11
BuildRequires: SFEautomake-114
##TODO## runtime requires, go read from pkgdepend's results and put it into "Requires:"

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%cairo_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%cairo.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version


%ifarch amd64 sparcv9
cd %{_builddir}/%name-%version/%{_arch64}/cairo-%{cairo.version}
cat > freetype-config <<EOF
#!/bin/sh
PKG_CONFIG_PATH=/usr/lib/%{_arch64}/pkgconfig
export PKG_CONFIG_PATH
OPT="\$1"
if [ "x\$OPT" = x--version ]; then
  OPT=--modversion
fi
exec /usr/bin/pkg-config \$OPT freetype2
EOF
chmod a+x freetype-config
%endif

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%cairo_64.build -d %name-%version/%_arch64
%endif

%cairo.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%cairo_64.install -d %name-%version/%_arch64
%endif

%cairo.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
#cd %{_builddir}/%name-%version/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%doc -d %{base_arch} cairo-%{cairo.version}/README
%doc -d %{base_arch} cairo-%{cairo.version}/AUTHORS
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.0
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.2
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.4
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.6
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.8
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/COPYING
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/COPYING-LGPL-2.1
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/COPYING-MPL-1.1
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/NEWS
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
##TODO## no manpages at the moment # %dir %attr (0755, root, sys) %{_datadir}
##TODO## no manpages at the moment # %dir %attr(0755, root, bin) %{_mandir}
##TODO## no manpages at the moment # %dir %attr(0755, root, bin) %{_mandir}/man3
##TODO## no manpages at the moment # %{_mandir}/man3/*
%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%changelog
for dir 'usr/gnu/share' with conflicting attributes:

    1 package delivers 'dir group=bin mode=0755 owner=root path=usr/gnu/share':
        pkg://localhosts11.2/library/desktop/gnu/cairo@1.12.2,5.11-0.0.175.3.1.0.5.0:20151024T203359Z
    42 packages deliver 'dir group=sys mode=0755 owner=root path=usr/gnu/share', including:
        pkg://localhosts11/file/file@5.21,5.11-0.0.175.0.0.0.2.0:20150108T030145Z

* Sat Oct 24 2015 - Thomas Wagner
- adopted from solaris userland
- prerequisite for updated poppler pdf lib
- bump to version
* Mon Dec 01 2014 - swaroop.sadare@oracle.com
- Added TPNO and modified the copyright file.
* Mon Oct 29 2012 - rohini.s@oracle.com
- Fix packaging after updating to 1.12.2.  Fix Requires/BuildRequires.
* Wed Aug 26 2009 - christian.kelly@sun.com
- Re-enable 64bit libs.
* Mon Aug 24 2009 - christian.kelly@sun.com
- Comment out 64bit libs from %files. They seem to have disappeared.
* Tue Jun 02 2009 - dave.lin@sun.com
- add 'Requires: SUNWpng-deve/SUNWxwinc' to fix bug CR6842561
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)

