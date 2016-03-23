#
# spec file for package gpac
#
# includes module(s): gpac
#

%define	src_name gpac

Name:                gpac
Summary:             Open Source multimedia framework
Version:             0.5.2
URL:                 http://gpac.sourceforge.net/
#Source:              %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Source:              http://github.com/gpac/gpac/archive/v%{version}.tar.gz -O %{_sourcedir}/%{src_name}-%{version}.tar.gz
Patch1:		     gpac-01-configure.diff
Patch2:              gpac-02-stringcat.diff 
Patch3:              gpac-03-ldflags.diff
Patch4:              gpac-04_wxT.diff
Patch5:              gpac-05-Playlist_wxT.diff
Patch6:              gpac-06-missing-LDFLAGS.diff
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%prep
unset P4PORT
%setup -q -n %{name}-%{version}
#%setup -q -T -n %{name}-%{version}
#gzip -dc `echo %SOURCE0 | sed -e 's/ .*//'` | (cd ..; tar xf -)
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1
%patch6 -p1

gsed -i.bak -e 's?wx-config?/usr/g++/bin/wx-config?' configure

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

CC=gcc
CXX=g++

export LD=`which ld-wrapper`

if [ -f %{_includedir}/openjpeg.h ]
   then
    #example           #define OPENJPEG_VERSION "1.3.0"
    #SFEopenjpeg
    LIBVERSION=$( /usr/bin/ls -1 /usr/lib/libopenjpeg.so.[0-9]*.* | gsed -e 's?.*\.so\.??' )
    #if openjpeg.h doesn't define macro OPENJPEC_VERSION, pass that as "-D"
    #to the prepocessor via CFLAGS setting
    #Version 1.5.0 replaced the macro with a function call, gpac 0.4.5 expects the macro
##TODO## version bump to gpac 0.5.0 may make this obsolete
    grep OPENJPEC_VERSION %{_includedir}/openjpeg.h \
     || export OPENJPEC_CFLAGS="-DOPENJPEG_VERSION=\"$LIBVERSION\""
fi


export CFLAGS="%optflags -I/usr/g++/include -I%{_includedir}/libpng12 -I%{_includedir} $OPENJPEC_CFLAGS"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include -I%{_includedir}/libpng12 -I%{_includedir}"
LDFLAGS_GPP=$( echo %{gnu_lib_path} | sed -e 's?gnu?g++?g' )
#unfortunatly all over the makefiles, $CC is used for linking but that misses the "-m64" on _arch64 builds
#adding %optflags helps getting -m64 automaticly
export LDFLAGS="$LDFLAGS_GPP %_ldflags %optflags"
#RANLIB is a dummy (ar does the work)
export RANLIB=/usr/bin/ranlib
export AR=/usr/bin/ar

%if %with_jack
	JACK_OPTS="--enable-jack"
%else
	JACK_OPTS="--disable-jack"
%endif
%if %with_pulseaudio
	PULSEAUDIO_OPTS="--enable-pulseaudio"
%else
	PULSEAUDIO_OPTS="--disable-pulseaudio"
%endif
#if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
#	WXAPP="--disable-wx --use-theora=no"
#else
#	WXAPP="--enable-wx"
#fi

%if %{opt_arch64}
BINDIR_ARCH="bin/%{_arch64}"
LIBDIR_ARCH="lib/%{_arch64}"
%else
BINDIR_ARCH="bin"
LIBDIR_ARCH="lib"
%endif

#doesn't work with ksh93  /bin/sh -> amd64/ksh93
perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure
chmod 755 ./configure
./configure --prefix=%{_prefix}		\
            --bindir=$BINDIR_ARCH         \
            --libdir=$LIBDIR_ARCH         \
            --mandir=%{_mandir}		\
	    --cc=$CC			\
	    --extra-libs="-lrt -lm"	\
	    --disable-opt		\
	    --mozdir=/usr/lib/firefox	\
	    $JACK_OPTS			\
	    $PULSEAUDIO_OPTS		\
            $WXAPP			\
	    --extra-cflags="$CFLAGS"	\
	    --extra-ldflags="$LDFLAGS"


echo "opt_arch64 ist:  %{opt_arch64}"
%if %{opt_arch64}
	gsed -i.bak1 \
           -e 's/OSS_CFLAGS=/OSS_CFLAGS=-m64/' \
           -e '/^moddir/ s?/^moddir=%{prefix}/lib?/moddir=%{prefix}/lib/%{_arch64}?' \
           -e '/^libdir/ s?/^libdir=lib?/libdir=lib/%{_arch64}?' \
           config.mak
           #
%endif

#add "bindir" to config.mak
echo "bindir=$BINDIR_ARCH" >> config.mak

gsed -i.bak1 -e 's?ar ?\$(AR) ?' \
             -e 's?ranlib ?\$(RANLIB) ?' \
             -e 's?\$(prefix)/bin?\$(prefix)/\$(bindir)?' \
             src/Makefile

gsed -i.bak1 -e 's?\$(prefix)/bin?\$(prefix)/\$(bindir)?' \
             Makefile


gmake -j$CPUS

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/gpac
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 23 2016 - Thomas Wagner
- bump to 0.5.2
- new Source URL to download tarball from github
* Mon Jan  6 2014 - Thomas Wagner
- bump to 0.5.0
- propper make install, layout and hard-links to isaexec for 32-bit/64-bit commandline tools,
  set BINDIR_ARCH, LIBDIR_ARCH as configure is terribly non-standard requiring --bindir=bin/amd64,
  tweak config.mak to get moddir, libdir, add bindir for propper 64-bit directory,
  fix Makefile to install in correct 64-bit directory
- define cc_is_gcc 1 (we use only gcc for now, option would be a separate spec file for Studio), 
  remove with_wxw_gcc
- use bash for configure instead of /bin/sh (is symlink to amd64/ksh93 on S12) 
- find wx-config in /usr/g++/bin/wx-config
- change (Build)Requires to %{pnm_buildrequires_x11_library_freeglut}, %{pnm_buildrequires_SFEpulseaudio_devel}, include packagenamemacros.inc
- add (Build)Requires) SFEopenjpeg(-devel)
- add temporary support for missing define OPENJPEG_VERSION (can go away if gpac version can use function calls for version)
- re-work LDFLAGS / CFLAGS to get "-m64" via %optflags when linking is done with gcc
- cosmetic cleanup to get Solaris $AR and $RANLIB
* Wed Dec 25 2013 - Thomas Wagner
- re-order options to configure (misinterpretes pulseaudio switches on S12)
- add patch6 gpac-06-missing-LDFLAGS.diff (missing LDFLAGS, missing -m64 causes 32!=64 mismatch for oss.o, pulseaudio.o)
* Wed Dec 25 2013 - Thomas Wagner
- re-order options to configure (misinterpretes pulseaudio switches on S12)
- add patch6 gpac-06-missing-LDFLAGS.diff (missing LDFLAGS, missing -m64 causes 32!=64 mismatch for oss.o, pulseaudio.o)
- improve work around missing macro OPENJPEG_VERSION=\"1.5.0\")
* Sat Nov 14 2013 - Thomas Wagner
- add switch for Pulseaudio, currently disabled, select package by pnm_macro
- set LD to Solaris ld / ld-wrapper
- add missing dependency SFEopenjpeg
- work around missing macro OPENJPEG_VERSION=1.5.0
- read include from /usr/g++/include first, read libs from /usr/g++/lib first
* Mon Jul  1 2013 - Thomas Wagner
- new download URL
#- bump to 0.5.0
* Wed Nov 10 2010  - Thomas Wagner
- png14 misses symbol png_infopp_NULL but png12 hasit, add CFLAGS/CXXFLAGS -I%{_includedir}/libpng12
* Mar 12 2010 - Gilles dauphin
- misssing lib/amd64
- minor patch for _T macro and new wxWidget
* Wed Sep 16 2009 - trisk@forkgnu.org
- Add patch3
- Support jack and pulseaudio
* Sun Aug 29 2009 - gilles Dauphin
- don't parallel make
* Sun Aug 24 2009 - Milan Jurik
- Initial base spec file
