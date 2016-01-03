#
# spec file for package SFEcairo-gpp
#
# includes module(s): cairo
#

%include Solaris.inc
%include usr-g++.inc
# g++ packages are built with gcc
%define cc_is_gcc 1
%include packagenamemacros.inc
%include base.inc
%include pkgbuild-features.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use cairo_64 = cairo.spec
%endif

%include base.inc

%use cairo = cairo.spec

Name:                    SFEcairo-gpp
IPS_package_name:        library/desktop/g++/cairo
Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Meta(com.oracle.info.name): %{cairo.name}
Meta(com.oracle.info.version): %{cairo.version}
Meta(com.oracle.info.description): %{cairo.summary} (/usr/g++)
#Meta(com.oracle.info.tpno): 7377
Summary:                 Vector graphics library
Version:                 %{cairo.version}
License:                 %{cairo.license}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
##TODO## SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEglib2-gpp-devel
BuildRequires: SFEpixman-gpp-devel
BuildRequires: library/zlib
BuildRequires: system/library/freetype-2
BuildRequires: system/library/fontconfig
BuildRequires: image/library/libpng
BuildRequires: x11/compatibility/links-svid
BuildRequires: x11/server/xorg
#relax dependency
#BuildRequires: developer/build/automake-111
#need minimum 1.11
BuildRequires: SFEautomake-115
##TODO## runtime requires, go read from pkgdepend's results and put it into "Requires:"

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}


#targets sfe.opencsw.org produced binaries. make our old gnu/cairo go away.
%if %{solaris11}
#START automatic renamed package  (remember to add as well %actions)
# create automatic package with old name and "renamed=true" in it
%include pkg-renamed.inc

#STRONG NOTE:
#remember to set in this spec file the %action which
#adds the depend rule in a way that the new package 
#depends on the old package in a slightly updated branch
#version and has the flag "renamed=true" in it

#This is specific to Solaris 11 only
%package noinst-1
Summary:     renamed to library/g++/cairo and relocated to (/usr/g++)
#if oldname is same as the "Name:"-tag in this spec file:
#use the SFExyz package name, it is only a dummy!
#example_ab# %define renamed_from_oldname      %{name}
#example_ab# %define renamed_from_oldname      SFEstoneoldpkgname
#
#example_a#  %define renamed_to_newnameversion category/newpackagename = *
#or
#example_b#  %define renamed_to_newnameversion category/newpackagename >= 1.1.1
#
#do not omit version equation!
%define renamed_from_oldname      library/desktop/gnu/cairo
%define renamed_to_newnameversion library/desktop/g++/cairo = *
%include pkg-renamed-package.inc

#%description noinst-1
#there has been a problem for gnome-terminal with libvte.so which loads
#our cairo library from /usr/gnu/lib/ in error. Our cairo is now
#relocated to /usr/g++/lib where libvte doesnt search for cairo.

#END automatic renamed package  (remember to add as well %actions)


#list *all* old package names here which could be installed on
#user's systems
#stay in sync with section above controlling the "renamed" packages
#example: SFEurxvt@9.18-5.11,0.0.175.0.0.0.2.1 (note: last digit is incremented calculated
#on the branch version printed by pkg info release/name

#list all the old published package name wich need to go away with upgrade to our new package name/location
#pkg://localhosts11/library/desktop/gnu/cairo@1.12.2,5.11-0.0.175.2.12.0.3.0:20151101T000000Z ---
#pkg://localhosts11/library/desktop/gnu/cairo@1.12.2,5.11-0.0.175.2.12.0.3.0:20151030T215906Z i--

%actions
depend fmri=library/desktop/gnu/cairo@1.12.2,5.11-0.0.175.2 type=optional
#depend fmri=SFEotheroldnamesgohere@%{ips_version_release_renamedbranch} type=optional

%endif
##END solaris 11


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
export CC=gcc
export CXX=g++

PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
export LDFLAGS="%_ldflags -L/usr/g++/lib/amd64 -R/usr/g++/lib/amd64"
export PKG_CONFIG_PATH="%_pkg_config_path64"
%cairo_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="%_pkg_config_path"
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
%_bindir/cairo-trace
%_bindir/%_arch64/cairo-trace
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%_libdir/cairo/libcairo-trace.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%_libdir/%_arch64/cairo/libcairo-trace.so*
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
* Fri Dec 28 - Alex Viskovatoff <herzen@imap.cc>
- Use newer glib2 in /usr/g++; build with gcc to maintain consistency
- create automatic renamed-to package
* Fri Nov  6 2015 - Thomas Wagner
- relocate usr-gpp.inc to stop gnome-terminal crash cia libvte.so loading our new libcairo.so
- make automatic renamed packge to remove old library/desktop/gnu/cairo in case we are on S11
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

