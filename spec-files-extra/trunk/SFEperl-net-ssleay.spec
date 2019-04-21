# 
# CONTAINED IN OS PERL DISTRIBUTION in e.g. version 1.36 - WHAT DO TO?
# 
# OPENINDIANA - nee to check if it is contained
# 
# OmniOS
# 
# Solaris 12
# 
# 
# Solaris 11.2:
#  ~/spec-files-extra pkg contents -r -m userland/userland-incorporation | grep -i ssleay
# depend facet.version-lock.library/perl-5/net-ssleay=true fmri=pkg:/library/perl-5/net-ssleay@1.36-0.175.2.0.0.40.0 type=incorporate
# depend facet.version-lock.library/perl-5/net-ssleay-512=true fmri=pkg:/library/perl-5/net-ssleay-512@1.36-0.175.2.0.0.40.0 type=incorporate
# depend facet.version-lock.library/perl-5/net-ssleay-584=true fmri=pkg:/library/perl-5/net-ssleay-584@1.36-0.175.2.0.0.40.0 type=incorporate
# depend facet.version-lock.SUNWperl-net-ssleay=true fmri=pkg:/SUNWperl-net-ssleay@1.35-0.133 type=incorporate


#  pkg://solaris/library/perl-5/net-ssleay-512@1.36,5.11-0.175.3.0.0.30.0:20150821T165637Z
#  pkg://localhosts11/sfe/library/perl-5/net-ssleay@1.63,5.11-0.0.175.3.1.0.5.0:20160405T175757Z



#
# spec file for package: SFEperl-net-ssleay
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

%define tarball_version 1.85
%define tarball_name    Net-SSLeay

Name:		SFEperl-net-ssleay
#do not interfere with Solaris userland/userland-incorporation! Keep the "sfe/" in IPS_Package_Name
IPS_package_name: sfe/library/perl-5/net-ssleay
Version:	1.85
IPS_component_version: 1.85
Group:          Development/Libraries                    
Summary:	Net::SSLeay - Net::SSLeay (site_perl)
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~mikem/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-%{tarball_version}.tar.gz

Patch1:         perl-01-net-ssleay-ask-ENV_CC-for-compiler-if-CC-defined.diff

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:	SFEperl-module-install
Requires:       SFEperl-module-install
BuildRequires:	SFEperl-extutils-cbuilder
Requires:       SFEperl-extutils-cbuilder

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Mike McCauley <mikem@airspayce.com>
Meta(info.upstream_url):        http://search.cpan.org/~mikem/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Net::SSLeay
Net::SSLeay
Secure Socket Layer (based on OpenSSL)

Attention: This package may have shared files with the OS provided package library/perl-5/net-ssleay
In case of package install problems, consider this:

You should manually uninstall library/perl-5/net-ssleay, if that is possible.
Then pkg install sfe/library/perl-5/net-ssleay

Attention: Instead of vendor_perl, this package installs into 
                      site_perl

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%patch1 -p1

%build

%include perl-bittness.inc
if test -f Makefile.PL
  then
  # style "Makefile.PL"
  echo "Switching off SSL test."
  echo "n" | \
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \



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
#%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
#%{_prefix}/%{perl_path_vendor_perl_version}/*
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
* Sun Apr 21 2019 - Thomas Wagner
- rework spec 1.72 -> 1.85
- fix build on hipster where perl -V:cc prints cc='/usr/gcc/4.9/bin/gcc -m64'; and this is not installed 
  by using ENV{CC} if defined - patch1 perl-01-net-ssleay-ask-ENV_CC-for-compiler-if-CC-defined.diff
- fix install path to store in site_perl
* Sat Apr 20 2019 - Thomas Wagner
- add (Build)Requires:  SFEperl-extutils-cbuilder (OIH)
* Sat Feb  9 2019 - Thomas Wagner
- fix compile with 64-bit perl  (%include perl-bittness.inc)
* Sat Jan 26 2019 - Thomas Wagner
- add (Build)Requires SFEperl-module-install
* Tue Apr  5 2016 - Thomas Wagner
- rework/new version 1.63 -> 1.72
#- keep the changed package name sfe/
- note: installs into site_perl to avoid file conflicts with OS provided Net::SSLeay
* Sun Aug 10 2014 - Thomas Wagner
- rename IPS_package_name: sfe/library/perl-5/net-ssleay (Some osdistro already have net-ssleay which leads to e.g. updating the sfe-incorporation on OI)
* Sun Jun  8 2014 - Thomas Wagner
- initial spec 1.63
