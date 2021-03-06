#
# spec file for package SFEvlc
#
# includes module(s): vlc
#

##TODO##
#'t find: SFElibdts developer/documentation-tool/gtk SUNWsmbau SUNWgtk
#00:58 < Hazelesque2> and it complains that SUNWxwplt matches multiple packages


# NOTE EXPERIMENTAL - current stat: 1.1.4.1 compiles, really needs a smart solution for NAME_MAX
#                     see patch header in Patch24 vlc-24-1114-NAME_MAX-dirty-fix-need-rework-x11_factory.cpp.diff,
#                     needs review of disabled patches if they still apply to 1.1.4.1,
#                     X consolidation for build 153 adds "x11-xcb" which is needed for vlc to
#                     display video inside the main window (and more) - see http://twitter.com/#!/alanc/status/29060334076
#                     and http://bugs.opensolaris.org/bugdatabase/view_bug.do?bug_id=6667057 Fixed in: snv_153
#                     on old osbuilds you get two separate windows. on new osbuild xcb helps with videodisplay inside the vlc
#                     window


# NOTE EXPERIMENTAL - does contain a few null pointer uses, so you might want to  " LD_PRELOAD=/usr/lib/0@0.so.1 vlc  "
# NOTE EXPERIMENTAL - uses SFEqt-gpp which is installed in the new location /usr/g++ (GNU C++ library) - needs patching
# NOTE EXPERIMENTAL - patches from old revision are not all reviewd if they are still needed

# tickets
#
# Ticket #3034 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3034
#    confusing delayed Interface initialization failed message
#    Fixed by 1861697 


#  Ticket #3036 (reopened patch) https://trac.videolan.org/vlc/ticket/3036
#    vlc-config calls /bin/sh but uses bash-isms

#  Ticket #3033 (new defect) https://trac.videolan.org/vlc/ticket/3033
#    lazy use of NULL pointers causes segfaults on Solaris

#  Ticket #3039 (new defect) https://trac.videolan.org/vlc/ticket/3039
#    no MMX symbols on Solaris 10?


# ticket worked around here in he spec-file (see tickets related to patches below in the patch section)
#  Ticket #3035 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3035
#    Solaris needs explicit -lsocket
#    Fixed by d17b37c 


%include Solaris.inc
%include osdistro.inc

%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%if %arch_sse2
#######%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%endif
 
%include base.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

#we have new X-org with x11-xcb CR 6667057
##TODO## check if other solarish OS do have same x11-xcb integrated with build 153
%if %( expr %{osbuild} '>=' 153 )
%define enable_x11_xcb 1
%else
%define enable_x11_xcb 0
#just in case it is unexpectedly present, use it
%define enable_x11_xcb %(/usr/bin/pkginfo -q SUNWlibxcb && echo 1 || echo 0)
%if %{enable_x11_xcb}
BuildRequires: SUNWlibxcb
Requires: SUNWlibxcb
%endif
%endif

#just in case it is present, use SFElibxcb-devel anyways
##%if %(/usr/bin/pkginfo -q SFElibxcb && echo 1 || echo 0)
##%define enable_x11_xcb 1
##BuildRequires: SFElibxcb-devel
##Requires: SFElibxcb
##%endif

##TODO## temporarily disable building samba support (needs better detection
#  where smbclient.so lives)
%define enable_samba 0

##TODO## temporarily disable building pulseaudio support
%define enable_pulseaudio 0


%define	src_name	vlc
%define	src_url		http://download.videolan.org/pub/videolan/vlc

Name:                   SFEvlc
Summary:                vlc - the cross-platform media player and streaming server
Version:                 1.1.4.1
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.bz2
#Patch1:                 vlc-01-configure-no-pipe.diff
#obsoleted by ticket #3027 Solaris does not have AF_LOCAL - define AF_LOCAL as AF_UNIX
#Patch2:                 vlc-02-solaris.diff-1.0.1
Patch3:                 vlc-03-1141-oss.diff
Patch4:                 vlc-04-solaris_specific.diff
Patch5:                 vlc-05-solaris-cmds.diff-1.0.1
Patch6:                 vlc-06-intl.diff-1.0.1
Patch7:                        vlc-07-live.diff-1.0.1
Patch8:                        vlc-08-osdmenu_path.diff-1.0.1
#pausiert ##TODO## ##FIXME## Patch9:                   vlc-09-pic-mmx.diff
Patch10:               vlc-10-real_codecs_path.diff-1.0.1
Patch12:               vlc-12-for-int-loop.diff-1.0.1
#Patch13:               vlc-13-x264-git-20090404.diff
#https://trac.videolan.org/vlc/ticket/3028
#Fixed by [23414d6]
Patch14:               vlc-14-modules-access-file.c-disable_have_fstatfs.diff
Patch16:               vlc-16-modules.c-file_offset_bits_ticket_3031.diff
#seems only relevant to older SunOS releases (5.10, eventuall older builds of 5.11)
##TODO## need rework to test for already existing dirfd else define 
#Patch17:               vlc-17-dirfd-missing-ticket-3029-Fixed-by-c438250.diff
#Patch17:               vlc-17-1114-dirfd.diff
Patch18:               vlc-18-empty-struct.diff-1.0.1
Patch21:               vlc-21-1114-filesystem.c-NAME_MAX.diff
Patch22:               vlc-22-remove-dirent.h-checks.diff
Patch23:               vlc-23-1114-dirfd.diff
Patch24:               vlc-24-1114-NAME_MAX-dirty-fix-need-rework-x11_factory.cpp.diff

#note: ts.c:2455:21: error: implicit declaration of function 'dvbpsi_SDTServiceAddDescriptor'
#needs libdvbpsi >=0.1.6




SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
Requires:       SUNWlibsdl
%else
BuildRequires:  SFEsdl-devel
Requires:       SFEsdl
%endif
BuildRequires:  SFEsdl-image-devel
Requires:       SFEsdl-image
Requires:       SUNWhal
BuildRequires:  SUNWdbus-devel
Requires:       SUNWdbus
Requires:       SUNWxorg-clientlibs
BuildRequires:  SUNWsmbau
BuildRequires:  SFElibfribidi-devel
Requires:       SFElibfribidi
#BuildRequires:  SFEfreetype-devel
Requires:       SUNWfreetype2
BuildRequires:  SFEliba52-devel
Requires:       SFEliba52
BuildRequires:  SFEffmpeg-devel
Requires:       SFEffmpeg
BuildRequires:  SFElibmad-devel
Requires:       SFElibmad
BuildRequires:  SFElibmpcdec-devel
Requires:       SFElibmpcdec
BuildRequires:  SFElibmatroska-devel
Requires:       SFElibmatroska
BuildRequires:  SUNWogg-vorbis-devel
Requires:       SUNWogg-vorbis
BuildRequires:  SFElibdvbpsi-devel
Requires:       SFElibdvbpsi
BuildRequires:  SFElibdvdnav-devel
Requires:       SFElibdvdnav
BuildRequires:  SFElibdts-devel
Requires:  SFElibdts
BuildRequires:  SFElibcddb-devel
Requires:       SFElibcddb
BuildRequires:  SFElibmpeg2-devel
Requires:       SFElibmpeg2
BuildRequires:  SFElibupnp-devel
Requires:       SFElibupnp
BuildRequires:  SFEvcdimager-devel
Requires:       SFEvcdimager
BuildRequires:  SFElibx264-devel
Requires:       SFElibx264
BuildRequires:  SFElibtar-devel
Requires:       SFElibtar
##TODO## maybe old osbuilds need SFElua
#BuildRequires:	SFElua
#Requires:	SFElua
BuildRequires:	SUNWlua
Requires:	SUNWlua

BuildRequires:	SFEqt-gpp-devel
Requires:	SFEqt-gpp

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n vlc-%version
#%patch1 -p1
#obsolete ticket 3027 - %patch2 -p1
%patch3 -p1
##1.1.4.1 %patch4 -p1
##1.1.4.1 %patch5 -p1
##1.1.4.1 %patch6 -p1
##1.1.4.1 %patch7 -p1
##1.1.4.1 %patch8 -p1
#%patch9 -p1
##1.1.4.1 %patch10 -p1
##1.1.4.1 %patch12 -p1
##1.1.4.1 %patch14 -p1
##1.1.4.1 %patch16 -p1
##1.1.4.1 %patch18 -p1
#seems only relevant to older SunOS releases (5.10, eventuall older builds of 5.11)
##TODO## need rework to test for already existing dirfd else define 
#%patch17 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

perl -w -pi.bak -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec grep -q "#\!.*/bin/sh" {} \; -print | egrep -v "/libtool"`

##TODO## experimental
# text references
#perl -w -pi.bakztext -e "s, -z def,," libtool

#especially for configure.in ....
perl -w -pi.bak2 -e "s,hostname -s,hostname," configure*

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# ffmpeg is build with g++, therefore we need to build with g++

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"

##evil!!! export PATH=/usr/gnu/bin:$PATH
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ./m4"
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
#export CXXFLAGS="%cxx_optflags"
#export CFLAGS="%optflags -D_XOPEN_SOURCE=500 -D__C99FEATURES__ -D__EXTENSIONS__"
#export CPPFLAGS="-D_XOPEN_SOURCE=500 -D__C99FEATURES__ -D__EXTENSIONS__ -I/usr/X11/include -I/usr/gnu/include -I/usr/include/libavcodec -I./include"
#
#notes to flags:
# Ticket #3040 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3040
# need to define _XPG4_2 on Solaris
#
#this page mentions Solaris *FLAGS etc.
#export CFLAGS="-D _XPG4_2 -D __SunOS -D __STDC_ISO_10646__ -D __EXTENSIONS__ -features=extensions -fast"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__C99FEATURES__ -D__EXTENSIONS__ -L/lib -R/lib"
#export CFLAGS="%optflags -D_XPG4_2 -D__C99FEATURES__ -D__EXTENSIONS__ -D__STDC_ISO_10646__ -L/lib -R/lib"
export CFLAGS="%optflags -D_XPG4_2 -D__C99FEATURES__ -D__EXTENSIONS__ -L/lib -R/lib"
#give these flags only to the C-Pre-Processor
export CPPFLAGS="-I/usr/X11/include -I/usr/gnu/include -I/usr/include/libavcodec -I./include -D_XPG4_2 -D__C99FEATURES__ -D__STDC_ISO_10646__ -D__EXTENSIONS__"

%if %debug_build
export CFLAGS="$CFLAGS -g"
%else
export CFLAGS="$CFLAGS -O4"
%endif
##TODO## experime
#export LD=/usr/gnu/bin/ld
#export LDFLAGS="%_ldflags $X11LIB $GNULIB"
##TODO## experime
#export LDFLAGS="%_ldflags $X11LIB $GNULIB -lsocket -lxnet"
#export EXTRA_LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib $X11LIB $GNULIB -lsocket -lxnet"
export EXTRA_LDFLAGS="$X11LIB $GNULIB -lsocket -lxnet"
export LDFLAGS="%_ldflags"
#export LDFLAGS="         $X11LIB $GNULIB -lsocket -lxnet"


export CONFIG_SHELL=/usr/bin/bash

[ -L include/ffmpeg ] || ln -s /usr/include/libavcodec include/ffmpeg
#rm ./configure
#./bootstrap
perl -w -pi.bak3 -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," configure

#let Qt modules in vlc have a good runtime search patch for libraries
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig 
[ -d pkgconfig ] || mkdir pkgconfig
#-L/usr/g++/lib -->> -L/usr/g++/lib -R/usr/g++/lib
sed -e '/^Libs:/s/-L\([^ ]*\)/-L\1 -R\1/' < /usr/g++/lib/pkgconfig/QtGui.pc > pkgconfig/QtGui.pc
sed -e '/^Libs:/s/-L\([^ ]*\)/-L\1 -R\1/' < /usr/g++/lib/pkgconfig/QtCore.pc > pkgconfig/QtCore.pc
export PKG_CONFIG_PATH=`pwd`/pkgconfig:/usr/g++/lib/pkgconfig 

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-shared			\
	    --disable-static			\
	    --disable-rpath			\
	    --enable-mkv			\
	    --enable-live555			\
	    --enable-ffmpeg			\
	    --enable-xvid			\
	    --enable-real			\
	    --enable-realrtsp			\
            --disable-dvb                       \
%if %{enable_x11_xcb}
            --enable-xcb                        \
%else
            --disable-xcb                       \
%endif
%if %{enable_samba}
            --enable-smb                        \
%else
            --disable-smb                        \
%endif
%if %{enable_pulseaudio}
            --enable-pulse                        \
%else
            --disable-pulse                        \
%endif
%if %debug_build
	    --enable-debug=yes			\
%endif
	    --disable-static			\
	    $nlsopt

#           --with-gnu-ld                       \


%if %build_l10n
printf '%%%s/\/intl\/libintl.a/-lintl/\nwq\n' | ex - vlc-config
%endif

# spatializer fails to compile, disable for now
#  Ticket #3037 (reopened defect) https://trac.videolan.org/vlc/ticket/3037
#  spatializer does not compile on Solaris
perl -w -pi.bakspatializer -e "s, spatializer , ," vlc-config
##TODO## experime
#perl -w -pi.bak420 -e "s, (i420_rgb_mmx|i420_ymga|i420_ymga_mmx|i420_yuy2|i420_yuy2_mmx|i422_i420|i422_yuy2|i422_yuy2_mmx|yuy2_i420|yuy2_i422) ,," vlc-config

#/bin/false

##TODO## investigate. Test if this goes away with new vlc version
#sometimes it fails with a core dump at vlc-cache-gen, just try again.
#does vlc-cache-gen work at all?
gmake -j$CPUS  || gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
find $RPM_BUILD_ROOT%{_libdir}/ -name '*.la' -exec rm {} \;
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then 
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vlc
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vlc*
%{_libdir}/libvlc*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%{_datadir}/icons/hicolor/32x32/apps/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/icons/hicolor/256x256/apps/*
%dir %attr (-, root, other) %{_datadir}/kde4
%dir %attr (-, root, other) %{_datadir}/kde4/apps
%dir %attr (-, root, other) %{_datadir}/kde4/apps/solid
%dir %attr (-, root, other) %{_datadir}/kde4/apps/solid/actions
%{_datadir}/kde4/apps/solid/actions/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/lib*.a
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Aug  6 2011 - Thomas Wagner
- use Build(Requires) SFEqt-gpp(-devel) in /usr/g++, create local modified copy
  of QtGui.pc QtGui.pc to include -R/usr/g++/lib as well (or libQt* not found)
- ##TODO## temporarily disable building samba support (needs better detection 
  where smbclient.so lives)
- user QT4_LIBS and QT4_CFLAGS to override what pkg-config thinks (or at runtime
  qt not found or get with -L and added -R compile errors
- configure switches for xcb, samba (temp-disabled), pulseaudio (temp-disabled)
- configure switch --disable-mmx (video_*) does not compile
- ../bin/vlc-cache-gen (plugins) fails once, just re-run gmake in that case
- adjust %files
* Sat Mar 26 2011 - Thomas Wagner
- use SFEqt47-gpp with new Path layout, add PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig fo find QT
- add (Build)Requires:  SFElua
- create symlink for ffmpeg only if not already there
* Thu Nov 11 2010 - Thomas Wagner
- bump tp 1.1.4.1
- switch to gmake to have 3.81 version at least (old cbe 1.6.2 uses gmake 3.80)
- adjust %install for icons (remove extra mkdir/copy), add new icon directories to %files
- add patches ......  vlc-21-1114-filesystem.c-NAME_MAX.diff, vlc-22-remove-dirent.h-checks.diff
  vlc-23-1114-dirfd.diff, vlc-24-1114-NAME_MAX-dirty-fix-need-rework-x11_factory.cpp.diff
- rework/name_new patches vlc-03-1.1.4.1-oss.diff, ......
- remove patches ......
- build with mmx
- build with mpeg2
- enable or disable new xcb of xorg has x11-xcb integrated (%osbuild >= 153, CR 6667057)
- add (Build)Requires:  SUNWlibxcb(-devel) if %osbuild >= 153
- note: ts.c:2455:21: error: implicit declaration of function 'dvbpsi_SDTServiceAddDescriptor'
  needs libdvbpsi >=0.1.6 - upgrade your package with SFElibdvbpsi.spec (updated to 0.1.7)
* Aug 26 2009 - Gilles dauphin
- add patch , avoid empty struct for SS12
* Fri Aug 14 2009 - Thomas Wagner
- copy to encumbered/SFEvlc-1.0.1-experimental.spec
- remove patch11 libprostproc detection is upstream
- rework some patches for vlc-1.0.1
- still does not link correctly with sun and gnu linker - volunteers welcome, please get in contact
* April 2009 - Gilles Dauphin
- postprocess.h is in libpostproc
- TODO upgrade vlc, that's a nightmare
* Thu Dec 02 2008 - dauphin@enst.fr
- try to use the actual SFE ffmpeg , probleme in new ffmpeg API
- I just resign now, but... later i will retry
- TODO link to libpostproc: s/postproc/libpostproc/ .
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Rename SFElibdvdread dependency to SFElibdvdnav
* Fri Aug  3 2007 - dougs@truemail.co.th
- Added devel and l10n
- Added options to better find codecs
- Added icons for app
* Tue Jul 31 2007 - dougs@truemail.co.th
- added --disable-rpath option
- added SFElibx264 to the requirements
* Sun Jul 15 2007 - dougs@truemail.co.th
- --with-debug enables --enable-debug, added some dependencies
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build with gcc
* Fri Mar 23 2007 - daymobrew@users.sourceforge.net
- Add two patches, 01-configure-no-pipe and 02-solaris. Add multiple
  dependencies. Getting closer but not quite building yet.
  Patch 01-configure-no-pipe removes the '-pipe' test. It causes problems later
  with -DSYS_SOLARIS being added after -pipe and being rejected by the linker.
  Patch 02-solaris.diff fixes two compiler issues. First involves expansion of
  ?: code; second changes AF_LOCAL to AF_UNIX as the former is not defined in
  <sys/socket.h>.

* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Initial version
