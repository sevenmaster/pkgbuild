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
%define _pkg_docdir %_docdir/%srcname

%define with_fribidi %(pkginfo -q SFElibfribidi && echo 1 || echo 0)
%define with_openjpeg %(pkginfo -q SFEopenjpeg && echo 1 || echo 0)
# NVDAgraphics is the driver supplied directly by Nvidia
%define with_system_nvidia %(pkginfo -q NVDAgraphics && echo 0 || echo 1)

Name:			SFEmpv
IPS_Package_Name:	media/mpv
Summary:		de facto successor of mplayer2, of which it is a fork
License:		GPLv3
SUNW_Copyright:		mpv.copyright
Version:		0.3.3
URL:			http://mpv.io/
Source: http://github.com/mpv-player/mpv/archive/v%version.tar.gz
Group:			Applications/Sound and Video
SUNW_BaseDir:		%_basedir

BuildRequires: SFEffmpeg-devel
BuildRequires: SFElibcdio-devel
BuildRequires: SFElibdvdnav-devel
BuildRequires: SFEpython26-docutils
BuildRequires: SUNWgroff
%if %with_system_nvidia
BuildRequires: driver/graphics/nvidia
%endif
%if %with_fribidi
BuildRequires: SFElibfribidi-devel
%endif
BuildRequires: SFEmpg123-devel
BuildRequires: SFEliba52-devel
%if %with_openjpeg
BuildRequires: SFEopenjpeg-devel
%endif
BuildRequires: SFElibass-devel
BuildRequires: SFElibquvi

# pkgbuild now takes care of most install-time dependencies, so do not
# declare them unless pkgbuild can't find them


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

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

# Solaris headers do not define BYTE_ORDER or BIG_ENDIAN, breaking sound
export CFLAGS="-O3 -march=prescott -fomit-frame-pointer -DBYTE_ORDER=0 -DBIG_ENDIAN=1"

export LDFLAGS="%gnu_lib_path"
export CC=gcc

# Enabling gl makes compilation fail.  When mplayer did compile with
# gl enabled, gl made it crash immediately.
# Force vdpau, because vdpau.pc is missing from the nvidia package.
bash ./old-configure			\
	--prefix=%_prefix		\
	--mandir=%_mandir		\
        --confdir=%_sysconfdir		\
        --extra-libs="-lsocket -lnsl -lvdpau" \
        --disable-gl			\
	--disable-alsa			\
        --enable-rpath			\
	--enable-vdpau

gmake -j$CPUS 


%install
rm -rf %buildroot
make install DESTDIR=%buildroot

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
%doc README.md RELEASE_NOTES
%doc -d DOCS encoding.rst tech-overview.txt OUTDATED-tech/formats.txt OUTDATED-tech/general.txt OUTDATED-tech/hwac3.txt OUTDATED-tech/libao2.txt OUTDATED-tech/libvo.txt OUTDATED-tech/mpsub.sub OUTDATED-tech/swscaler_filters.txt OUTDATED-tech/swscaler_methods.txt
%_datadir/applications/%srcname.desktop
%_datadir/icons

%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%attr (-, root, root) %_sysconfdir/%srcname/encoding-profiles.conf


%changelog
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
* Thu Nov 17 2011 - Alex Viskovatoff
- Add optional dependency on SFElibdts; disable esd (not part of Solaris 11)
* Sun Oct 30 2011 - Alex Viskovatoff
- Update tarball and switch to new versioning scheme
- Disable gt (causes crashes with gcc 4.6.2) and enable runtime cpu detection
* Wed Oct 19 2011 - Alex Viskovatoff
- Enable 3dnow and 3dnowext; add missing (build) dependency on SFEmpg123
- Disable libmad (only used on integer-only platforms, unsupported by SFE)
- Remove --enable-dynamic-plugins (deprecated by upstream)
* Fri Aug  5 2011 - Alex Viskovatoff
- Require driver/graphics/nvidia
* Wed Aug  3 2011 - Alex Viskovatoff
- Add missing (build) dependency on SFElibdvdnav
* Fri Jul 22 2011 - Alex Viskovatoff
- Default to not renaming mplayer to "mplayer2"; symlink to a DejaVu font
  which is available on all platforms; add SUNW_Copyright
* Sat Jul 16 2011 - Alex Viskovatoff
- Update to git version, so mplayer2 can link against newest ffmpeg
* Mon May  2 2011 - Alex Viskovatoff
- Fork SFEmplayer2.spec off SFEmplayer-snap.spec, making the appropriate changes
- Rename everything "mplayer2" for now so can coexist with original mplayer
* Wed Apr 27 2011 - Alex Viskovatoff
- Add missing optional dependencies
* Sat Apr  2 2011 - Alex Viskovatoff
- Update to new tarball
* Tue Jan 18 2011 - Alex Viskovatoff
- Update to new tarball, with Patch6 no longer required
- Replace --without-gui option with --with-gui, disabling gui by default
* Fri Nov  5 2010 - Alex Viskovatoff
- Use fixed (constant) tarball from Arch Linux repository by default
- Remove obsolete configure switch --enable-network
- Restore cpu detection patch by Milan Jurik
- Add Patch6 by Thomas Wagner to make mkstemp get used
- Add --without-gui option: the configure default is to disable the gui,
  and the MPlayer download page effectively deprecates the included gui
- Create a formatted man page, since nroff cannot handle the man page
* Wed Aug 18 2010 - Thomas Wagner
- rename configure switch --enable-faad-external to --enable-faad   
- use gmake in %build instead make (might have solved makefile syntax error)
* Fri May 21 2010 - Milan Jurik
- openjpeg and giflib support
* Thu Aug 20 2009 - Milan Jurik
- -fomit-frame-pointer to workaround Solaris GCC bug on Nehalem
* Sun Aug 16 2009 - Milan Jurik
- GNU grep not needed
* Sat Jul 18 2009 - Milan Jurik
- improved handling of tarball
* Sat Jul 11 2009 - Milan Jurik
- Initial version
