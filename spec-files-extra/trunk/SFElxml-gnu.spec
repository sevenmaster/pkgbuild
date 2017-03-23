#
# spec file for package SFElxml (libxml2)
#

# owner: tom68
# NO UNTESTED VERSION BUMPS PLEASE

%include Solaris.inc
%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use lxml_64 = lxml.spec
%endif

%include base.inc
%use lxml = lxml.spec

%include packagenamemacros.inc

%define src_name libxml2


Name:                    SFElxml-gnu
IPS_package_name:	 library/gnu/libxml2
Summary:                 %{lxml.summary}
Version:                 %{lxml.version}
#2.9.0-rc2 -> 2.9.0.0.2   2.9.0 -> after release make it 2.9.0.1
IPS_component_version:   %( echo %{version} | sed  -e '/\.[0-9][0-9]*$/ s/$/.1/' -e '/-rc[0-9][0-9]*/ s/-rc/.0./' )
#Source:                  ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
Source:                  http://gd.tuwien.ac.at/gds/languages/html/libxml/libxml2-%{version}.tar.gz
URL:                     %{lxml.url}
SUNW_BaseDir:            %{_prefix}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWzlib_devel}
Requires:      %{pnm_buildrequires_SUNWzlib}
BuildRequires: %{pnm_buildrequires_SFExz_gnu}
Requires:      %{pnm_buildrequires_SFExz_gnu}
BuildRequires: SFElibiconv
Requires:      SFElibiconv

%package python
Summary:                 Python bindings for libxml2 (32-bit only)
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: 		 %{name}
BuildRequires:           %{pnm_buildrequires_python_default}
Requires:                %{pnm_requires_python_default}


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: 		 %{name}
Requires:                %{pnm_requires_python_default}

%prep
rm -rf %{name}-%{version}
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%lxml_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_arch
%lxml.prep -d %{name}-%{version}/%base_arch



%build
%ifarch amd64 sparcv9
%lxml_64.build -d %{name}-%{version}/%_arch64
%endif

%lxml.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%lxml_64.install -d %{name}-%{version}/%_arch64
%endif

%lxml.install -d %{name}-%{version}/%{base_arch}

#create isaexec layout (move i86 binaries to i86/, create symbolic links to isaexec)
mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
#for binary in `cd %{buildroot}/%{_bindir}; find . -type f -print`
for binary in `cd %{buildroot}/%{_bindir}; ls -1d x*`
  do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  ln -f -s /usr/lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary
#exception! /usr/bin/xml2-config is a shell script and can't really
#decide which ISA is asked. For now we *remove* this symbolic link
#and ask the consuming programs to use /usr/bin/i86/xml2-config (32-bit)
#and /usr/bin/amd64/xml2-config (64-bit).
#pkgconfig with proper PKG_CONFIG_PATH knows much better how to handle 32-/64-bit multiarch!
rm %{buildroot}/%{_bindir}/xml2-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%ifarch amd64 sparcv9
%hard %{_bindir}/xmlcatalog
%hard %{_bindir}/xmllint
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
%defattr (-, root, other)
%{_datadir}/doc
%{_datadir}/aclocal
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man*/*

%files python
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python*

%files devel
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#only in subdir!%{_bindir}/xml2-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%{_libdir}/cmake/*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/cmake/*
%endif


%changelog
* Thu Mar 23 2017 - Thomas Wagner
- bump to 2.9.4
- add patch5 patch6 patch7 for CVE-2016-4658 and CVE-2016-5131
* Fri Aug  2 2013 - Thomas Wagner
- bump to 2.9.1 / 2.9.1 (IPS) CVE-2013-2877
- remove now obsolete patch1 libxml2-01-2.9.0-fix-PTHREAD_ONCE_INIT.diff
* Sun Jan 13 2013 - Thomas Wagner
- fix isaexec (hardlink)
- fix %hard %files %_bindir for multiarch
- add patch1 libxml2-01-2.9.0-fix-PTHREAD_ONCE_INIT.diff 
- bump to 2.9.0 / 2.9.0.1 (IPS)
- add dependencies
* Mon Jan  7 2013 - Thomas Wagner
- fix package Name: SFElxml-gnu (not SUNWlxml-gnu), fix deps for sub packages
- Use http mirror for download
# not - bump to 2.9.0 / 2.9.0.1 (IPS)
* Sat Sep  8 2012 - Thomas Wagner
- move to /usr/gnu
- bump to 2.8.0 / 2.8.0.1 (IPS)
- rework to use regular 32/64-bit build method with base-specs/lxml.spec
- need a more fresh xml version, adapt to pnm_macros
- new Download URL
- move to /usr/gnu
- a few parts taken from older SUNWlxml.spec
