a

#!!only for autogen version 5.16.2
#build this spec on solaris 11 and OmniOS
%if %( expr %{omnios} '+' %{solaris11} '<=' 0 )
#do not build on Solaris 12, openindiana hipster
echo "Only to be used on OmniOS and Solaris 11, other OS-distro use distro provided guile"
exit 1
%endif

%include Solaris.inc
%include packagenamemacros.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use autogen_64 = autogen.spec
%endif

%include base.inc
%use autogen = autogen.spec




Name:                SFEautogen
IPS_Package_Name:    sfe/developer/build/autogen
Summary:             Templatized program/text generation system
Version:             %{autogen.version}
#beware of IPS once sub-micro version is removed, IPS would not upgrade if simply removed
#needs guile 2.x Version:             5.18.5.029
IPS_Component_Version: %( echo %{version} | sed -e 's?\.0*?.?g' )
Source2:             guile-config_remove_compiler_defines_pthreads
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


#Requires: SUNWbash
BuildRequires: %{pnm_buildrequires_SUNWlxml_devel}
Requires:      %{pnm_requires_SUNWlxml}
#too old. needs 2.x BuildRequires: %{pnm_buildrequires_SUNWguile_devel}
#too old. needs 2.x Requires:      %{pnm_requires_SUNWguile}
#autogen 5.18 needs guild 2.x BuildRequires:  SFEguile
#autogen 5.18 needs guild 2.x Requires:       SFEguile
BuildRequires: %{pnm_buildrequires_SUNWguile_devel}
Requires:      %{pnm_requires_SUNWguile}
#BuildRequires: SUNWgnu-mp
#BuildRequires:  SFEguile
#Requires:       SFEguile

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %{name}-%{version}

%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%autogen_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_isa
%autogen.prep -d %{name}-%{version}/%base_isa

%build
%ifarch amd64 sparcv9
%autogen_64.build -d %{name}-%{version}/%_arch64
%endif

%autogen.build -d %{name}-%{version}/%{base_isa}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%autogen_64.install -d %{name}-%{version}/%_arch64
%endif

%autogen.install -d %{name}-%{version}/%{base_isa}

mkdir -p %{buildroot}/%{_bindir}/%{base_isa}

for binary in `cd %{buildroot}/%{_bindir}; ls -1`
  do
  [ "$binary" == "%{base_isa}" ] && continue
  [ "$binary" == "%{_arch64}" ] && continue
  #move real i386/sparc 32 bit binaries to %{_bindir}/%{base_isa}
  echo "move / symlink file $binary"
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  #sorry, this is a hack. we have no isaexec in /usr/gnu/lib
  ln -s -f /usr/lib/isaexec %{buildroot}/%{_bindir}/${binary}
done #for binary
#symbolic links remain in place, they are copied instead

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (0755, root, bin)
%ifarch amd64 sparcv9
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%hard %{_bindir}/autogen
%hard %{_bindir}/autoopts-config
%hard %{_bindir}/columns
%hard %{_bindir}/getdefs
%hard %{_bindir}/xml2ag
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

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/autoopts
%{_includedir}/autoopts/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/autogen
%{_datadir}/autogen/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*


%changelog
* Sun Jul 31 2016 - Thomas Wagner
- check if infodir exists before trying to delete it (OM)
- re-enable (Build)Requires %{pnm_buildrequires_SUNWguile_devel} (the one from OSDistro might be too old)
* Tue May 24 2016 - Thomas Wagner
- go back to version 5.16.2
- fix build with wrapper around guile-config (remove -pthreads)
* Thu Apr 14 2016 - Thomas Wagner
- set IPS_Package_Name to sfe/developer/build/autogen to escape the consolidation/userland/userland-incorporation version-dictatroship
- rework to 32/64-bit, remove -devel package
* Wed Apr 13 2016 - Thomas Wagner
- bump to 5.18.5.029 (beware of IPS once sub-micro version is removed, IPS would not upgrade then)
* Sun Jan 18 2009 - halton.huo@sun.com
- Bump to 5.9.7
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 5.9.5
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Bump to 5.9.4
* Mon Sep 10 2007 - nonsea@users.sourceforge.net
- Bump to 5.9.2
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 5.9.1
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 5.9
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Mar 20 2007 - daymobrew@users.sourceforge.net
- Use single thread make so as not to break build.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
