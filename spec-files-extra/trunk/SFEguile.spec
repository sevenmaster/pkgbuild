#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

# To set a specific guile version to be build, do this from *outside*
# pkgtool build SFEguile --define 'guile_version 4.7.2'
%define default_version 1.8.8

%if %{!?guile_version:1}
#make version bump *here* - this is the default version being built
%define version %{default_version}
%else
#guile version is already defined from *outside*, from the pkgtool command line
%define version %{guile_version}
%endif
#special handling of version / guile_version

%ifarch amd64 sparcv9
%include arch64.inc
%use guile_64 = guile.spec
%endif

%include base.inc
%use guile = guile.spec


Name:                SFEguile
IPS_Package_Name:	library/guile
URL:                 http://www.gnu.org/software/guile/
Summary:             Embeddable Scheme implementation written in C
Version:             %{version}
Source:              http://ftp.gnu.org/pub/gnu/guile/guile-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEgmp
Requires:      SFEgmp
#not in version 1.8.8 BuildRequires: SFElibunistring
#not in version 1.8.8 Requires:      SFElibunistring
BuildRequires:  %{pnm_buildrequires_SFEautomake_115}
BuildRequires: %{pnm_buildrequires_SUNWlibtool_devel}
Requires:      %{pnm_requires_SUNWlibtool}
BuildRequires: %{pnm_buildrequires_SUNWltdl_devel}
Requires:      %{pnm_requires_SUNWltdl}
BuildRequires: %{pnm_buildrequires_SUNWlibm}
Requires:      %{pnm_requires_SUNWlibm}

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %{name}-%{version}

%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%guile_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_isa
%guile.prep -d %{name}-%{version}/%base_isa

%build

%ifarch amd64 sparcv9
%guile_64.build -d %{name}-%{version}/%_arch64
%endif

%guile.build -d %{name}-%{version}/%{base_isa}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%guile_64.install -d %{name}-%{version}/%_arch64
%endif

%guile.install -d %{name}-%{version}/%{base_isa}

#mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
#No ISAEXEC please. Directly call /usr/bin/guile for 32-bit or /usr/bin/amd64/guile or /usr/bin/sparc*/guile

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%ifarch amd64 sparcv9
#%{_bindir}/%{base_isa}/*
%{_bindir}/guile*
%{_bindir}/%{_arch64}/*
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/guile/*
%{_datadir}/info/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%if %( expr %{omnios} '=' 0 )
#not on OmniOS
%dir %attr (0755, root, bin) %{_datadir}/emacs
%dir %attr (0755, root, bin) %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*
%endif

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
* Sun Jul 31 2016 - Thomas Wagner
- make it 32/64 bit for autogen
* Tue May 24 2016 - Thomas Wagner
- add patch2 guile-02-1.8.8-dd_fd-d_fd.diff (OIH)
* Fri Apr 29 2016 - Thomas Wagner
- change (Build)Requires %{pnm_buildrequires_SFEautomake_115}
* Wed Apr 13 2016 - Thomas Wagner
- Bump to 2.0.11
- build on S11 and OmniOS
* Wed Jan 13 2016 - Thomas Wagner
- Bump to 1.8.8
- change back to SFEgmp (OM)
* Sat Oct 11 2013 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWlibm}, %include packagenamacros.inc
* Sun Jan 18 2009 - halton.huo@sun.com
- Change SFEgmp to SUNWgnu-mp
- Add patch autoconf.diff to fix AM_INTL_SUBDIR not found issue
* Tue Sep 02 2008 - halton.huo@sun.com
- Add /usr/share/aclocal to ACLOCAL_FLAGS to fix build issue
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add site dir
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Bump to 1.8.5
- Remove upstreamed patches: suncc-inline.diff,
  var-imaginary.diff and define-function.diff.
- Update %files 
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Update Requires
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Bump to 1.8.3 
- Add patch define-function.diff
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 1.8.2
- Use default automake and aclocal
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Fix Source from ftp to http.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Use automake-1.9 and aclocal-1.9
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 1.8.1.
- Add patch suncc-inline.diff and var-imaginary.diff
- Seperate package -devel
- Add Requires/BuildRequries after check-deps.pl run.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
