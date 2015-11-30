#
# spec file for package SFEmpv
#

# mpv is a movie player based on MPlayer and mplayer2.
# For mnemonic purpsoses, its name can be considered to be a recursive acronym
# for "mpv plays videos", although the developers deny that it is a recursive
# acronym.

# NOTE: To make man display the man page correctly, use
#	export PAGER="/usr/bin/less -insR"
#	This will allow less to display /usr/share/man/cat1/mpv.1 correctly,
#	which is pre-formatted with groff (Solaris's man page is apparently
#	hard-wired to use groff, which doesn't understand some nroff macros).

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname mpv

# NVDAgraphics is the driver supplied directly by Nvidia
%define with_system_nvidia %(pkginfo -q NVDAgraphics && echo 0 || echo 1)

Name:			SFEmpv
IPS_Package_Name:	media/mpv
Summary:		Video player based on MPlayer/mplayer2
License:		GPLv3
SUNW_Copyright:		mpv.copyright
Version:		0.3.4
URL:			http://mpv.io/
Source: http://github.com/mpv-player/mpv/archive/v%version.tar.gz
Group:			Applications/Sound and Video
SUNW_BaseDir:		%_basedir

BuildRequires: SFEffmpeg-devel
# libcdio is not found
#BuildRequires: SFElibcdio-devel
BuildRequires: SFElibdvdnav-devel
BuildRequires: SFEpython26-docutils
BuildRequires: %{pnm_buildrequires_SUNWgroff}
%if %with_system_nvidia
BuildRequires: driver/graphics/nvidia
%endif
BuildRequires: library/fribidi
BuildRequires: SFEliba52-devel
BuildRequires: %{pnm_buildrequires_SFEopenjpeg}
Requires:      %{pnm_requires_SFEopenjpeg}
BuildRequires: SFElibass-devel
BuildRequires: SFElibquvi

# pkgbuild now takes care of most install-time dependencies, so do not
# declare them unless pkgbuild can't find them
Requires: libquvi

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


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
# Solaris headers do not define BYTE_ORDER or BIG_ENDIAN, breaking sound
export CFLAGS="-O3 -march=prescott -fomit-frame-pointer -DBYTE_ORDER=0 -DBIG_ENDIAN=1"
export LDFLAGS="-lsocket -lnsl"
# Use locally created vdpau.pc, because ./waf configure
# refuses to accept --enable-vdpau if the autodetection test fails.
export PKG_CONFIG_PATH="."

# Enabling gl makes compilation fail.  When mplayer did compile with
# gl enabled, gl made it crash immediately.
# ./old-configure disables mpg123, which does not build.  FFmpeg can play mp3
# streams, anyway.
./waf configure				\
	--prefix=%_prefix		\
        --confdir=%_sysconfdir		\
        --disable-gl			\
	--disable-mpg123		\
	--disable-alsa

./waf -j$CPUS 


%install
rm -rf %buildroot
./waf install --destdir=%buildroot

mkdir examples
mv etc/example.conf etc/input.conf examples

# nroff does not understand macros used by mplayer man page
# See http://www.mplayerhq.hu/DOCS/tech/manpage.txt
pushd %buildroot/%_datadir/man
mkdir cat1
groff -mman -Tutf8 -rLL=80n man1/mpv.1 | col -bxp > cat1/mpv.1
popd
cd %buildroot/%_sysconfdir
mkdir %srcname
mv encoding-profiles.conf %srcname

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%_bindir/%srcname
%_mandir
%defattr (-, root, other)
%doc README.md RELEASE_NOTES examples/example.conf examples/input.conf
%doc -d DOCS encoding.rst tech-overview.txt OUTDATED-tech/formats.txt OUTDATED-tech/general.txt OUTDATED-tech/hwac3.txt OUTDATED-tech/libao2.txt OUTDATED-tech/libvo.txt OUTDATED-tech/mpsub.sub OUTDATED-tech/swscaler_filters.txt OUTDATED-tech/swscaler_methods.txt
%_datadir/applications/%srcname.desktop
%_datadir/icons

%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%attr (-, root, root) %_sysconfdir/%srcname/encoding-profiles.conf


%changelog
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
