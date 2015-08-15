#
# spec file for package SFEopenjpeg
#
# includes module(s): openjpeg
#
%define _use_internal_dependency_generator 0


%include Solaris.inc

%define	src_name openjpeg
%define	src_url	http://www.openjpeg.org

%define version 1.5.1
%define major_minor_version 1.5

%ifarch amd64 sparcv9
%include arch64.inc
%use openjpeg_64 = openjpeg.spec
%endif

%include base.inc
%use openjpeg = openjpeg.spec

Name:		SFEopenjpeg
IPS_Package_Name:	image/library/openjpeg
Group:		System/Libraries
Summary:                 %{openjpeg.summary}
Version:                 %{openjpeg.version}
URL:		http://www.openjpeg.org/
Source:		http://openjpeg.googlecode.com/files/openjpeg-%{version}.tar.gz
License:	BSD
SUNW_Copyright:	openjpeg.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEcmake

BuildRequires: SFElcms2-gnu
Requires:      SFElcms2-gnu

#pkgdepend resolve returned 0
#  dependency discovered: image/library/libpng@1.4.8-0.175.0.0.0.0.0
#  dependency discovered: image/library/libtiff@3.9.5-0.175.0.0.0.0.0
#  dependency discovered: system/library/math@0.5.11-0.174.0.0.0.0.0
#  dependency discovered: system/library@0.5.11-0.175.0.0.0.2.1


%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %{name}-%{version}
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%openjpeg_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_arch
%openjpeg.prep -d %{name}-%{version}/%base_arch


%build
%ifarch amd64 sparcv9
%openjpeg_64.build -d %{name}-%{version}/%_arch64
%endif

%openjpeg.build -d %{name}-%{version}/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%openjpeg_64.install -d %{name}-%{version}/%_arch64
#1.5.0 #install does not honour OPENJPEG_INSTALL_BIN_DIR:PATH
#1.5.0 mkdir %{buildroot}%{_bindir}/%_arch64
#1.5.0 mv %{buildroot}%{_bindir}/j* %{buildroot}/%{_bindir}/%_arch64/
#1.5.0 mv %{buildroot}%{_bindir}/i* %{buildroot}/%{_bindir}/%_arch64/
%endif

%openjpeg.install -d %{name}-%{version}/%{base_arch}

#create isaexec layout (move i86 binaries to i86/, create symbolic links to isaexec)
mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
for binary in `cd %{buildroot}/%{_bindir}; ls -1 | egrep -v "%{base_isa}|%{_arch64}"`
  do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  ln -f -s /usr/lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%ifarch amd64 sparcv9
%hard %{_bindir}/j2k_dump
%hard %{_bindir}/j2k_to_image
%hard %{_bindir}/image_to_j2k
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/openjpeg-*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/openjpeg-*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
#%{_datadir}/openjpeg-%{major_minor_version}
%{_docdir}/openjpeg-*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Sat May 22 2015 - pjama
- update download URL
* Sat Mar 22 2014 - Thomas Wagner
- Workaround broken search for liblcms2.so in configure.
  On some OS and installed package mix, the amd64 build traps over /usr/gnu/lib/lcms2.so (=32bit)
* Mon Jan  6 2014 - Thomas Wagner
- bump to 1.5.1
- fix %files twice
* Fri Jan  3 2014 - Thomas Wagner
- change (Build)Requires to SFElcms2-gnu, update CFLAGS/LDFLAGS to first search gnu_inc / gnu_lib_path
* Wed Jan 01 2014 - Thomas Wagner
- add (Build)Requires: SFElcms2
- update 32/64-bit support
* Sun Nov 17 2013 - Thomas Wagner
- add 32/64-bit support
* Sat Feb 18 2012 - Milan Jurik
- bump to 1.5.0
* Tue Oct 11 2011 - Milan Jurik
- bump to 1.4
- add IPS package name
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Fri May 21 2010 - Milan Jurik
- update to 1.3, split devel package
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
