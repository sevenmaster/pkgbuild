#
# spec file for package libx264
#
# includes module(s): libx264
#

# NOTE:  At present, the CLI (x264 executable) is not very useful, since it
#	 cannot link to libavcodec and libavformat, which means that it can
#	 only process raw video streams.

################################################################################
#  x264_build MUST CORRESPOND to libx264.so.<number> as produced by the build  #
################################################################################
%define x264_build       136
%define snap             20130910

%define snaph            2245-stable
%define src_name         x264-snapshot
%define src_url          http://download.videolan.org/pub/videolan/x264/snapshots

Name:		libx264
Summary:	H.264 encoder library
Version:	0.%x264_build.0.%snap
Source:		%src_url/%src_name-%snap-%snaph.tar.bz2
URL:		http://www.videolan.org/developers/x264.html
Patch2:		libx264-02-version.diff
Patch6:		libx264-06-gpac.diff
BuildRoot:	%_tmppath/%name-%version-build

%prep
%setup -q -n %src_name-%snap-%snaph

%patch2 -p1
%patch6 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"

if $( echo "%_libdir" | /usr/xpg4/bin/grep -q %_arch64 ) ; then
        export LDFLAGS="$LDFLAGS -m64"
	if [ `uname -p` == "i386" ]; then
		export host="amd64-pc-solaris2.11"
	fi
	if [ `uname -p` == "sparc" ]; then
		sed s/v8plusa/v9a/ configure > configure.new
		mv configure.new configure
		chmod +x configure 
	fi
else
	unset host
fi

# Don't build cli, because
#   (1) It's useless, since it can only read raw streams at present
#   (2) It creates a perverse circular dependency with ffmpeg
# (The reason that wasn't a problem before is that the old version
#  of pkgbuild didn't do a dependency check when creating IPS packages.)
./configure	\
    --prefix=%_prefix		\
    --bindir=%_bindir		\
    --libdir=%_libdir		\
    --enable-pic		\
    --extra-cflags="$CFLAGS"	\
    --extra-ldflags="$LDFLAGS"	\
    --disable-cli		\
    --enable-visualize		\
    --enable-shared		\
    --disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Sep 11 2013 - Alex Viskovatoff
- update to 20130910
- do not build the cli, because that complicates builds with the new pkgbuild
- use --disable-static, so we do not have to bother deleting static libraries
* Sun Mar 3 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 20130303
* Sun Sep 30 2012 - Milan Jurik
- update to 20120930
* Thu Jun 21 2012 - Milan Jurik
- update to 20120620
* Wed Dec 14 2011 - Alex Viskovatoff
- update to new tarball
* Sun Oct 23 2011 - Alex Viskovatoff
- update to new tarball, disabling obsolete patch libx264-07-soname.diff
- add %x264_build to version number; link CLI to system libx264
* Sun Oct 16 2011 - Milan Jurik
- fix multicore build
* Wed Oct 12 2011 - Alex Viskovatoff
- update to new tarball
* Thu Sep 01 2011 - Milan Jurik
- fix version.sh
* Sun Aug 28 2011 - Alex Viskovatoff
- update to new tarball
* Fri Jul 15 2011 - Alex Viskovatoff
- update to new tarball
* Thu Apr 27 2011 - Alex Viskovatoff
- update to new tarball, reworking one patch
* Fri Apr  1 2011 - Alex Viskovatoff
- update to new tarball, reworking patches
* Tue Jan 18 2011 - Alex Viskovatoff
- update to new tarball
* Wed Nov 10 2010 - Alex Viskovatoff
- update to new tarball
- reworked patches libx264-02-version.diff (though replaced by Source1),
  libx264-03-ld.diff
  re-worked and re-added libx264-06-gpac.diff (gpac_static not found -> use gpac)
- added Source1 ext-sources/libx264-replacement-version.sh to just copy the file
  over instead of patching (no more patch reworking)
- removed obsolete configure options
* Fri May 21 2010 - Milan Jurik
- update to new tarball
* Sat Nov 28 2009 - Albert Lee <trisk@opensolaris.org>
- Remove GPAC dependency
* Fri Oct 30 2009 - Milan Jurik
- support for multiarch on sparc
* Tue Sep 08 2009 - Milan Jurik
- initial base spec file
