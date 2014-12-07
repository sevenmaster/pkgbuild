#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%define _gpp g++
%include base.inc


%define with_openal %(pkginfo -q SFEopenal && echo 1 || echo 0)
%define with_x264 %(pkginfo -q SFElibx264 && echo 1 || echo 0)
%define with_giflib %(pkginfo -q SFEgiflib && echo 1 || echo 0)
%define with_schroedinger %(pkginfo -q SFElibschroedinger && echo 1 || echo 0)
%define with_faac %(pkginfo -q SFEfaac && echo 1 || echo 0)

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:		SFEmplayer
IPS_Package_Name:	media/mplayer
Summary:	mplayer - The Movie Player
Version:	1.1.1
%define tarball_version 1.1.1
URL:		http://www.mplayerhq.hu/
Source:         http://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{tarball_version}.tar.xz
Source2:	http://www.mplayerhq.hu/MPlayer/skins/XFce4-1.0.tar.bz2
Source3:	http://www.mplayerhq.hu/MPlayer/skins/Blue-1.8.tar.bz2
Source4:	http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.7.tar.bz2
Source5:	http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:	http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
Source7:	http://www.mplayerhq.hu/MPlayer/skins/brushedGnome-1.0.tar.bz2
Patch1:		mplayer-01-cddb.diff
Patch11:	mplayer-11-cpudetect.diff
Patch12:	mplayer-12-realplayer.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{tarball_version}-build

%include default-depend.inc
BuildRequires: SFEyasm
BuildRequires: %{pnm_buildrequires_SUNWsmba}
##TODO## check if it is sufficient to install "libsmb" or something on a recent build to get the smbclient features
Requires: %{pnm_requires_SUNWsmba}
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWxorg-clientlibs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWogg-vorbis
Requires: SUNWlibtheora
BuildRequires: SFEgcc
Requires: SFEgccruntime
Requires: SUNWgnome-base-libs
BuildRequires: SUNWxwrtl
Requires: SUNWxwrtl
BuildRequires: SUNWxorg-mesa
Requires: SUNWxorg-mesa
BuildRequires: %{pnm_buildrequires_SUNWaalib_devel}
Requires:      %{pnm_buildrequires_SUNWaalib}
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: %{pnm_buildrequires_SUNWlibm}
Requires:      %{pnm_buildrequires_SUNWlibm}
Requires: SFElivemedia
BuildRequires: SFElivemedia
Requires: SFElibcdio
BuildRequires: SFElibcdio-devel
BuildRequires: SUNWaudh
BuildRequires: %{pnm_buildrequires_SUNWlibmng_devel}
Requires:      %{pnm_requires_SUNWlibmng}
BuildRequires: SFElzo-devel
Requires:      SFElzo

BuildRequires: %{pnm_buildrequires_SFElibsndfile_devel}
Requires:      %{pnm_requires_SFElibsndfile}

Requires: SFElame
BuildRequires: SFElame-devel
Requires: SFEtwolame
BuildRequires: SFEtwolame-devel
BuildRequires: %{pnm_buildrequires_SUNWgawk_devel}
Requires: SFElibmpcdec
BuildRequires: SFElibmpcdec-devel
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
Requires: SFElibdvdcss
BuildRequires: SFElibdvdcss-devel
Requires: SFElibdvdread
BuildRequires: SFElibdvdread-devel
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
Requires: SFElibgsm
BuildRequires: SFElibgsm-devel
Requires: SFEopencore-amr 
BuildRequires: SFEopencore-amr-devel
Requires: SFEopenjpeg
BuildRequires: SFEopenjpeg-devel
%if %with_openal
Requires: SFEopenal
BuildRequires: SFEopenal-devel
%endif
Requires: SFExvid
BuildRequires: SFExvid-devel
%if %with_x264
Requires: SFElibx264
BuildRequires: SFElibx264-devel
%endif
%if %with_giflib
Requires: SFEgiflib
BuildRequires: SFEgiflib-devel
%endif
%if %with_schroedinger
Requires: SFElibschroedinger
BuildRequires: SFElibschroedinger-devel
%endif
%if %with_faac
Requires: SFEfaac
BuildRequires: SFEfaac-devel
%endif
BuildRequires: %{pnm_buildrequires_SUNWunrar}
Requires: %{pnm_requires_SUNWunrar}

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
#don't unpack please
%setup -q -c -T -n MPlayer-%tarball_version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)
%patch1 -p1
%patch11 -p1
%patch12 -p1

###or get {LDFLAGS} not found (S11)
##perl -w -pi.bak_bash -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure

gsed -i.bak_termios.h -e '/for _termios_header in/ s?"termios.h" "sys/termios.h"?"sys/termios.h" "termios.h"?' configure

# grep -rw "ERR(" .
#replace "ERR(" with "printf(" if string is found after white_space or beginning of the line
#the include regset.h does #define ERR 13 if -D__EXTENSTIONS__ (which is needed elsewhere)
#so just patch the source to not rely on #define ERR printf
gsed -i.bak_ERR -e 's?\(\s\|^\)ERR(?\1printf(?' loader/elfdll.c loader/pe_image.c loader/module.c

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#msg_controllen missing -> extra flags
#-D_STDC_C99
export CFLAGS="%{optflags} -D_XOPEN_SOURCE=500 -D_XOPEN_SOURCE_EXTENDED=1 -D_XPG4_2 -D_XPG6 -D__EXTENSIONS__"
export CXXFLAGS="%{cxx_optflags} -D_XOPEN_SOURCE=500 -D_XOPEN_SOURCE_EXTENDED=1 -D_XPG4_2 -D_XPG6 -D__EXTENSIONS__"

%if %debug_build
dbgflag=--enable-debug
export CFLAGS="${CFLAGS} -g -D__hidden=\"\""
%else
dbgflag=--disable-debug
export CFLAGS="${CFLAGS} -O3 -fomit-frame-pointer -D__hidden=\"\" -std=gnu99"
%endif


export LDFLAGS="%{_ldflags} -L%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -L%{_libdir} -R%{_libdir} -liconv"
export CC=gcc
export CXX=g++


bash ./configure			\
	    --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --confdir=%{_sysconfdir}	\
            --enable-gui		\
            --enable-menu		\
            --extra-cflags="-I%{_libdir}/live/liveMedia/include -I%{_libdir}/live/groupsock/include -I%{_libdir}/live/UsageEnvironment/include -I%{_libdir}/live/BasicUsageEnvironment/include -I%{x11}/include -I/usr/sfw/include -I%{_prefix}/X11/include -I/usr/include/libmng" \
            --extra-ldflags="-L%{_libdir}/live/liveMedia -R%{_libdir}/live/liveMedia -L%{_libdir}/live/groupsock -R%{_libdir}/live/groupsock -L%{_libdir}/live/UsageEnvironment -R%{_libdir}/live/UsageEnvironment -L%{_libdir}/live/BasicUsageEnvironment -R%{_libdir}/live/BasicUsageEnvironment -L%{x11}/lib -R%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib" \
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lstdc++ -liconv' \
            --codecsdir=%{_libdir}/mplayer/codecs \
	    --enable-crash-debug	\
            --enable-dynamic-plugins	\
%ifarch i386 amd64
            --enable-runtime-cpudetection	\
%endif
            --disable-xvr100		\
            --disable-crash-debug	\
            --disable-dvdread-internal	\
            --disable-esd		\
            --disable-mp3lib \
	    $dbgflag

       #     --disable-live		\

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
(
	cd $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
	gtar fxj %SOURCE2
	gtar fxj %SOURCE3
	gtar fxj %SOURCE4
	gtar fxj %SOURCE5
	gtar fxj %SOURCE6
	gtar fxj %SOURCE7
	ln -s Blue default
)
ln -s /usr/share/fonts/TrueType/freefont/FreeSerif.ttf $RPM_BUILD_ROOT%{_datadir}/mplayer/subfont.ttf
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/mplayer
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/256x256/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/256x256/apps/
%{_datadir}/icons/hicolor/256x256/apps/*

%changelog
* Sun Dec  7 2014 - Thomas Wagner
- add -D_XPG6 (inttypes.h) to CFLAGS CXXFLAGS 
- --disable-mp3lib (mp3lib/decode_i586.c: 'synth_1to1_pent': PIC register clobbered by '%ebx' in 'asm')
- remove -D__EXTENSIONS__ or get wrong include and %define ERR 13 instead of %define ERR printf
- bump to 1.1.1
- use *xz source
- change (Build)Requires to %{pnm_buildrequires_SUNWaalib}, %{pnm_requires_SUNWlibmng}, %{pnm_requires_SFElibsndfile}, %{pnm_requires_SUNWunrar}
- fix debug switch clearing CFLAGS
* Sat Apr 13 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWgawk}
* Sat Oct 11 2013 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWlibm}
* Sat Jan 12 2013 - Thomas Wagner
- change (Build)Requires from liveMedia to livemedia
* Tue Aug  8 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWsmba}
- add missing BuildRequires: SFEyasm
* Fri Jun 22 2012 - Milan Jurik
- bump to 1.1
- remove pnm_XXX for now
* Mon Dec 12 2012 - Thomas Wagner
- change to (Build)Requires pnm_requires_SUNWsmba
- add missing (Build)Requires pnm_(build)requires_SUNWlibmng(_devel) SFElzo(-devel)
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Sun Feb 06 2011 - Milan Jurik
- use system libdvdread, faac as optional
- clean up dependencies
* Thu Feb 03 2011 - Milan Jurik
- ESD is obsolete and source of problems, disabled
* Sun Jan 30 2011 - Milan Jurik
- bump to 1.0rc4, remove unneeded patches
* Thu Jun 03 2010 - Milan Jurik
- SFElibschroedinger as optional
* Mon May 31 2010 - Milan Jurik
- update to rc3, cleanup in patches
* Sun May 23 2010 - Milan Jurik
- rtsp integer overflow fix
* Mars 12 2010 - Gilles Dauphin
- includedir search path in /usr/SFE
* Tue Sep 14 2009 - Thomas Wagner
- make (Build)Requires a build-time --with_gcc4 switch defaulting to off (which is then: use SUNWgcc, gcc3)
* Sun Aug 09 2009 - Thomas Wagner
- switch to gcc4
- add (Build)Requires: SFEgcc/SFEgccruntime SUNWxwrtl SUNWxorg-mesa SUNWaalib SUNWlibsdl-devel/SUNWlibsdl SUNWlibm
* Sun Jul 05 2009 - Milan Jurik
- disable x264 support for now, incompatible with the latest x264
* Sat Mar 14 2009 - Milan Jurik
- Xvid support
- Dynamic plugin support
- SSE(2) autodetection support
- CVE-2008-5616, CVE-2008-5276, CVE-2008-0486, CVE-2008-0485, CVE 2007-2948, CVE-2008-0630
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Wed Nov 29 2008 - dauphin@enst.fr
- change to SUNWgawk is in b101
* Wed Oct 22 2008 - dick@nagual.nl
- added SFEgawk as dep. Needed to compile without errors.
* Sun Aug 17 2008 - nonsea@users.sourceofrge.net
- Use SUNWfreetype2 instead of SFEfreetype
- Remove missed patches: Patch6, Patch7, Patch8, Patch9
- Remove BuildRequires: SFEgawk for it is in CBE now
* Thu Jul 31 2008 - trisk@acm.jhu.edu
- Use SFElibdvdnav instead of SFElibdvdplay
- Add security patches
* Sat Jun 14 2008 - trisk@acm.jhu.edu
- Update Abyss skin to 1.7
- Disable 3GPP AMR codecs as they are non-redistributable
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Link with SFEfreetype to fix missing symbol problem.
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Updated LDFLAGS to add extra libs to fix link failure
- Chenged to dependency to SFEfreetype to get newer version of freetype2
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Remove SUNWlibiconv dependency to try to get the module to build.
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 1.0rc2.  Change SUNWlibcdio to SFElibcdio.  Remove SFElibfame.
- Comment mplayer-02-makefile-libfame-dep.diff (libfame removed).  Bump patch1.
- Comment patch3 (already applied). Add BuildRequires: SFEgawk.  Add patch5
- as SFEgcc 4.2.2 does not understand -rdynamic.
* Fri Oct 19 2007 - dougs@truemail.co.th
- Fixed 3gpp urls
* Tue Aug 28 2007 - dougs@truemail.co.th
- Added debug option
* Tue Jul 31 2007 - dougs@truemail.co.th
- Removed dirac codec from Requirement
* Sun Jul 15 2007 - dougs@truemail.co.th
- Removed dirac codec patch - causes crashes
* Sat Jul 14 2007 - dougs@truemail.co.th
- Added dirac codec patch
- Added SFEladspa,SFElibfribidi requirement
* Tue May  1 2007 - dougs@truemail.co.th
- Removed SFEsdl from the Required. Conflicts with SUNWlibsdl
* Sun Apr 22 2007 - dougs@truemail.co.th
- Added /usr/gnu/libs to LDFLAGS
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires SUNWsmbau after check-deps.pl run.
* Sun Jan  7 2007 - laca@sun.com
- split the codecs out into SFEmplayer-codecs
* Wed Jan  3 2007 - laca@sun.com
- re-add patches cddb and makefile-libfame-dep after merging with 1.0rc1
- add patches asmrules_20061231 (fixes a buffer overflow) and
  cabac-asm (disables some asm stuff that doesn't seem to compile on Solaris.
* Wed Nov 29 2006 - laca@sun.com
- bump to 1.0rc1
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Tue Sep 26 2006 - halton.huo@sun.com
- Bump Source4 to version 1.6
* Thu Jul 27 2006 - halton.huo@sun.com
- Bump Source3 to version 1.6
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEmplayer
- delete -share subpkg
- update file attributes
* Mon Jun 13 2006 - dougs@truemail.co.th
- Bumped version to 1.0pre8
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
