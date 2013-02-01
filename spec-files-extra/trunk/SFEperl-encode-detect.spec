#
# spec file for package: SFEperl-encode-detect
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 1.01
%define tarball_name    Encode-Detect

Name:		SFEperl-encode-detect
IPS_package_name: library/perl-5/encode-detect
Version:	1.01
IPS_component_version: 1.1
Summary:	An Encoding that detects encoding from data
License:	mozilla1.1
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~jgmyers/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: mozilla1.1.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/J/JG/JGMYERS/Encode-Detect-%{tarball_version}.tar.gz
Patch1:	                 encode-detect-01-sunpro.diff

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
#from former spec file
BuildRequires:           %{pnm_buildrequires_SUNWsfwhea}
BuildRequires:           %{pnm_buildrequires_SFEperl_extutils_cbuilder}
#pkgtool doesn't detect this otherwise
Requires:                %{pnm_requires_SFEperl_extutils_cbuilder}
BuildRequires:           SFEperl-module-build

Meta(info.upstream):            John Gardiner Myers <jgmyers@proofpoint.com>
Meta(info.upstream_url):        http://search.cpan.org/~jgmyers/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
An Encoding that detects encoding from data

%prep
%setup -q -n %{tarball_name}-%{tarball_version}
chmod +w Detector.xs
%patch1 -p1

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
#perl Makefile.PL \
#    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
#    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
#    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
#    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
#    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
#    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
#    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
#    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3

# hack: use C++ compiler because it tries with cc otherwise
export CC=$CXX
/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT

/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build build \
    --config "cc=$CXX" --config "ld=$CXX" \
    --extra_compiler_flags "-Iinclude" --extra_linker_flags ""

%install
rm -rf $RPM_BUILD_ROOT
/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build install 
#\
#    --destdir $RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
#%dir %attr(0755,root,bin) %{_bindir}
#%{_bindir}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Wed Nov 28 2012 - Thomas Wagner
- re-create spec file by script
- use "Build" to build
* Sat May 12 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SFEperl_extutils_cbuilder}
- fix building with C++ on perl 5.8.4 and 5.12 (5.10)
* Sat Jul  2 2011 - Thomas Wagner
- fix Version: %{perl_version}.%{module_version}
- use full path to perl intepreter (still wrong interpreter used by Makefile (perl 5.12))
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- BuildRequires: %{pnm_buildrequires_SUNWsfwhea}
- make %build look more like the other spec files, old commands commented for history
- BuildRequires: SFEperl-modules-build
- use absolute path the perl interpreter (avoid wrong hit by searchpath)
* Thr Apr 30 2009 - Thomas Wagner
- bump to 1.01
- rework patch1
- make version number IPS capable
* Tue Apr 08 2008 - trisk@acm.jhu.edu
- Initial spec
