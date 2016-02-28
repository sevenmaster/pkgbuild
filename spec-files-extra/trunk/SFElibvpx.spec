#
# spec file for package SFElibvpx
#
# includes module(s): libvpx
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# No sparcv9 target

%ifarch amd64
%include arch64.inc
%use libvpx_64 = libvpx.spec
%endif

%include base.inc
%use libvpx = libvpx.spec

Name:		SFElibvpx
IPS_Package_Name:	library/video/libvpx
Summary:	The VP8 Codec SDK
Group:		System/Multimedia Libraries
Version:	%{libvpx.version}
#give the IPS version number a slight advance to stay ahead of the OpenIndiana Hipster delivered libvpx
IPS_Component_Version: %{version}.0.1
URL:            http://www.webmproject.org/code/
#versioned snapshots: http://downloads.webmproject.org/releases/webm/index.html
License:        BSD
SUNW_Copyright:	libvpx.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEgcc
Requires: SFEgccruntime
BuildRequires: SFEyasm

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64
mkdir %name-%version/%_arch64
%libvpx_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libvpx.prep -d %name-%version/%{base_arch}

%build
export CC=gcc

%ifarch amd64
%libvpx_64.build -d %name-%version/%_arch64
%endif

%libvpx.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64
%libvpx_64.install -d %name-%version/%_arch64
%endif

%libvpx.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_libdir/libvpx.so*
%ifarch amd64
%_libdir/%_arch64/libvpx.so*
%endif

%files devel
%defattr (-, root, bin)
%_includedir
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/vpx.pc
%ifarch amd64
%dir %attr (0755, root, other) %_libdir/%_arch64/pkgconfig
%_libdir/%_arch64/pkgconfig/vpx.pc
%endif

%changelog
* Sat Feb 27 2016 - Thomas Wagner
- bump to 1.4.0.0.1 trick the IPS solver to stay ahead with the OpenIndiana Hipster delivered version of libvpx by using IPS_Component_Version
- fix download filename (no >v<)
* Fri Feb 26 2016 - Thomas Wagner
#- bump to 1.5.0 need patch rework
- bump to 1.4.0 - pause patch3, import patch2 for 1.4.0 from OI
- new Source URL and trick stupid gitub causing duplicate filenames between different projects ( "think-1.1.1.tar" and "otherproject-1.1.1.tar" would be both SOURCES/1.1.1.tar )
* Sun Mar 23 2014 - Ian Johnson
- add --disable-unit-tests to configure line (test suite fails to build on Solaris 11.1)
* Sat Sep 28 2013 - Milan Jurik
- bump to 1.2.0 (trigger autobuild)
* Tue Nov  1 2011 - Alex Viskovatoff
- Fix directory attributes
* Sun Aug 05 2012 - Milan Jurik
- bump to 1.1.0
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Oct 23 2011 - Milan Jurik
- bump to 0.9.7-p1
* Fri Mar 18 2011 - Milan Jurik
- fix x86 multiarch
* Thu Mar 17 2011 - Milan Jurik
- initial spec
