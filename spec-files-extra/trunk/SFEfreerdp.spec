#
# spec file for package SFEfreerdp
#

%include Solaris.inc
%include x86_sse2.inc

Name:		SFEfreerdp
IPS_Package_Name:	 desktop/remote-desktop/freerdp
Summary:	Free implementation of the Remote Desktop Protocol
URL:		http://www.freerdp.com/
Version:	1.0.2
License:	Apache
Source:		http://pub.freerdp.com/releases/freerdp-%{version}.tar.gz
Patch0:		freerdp-00-avcodec_max_audio_frame_size.diff
Patch1:		freerdp-01-dsp_mask.diff
Patch2:		freerdp-02-codecid.diff
SUNW_Copyright:	%{license}.copyright
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

# x86_sse2.spec gives us the CFLAGS we want, but also sets buildarch-specific
# bindir and libdir that we don't want.
%define _bindir /usr/bin
%define _libdir /usr/lib

BuildRequires:	SUNWxwinc
BuildRequires:	SFEcmake

%prep
%setup -q -n freerdp-%version
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

cmake -DCMAKE_INSTALL_PREFIX=/usr \
	-DCMAKE_BUILD_TYPE=Debug \
	-DCMAKE_C_FLAGS="%{optflags}" \
	-DCMAKE_EXE_LINKER_FLAGS="%{_ldflags} %{xorg_lib_path}" \
	-DWITH_SSE2=ON \
	-DWITH_ALSA=OFF \
	.
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%buildroot

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %{_bindir}
%{_bindir}/*
%dir %{_includedir}
%{_includedir}/*
%dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %{_libdir}/freerdp
%{_libdir}/freerdp/*
%{_libdir}/*.so*
%dir %attr (0755,root,sys) /usr/share
/usr/share/*

%changelog
* Fri Mar 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add patch0, patch1, and patch2 for compatibility with newer ffmpeg
* Fri Mar 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Change Source URL to one that works with pkgtool --download
- Fix source directory name in %setup accordingly
* Thu Mar 20 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec (version 1.0.2)

