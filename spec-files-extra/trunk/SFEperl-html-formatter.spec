#
# spec file for package: SFEperl-html-formatter
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

%define tarball_version 2.14
%define tarball_name    HTML-Formatter

Name:		SFEperl-html-formatter
IPS_package_name: library/perl-5/html-formatter
Version:	2.14
IPS_component_version: 2.14
Group:          Development/Libraries                    
Summary:	HTML::Formatter - Convert HTML to plain text or Postscript
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~jgoff/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/N/NI/NIGELM/HTML-Formatter-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

BuildRequires:  SFEperl-test-cpan-meta
BuildRequires:  SFEperl-test-notabs
BuildRequires:  SFEperl-test-eol
BuildRequires:  SFEperl-html-tree

#SFEperl-html-formatter.log:pkgbuild:  - ERROR: Test::CPAN::Meta is not installed
#SFEperl-html-formatter.log:pkgbuild:  - ERROR: Test::NoTabs is not installed
#SFEperl-html-formatter.log:pkgbuild:  - ERROR: Test::EOL is not installed
#SFEperl-html-formatter.log:pkgbuild:  - ERROR: HTML::Element is not installed  -->>  SFEperl-html-tree
#SFEperl-html-formatter.log:pkgbuild:  - ERROR: HTML::TreeBuilder is not installed  -->>  SFEperl-html-tree


Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Jeff Goff <drforr@pobox.com>
Meta(info.upstream_url):        http://search.cpan.org/~jgoff/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
HTML::Formatter
Convert HTML to plain text or Postscript

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

if test -f Makefile.PL
  then
  # style "Makefile.PL"
  /usr/perl%{perl_major_version}/%{perl_version}/bin/perl Makefile.PL \
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
  /usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT

  /usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build build
fi

%install
rm -rf $RPM_BUILD_ROOT
if test -f Makefile.PL
   then
   # style "Makefile.PL"
   make install
else
   # style "Build.PL"
   /usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build install
fi

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
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Fri Feb 26 2016 - Thomas Wagner
- add dependencies
* Sat Feb 20 2016 - Thomas Wagner
- initial spec
