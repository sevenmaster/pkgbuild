#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

#change version number only here.
%define ffmpeg_version 2.1.3

#older ffmpeg version can't use every patch
%define enable_patch13 1


%ifarch sparc
%define arch_opt --disable-optimizations
%endif

%ifarch i386
%define arch_opt --cpu=prescott --enable-runtime-cpudetect --enable-mmx --enable-mmxext --enable-sse --enable-ssse3 --enable-sse4 --enable-sse42 --enable-avx --enable-amd3dnow --enable-amd3dnowext --enable-fma4
%endif

%define extra_gcc_flags

%use ffmpeg = ffmpeg.spec

Name:			SFEffmpeg
IPS_Package_Name:	video/ffmpeg
Summary:		%{ffmpeg.summary} (sse2-only)
Version:		%{ffmpeg.version}
License:		GPLv2+ and LGPLv2.1+
SUNW_Copyright:		ffmpeg.copyright
URL:			%{ffmpeg.url}
Group:			System/Multimedia Libraries

SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Autoreqprov:		on

%include default-depend.inc
BuildRequires: SFEyasm
BuildRequires: SUNWtexi
BuildRequires: %pnm_buildrequires_perl_default
BuildRequires: SUNWxwinc
Requires: SUNWxwrtl
Requires: SUNWzlib
BuildRequires: %{pnm_buildrequires_SUNWlibsdl_devel}
Requires:      %{pnm_requires_SUNWlibsdl}
BuildRequires: SFElibgsm-devel
Requires: SFElibgsm
BuildRequires: SFExvid-devel
Requires: SFExvid
BuildRequires: SFElibx264-devel
Requires: SFElibx264
BuildRequires: SFEfaac-gpp-devel
Requires: SFEfaac-gpp
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex
BuildRequires: SFEopencore-amr-devel
Requires: SFEopencore-amr
BuildRequires: %{pnm_buildrequires_SUNWgsed}
BuildRequires: SFEopenjpeg-devel
Requires: SFEopenjpeg
BuildRequires: SFElibschroedinger-devel
Requires: SFElibschroedinger
BuildRequires: SFErtmpdump-devel
Requires: SFErtmpdump
BuildRequires: SFElibass-devel
Requires: SFElibass
BuildRequires: SFEopenal-devel
Requires: SFEopenal
BuildRequires: SFElibvpx-devel
Requires: SFElibvpx
BuildRequires: %{pnm_buildrequires_NVDAgraphics_devel}
Requires:      %{pnm_requires_NVDAgraphics}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%ffmpeg.prep -d %name-%version/%base_arch

%build
%ffmpeg.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%ffmpeg.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT


%files
%define _pkg_docdir %_docdir/ffmpeg
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/ffmpeg
%{_datadir}/ffmpeg/*.ffpreset
%{_datadir}/ffmpeg/ffprobe.xsd
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/ffmpeg
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libavutil
%{_includedir}/libavcodec
%{_includedir}/libavfilter
%{_includedir}/libavformat
%{_includedir}/libavdevice
%{_includedir}/libpostproc
%{_includedir}/libswscale
%{_includedir}/libswresample
%_includedir/libavresample
%dir %attr(0755, root, bin) %{_datadir}/ffmpeg
%{_datadir}/ffmpeg/examples
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*


%changelog
* Sun Jan 26 2014 - Alex Viskovatoff
- bump to 2.1.3
* Mon Jan 13 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_NVDAgraphics_devel}, %{pnm_buildrequires_SUNWlibsdl_devel}
- change (Build)Requires to SFEfaac-gpp(-devel)
- follow /usr/g++ directory layout, add to CFLAGS / LDFLAGS include /usr/g++/include and -R|-L/usr/g++/lib/%{arch}
* Thu Nov 28 2013 - Thomas Wagner
- make version controllable from calling spec
* Fri Oct 11 2013 - Alex Viskovatoff
- Update to work with ffmpeg 2.0.2; Do not give special treatment to Intel
  processors: this is unnecessary, since runtime cpu detection is used
* Wed Sep 11 2013 - Alex Viskovatoff
- Update to work with ffmpeg 1.2.3
- Change cpu from pentiumpro to prescott
- Remove dependency on alsa-lib, which is of no use on Solaris
* Tue Jan 24 2012 - James Choi
- Add libass, openal dependency
* Tue Nov  1 2011 - Alex Viskovatoff
- Add dependency on libvpx and conditional dependency on alsa-lib
* Wed Oct 19 2011 - Alex Viskovatoff
- Remove dependency on SFEfaad2, which ffmpeg does not use
- Set cpu to pentiumpro and enable amd3dnow and amd3dnowext
* Wed Oct 12 2011 - Alex Viskovatoff
- Add dependency on SFErtmpdump, since librtmp is now enabled
* Tue Aug  9 2011 - Alex Viskovatoff
- Require driver/graphics/nvidia; correct attributes of %_docdir
* Mon Jul 18 2011 - Alex Viskovatoff
- Do not use x86_sse2.inc: it adds Sun Studio-specific flags
* Sat Jul 16 2011 - Alex Viskovatoff
- Fork new spec off SFEffmpeg.spec with multiarch support (CPU < SSE2) removed
* Sat Jul 16 2011 - Alex Viskovatoff
- Add SFEyasm as a dependency; package documentation files
- Add --disable-asm as option for i386 so that newer versions build
* Wed May 11 2011 - Alex Viskovatoff
- Add SFEgccruntime as a dependency
* Mon Jan 24 2011 - Alex Viskovatoff
- Add missing build dependency
* Wed Jun 16 2010 - Milan Jurik
- update to 0.6
- remove older amr codecs, add libschroedinger and openjpeg
- remove mlib because it is broken now
- remove Solaris V4L2 support, more work needed
* Tue Apr 06 2010 - Milan Jurik
- missing perl build dependency (pod2man)
* Sun Mar 07 2010 - Milan Jurik
- replace amrXX for opencore implementation
* Tue Sep 08 2009 - Milan Jurik
- amrXX optional
- improved multiarch support (64-bit not done because of missing SUNW libraries)
* Mon Mar 16 2009 - Milan Jurik
- version 0.5
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- New spec for base-spec
