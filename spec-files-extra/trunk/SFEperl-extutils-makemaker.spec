#Important Note - this spec file disables bundling other modules!
#read: https://github.com/Perl-Toolchain-Gang/ExtUtils-MakeMaker/blob/master/bundled/README
#This directory contains CPAN modules which ExtUtils-MakeMaker depends on.
#They are bundled with ExtUtils-MakeMaker to avoid dependency loops.
#Vendor packages will want to disable this bundling.  See README.packaging in the top
#level directory for details.


#
# spec file for package: SFEperl-extutils-makemaker
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
%define _use_internal_dependency_generator 0

%define tarball_version 7.18
%define tarball_name    ExtUtils-MakeMaker

Name:		SFEperl-extutils-makemaker
IPS_package_name: library/perl-5/extutils-makemaker
Version:	7.18
IPS_component_version: 7.18
Group:          Development/Libraries                    
Summary:	ExtUtils::MakeMaker - Writes Makefiles for extensions
License:	Artistic
Url:		http://search.cpan.org/~mschwern/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/ExtUtils-MakeMaker-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

#Using included version of CPAN::Meta::Requirements (2.127) because it is not already installed.
#Using included version of ExtUtils::Manifest (1.65) as it is newer than the installed version (1.57).
#Using included version of JSON::PP (2.27203) because it is not already installed.
BuildRequires:  SFEperl-parse-cpan-meta
Requires:       SFEperl-parse-cpan-meta
BuildRequires:  SFEperl-cpan-meta-requirements
Requires:       SFEperl-cpan-meta-requirements
BuildRequires:  SFEperl-extutils-manifest
Requires:       SFEperl-extutils-manifest
BuildRequires:  SFEperl-json-pp
Requires:       SFEperl-json-pp

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Michael G Schwern <mschwern@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~mschwern/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
ExtUtils::MakeMaker
Writes Makefiles for extensions

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

echo "BUILDLING AS A PACKAGE WITH NO BUNDLED PREREQUISITE PERL MODULES"
echo "else you get file conflicts with e.g. parse-cpan-meta perl module"
echo "Setting ENV variable  export BUILDING_AS_PACKAGE=1"
echo "See README.packaging in the source"

#background: if system has a dependency not yet installed, then extutils-makemaker
#uses the bundles sources from this tarball. You end up in more then one IPS package
#packaging the *same* filenames *if* a prerequisite module is not built and installed
#before.
#happended with not installed SFEperl-parse-cpan-meta, this is now added as IPS dependency
#to the prerequisite perl module Parse::CPAN::Meta

#safety measure: Build will/should fail with unsatisfied perl dependency, then we can fix it on the
#build side and have a IPS depedency
export BUILDING_AS_PACKAGE=1

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
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3

  make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC
else
  # style "Build.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT

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

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

#hack: file of same name already present
[ -f $RPM_BUILD_ROOT%{_mandir}/man3/version.3 ] && mv $RPM_BUILD_ROOT%{_mandir}/man3/version.3 $RPM_BUILD_ROOT%{_mandir}/man3/version_.3

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
* Sun Jun  5 2016 - Thomas Wagner
- bump to 7.18
- set build process to *NOT* include bundles prerequisite modules. You would end
  up with file conflicts in IPS, depending of the order you build the perl modules
  export BUILDING_AS_PACKAGE=1
* Thu Mar 10 2016 - Thomas Wagner
- add (Build)Requires SFEperl-cpan-meta-requirements SFEperl-extutils-manifest SFEperl-json-pp
* Mon Mar  7 2016 - Thomas Wagner
- bump to 7.10
- rework spec
* Mon Jun 30 2014 - Thomas Wagner
- bump to 6.98 as download vanished
* Sat Aug 17 2013 - Thomas Wagner
- initial spec 6.72 - note exception to install into site_perl instead vendor_perl
