#
# spec file for package SFElxsl-gnu (libxslt)
#

# owner: tom68
# NO UNTESTED VERSION BUMPS PLEASE

%include Solaris.inc
%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use xslt_64 = xslt.spec
%endif

%include base.inc
%use xslt = xslt.spec

%include packagenamemacros.inc

%define src_name libxslt


Name:                    SFElxsl-gnu
IPS_package_name:	 library/gnu/libxslt
Summary:                 %{xslt.summary}
Version:                 %{xslt.version}
IPS_component_version:   %( echo %{version} | sed  -e '/\.[0-9][0-9]*$/ s/$/.1/' -e '/-rc[0-9][0-9]*/ s/-rc/.0./' )
#Source:                  ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
Source:                  ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
URL:                     %{xslt.url}
Patch1:                  libxslt-01-disable-version-script.diff
SUNW_BaseDir:            %{_prefix}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElxml-gnu-devel
Requires:      SFElxml-gnu
BuildRequires: %{pnm_buildrequires_SFElibgpg_error_devel}
Requires:      %{pnm_buildrequires_SFElibgpg_error}
BuildRequires: %{pnm_buildrequires_SUNWlibgcrypt_devel}
Requires:      %{pnm_buildrequires_SUNWlibgcrypt}
BuildRequires: %{pnm_buildrequires_SUNWzlib_devel}
Requires:      %{pnm_buildrequires_SUNWzlib}



%package python
Summary:                 Python bindings for libxslt (32-bit only)
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
%xslt_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_arch
%xslt.prep -d %{name}-%{version}/%base_arch



%build
%ifarch amd64 sparcv9
%xslt_64.build -d %{name}-%{version}/%_arch64
%endif

%xslt.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%xslt_64.install -d %{name}-%{version}/%_arch64
%endif

%xslt.install -d %{name}-%{version}/%{base_arch}

#create isaexec layout (move i86 binaries to i86/, create symbolic links to isaexec)
mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
for binary in `cd %{buildroot}/%{_bindir}; ls -1d x*`
  do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  ln -f -s /usr/lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary
#exception! /usr/bin/xslt-config is a shell script and can't really
#decide which ISA is asked. For now we *remove* this symbolic link
#and ask the consuming programs to use /usr/bin/i86/xslt-config (32-bit)
#and /usr/bin/amd64/xslt-config (64-bit).
#pkgconfig with proper PKG_CONFIG_PATH knows much better how to handle 32-/64-bit multiarch!
rm %{buildroot}/%{_bindir}/xslt-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%ifarch amd64 sparcv9
%hard %{_bindir}/xsltproc 
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/libxslt-plugins
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/libxslt-plugins
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
#only in subdir!%{_bindir}/xslt-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xsltConf.sh

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/xsltConf.sh
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Sun Jan 13 2013 - Thomas Wagner
- fix Name: SFExslt-gnu -> SFElxsl-gnu
- fix isaexec (hardlink)
- fix %hard %files %_bindir for multiarch
- add (Build)Requires: SFElxml-gnu(-devel) SUNWzlib
- add dependencies
* Thu Jan 10 2013 - Thomas Wagner
- rename SVR4 package from SFElxslt-gnu to SFElxsl-gnu
* Mon Jan  8 2013 - Thomas Wagner
- initial spec, copied from libxml2
