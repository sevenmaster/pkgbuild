#
# spec file for package SFEmpv
#

# mpv is a movie player based on MPlayer and mplayer2.
# For mnemonic purpsoses, its name can be considered to be a recursive acronym
# for "mpv plays videos", although the developers deny that it is a recursive
# acronym.

%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc
%define srcname mpv

%include packagenamemacros.inc

# NVDAgraphics is the driver supplied directly by Nvidia
%define with_system_nvidia %(pkginfo -q NVDAgraphics && echo 0 || echo 1)

Name:			SFEmpv
IPS_Package_Name:	media/mpv
Summary:		Video player based on MPlayer/mplayer2
License:		GPLv2
SUNW_Copyright:		mpv.copyright
Version:		0.18.0
URL:			http://mpv.io/
Source: http://github.com/mpv-player/mpv/archive/v%version.tar.gz
Group:			Applications/Sound and Video
Patch1:			mpv-01-ao-reorder.patch

BuildRequires: SFEffmpeg-devel
Requires:      SFEffmpeg
BuildRequires: SFElibcdio-devel
Requires:      SFElibcdio
BuildRequires: SFElibdvdnav-devel
Requires:      SFElibdvdnav
BuildRequires: SFEpython27-docutils
Requires:      SFEpython27
BuildRequires: %{pnm_buildrequires_SUNWgroff}
BuildRequires: %{pnm_buildrequires_driver_graphics_nvidia}
BuildRequires: SFElibfribidi-devel
Requires:      SFElibfribidi
BuildRequires: SFEliba52-devel
Requires:      SFEliba52
BuildRequires: SFElibiconv
Requires:      SFElibiconv
BuildRequires: %{pnm_buildrequires_SFEopenjpeg}
Requires:      %{pnm_requires_SFEopenjpeg}
# mpv will not display subtitles without libass
BuildRequires:	SFElibass-devel
Requires:	SFElibass
# Lua is used for the gui
BuildRequires:	runtime/lua
Requires:	runtime/lua
# This really should be an optional dependency;
# It makes mpv play a YouTube video if you give a link to it
Requires:	SFEpython34-youtube-dl

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name

%description
mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special input
URL types are available to read input from a variety of sources other than disk
files.


%prep
%setup -q -n %srcname-%version
# SFEwaf.spec exists, but the version is too old, whereas recent versions
# don't install.  Furthermore, the waf FAQ say, "packaging of waf in
# distributions [is] discouraged".
./bootstrap.py	# download latest tested version of waf (Python build system)

# stream/ai_oss.c produces a warning "implicit declaration of function 'ioctl'"
pushd waftools/detections
sed -i 's/-Werror=implicit-/-Wno-error=implicit-/' compiler.py
popd

# vdpau.pc is missing from driver/graphics/nvidia
cat > vdpau.pc << EOM
prefix=/usr
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
moduledir=${exec_prefix}/lib/vdpau

Name: VDPAU
Description: The Video Decode and Presentation API for UNIX
Version: 1
Requires.private: x11
Cflags: -I${includedir}
Libs: -L${libdir} -lvdpau
EOM

# index_t is defined in sys/types.h: avoid "conflicting types for 'index_t'" error
gsed -i 's/index_t/index__t/g' video/out/dither.c

%patch1 -p1


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="-O3 -march=prescott -fomit-frame-pointer -D__EXTENSIONS__"
# -L/usr/gnu/lib is for iconv
# xorg runtime path is for libdrm.so; /usr/gnu/lib is for lcms2
export LDFLAGS="-lsocket -lnsl -liconv -L/usr/gnu/lib -R/usr/g++/lib:/usr/gnu/lib:/usr/lib/xorg"
# Use locally created vdpau.pc, because ./waf configure
# refuses to accept --enable-vdpau if the autodetection test fails.
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig:/usr/gnu/lib/pkgconfig:."

# Enabling gl makes compilation fail.
./waf configure				\
	--prefix=%_prefix		\
	--confdir=%_sysconfdir/%srcname	\
	--disable-gl			\
	--disable-alsa

./waf -j$CPUS 


%install
rm -rf %buildroot
./waf install --destdir=%buildroot

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%_bindir/%srcname
%_mandir
%defattr (-, root, other)
%_docdir
%_datadir/applications/%srcname.desktop
%_datadir/icons

%files root
%attr (-, root, root) %{_sysconfdir}/%srcname/encoding-profiles.conf


%changelog
* Mon July 4 2016 - Alex Viskovatoff <herzen@imap.cc>
- update to 0.18.0; try oss before pulse for audio output
* Sat May 28 2016 - Alex Viskovatoff <herzen@imap.cc>
- update to 0.17.0
* Fri May 27 2016 - Thomas Wagner
- make BuildRequires resolvable at build-time (pkgtool --autodeps build-order SFEmpv.spec)
- use pnm_macro for nvidia, set the macro to system/kernel if you don't want this dependency at build time
* Sun Jan 31 2016 - Alex Viskovatoff <herzen@imap.cc>
- update to 2.8.5; mpv now needs to know about /usr/g++ on account of libass
* Wed Jan 06 2016 - Rene Elgaard
- Include packagenamemacros to resolve pnm macros
* Sun Nov 29 2015 - Thomas Wagner
- change (Build)Requires to pnm_buildrequires_SFEopenjpeg (OIH)
* Sat Apr 13 2014 - Thomas Wagner
- change (Build)Requires: pnm_buildrequires_SUNWgroff
* Thu Feb 06 2014 - Alex Viskovatoff <herzen@imapmail.org>
- bump to 0.3.4; build with waf; delete %changelog entries from before fork
  from SFEmplayer2.spec - they are not very relevant
* Mon Jan 20 2014 - Alex Viskovatoff <herzen@imapmail.org>
- bump to 0.3.3
* Sun Jan 12 2014 - Alex Viskovatoff <herzen@imapmail.org>
- update to 0.3.2; configure is now called "old-configure", so call that
- deliver encoding-profiles.conf to /etc/mpv as expected by upstream - inelegant
- restore comment about options that must be passed to less for man page to work
* Thu Dec 12 2013 - Alex Viskovatoff <herzen@imapmail.org>
- bump to 0.2.4
* Sat Nov  9 2013 - Alex Viskovatoff <herzen@imapmail.org>
- bump to 0.2.3
- disable alsa: stupid alsa errors show up on the console
* Sun Nov  3 2013 - Alex Viskovatoff <herzen@imapmail.org>
- bump to 0.2.2
* Thu Oct 31 2013 - Alex Viskovatoff <herzen@imapmail.org>
- Add documentation
* Mon Oct 28 2013 - Alex Viskovatoff <herzen@imapmail.org>
- Update to 0.2.1; use libquvi (for YouTube)
- Do not unconditionally require system nvidia
* Fri Oct 11 2013 - Alex Viskovatoff
- Fork SFEmpv.spec off SFEmplayer2.spec
