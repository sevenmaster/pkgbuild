
CONTAINED IN OS PERL DISTRIBUTION in e.g. version 1.36 - WHAT DO TO?

OPENINDIANA - nee to check if it is contained

OmniOS

Solaris 12


Solaris 11.2:
 ~/spec-files-extra pkg contents -r -m userland/userland-incorporation | grep -i ssleay
depend facet.version-lock.library/perl-5/net-ssleay=true fmri=pkg:/library/perl-5/net-ssleay@1.36-0.175.2.0.0.40.0 type=incorporate
depend facet.version-lock.library/perl-5/net-ssleay-512=true fmri=pkg:/library/perl-5/net-ssleay-512@1.36-0.175.2.0.0.40.0 type=incorporate
depend facet.version-lock.library/perl-5/net-ssleay-584=true fmri=pkg:/library/perl-5/net-ssleay-584@1.36-0.175.2.0.0.40.0 type=incorporate
depend facet.version-lock.SUNWperl-net-ssleay=true fmri=pkg:/SUNWperl-net-ssleay@1.35-0.133 type=incorporate



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

%define tarball_version 1.63
%define tarball_name    Net-SSLeay

Name:		SFEperl-net-ssleay
IPS_package_name: library/perl-5/net-ssleay
Version:	1.63
IPS_component_version: 1.63
Summary:	Secure Socket Layer (based on OpenSSL)
License:	OpenSSL
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~flora/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
#SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Florian Ragwitz <rafl@debian.org>
Meta(info.upstream_url):        http://search.cpan.org/~flora/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Secure Socket Layer (based on OpenSSL)

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
echo "n" | perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3

##TODO## find a propper way to not ask about testing
#workaround testing question (no / do not test)
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC


%install
rm -rf $RPM_BUILD_ROOT
make install

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
* Sun Jun  8 2014 - Thomas Wagner
- initial spec 1.63
