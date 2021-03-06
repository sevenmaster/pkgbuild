#
# spec file for package SFEmpd
#


# For the output section of ~/.mpdconf or /etc/mpd.conf try:
#
# audio_output {
#     type	"ao"
#     name      "libao audio device"
#     driver	"sun"
# }

%define build_encumbered %{?_without_encumbered:0}%{?!_without_encumbered:1}

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define src_name mpd

Name:                SFEmpd
IPS_package_name:    audio/mpd
Summary:             Daemon for remote access music playing & managing playlists
License:             GPLv2
SUNW_Copyright:	     mpd.copyright
Meta(info.upstream): Max Kellermann <max@duempel.org>
#requires c++14, fails with std::gets not defined - Version:             0.20.5
Version:             0.19.20
%define major_minor %( echo %{version} |  sed -e 's/\.[0-9]*$//' )
Source:              http://www.musicpd.org/download/mpd/%{major_minor}/mpd-%{version}.tar.xz
URL:		     http://www.musicpd.org/

SUNW_BaseDir:        %{_basedir}
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_system_header_header_audio}
BuildRequires: %{pnm_buildrequires_SFExz_gnu}
BuildRequires: SFElibao-devel
BuildRequires: SFElibsamplerate-devel
BuildRequires: %{pnm_buildrequires_SUNWogg_vorbis_devel}
BuildRequires: %{pnm_buildrequires_gnome_gnome_audio} 
BuildRequires: %{pnm_buildrequires_SUNWflac_devel}
BuildRequires: SFEopus-devel
BuildRequires: SFEwavpack-devel
BuildRequires: SFElibmms-devel
BuildRequires: SFElibshout
BuildRequires: SFElibcdio
BuildRequires: SFElibmpdclient-devel
BuildRequires: %{pnm_buildrequires_SUNWsqlite3}
BuildRequires: %{pnm_buildrequires_SFElibsndfile_devel}
BuildRequires: %{pnm_buildrequires_SUNWglib2_devel}
BuildRequires: %{pnm_buildrequires_SUNWcurl_devel}
BuildRequires: %{pnm_buildrequires_SUNWlibsoup_devel}
#TODO# BuildRequires: SFElibpulse-devel
BuildRequires: %{pnm_buildrequires_SUNWavahi_bridge_dsd_devel}
## MPD INSTALL file says AO "should be used only if there is no native plugin
## available or if the native plugin doesn't work."
Requires: SFElibao
Requires: SFElibsamplerate
Requires: %{pnm_requires_SUNWogg_vorbis}
Requires: %{pnm_requires_gnome_gnome_audio}
Requires: %{pnm_requires_SUNWflac}
Requires: SFEopus
Requires: SFEwavpack
Requires: SFElibmms
Requires: SFElibshout
Requires: SFElibcdio
Requires: SFElibmpdclient
Requires: %{pnm_requires_SUNWsqlite3}
Requires: %{pnm_requires_SFElibsndfile}
Requires: %{pnm_requires_SUNWglib2}
Requires: %{pnm_requires_SUNWcurl}
Requires: %{pnm_requires_SUNWlibsoup}
#TODO# Requires: SFElibpulse
Requires: %{pnm_requires_SUNWavahi_bridge_dsd}
%if %build_encumbered
BuildRequires: SFEffmpeg-devel
BuildRequires: SFElibmpcdec-devel
BuildRequires: SFEmpg123-devel
BuildRequires: SFEfaad2-devel
BuildRequires: SFElame-devel
BuildRequires: SFEtwolame-devel
# libid3tag is not encumbered, but it is not used by flac or ogg
BuildRequires: SFElibid3tag-devel
Requires: SFEffmpeg
Requires: SFElibmpcdec
Requires: SFEfaad2
Requires: SFElame
Requires: SFEtwolame
Requires: SFEmpg123
Requires: SFElibid3tag
#audio/g++/faac
BuildRequires:  SFEfaac-gpp
Requires:       SFEfaac-gpp
BuildRequires:  SFElibgsm
Requires:       SFElibgsm
BuildRequires:  SFEopencore-amr
Requires:       SFEopencore-amr
BuildRequires:  SFErtmpdump
Requires:       SFErtmpdump
BuildRequires:  SFElibx264
Requires:       SFElibx264
BuildRequires:  SFExvid
Requires:       SFExvid
%endif

BuildRequires:  %{pnm_buildrequires_boost_gpp_default}
Requires:       %{pnm_requires_boost_gpp_default}
BuildRequires:  SFEicu-gpp
Requires:       SFEicu-gpp


BuildRequires:  SFEwildmidi
Requires:       SFEwildmidi

BuildRequires:  SFExz-gnu
Requires:       SFExz-gnu
BuildRequires:  SFEorc
Requires:       SFEorc
BuildRequires:  SFElibschroedinger
Requires:       SFElibschroedinger
BuildRequires:  %{pnm_buildrequires_SUNWlibtheora_devel}
Requires:       %{pnm_requires_SUNWlibtheora}
BuildRequires:  SFElibvpx
Requires:       SFElibvpx
BuildRequires: SFEshine-gpp
Requires:      SFEshine-gpp


#Version 0.20.5 requires c++14 support
#BuildRequires: SFEgcc-49
#Requires:      SFEgccruntime-49


%description
Music Daemon to play common audio fileformats to audio devices or 
audio-networks. 

Uses a database to store indexes (mp3-tags,...) and supports Playlists.
Controlled via Network by SFEgmpc, SFEmpc, SFEncmpc, pitchfork and others.
Output might go to local Solaris Audio-Hardware, Streams with SFEicecast,
auto-network SFEpulseaudio ( via pulseaudio, libao (sun|pulse) ).


%prep
#don't unpack please
%setup -q -c -T -n %{src_name}-%{version}
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
 
# LDFLAGS below are based on the following fix to the same problem:
# http://lists.libsdl.org/pipermail/commits-libsdl.org/2013-March/006360.html

#export CC=/usr/gcc-sfe/4.9/bin/gcc
#export CPP="/usr/gcc-sfe/4.9/bin/gcc -E"
#export CXX=/usr/gcc-sfe/4.9/bin/g++
CC=gcc
CPP="gcc -E"
CXX=g++

#get CMSG_FIRSTHDR with _XPG4_2
export CFLAGS="%optflags  -D_POSIX_PTHREAD_SEMANTICS -D__EXTENSIONS__ -D_XPG4_2 -D_XPG6 -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags  -D_POSIX_PTHREAD_SEMANTICS -D__EXTENSIONS__ -D_XPG4_2 -D_XPG6 -D_GNU_SOURCE -I/usr/g++/include"
# Without -R, icu libs are not found (RPATH does not get added to SOs)
export LDFLAGS="%_ldflags -Wl,-zdeferred $PULSEAUDIO_LIBS -R/usr/g++/lib -L/usr/g++/lib -Wl,-znodeferred"
#                                             SFEorc orc-0.4.pc
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/gnu/lib/pkgconfig

sed -i -e 's,#! */bin/sh,#! /usr/bin/bash,' configure 

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --with-boost=%{boost_gpp_default_prefix} \
    	    --enable-ao          \
	    --enable-iso9660     \
	    --enable-shout       \
            --disable-alsa       \
            --disable-mad        \
%if %build_encumbered
            --enable-mpg123      \
%else
            --disable-ffmpeg     \
            --disable-mpg123     \
            --disable-aac        \
            --disable-mpc        \
            --disable-lame-encoder \
            --disable-twolame-encoder \
%endif
#optional:
            # --with-zeroconf=no   \
#let pulse be autodetected and added as dependency by pkgdepend on IPS based systems
            # --enable-pulse

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'retval=0';
  echo '[ -f /etc/mpd.conf ] || cp -p $PKG_INSTALL_ROOT%{_datadir}/doc/mpd/mpdconf.example $PKG_INSTALL_ROOT%{_sysconfdir}/mpd.conf'
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mpd
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/mpd.1
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/mpd.conf.5
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Mon Feb 27 2017 - Thomas Wagner
- add (Build)Requires: SFEshine-gpp
- bump to 0.19.20  (0.20.x needs c++14, fails with std::gets undefined)
* Sun Nov 11 2016 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWogg_vorbis_devel}, SUNWglib2, SUNWgnome-audio, SUNWflac, SUNWlibsoup, SUNWavahi-bridge-dsd
* Wed Nov 23 2016 - Thomas Wagner
- add to PKG_CONFIG_PATH to find SFEorc in /usr/gnu/
* Fri Jun 11 2016 - Thomas Wagner
- bump to 0.19.15
- add (Build)Requires SFEwildmidi SFExz-gnu SFEorc SFElibschroedinger SUNWlibtheora SFElibvpx SFEfaac-gpp SFElibgsm SFEopencore-amr SFErtmpdump SFElibx264 SFExvid
  (play audio from video files, e.g. music videos)
* Fri Jun 10 2016 - Thomas Wagner
- add to FLAGS -D_POSIX_PTHREAD_SEMANTICS to fix compile on S11.3 with getting wrong number of arguments to getpwnam_r (see documentation in /usr/include/pwd.h)
  src/fs/StandardDirectory.cxx:71:56: error: too many arguments to function 'passwd* getpwnam_r(const char*, passwd*, char*, int)'
  (still to check: should CFLAGS be synced with CXXFLAGS)
- fix --autodeps: Requires: SFEffmpeg
* Wed Mar 16 2016 - Thomas Wagner
- bump to 0.19.13
* Fri Dec 18 2015 - Alex Viskovatoff <herzen@imap.cc>
- bump to 0.19.12; reenable icu
* Mon Sep  1 2015 - Thomas Wagner
- find boost --with-boost=%{boost_gpp_default_prefix}
- change to %{pnm_buildrequires_boost_gpp_default}, developer_icu, 
- enable icu
* Tue Sep 01 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 0.19.10; disable icu for now (link fails)
* Thu Apr 02 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 0.19.9
* Thu Mar 20 2014 - Thomas Wagner
- add SFEopus, SFEwavpack, SFElibmms, SUNWlibsoup, SFElibmpdclient
- let pulseaudio be auto-detected for the moment, should be a pnm_macro in the future
- compile problem in Error.hh still unresolved, stay with gcc for now
* Wed Feb 12 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- change (Build)Requires to %{pnm_buildrequires_SUNWcurl_devel}
* Tue Feb 11 2014 - Alex Viskovatoff <herzen@imap.cc>
- update to 0.18.8
  (thanks to upstream for fixing http://bugs.musicpd.org/view.php?id=3941)
- use gcc (does not compile with Studio); enable ffmpeg
* Sun Sep 15 2013 - Thomas Wagner
- reverse changes to use pnm_macros for libsndfile and header/audio
* Thu Sep 12 2013 - Alex Viskovatoff
- update to 0.17.5
- use system xz and libsndfile
* Sat Jul 27 2013 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SFElibsndfile_devel}
- bump to 0.17.4
- new download URL, add BuildRequires %{pnm_buildrequires_SFExz_gnu}, make %prep xz friendly 
* Mon Mar  4 2013 - Thomas Wagner
- --enable-aac (was explicitly --disable-aac before)
* Sun Jan 20 2013 - Thomas Wagner
- bump to 0.17.3
- use %{sf_download} macro for Source
* Sat Oct 13 2012 - Thomas Wagner
- bump to 0.17.2
* Thu Aug 19 2012 - Thomas Wagner
- bump to 0.17.1
- make configure use bash
* Thu Jul  5 2012 - Thomas Wagner
- bump to 0.17, changed download URL
- change to (Build)Requires to %{pnm_buildrequires_SUNWsqlite3}, %include packagenamacros.inc
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- added ips package name.
* Wed Oct 19 2011 - Alex Viskovotoff
- Use mpg123 instead of libmad for mp3s, since libmad is for integer-only CPUs
* Mon Aug  8 2011 - Alex Viskovatoff
- Add missing (build) dependencies
* Mon Jul 18 2011 - Alex Viskovatoff
- ffmpeg currently breaks build, so disable it
* Mon May 16 2011 - Alex Viskovatoff
- Add missing dependency; fix setting of build_encumbered
* Tue Apr 12 2011 - Alex Viskovatoff
- Bump to 0.16.2; add --without-encumbered option
* Tue Jan 18 2011 - Alex Viskovatoff
- Update to 0.16.1; use libxnet
* Sun Oct  3 2010 - Alex Viskovatoff
- Bump to 0.15.12; use gmake.
- mpd does not use id3lib (only faad2 does): remove the dependency.
* Thu Nov 19 2009 - oliver.mauras@gmail.com
- Version bump to 0.15.6
* Thu Jul 30 2009 - oliver.mauras@gmail.com
- Remove libMAD fix as libMAD spec fixed in r1997
* Wed Jul 29 2009 - oliver.mauras@gmail.com
- Small fix to the srcname declaration
* Tue Jul 28 2009 - oliver.mauras@gmail.com
- Version bump to 0.15.1
- Add realname variable
- No problems found with libsamplerate so reactivated it
* Sun Mar 15 2009 - oliver.mauras@gmail.com 
- Version bump
- Fix LibMAD detection
* Sat Dec 20 2008 - Thomas Wagner
- add nice and clean conditional (Build-)Requires: %if %SUNWid3lib ... %else ... SFEid3lib(-devel)
* Wed Nov 28 2007 - Thomas Wagner
- add --disable-lsr, remove (Build-)Requires SFElibsamplerate(-devel) (maybe cause for skipping music every few seconds)
- comment out --enable-pulse to not require pulseaudio
- comment out --*-zeroconf   to not require avahi/bonjour/zeroconf (should be included if it's present on the build-system, pending final solution - suggestions welcome)
- quick fix to "empty struct" when --disable-lsr is used (patch5) (remove patch5 if change is upstream)
* Sun Nov 18 2007 Thomas Wagner
- (Build)Requires: SUNWavahi-bridge-dsd(-devel)
  since parts of avahi interface made it into Nevada :-)
  if you have problems witch avahi/zeroconf, change ./configure to --with-zeroconf=no
* Sun Nov 18 2007 Thomas Wagner
- --disable-alsa (at the moment we use libao)
- (Build)Requires SFElibsamplerate(-devel)
* Tue Sep 04 2007 Thomas Wagner
- add description
- add libao example to mpd.conf (sun|pulse)
- enable missed patch3
- add more configexamples see share/doc/mpd/mpdconf.example if you are upgrading
  pulseaudio native output, libao driver "sun" or "pulse", icecast streaming (second example)
* Mon May 28 2007 Thomas Wagner
- bump to 0.13.0
- --enable-flac --enable-oggflac
  mpd now compiles with newer flac versions
- --enable-shout for buffered streaming to the net in ogg format
- add depency SFElibshout(-devel)
- if SFEavahi is present, mpd resources will be announced with
  zeroconf/avahi/mDNS broadcasts
- patch3: make id3_charset in mpdconf.example default to UTF-8
  NOTE: If files with special characters in id3_tags are missing in your
  database, then update your existing /etc/mpd.conf|~/.mpdconf to set
      id3v1_encoding  "UTF-8"
  and recreate the db (mpd --create-db).
- removed wrong export PKG_CONFIG=/usr/lib/pkgconfig
* May 17 2007 - Thomas Wagner
- --enable-shout - you need gcc to have configure detect shout libs
- added dependcies SFElibshout(-devel)
* Thu Apr 26 2007 - Thomas Wagner
- --disable-flac, --disable-oggflac
  mpd possibly has to be updated to reflect new libFLAC includes
  does not compile with libflac from vermillion_64 (sorry, 62 was a typo)
  you may enable *flac if using oder versions of libFLAC
* Thu Apr 26 2007 - Thomas Wagner
- make filesystem_charset in mpdconf.example default to UTF-8
  NOTE: If directories/files with UTF-8 names missing in the 
  database, then update your existing /etc/mpd.conf|~/.mpd.conf 
  and recreate the db (mpd --create-db).
  does not compile with libflac from vermillion_62
* Wed Apr 04 2007 - Thomas Wagner
- missing " in patch to mpdconf.example 
* Wed Apr 04 2007 - Thomas Wagner
- bump to 0.12.2
- added dependencies
- modified configuration note to name /etc/mpd.conf
- copy patched mdconf.example to /etc/mpd.conf
- re-add id3 tags (untested)
* Mon Nov 06 2006 - Eric Boutilier
- Fix attributes
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
