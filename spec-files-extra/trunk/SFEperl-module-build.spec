#
# spec file for package: SFEperl-module-build
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

#consider switching off dependency_generator to speed up packaging step
#if there are no binary objects in the package which link to external binaries
#%define _use_internal_dependency_generator 0

%define tarball_version 0.4224
%define tarball_name    Module-Build

Name:		SFEperl-module-build
IPS_package_name: library/perl-5/module-build
Version:	0.4224
IPS_component_version: 0.4224
Group:          Development/Libraries                    
Summary:	Module::Build - Module::Build
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~leont/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/Module-Build-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:  SFEperl-perl-ostype
Requires:       SFEperl-perl-ostype
BuildRequires:  SFEperl-module-metadata
Requires:       SFEperl-module-metadata
BuildRequires:  SFEperl-version
Requires:       SFEperl-version

BuildRequires:  SFEperl-cpan-meta-yaml
Requires:       SFEperl-cpan-meta-yaml
#CPAN::Meta (2.141520) is installed, but we need version >= 2.142060
BuildRequires:  SFEperl-cpan-meta
Requires:       SFEperl-cpan-meta
#parse-cpan-meta >= 1.4401
BuildRequires:  SFEperl-parse-cpan-meta
Requires:       SFEperl-parse-cpan-meta
#TAP::Harness (3.17) is installed, but we need version >= 3.29
#contained in Test::Harness
#we assume perl 5.22.1 has harness fresh enough (##TODO## research which perl version bundles harness >= 3.29, adjust perl_version_padded)
%if %( expr %{perl_version_padded}.0 '<' 0005002200010000.0 )
BuildRequires:  SFEperl-test-harness
Requires:       SFEperl-test-harness
%endif
#inc::latest (0.3603) is installed, but we need version >= 0.5
BuildRequires:  SFEperl-inc-latest
Requires:       SFEperl-inc-latest

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Ken Williams <kwilliams@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~kwilliams/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Module::Build
Build, test, and install Perl modules

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

if test -f Makefile.PL
  then
  # style "Makefile.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \



%if %( perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null && echo 1 || echo 0 )
  make
%else
  make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC
%endif

else
  # style "Build.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT \



  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build build
fi

%install
rm -rf $RPM_BUILD_ROOT
if test -f Makefile.PL
   then
   # style "Makefile.PL"
   make install
else
   # style "Build.PL"
   %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build install
fi

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}
mv $RPM_BUILD_ROOT%{_prefix}/lib/site_perl/Module $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

[ -d $RPM_BUILD_ROOT/%{_mandir} ] || mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv $RPM_BUILD_ROOT/%{_prefix}/man $RPM_BUILD_ROOT/%{_mandir}/

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
%{_mandir}/*/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Sat Feb  9 2019 - Thomas Wagner
- reworked, bump from 0.4216 to 0.4224 
* Sun Dec  3 2017 - Thomas Wagner
- fix expr in perl_version_padded for dependency calulation
* Sat Dec  2 2017 - Thomas Wagner
- make Build)Requires conditional, new perl doesn't need Test::Harness in updated version (all)
* Mon Mar  7 2016 - Thomas Wagner
- renewed spec
- add (Build)Requires 
* Fri Sep 27 2013 - Thomas Wagner
- add (Build)Requires SFEperl-perl-ostype, SFEperl-module-metadata, SFEperl-version
* Sat Aug 17 2013 - Thomas Wagner
- recreate spec file by make_perl_cpan_settings.pl
- bump to 0.39_02 (0.3902 on IPS)
* Sat Jun 23 2012 - Thomas Wagner
- change to BuildRequires: %{pnm_buildrequires_SFEperl_extutils_cbuilder}
  note: more fresh perl versions bundle that module, pnm_macros knows that
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Thu Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- take care of special moving around of mis-layed directories (as well now with parametrized perl location/version)
- remove /auto/.packlist
* Wed Sep 12 2007 - nonsea@users.sourceforge.net
- Initial spec
