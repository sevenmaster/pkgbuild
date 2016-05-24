#
# spec file for package SFEwine.spec
#
# includes module(s): wine
#
# Owner: lewellyn
#
# Confirmed build of Wine 1.6.2 on oi_151a/GCC 4.6.4 07/09/14  - Ken Mays
# Confirmed build of Wine 1.7.10 on oi_151a/GCC 4.7.3 1/3/14   - Ken Mays
#                         1.9.10 on S11.3 + OI-H 2015.0.1.1    - tom68

%include Solaris.inc

%define src_url		%{sf_download}/%{sname}

%include packagenamemacros.inc

# To attempt building a certain wine version, as opposed to the latest
# Wine version available from Sourceforge, pass the version as an argument.
# example version number: 1.6.2
# $ pkgtool build SFEwine --define 'version 1.6.2'

# In case of an unstable wine version, temporarily set this to the
# last-known-good version. This should be reverted the next stable version.
# %if %{!?version:1}
# 	%define version 1.7.22
# %endif

#%if %{!?version:1}
#	%define version %{!?version:%( version=`wget -O - "ftp://ibiblio.org/pub/linux/system/emulators/wine/wine.lsm" 2>/dev/null | grep "Version: " | head -1 | sed -e 's,^Version: ,,'`; if [ "$version" = "" ]; then version=`ls %{_sourcedir}/wine-*.tar.bz2 | sed -e 's,^.*wine-,,' -e 's,\.tar\.bz2,,' | tail -1`; fi; echo $version )}
#%endif

Name:                   SFEwine
Summary:                Windows API compatibility and ABI runtime
IPS_package_name:       desktop/wine
Group:                  Desktop (GNOME)/Sessions
Version:                1.9.10
URL:                    http://www.winehq.org/
Source:                 http://downloads.sourceforge.net/project/wine/Source/wine-%{version}.tar.bz2
#
# See: http://lists.freedesktop.org/archives/tango-artists/2009-July/001974.html
#
# See http://wiki.winehq.org/Gecko for which version to use.
#
Source1:		http://winetricks.org/winetricks
Source2:                %{src_url}/%{sname}_gecko-2.24-x86.msi
Source3:		%{src_url}/%{sname}_gecko-2.24-x86_64.msi
Source4:    		http://kegel.com/wine/wisotool
Source100:              wine.directory
Source101:              winetricks.desktop
Source102:              wine-appwiz.desktop
Source103:              wine-cmd.desktop
Source104:              wine-notepad.desktop
Source105:              wine-regedit.desktop
Source106:              wine-taskmgr.desktop
Source107:              wine-winecfg.desktop
Source108:              wine-winefile.desktop
Source109:              wine-winemine.desktop
Source110:              wine-wordpad.desktop
Source1000:             wine-svg-icons.tar.bz2
Patch1:			wine-01-solaris.diff
#undef GS from sys/regset.h - only recent illumos distro have fix for this namespace pollution
Patch4:                 wine-04-d3d10effect.h-undef_GS.diff
NoSource:		1
Group:			System/Virtualization
License:		LGPL
SUNW_HotLine:		http://www.winehq.org/help
SUNW_Copyright:		%{name}.copyright
ExclusiveArch:		i386 amd64
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-camera-devel
Requires:	SUNWgnome-camera
BuildRequires:	SUNWhea
Requires:	SUNWhal
BuildRequires:	SUNWdbus-devel
Requires:	SUNWdbus
Requires:	SUNWxorg-clientlibs
BuildRequires:	SUNWxorg-headers
Requires:	SUNWxorg-mesa
BuildRequires:	SUNWjpg-devel
Requires:	SUNWjpg
BuildRequires:	SUNWpng-devel
Requires:	SUNWpng
Requires:	SUNWlxml
Requires:	SUNWlxsl
BuildRequires:	%{pnm_buildrequires_SUNWcups}
Requires:	%{pnm_requires_SUNWcups}
BuildRequires:  %{pnm_buildrequires_SUNWsane_backend_devel}
Requires:       %{pnm_requires_SUNWsane_backend}
BuildRequires:  %{pnm_buildrequires_SUNWncurses_devel}
Requires:       %{pnm_requires_SUNWncurses}
BuildRequires:  %{pnm_buildrequires_SUNWopenssl_include}
Requires:       %{pnm_requires_SUNWopenssl_libraries}
#BuildRequires:	SUNWgnutls-devel
#Requires:	SUNWgnutls
#use uptodate SFEgnutls
BuildRequires:  SFEgnutls-devel
Requires:       SFEgnutls
Requires:	SUNWfreetype2
Requires:	SFElibaudioio
BuildRequires:  SFElibgsm-devel
Requires:       SFElibgsm
Requires:       SFEmpg123
Requires:       SFEopenal
Requires:       SUNWaudh
BuildRequires:	SFElcms2-gnu
Requires:	SFElcms2-gnu
BuildRequires:  x11/library/libxcursor
Requires:       x11/library/libxcursor

%package devel
Summary:                 wine - developer files, /usr
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n %{sname}-%{version}
%setup -n %{sname}-%{version} -D -T -a 1000
%patch1 -p1
%patch4 -p1

#rework configure to get typeof -->> __typeof__ effective or get xrandr, xinerama, gnutls, libpng ... not detected propperly
#error: invalid storage class for function 'typeof'
gsed -i.bak_typeof \
   -e 's?typeof?__typeof__?g'  \
   configure.ac

gsed -i.bak_boolean_t \
   -e '/^typedef BOOL boolean_t/ s?^?// ?' \
   programs/winedbg/db_disasm64.c

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=gcc
export CXX=g++

#
# I retuned for GCC 4.5.3/4.6 optimizations for wider usage. (kmays)
#

####export CFLAGS="-std=c99 -fextended-identifiers -g -Os -pipe -fno-omit-frame-pointer -I/usr/include -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -Xlinker -pthread" 
####export LDFLAGS="-L/lib -R/lib -L/usr/lib -R/usr/lib %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path}"
#try minimalistic, port.o would othervise not export ASM function wine_call_on_stack
#bad /usr/bin/nm port.o
#[21]    |         0|         0|NOTY |GLOB |0    |UNDEF  |wine_call_on_stack
#good
#[30]    |       176|         0|NOTY |GLOB |0    |1      |wine_call_on_stack

#/usr/bin/nm libs/wine/port.o | grep "UNDEF.*wine_call_on_stack" && echo "Fatal Error: port.o does not define wine_call_on_stack propperly. check -stdc=gnu99 CFLAGS"


#pkgbuild@s11175> /usr/gcc/4.9/bin/gcc -c -o port.o port.c -I. -I../../include -D__WINESRC__ -DWINE_UNICODE_API=""    -Wall  -std=c99 -D__EXTENSIONS__ -I/usr/include -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include 
##THIS IS AN GNU-nm example!
#pkgbuild@s11175> /usr/gnu/bin/nm port.o 
#00000071 T __asm_dummy_wine_call_on_stack
#         U abort
#         U asm
#00000000 D libwine_port_functions
#         U memcpy
#00000000 b pthread_functions
#         U wine_call_on_stack
#         U wine_cp_enum_table
#         U wine_cp_get_table
#         U wine_cp_mbstowcs
#         U wine_cp_wcstombs
#         U wine_cpsymbol_mbstowcs
#         U wine_cpsymbol_wcstombs
#         U wine_fold_string
#00000000 T wine_pthread_get_functions
#00000029 T wine_pthread_set_functions
#00000052 T wine_switch_to_stack
#         U wine_utf8_mbstowcs
#         U wine_utf8_wcstombs
#pkgbuild@s11175> /usr/gcc/4.9/bin/gcc -c -o port.o port.c -I. -I../../include -D__WINESRC__ -DWINE_UNICODE_API=""    -Wall  -std=gnu99 -D__EXTENSIONS__ -I/usr/include -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include 
#pkgbuild@s11175> /usr/gnu/bin/nm port.o 
#00000071 T __asm_dummy_wine_call_on_stack
#         U abort
#00000000 D libwine_port_functions
#         U memcpy
#00000000 b pthread_functions
#00000074 T wine_call_on_stack
#         U wine_cp_enum_table
#         U wine_cp_get_table
#         U wine_cp_mbstowcs
#         U wine_cp_wcstombs
#         U wine_cpsymbol_mbstowcs
#         U wine_cpsymbol_wcstombs
#         U wine_fold_string
#00000000 T wine_pthread_get_functions
#00000029 T wine_pthread_set_functions
#00000052 T wine_switch_to_stack
#         U wine_utf8_mbstowcs
#         U wine_utf8_wcstombs
#pkgbuild@s11175> exit 1
#exit


#get PATH_MAX with __EXTENSIONS__
export CFLAGS="-std=gnu99 -D__EXTENSIONS__ -I/usr/include -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -Xlinker -pthread"
export LDFLAGS="%{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path}"
#try gnuld
#export LD=/usr/gnu/bin/ld

#try gnu ar
export AR=/usr/gnu/bin/ar

#rework configure to get typeof -->> __typeof__ effective or get xrandr, xinerama, gnutls, libpng ... not detected propperly
autoconf --force
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-cups=/usr            \
	    --with-openssl=/usr/sfw     \
	    --without-capi		\
	    --with-cms			\
	    --without-coreaudio		\
	    --with-cups			\
	    --with-curses		\
	    --with-fontconfig		\
	    --with-freetype		\
	    --with-gphoto		\
	    --with-glu			\
	    --with-gnutls		\
	    --with-gsm			\
	    --with-hal			\
	    --with-jpeg			\
	    --without-ldap              \
	    --with-mpg123		\
	    --with-opengl		\
	    --with-openssl		\
	    --with-oss			\
	    --with-png			\
	    --with-pthread		\
	    --with-sane			\
	    --with-xcomposite		\
	    --with-xcursor		\
    	    --with-xinerama		\
	    --with-xinput		\
	    --with-xml			\
	    --with-xrandr		\
	    --with-xrender		\
	    --with-xshape		\
	    --with-xshm			\
	    --with-xslt			\
	    --with-xxf86vm		\
	    --with-x


#intetional
gmake -j$CPUS V=2 
gmake -j$CPUS V=2 || { [ -f libs/wine/port.o ] && /usr/bin/nm libs/wine/port.o | grep "UNDEF.*wine_call_on_stack" && echo "Fatal Error: port.o does not define wine_call_on_stack propperly. check -stdc=gnu99 CFLAGS"; exit 111; }


%install
# First, install wine.
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

# Then, it's time for winetricks
#mkdir -p $RPM_BUILD_ROOT%{_bindir}
#install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir} # winetricks
#rm %{SOURCE1} # So it's freshly downloaded next time, as it's straight from svn

# Now we deal with Gecko & wisotool.
#mkdir $RPM_BUILD_ROOT%{_datadir}/%{sname}/gecko
#install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{sname}/gecko/ # gecko
#install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/%{sname}/gecko/ # gecko-64
#install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/%{sname}/gecko/ # wisotool

# Next, deal with the icons.
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
# The default wine icon is... ugly.
# When it gets updated, this should be about the right thing to do, instead.
# install -m 0644 programs/winemenubuilder/wine.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine.xpm
# And, since the program icons are also ugly, fix them up too. None for winecfg; using wine.svg
#install -m 0644 wine-svg-icons/oic_winlogo-svg/oic_winlogo-48.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine.svg
#install -m 0644 wine-svg-icons/wcmd.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-cmd.svg
#install -m 0644 wine-svg-icons/notepad-svg/notepad.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-notepad.svg
#install -m 0644 wine-svg-icons/regedit/regedit-48.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-regedit.svg
#install -m 0644 wine-svg-icons/taskmgr.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-taskmgr.svg
#install -m 0644 wine-svg-icons/winefile.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-winefile.svg
#install -m 0644 wine-svg-icons/winemine.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-winemine.svg
#install -m 0644 wine-svg-icons/wordpad-svg/wordpad-48.svg $RPM_BUILD_ROOT%{_datadir}/pixmaps/wine-wordpad.svg
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps 2>&1
#install -m 0644 wine-svg-icons/wcmd.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/wine-cmd.svg
#install -m 0644 wine-svg-icons/notepad-svg/notepad.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/wine-notepad.svg
#install -m 0644 wine-svg-icons/taskmgr.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/wine-taskmgr.svg
#install -m 0644 wine-svg-icons/winefile.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/wine-winefile.svg
#install -m 0644 wine-svg-icons/winemine.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/wine-winemine.svg
#for size in 16 22 32 48; do
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps 2>&1
#install -m 0644 wine-svg-icons/oic_winlogo-svg/oic_winlogo-${size}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/wine.svg
#install -m 0644 wine-svg-icons/regedit/regedit-${size}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/wine-regedit.svg
#install -m 0644 wine-svg-icons/wordpad-svg/wordpad-${size}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/wine-wordpad.svg
#done
#for size in 16 24 32 48; do
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps 2>&1
#install -m 0644 wine-svg-icons/humanity-folder/humanity-folder-${size}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/wine-humanity-folder.svg
#done
#for size in 16 22 32; do
#install -m 0644 wine-svg-icons/notepad-svg/notepad-${size}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/wine-notepad.svg
#done
#for size in 32 48; do
#install -m 0644 wine-svg-icons/appwiz/appwiz-${size}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/wine-appwiz.svg
#done

# Finally, the menu items.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/desktop-directories
#install -m 0644 %{SOURCE100} $RPM_BUILD_ROOT%{_datadir}/desktop-directories # wine.directory
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
#install -m 0644 %{SOURCE101} $RPM_BUILD_ROOT%{_datadir}/applications # winetricks.desktop
#install -m 0644 %{SOURCE102} $RPM_BUILD_ROOT%{_datadir}/applications # wine-appwiz.desktop
#install -m 0644 %{SOURCE103} $RPM_BUILD_ROOT%{_datadir}/applications # wine-cmd.desktop
#install -m 0644 %{SOURCE104} $RPM_BUILD_ROOT%{_datadir}/applications # wine-notepad.desktop
#install -m 0644 %{SOURCE105} $RPM_BUILD_ROOT%{_datadir}/applications # wine-regedit.desktop
#install -m 0644 %{SOURCE106} $RPM_BUILD_ROOT%{_datadir}/applications # wine-taskmgr.desktop
#install -m 0644 %{SOURCE107} $RPM_BUILD_ROOT%{_datadir}/applications # wine-winecfg.desktop
#install -m 0644 %{SOURCE108} $RPM_BUILD_ROOT%{_datadir}/applications # wine-winefile.desktop
#install -m 0644 %{SOURCE109} $RPM_BUILD_ROOT%{_datadir}/applications # wine-winemine.desktop
#install -m 0644 %{SOURCE110} $RPM_BUILD_ROOT%{_datadir}/applications # wine-wordpad.desktop

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/desktop-directories
%{_datadir}/wine
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon May 23 2016 - Thomas Wagner
- bump to 1.9.10
- remove/change to (Build)Requires -SUNWlcms -SUNWgnutls pnm_.*SUNWcupsu pnm.*SUNWsane-backendu
- remove double define typedef BOOL boolean_t
- port.o w/o exported wine_call_on_stack caused by -std=c99, fixed by -std=gnu99 - yes this changes undefined function 
- go with a shortened CFLAGS for now, -std=gnu99 -D__EXTENSIONS__ for PATH_MAX
- add check for propperly exported function wine_call_on_stack if make fails
* Wed Jan 20 2016 - Thomas Wagner
- bump to 1.9.1
- remove "-i" (ignore LD_LIBRARY_PATH) from LDFLAGS as it makes configure fail on testing X11 funcs like xcursor
- add -pthread to CFLAGS
- change  typeof -->> __typeof__ in configure.ac, run autoconf --force
- add patch4 wine-04-d3d10effect.h-undef_GS.diff needed for non-illumos distro
* Sat Mar  7 2015 - Thomas Wagner
- bump to 1.7.38
- change (Build)Requires to %{pnm_requires_SUNWopenssl_include}, %include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_SUNWncurses_devel}
* Wed Jul 9 2014 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.22
* Tue Feb 11 2014 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.12
* Fri Jan 25 2014 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.11
* Fri Jan 3 2014 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.10
* Fri Dec 20 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.9
* Mon Dec 9 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.8
* Mon Dec 1 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.7
- Added patches/wine-01-solaris.diff
* Fri Nov 15 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.6
* Sat Jan 19 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.5.22
* Fri Jan 4 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.5.21
* Sat Jun 16 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4.1
* Wed Mar 7 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4
- MS Office 2010/Adobe Photoshop CS5 Extended tested
* Sat Mar 3 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4-rc6
* Tue Feb 28 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4-rc5
* Sun Feb 19 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4-rc4
* Wed Feb 14 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4-rc3
* Sat Feb 4 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4-rc2
* Sat Jan 28 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4-rc1
- Fixed link due to temp issue naming of 1.3.38/1.4rc1 release
- Autocad 2012, Nvidia 290.10 driver tested 
* Thu Jan 26 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.37
* Mon Jan 02 2012 - Milan Jurik
- fix packaging
* Sun Jan 1 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.36
* Fri Dec 2 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.34
* Mon Oct 22 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.31
* Mon Oct 11 2011 - Alex Viskovatoff
- Add IPS_package_name
* Mon Oct 11 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.30
* Mon Oct 3 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.29
* Tue Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.28
* Wed Aug 31 2011 - Thomas Wagner
- fix download URL for Source2 + Source3 wine_gecko-1.3-x86.msi + wine_gecko-1.3-x86_64.msi
* Tue Aug 30 2011 - Ken Mays <kmays2000@gmail.com>
- Enabling SFE-vlc fixes Skype 5.5 & MediaMonkey 3.2.4 
* Sat Aug 27 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.27
- Compiled cleanly on oi_151.
- Added wine_gecko-1.3-x86_64.msi 
* Fri Aug 26 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.3.26
- Test build completed cleanly on oi_151 with GCC 3.4.3
* Tue Jun 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped Wine 1.3.21 with fixed links to Wine-Gecko 1.2.0.
- Needs more rework resolution to Bugs #2963445,2874868,2019193. 
- Relaxed GCC optimizations for wider CPU compatibility (Pentium4 and higher)
* Fri Mar 19 2010 - matt@greenviolet.net
- Remove patch for Wine bug 20714. 1.1.41 has a fix.
* Fri Mar 05 2010 - matt@greenviolet.net
- Add wine-gecko.
* Wed Mar 03 2010 - matt@greenviolet.net
- Package SVG icons locally.
- Add new icon for wine folders.
- Attempted patch for http://bugs.winehq.org/show_bug.cgi?id=20714
- Add dependency on SFElibgsm.
- Add dependency on SFEopenal.
- Remove autoheader/autoconf invocation.
- Comment out aclocal from packaging.
- Explicitly declare which modules to configure with.

* Tue Aug 25 2009 - matt@greenviolet.net
- Add dependency on SFEmpg123, as it will no longer
  be included with wine as of 1.1.29, and is required for
  winemp3.acm (to allow DirectShow playback of MP3 files). See
  http://source.winehq.org/git/wine.git/?a=commit;h=db71d7c083dccd0e3f1cf43aa1034c9a46a70715

* Fri Aug 22 2009 - matt@greenviolet.net
- Fix the version detection logic to hopefully bypass the mirror system
- Allow packaging with an empty aclocal

* Thu Aug 20 2009 - matt@greenviolet.net
- Allow overriding automatic versioning
- Add Winetricks and Wine applications to the menus
- Fix configure flags; force CUPS and OpenSSL
- Jump to SFEgcc for gcc4 (back to /usr/gnu/bin)
- Disable Xshm due to X server bugs in current Xorg
- Clean up %post tasks
- A bit of compile/link flags updating
- Remove dependency on SFEgxmessage as it is no longer required by winetricks
- Clean up winetricks prep/install
- Move winetricks to Source1 (working around pkgbuild bug, still)
- Change maintainership to myself
* Wed Aug 12 2009 - matt@greenviolet.net
- Remove obsolete patches
- Clean up configure options
- Remove old freetype deps
- Add dependency SFEgxmessage currently needed for winetricks fallback messages
- Force winetricks to be redownloaded each build, as filename doesn't change
- Remove soundcard.h, as Boomer's is serviceable and it's unneeded pre-Boomer
- Auto-version based on newest (topmost) version number reference on sf.net
- Install icons for wine
- Changed summary to be more descriptive
- Added a bit of metainformation "sugar" for completeness
- Enable gnutls, as disabling it causes loss of functionality
* Mon Jun 01 2009 - trisk@forkgnu.org
- Add patch4
* Sun May 31 2009 - andras.barna@gmail.com
- Add SFEcabextract dep needed by winetricks
* Sun May 31 2009 - trisk@forkgnu.org
- Use included soundcard.h
- Use winetricks from trunk
- Update patch2
- Disable patch101
- Explicitly disable GnuTLS to prevent schannel-related crashes
- Add SUNWncurses dependency
* Sat May 30 2009 - andras.barna@gmail.com
- bump to 1.1.22
* Sat Apr 11 2009 - andras.barna@gmail.com
- bump to 1.1.19
* Tue Mar 24 2009 - andras.barna@gmail.com
- fix Requires, disable patch2 (needs rework?)
* Mon Mar 16 2009 - andras.barna@gmail.com
- Bump to 1.1.17, disable patch3, it's fixed upstream
* Sun Jan 25 2009 - Thomas Wagner
- Bump to 1.1.13
- rework patch3 wine-03-iphlpapi.diff for 1.1.13 - could update bug http://bugs.winehq.org/show_bug.cgi?id=14185
* Mon Dec 15 2008 - halton.huo@sun.com
- Bump to 1.1.10
* Mon Nov 17 2008 - halton.huo@sun.com
- Bump to 1.1.8
- Remove upstreamed patch and reorder
* Thu Jul 31 2008 - trisk@acm.jhu.edu
- Bump to 1.1.2
- Pause patch7 (partially upstreamed), add patch8
* Wed Jul 16 2008 - trisk@acm.jhu.edu
- Bump to 1.1.1
* Wed Jul 09 2008 - trisk@acm.jhu.edu
- Bump to 1.1.0
- Drop patch1 (upstreamed), patch2 (unnecessary)
* Thu Jun 19 2008 - trisk@acm.jhu.edu
- Add patch7, remove mapfile hack
* Tue Jun 17 2008 - trisk@acm.jhu.edu
- Bump to 1.0
- Add patch1
- Add winetricks
* Mon Jun 09 2008 - trisk@acm.jhu.edu
- Replace SFEfreetype dependency
* Mon Jun 09 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc4
- Drop patch1
- Replace SFEcups with SUNWcupsu
- Add lots of missing dependencies
- Use curses instead of ncurses
* Wed Jun 04 2008 - trisk@acm.jhu.edu
- Drop SFEfontforge, SUNWlcms-devel dependencies
- Add patch5 for http://bugs.winehq.org/show_bug.cgi?id=9787
- List bug URLs
* Sat May 31 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc3
* Sat May 24 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc2
* Sun May 18 2008 - trisk@acm.jhu.edu.
- Add patch4
* Tue May 13 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc1
* Mon Apr 28 2008 - trisk@acm.jhu.edu
- Bump to 0.9.61, update patch1, patch2
* Mon Apr 28 2008 - trisk@acm.jhu.edu
- Drop patch4 and patch5
- Add fix for long-standing problem with non-contiguous library mappings
- Add new patch2 to work around pre-snv_85 XRegisterIMInstantiateCallback
* Mon Apr 21 2008 - trisk@acm.jhu.edu
- Bump to 0.9.60, drop patch7, patch2
* Wed Apr 09 2008 - trisk@acm.jhu.edu
- Bump to 0.9.59, add patch7, update patch6
- Update dependencies (SFEfontforge is only used for build)
* Sat Mar 22 2008 - trisk@acm.jhu.edu
- Bump to 0.9.58
- Update patch1
- Update source URL
* Tue Mar 18 2008 - trisk@acm.jhu.edu
- Add patch6 to implement network statistics in iphlpapi
- Use autoconf
- Pause patch2 - -shared works, and the configure.ac part is broken
* Mon Mar 10 2008 - trisk@acm.jhu.edu
- Add SFElibaudioio dependency for Sun audio
* Sun Mar 09 2008 - trisk@acm.jhu.edu
- Bump to 0.9.57
- Add -D__C99FEATURES__ for isinf (can we do -std=c99?)
- Update patch5 to not mangle gp_list_* functions
* Thu Feb 21 2008 - nonsea@users.sourceforge.net
- Bump to 0.9.55
- Remove upstreamed patch add-wine_list.h_includes.diff and reorder
- Use gcc /usr/sfw/bin (there is no gcc under /usr/gnu/bin)
* Mon Nov 30 2007 - trisk@acm.jhu.edu
- Bump to 0.9.50
* Mon Nov 26 2007 - Thomas Wagner
- pause patch4 (removal of prelink) - breaks wine atm
* Sun Nov 25 2007 - Thomas Wagner
- bump to 0.9.49
- never Nevada builds define /usr/include/sys/list.h -> "list"* starts clushing with include/wine/list.h.
  to cleanup addwd "change_functions_structs_named_list_asterisk.sh" as patch5 and patch6
  quick patch4 removes code to run preload for linux (load an specific addresses on Solaris upcoming)
* Fri Oct 19 2007 - Doug Scott <dougs@truemail.co.th>
- bump to 0.9.47
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- bump to 0.9.46
* Tue Aug 28 2007 - dougs@truemail.co.th
- bump to 0.9.44
* Mon Aug 13 2007 - dougs@truemail.co.th
- bump to 0.9.43
- Added SFEcups SFElcms SFEncurses to Required
* Sat Jul 14 2007 - dougs@truemail.co.th
* Fri Aug 03 2007 - dougs@truemail.co.th
- bump to 0.9.42
* Sat Jul 14 2007 - dougs@truemail.co.th
- bump to 0.9.41
* Mon Jul 10 2007 - dougs@truemail.co.th
- bump to 0.9.40
* Mon Apr 30 2007 - dougs@truemail.co.th
- bump to 0.9.37
* Mon Apr 30 2007 - dougs@truemail.co.th
- Remove $RPM_BUILD_ROOT before install
* Mon Apr 30 2007 - dougs@truemail.co.th
- Changed some scripts to use bash
* Mon Apr 30 2007 - dougs@truemail.co.th
- Added Requires: SFEfreetype to fix bad fonts
- bump to 0.9.36
* Mon Apr 23 2007 - dougs@truemail.co.th
- Fixed Summary
* Sun Apr 22 2007 - dougs@truemail.co.th
- Initial version
