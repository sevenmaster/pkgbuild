#
# spec file for package: SFEperl-netaddr-ip
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

%define tarball_version 4.079
%define tarball_name    NetAddr-IP

Name:		SFEperl-netaddr-ip
IPS_package_name: library/perl-5/netaddr-ip
Version:	4.079
IPS_component_version: 4.79
Group:          Development/Libraries                    
Summary:	NetAddr::IP - NetAddr::IP
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~miker/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIKER/NetAddr-IP-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Michael Robinton <michael@bizsystems.com>
Meta(info.upstream_url):        http://search.cpan.org/~miker/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
NetAddr::IP
NetAddr::IP
Manipulation and operations on IP addresses

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
* Mon Jan 28 2019 - Thomas Wagner
- fix compile with 64-bit perl (%include perl-bittness.inc)
*     Aug 12 2017
- reworked, bump version 4.066 -> 4.079
* Wed Nov 28 2012 - Thomas Wagner
- bump to 4.0.66 4.66 (IPS)
- re-make spec file with make_perl_cpan_settings.pl
* Sat Mar 31 2012 - Pavel Heimlich
- version bump
* Fri Jun 17 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- BuildRequires: %{pnm_buildrequires_SUNWsfwhea}
* Mon, 28 Apr 2009  - Thomas Wagner
- Initial spec
- make version number without leading zeros to meet IPS needs
