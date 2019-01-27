#
# spec file for package: SFEperl-xml-parser
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

%define tarball_version 2.44
%define tarball_name    XML-Parser

Name:		SFEperl-xml-parser
IPS_package_name: sfe/library/perl-5/xml-parser
Version:	2.44
IPS_component_version: 2.44
Group:          Development/Libraries                    
Summary:	XML::Parser - XML::Parser
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~toddr/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/XML-Parser-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

#Requires: binary dependency for /usr/perl5/site_perl/5.12/i86pc-solaris-64int/auto/XML/Parser/Expat/Expat.so

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Todd Rinaldo <toddr@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~toddr/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
XML::Parser
Flexible fast parser with plug-in styles

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

%include perl-bittness.inc

if test -f Makefile.PL
  then
  # style "Makefile.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1sfe \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3sfe \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1sfe \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3sfe \


%include perl-bittness.inc


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
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_site_perl_version}
%{_prefix}/%{perl_path_site_perl_version}/*
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
* Mon Jan 28 2019 - Thomas Wagner
- fix compile with 64-bit perl  (%include perl-bittness.inc)
* Thu Sep 28 2017 - Thomas Wagner
- reworked and bump verion 2.40 -> 2.44
- special: s/vendor_perl/site_perl/ to avoid clush with OS installed perl-xml-parser package
- special: IPS_package_name: sfe/library/perl-5/xml-parser
- special: relocate man pages into man1sfe and man3sfe (could have been man1site_perl and man3site_perl as well)
* Fri Jul  8 2011 - Alex Viskovatoff
- Change (Build)Requires to %{pnm_buildrequires_perl_default}
* Fri Mar  6 2011 - Alex Viskovatoff
- Generate new spec with make_perl_cpan_settings.pl
