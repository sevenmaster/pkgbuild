##TODO##

#The following packages all deliver file actions to usr/perl5/vendor_perl/5.24/i86pc-solaris-thread-multi-64/HTML/PullParser.pm:

  #pkg://localhostoih/library/perl-5/html-parser@3.72,5.11-0.2017.0.0.5:20190126T013908Z
  #pkg://openindiana.org/library/perl-5/html-parser-524@3.72,5.11-2017.0.0.0:20170609T215240Z


#
# spec file for package: SFEperl-html-parser
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

%define tarball_version 3.72
%define tarball_name    HTML-Parser

Name:		SFEperl-html-parser
IPS_package_name: library/perl-5/html-parser
Version:	3.72
IPS_component_version: 3.72
Group:          Development/Libraries                    
Summary:	HTML::Parser - HTML::Parser
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~gaas/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTML-Parser-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:  %{pnm_buildrequires_SUNWpcre_devel}
Requires:       %{pnm_buildrequires_SUNWpcre}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Gisle Aas <gisle@ActiveState.com>
Meta(info.upstream_url):        http://search.cpan.org/~gaas/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
HTML::Parser
HTML::Parser

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

%include perl-bittness.inc

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


%include perl-bittness-make.inc

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
%{_mandir}/*/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Sat Aug 12 2017 - Thomas Wagner
- reworked spec, same version 3.72
* Sat Mar 12 2016 - Thomas Wagner
- accept gcc compiler on OmniOS and Hipster, linking errors (OM OIH)
* Fri Mar 11 2016 - Thomas Wagner
- add (Build)Requires pnm_buildrequires_SUNWpcre_devel
* Sun Feb 28 2016 - Thomas Wagner
- initial spec
