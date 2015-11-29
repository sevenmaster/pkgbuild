#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#







##TODO## (Build)Requires









%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc

%define src_name lcms2

%define version 2.7

%ifarch amd64 sparcv9
%include arch64.inc
%use lcms2_64 = lcms2.spec
%endif

%include base.inc
%use lcms2 = lcms2.spec

Name:		SFElcms2-gnu
IPS_Package_Name:	library/gnu/lcms2
Group:		System/Libraries
Summary:	A little color management system (/usr/gnu)
Version:                 %{lcms2.version}
URL:		http://www.littlecms.com/
License:	MIT
SUNW_Copyright:	lcms2.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWzlib}
Requires:	%{pnm_requires_SUNWzlib}

BuildRequires:  %{pnm_buildrequires_SUNWlibms}
Requires:       %{pnm_requires_SUNWlibms}

BuildRequires:	%{pnm_buildrequires_SUNWTiff_devel}
Requires:	%{pnm_requires_SUNWTiff}

BuildRequires:	%{pnm_buildrequires_SUNWjpg_devel}
Requires:	%{pnm_requires_SUNWjpg}


%prep
rm -rf %{name}-%{version}
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%lcms2_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_arch
%lcms2.prep -d %{name}-%{version}/%base_arch

%build
%ifarch amd64 sparcv9
%lcms2_64.build -d %{name}-%{version}/%_arch64
%endif

%lcms2.build -d %{name}-%{version}/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%lcms2_64.install -d %{name}-%{version}/%_arch64
%endif

%lcms2.install -d %{name}-%{version}/%{base_arch}

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
%hard %{_bindir}/jpgicc
%hard %{_bindir}/tificc
%hard %{_bindir}/transicc
%hard %{_bindir}/linkicc
%hard %{_bindir}/psicc
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/*
#%dir %attr (0755, root, other) %{_docdir}
#%{_docdir}/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Sun Nov 29 2015 - Thomas Wagner
- new source url on sourceforge
* Fri Oct 23 2015 - Thomas Wagner
- merge local with pjama's changes
* Fri May 22 2015 - pjama
- bump from 2.5 to 2.7
- change (Build)Requires pnm_buildrequires_SUNWzlib, SUNWlibms, SUNWTiff, SUNWjpg, #include packagenamemacros.inc
* Fri Jan 03 2014 - Thomas Wagner
- add missing base-specs/lcms.spec
- add 32/64-bit support
* Sat Nov  5 2011 - Pavel Heimlich
- initial spec
