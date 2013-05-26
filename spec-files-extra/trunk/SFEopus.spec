# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use opus_64 = opus.spec
%endif

%include base.inc
%use opus = opus.spec

Name:		SFEopus
IPS_Package_Name:	library/audio/opus
Summary:      The Opus Audio Codec Library
Group:		Development/Libraries
Version:	1.0.2
Source:       http://downloads.xiph.org/releases/opus/opus-%{version}.tar.gz
URL:            http://opus-codec.org
License:	BSD3c
#SUNW_Copyright:	opus.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#BuildRequires: SFEgcc
#Requires: SFEgccruntime

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
Requires: %name

%description
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype's SILK codec and Xiph.Org's CELT codec. 

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%opus_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%opus.prep -d %name-%version/%base_arch


%build
%ifarch amd64 sparcv9
%opus_64.build -d %name-%version/%_arch64
%endif

%opus.build -d %name-%version/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%opus_64.install -d %name-%version/%_arch64
%endif

%opus.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sat May 25 2013 - Thomas Wagner
- initial spec derived from libvorbis.spec, SFEgmp.spec and opus.spec (SuSE)
- starting with GNU gcc (Studio compilers would need patching compiler switches in opus)
