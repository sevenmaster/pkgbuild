# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc


%ifarch amd64 sparcv9
%include arch64.inc
%use wavpack_64 = wavpack.spec
%endif

%include base.inc
%use wavpack = wavpack.spec

Name:		SFEwavpack
IPS_Package_Name:	library/audio/wavpack
Version:	%{wavpack.version}
Summary:        WavPack audio compression
Group:		Development/Libraries
URL:            http://www.wavpack.com
License:	Conifer
#SUNW_Copyright:	wavpack.copyright
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
WavPack is a completely open audio compression format providing lossless, high-quality lossy, and a unique hybrid compression mode. Although the technology is loosely based on previous versions of WavPack, the new version 4 format has been designed from the ground up to offer unparalleled performance and functionality.

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%wavpack_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%wavpack.prep -d %name-%version/%base_arch


%build
%ifarch amd64 sparcv9
%wavpack_64.build -d %name-%version/%_arch64
%endif

%wavpack.build -d %name-%version/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%wavpack_64.install -d %name-%version/%_arch64
%endif

%wavpack.install -d %name-%version/%{base_arch}

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
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
#%dir %attr (0755, root, other) %{_datadir}/aclocal
#%{_datadir}/aclocal/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
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
* Sat Mar 29 2014 - Thomas Wagner
- initial spec derived from SFEopus.spec base-specs/opus.spec
