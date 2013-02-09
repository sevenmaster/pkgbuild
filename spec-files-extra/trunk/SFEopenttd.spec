#
# spec file for package SFEopenttd.spec
#
%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc

%define src_name openttd

Name:           SFEopenttd
IPS_Package_Name:	games/openttd
Version:        1.2.3
Summary:        Transport system simulation game
Source:         http://binaries.openttd.org/releases/%{version}/%{src_name}-%{version}-source.tar.gz
Source1:	http://bundles.openttdcoop.org/opengfx/releases/0.4.6.1/opengfx-0.4.6.1.zip
Source2:	http://bundles.openttdcoop.org/opensfx/releases/0.2.3/opensfx-0.2.3.zip
Source3:	http://bundles.openttdcoop.org/openmsx/releases/0.3.1/openmsx-0.3.1.zip
Patch2:		openttd-02-alloca.diff
URL:		http://www.openttd.org/
Group:		Applications/Games
License:	GPLv2
SUNW_Copyright:	openttd.copyright
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

%include default-depend.inc
BuildRequires:	SFEgcc
Requires:	SFEgccruntime
BuildRequires:  SUNWlibsdl-devel
Requires:  SUNWlibsdl
BuildRequires:  SUNWpng-devel
Requires:  SUNWpng
BuildRequires:  SUNWunzip
BuildRequires:  SUNWzlib
Requires:  SUNWzlib
BuildRequires:  SUNWfontconfig
Requires:  SUNWfontconfig
BuildRequires:  SUNWfreetype2
Requires:  SUNWfreetype2
BuildRequires: SUNWdoxygen
Requires: SFElzo
BuildRequires: SFElzo
Requires: 	%{pnm_requires_SFExz_gnu}
BuildRequires:	%{pnm_buildrequires_SFExz_gnu}
BuildRequires:	SUNWgsed
BuildRequires:	SUNWgnome-desktop-prefs

%description
OpenTTD is modeled after a popular transportation business simulation game
by Chris Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.


%prep
%setup -q -n openttd-%{version}
%patch2 -p1


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

sed -e '1,$s@/usr/local@%{_prefix}@g' <config.lib >config.lib.sed
mv config.lib.sed config.lib
export CC=gcc
export CXX=g++
export CFLAGS="-I%{_includedir} -I%{_includedir}/lzo %optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
bash ./configure \
        --disable-strip \
	--without-icu \
        --prefix-dir= \
        --binary-dir=%{_bindir} \
        --data-dir=%{_datadir}/openttd \
        --icon-dir=%{_datadir}/pixmaps \
        --icon-theme-dir=%{_datadir}/icons/hicolor \
        --man-dir=%{_mandir}/man6 \
        --menu-dir=%{_datadir}/applications \
        --without-shared-dir \
        --doc-dir=%{_docdir} \
        --install-dir=$RPM_BUILD_ROOT

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install VERBOSE=1

# Remove the installed docs - we will install subset of those
rm -rf $RPM_BUILD_ROOT%{_docdir}

# install documentation
install -dpm 755 $RPM_BUILD_ROOT%{_datadir}/openttd/docs/
cp -r docs/* $RPM_BUILD_ROOT%{_datadir}/openttd/docs/

# Patch generated desktop file, as desktop-file-install doesn't know 1.1 format yet
sed -i 's/Version=1.1/Version=1.0/' media/openttd.desktop
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
        --add-category=StrategyGame \
        media/openttd.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/openttd/data

cd $RPM_BUILD_ROOT%{_datadir}/openttd/data && unzip %SOURCE1 && unzip %SOURCE2
chmod 755  $RPM_BUILD_ROOT%{_datadir}/openttd/data/open*-0.*
chmod og+r $RPM_BUILD_ROOT%{_datadir}/openttd/data/open*-0.*/*

mkdir -p $RPM_BUILD_ROOT%{_datadir}/openttd/gm

cd $RPM_BUILD_ROOT%{_datadir}/openttd/gm && unzip %SOURCE3
chmod 755  $RPM_BUILD_ROOT%{_datadir}/openttd/gm/open*-0.*
chmod og+r $RPM_BUILD_ROOT%{_datadir}/openttd/gm/open*-0.*/*


%clean
rm -rf $RPM_BUILD_ROOT


%post
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $BASEDIR/var/lib/postrun/postrun -i -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*
%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/openttd
%{_datadir}/openttd/*

%changelog
* Sat Feb 09 2013 - Milan Jurik
- bump to 1.2.3
* Sat Jan 12 2013 - Thomas Wagner
- change to pnm_buildrequires_SFExz_gnu
* Sat Jun 23 2012 - Thomas Wagner
- change to (Build)Requires pnm_requires_SFExz (solves SFExz conflict w/ compress/xz), %include packagenamemacros.inc
* Fri Apr 13 2012 - Milan Jurik
- bump to 1.1.5
* Fri Dec 23 2011 - Milan Jurik
- bump to 1.1.4
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
- bump to 1.1.3, opengfx 0.3.7
* Tue Sep 06 2011 - Milan Jurik
- bump to 1.1.2, opengfx 0.3.5
* Fri Jul 29 2011 - Alex Viskovatoff
- add missing dependency on SFEgcc
* Sun Jul 24 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Tue Jul 12 2011 - Milan Jurik
- bump to 1.1.1
* Sun May 22 2011 - Milan Jurik
- bump to 1.1.0
- disable libicu support to allow cross-version build
* Fri Nov 26 2010 - Milan Jurik
- fix music datafiles place
* Tue Nov 23 2010 - Milan Jurik
- bump to 1.0.5
* Wed Sep 15 2010 - Milan Jurik
- bump to 1.0.4
* Sat Aug 07 2010 - Milan Jurik
- update to 1.0.3
* Tue Jul 20 2010 - Milan Jurik
- update to 1.0.2
* Fri May 07 2010 - Milan Jurik
- update to 1.0.1
* Thu Apr 01 2010 - Milan Jurik
- update to 1.0.0
* Mon Mar 29 2010 - Milan Jurik
- update to 1.0.0-RC3, support for OpenTTD data files
* Wed Mar 24 2010 - Milan Jurik
- freetype from main as build dependency
* Sat jan 16 2010 - Milan Jurik
- update to 0.7.5
- disable makepend because of CR 6917536
* Sun Aug 16 2009 - Milan Jurik
- update to 0.7.2
- fix for post-scripts
* Sun Jul 05 2009 - Milan Jurik
- Initial version based on Fedora spec file
