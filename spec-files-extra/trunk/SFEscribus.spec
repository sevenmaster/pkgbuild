#
# spec file for package SFEscribus
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

%define src_name scribus

Name:           SFEscribus
IPS_Package_Name:	desktop/publishing/scribus
Summary:        Graphical desktop publishing (DTP) application
URL:		http://www.scribus.net/canvas/Scribus
Group:		Applications/Office
Version:        1.4.5
Source:		%{sf_download}/%{src_name}/%{version}/%src_name-%version.tar.bz2
License:	GPLv2
Patch1:		scribus-01-math_c99.diff
SUNW_BaseDir:   %_basedir
SUNW_Copyright: scribus.copyright
BuildRoot:      %_tmppath/%name-%version-build
%include	default-depend.inc
#Requires:	%name-root

BuildRequires: 	SFEqt-gpp-devel
Requires: 	SFEqt-gpp
BuildRequires:	SFElibiconv
Requires:	SFElibiconv
BuildRequires:	SFElcms2-gnu
Requires:	SFElcms2-gnu

BuildRequires: 	SFEcmake
##TODO## check dependency on python26 or if other versions do as well
BuildRequires: 	%{pnm_buildrequires_python_default}

BuildRequires:  %{pnm_buildrequires_SUNWfreetype2_devel}
Requires:       %{pnm_buildrequires_SUNWfreetype2}

##TODO## 
#BuildRequires:  SUNWcupsu

SUNW_BaseDir:   %_basedir
%include default-depend.inc

%description
Scribus is a GUI desktop publishing (DTP) application for Unix/Linux.


%prep
%setup -q -n %src_name-%version
%patch1 -p1
mkdir -p builddir

#look for SFElcms2 in /usr/gnu/<lib|include>
gsed -i -e 's?/usr/include?/usr/gnu/include?' -e 's?/usr/lib?/usr/gnu/lib?' cmake/modules/FindLCMS2.cmake

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
cd builddir
# Don't even think about trying to build this with Solaris Studio
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
# Use -D__C99FEATURES__ to get isfinite defined by iso/stlibc_99.h (patch1)
# Don't use -D_STDC_C99: that produces redefinition errors
# This is to avoid "error: `isfinite' is not a member of `std'"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"
export LD="/usr/bin/ld"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib  %{gnu_lib_path}"
export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++


# Use Qt Arthur, because library/desktop/cairo links to libpng12
cmake -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DPNG_PNG_INCLUDE_DIR:PATH=/usr/include/libpng14 -DCMAKE_INSTALL_PREFIX:PATH=%_prefix -DWANT_QTARTHUR=1 -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python2.6 -DPYTHON_INCLUDE_DIR:PATH=/usr/include/python2.6 -DPYTHON_LIBRARY:FILEPATH=/usr/lib/libpython2.6.so -DLCMS_LIBRARY=/usr/gnu/lib -DLCMS_INCLUDE_DIR=/usr/gnu/include ..
make -j$CPUS

%install
rm -rf %buildroot
cd builddir
make install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"
cd ..
mkdir %buildroot%_datadir/applications
cp %src_name.desktop %buildroot%_datadir/applications

# Fix spaces in filenames
cd %buildroot%{_datadir}/scribus/swatches
for i in *' '*; do mv "$i" "`echo $i | sed -e 's/ /_/g'`"; done

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%dir %attr (0755, root, bin) %_libdir
%dir %attr(0755, root, sys) %_datadir
%dir %attr(0755, root, bin) %_includedir
%dir %attr(0755, root, other) %_datadir/applications
%_datadir/applications/%src_name.desktop
%_bindir/scribus
#TODO
#%{_datadir}/gnome/apps/Applications/scribus.desktop
%dir %attr(0755, root, root) %_datadir/mime
%dir %attr(0755, root, root) %_datadir/mime/packages
%_datadir/mime/packages/scribus.xml
# TODO
#%{_datadir}/pixmaps/scribus.png
#%{_datadir}/pixmaps/scribusicon.png
%_datadir/scribus
%_includedir/scribus/
%_libdir/scribus/
%dir %attr (-, root, other) %_docdir
%_docdir/scribus
%dir %attr(0755, root, root) %_datadir/mimelnk
%dir %attr(0755, root, root) %_datadir/mimelnk/application
%_datadir/mimelnk/application/*
%_datadir/man


%changelog
* Sun Aug 16 2015 - Thomas Wagner
- add (Build)Requires pnm_buildrequires_SUNWfreetype2_devel
* Fri Mar  6 2015 - Thomas Wagner
- bump to 1.4.5, fix download extension .xz -> .tar.bz2
- change (Build)Requires: Requires: %{pnm_buildrequires_python_default}
- look for SFElcms2 in /usr/gnu/<include|lib>
* Mon Apr 14 2014 - Thomas Wagner
- change (Build)Requires: Requires: %{pnm_requires_SUNWPython26}, %include packagenamemacros.inc
* Sun Sep 01 2013 - Milan Jurik
- bump to 1.4.3
* Mon Dec 10 2012 - Logan Bruns <logan@gedanken.org>
- updated to 1.4.1
- explicitly force cmake to use python2.6 since it python3.x fails
* Sat Jun 23 2012 - Thomas Wagner
- make (Build)Requires SUNWcups SUNWlcms
* Sun Jan 08 2012 - Milan Jurik
- bump to 1.4.0
* Wed Nov  2 2011 - Alex Viskovatoff
- Bump to 1.4.0.rc6
* Tue Jul 26 2011 - Alex Viskovatoff
- Add missing (build) dependency
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* 26 Jun 2011 - Alex Viskovatoff
- Bump to 1.4.0.rc5
* 13 Apr 2011 - Alex Viskovatoff
- Update to 1.4.0.rc3; fix version name
* 29 Mar 2011 - Alex Viskovatoff
- Update to 1.4.0.rc2; use SFEqt47-gpp and SFEcmake; use Qt Arthur
* 29 Apr 2010 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial spec
