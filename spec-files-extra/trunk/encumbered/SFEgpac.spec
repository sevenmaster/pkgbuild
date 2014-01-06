#
# spec file for package SFEgpac
#
# includes module(s): gpac
#


##TODO## determine if the libraries export C++ symbols, if yes, move them into /usr/g++
##TODO## libpng12 - check for different versions on different osdistros (base-specs/gpac.spec)
#                   if newer version have symbol png_infopp_NULL

# most spec files building ontop use gcc, we switch to using wxwidgets-gpp here and compile with gcc

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

# disable jack and pulseaudio support for now
%define with_jack 0
%define with_pulseaudio 0

%ifarch amd64 sparcv9
%include arch64.inc
%use gpac_64 = gpac.spec
%endif

%include base.inc
%use gpac = gpac.spec

Name:                SFEgpac
IPS_Package_Name:	library/video/gpac
Summary:             %{gpac.summary}
Version:             %{gpac.version}
URL:                 http://gpac.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_x11_library_freeglut}
Requires:      %{pnm_requires_x11_library_freeglut}
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFEliba52-devel
Requires: SFEliba52
Requires: SUNWfreetype2
%if %with_jack
BuildRequires: SFEjack-devel
Requires: SFEjack
%endif
#can be SFEpulseaudio or SUNWpulseaudio
%if %with_pulseaudio
BuildRequires: %{pnm_buildrequires_SFEpulseaudio_devel}
Requires: %{pnm_requires_SFEpulseaudio}
%else
%endif
BuildRequires: SFEwxwidgets-gpp
Requires: SFEwxwidgets-gpp
BuildRequires: SFExvid-devel
Requires: SFExvid
BuildRequires: SFEopenjpeg-devel
Requires:      SFEopenjpeg

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%gpac_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gpac.prep -d %name-%version/%{base_arch}


%build

export CC=gcc
export CXX=g++
export AR=/usr/bin/ar

%ifarch amd64 sparcv9
%gpac_64.build -d %name-%version/%_arch64
%endif

%gpac.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gpac_64.install -d %name-%version/%_arch64
%endif

%gpac.install -d %name-%version/%{base_arch}

#create isaexec layout (move i86 binaries to i86/, create symbolic links to isaexec)
mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
for binary in `cd %{buildroot}/%{_bindir}; ls -1 | egrep -v "%{base_isa}|%{_arch64}"`
  do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  ln -f -s /usr/lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%ifarch amd64 sparcv9
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%hard %{_bindir}/MP4Box
%hard %{_bindir}/MP4Client
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gpac/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/gpac/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_datadir}/gpac
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
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
- add (Build)Requires SFEopenjpeg(-devel)
- work around missing macro OPENJPEG_VERSION=1.5.0
* Mon Jul  1 2013 - Thomas Wagner
- new download URL
#- bump to 0.5.0
* Sat Jun 29 2013 - Thomas Wagner
- always compile with gcc
- use only wxwidgets-gpp, change (Build)Requires to SFEwxwidgets-gpp
* Wed Dec 19 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_x11_library_freeglut}, %include packagenamemacros.inc
* Sun Oct 16 2011 - Milan Jurik
- add IPS package name
* Wed Sep 16 2009 - trisk@forkgnu.org
- Add (disabled) support for jack and pulseaudio
* Wed Sep 02 2009 - trisk@forkgnu.org
- Add dependency on SFEliba52
* Sun Aug 24 2009 - Milan Jurik
- multiarch support, update to 0.4.5
* Sun Nov 30 2008 - dauphin@enst.fr
- SUNWwxwigets is on b101
* Fri Nov 21 2008 - dauphin@enst.fr
- gpac with Studio12 and new freeglut
- TODO: check ffmepg option (build with)
* Tue Sep 02 2008 - halton.huo@sun.com
- s/SFEfreetype/SUNWfreetype2
* Thu Jun 19 2008 - river@wikimedia.org
- need to unset P4PORT during %setup or gpatch behaves oddly
* Fri May 23 2008 - michal.bielicki@voiceworks.pl
- rights change for mandir, fix by Giles Dauphin
* Mon Dec 31 6 2007 - markwright@internode.on.net
- Add patch 4 to fix trivial compiler error missing INADDR_NONE.
- Add --extra-libs="-lrt -lm".
* Mon Jul 30 2007 - dougs@truemail.co.th
- Install headers
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
