#
# spec file for package SFEsdl-mixer
#
# includes module(s): SDL
#
%include Solaris.inc
%include packagenamemacros.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use sdl_64 = sdl-mixer.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%use sdl_sse2 = sdl-mixer.spec
%endif

%include base.inc
%use sdl = sdl-mixer.spec


Name:			%{sdl.name}
IPS_Package_Name:	library/audio/sdl-mixer
Summary: 		%{sdl.summary}
Version:		%{sdl.version}
URL:			%{sdl.url}
Group:			System/Multimedia Libraries
License:		%{sdl.license}
SUNW_Copyright:		sdl-mixer.copyright
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_SUNWlibsdl_devel}
Requires:      %{pnm_requires_SUNWlibsdl}
BuildRequires:  %{pnm_buildrequires_SUNWlibmikmod_devel}
Requires:       %{pnm_requires_SUNWlibmikmod}
BuildRequires: %{pnm_buildrequires_SUNWogg_vorbis_devel}
Requires: %{pnm_requires_SUNWogg_vorbis}

BuildRequires: SUNWflac-devel
Requires: SUNWflac

%description
SDL_mixer is a sample multi-channel audio mixer library.

It supports any number of simultaneously playing channels of 16 bit stereo
audio, plus a single channel of music, mixed by the popular MikMod MOD,
Timidity MIDI, Ogg Vorbis, and SMPEG MP3 libraries.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%sdl_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%sdl_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%sdl.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%sdl_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.build -d %name-%version/%sse2_arch
%endif

%sdl.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%sdl_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.install -d %name-%version/%sse2_arch
%endif

%sdl.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
#%doc README CHANGES COPYING
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%if %arch_sse2
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/SDL/
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif

%changelog
* Sun Dec 11 2016 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWogg_vorbis_devel}
* Mon Jul 30 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibmikmod_devel}
* Sun Jun 24 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibsdl_devel}, %include packagenamacros.inc
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Thu Feb 03 2011 - Milan Jurik
- SFE vs. SUNW libmikmod detection
* Sun May 16 2010 - Milan Jurik
- added libmikmod for MOD support
* Thu Apr 08 2010 - Milan Jurik
- cleanup
* Fri Mar 05 2010 - Brian Cameron  <brian.cameron@sun.com>
- Add pkgconfig files.
* Sun Dec 07 2008 - Gilles Dauphin
- Can't find DOC README CHANGE etc...
* Tue Jun 05 2007 - Doug Scott
- Change to isabuild
* Sun Apr 22 2007 - Doug Scott
- Initial version
