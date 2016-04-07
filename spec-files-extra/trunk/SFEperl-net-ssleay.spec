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

%define tarball_version 1.72
%define tarball_name    Net-SSLeay

Name:		SFEperl-net-ssleay
#do not interfere with Solaris userland/userland-incorporation! Keep the "sfe/" in IPS_Package_Name
IPS_package_name: sfe/library/perl-5/net-ssleay
Version:	1.72
IPS_component_version: 1.72
Group:          Development/Libraries                    
Summary:	Net::SSLeay - Secure Socket Layer (based on OpenSSL) (site_perl)
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~flora/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Florian Ragwitz <rafl@debian.org>
Meta(info.upstream_url):        http://search.cpan.org/~flora/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
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

%build

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
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3


%if %( perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null && echo 1 || echo 0 )
  make
%else
  make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC 
##TODO## find a propper way to not ask about testing
#workaround testing question (no / do not test)
#make CC=$CC CCCDLFLAGS="%picflags  -DSTRLEN=site_t" OPTIMIZE="%optflags" LD=$CC
%endif

else
  # style "Build.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs site --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_site_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_site_perl_version}/%{perl_dir} \
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
* Tue Apr  5 2016 - Thomas Wagner
- rework/new version 1.63 -> 1.72
#- keep the changed package name sfe/
- note: installs into site_perl to avoid file conflicts with OS provided Net::SSLeay
* Sun Aug 10 2014 - Thomas Wagner
- rename IPS_package_name: sfe/library/perl-5/net-ssleay (Some osdistro already have net-ssleay which leads to e.g. updating the sfe-incorporation on OI)
* Sun Jun  8 2014 - Thomas Wagner
- initial spec 1.63
