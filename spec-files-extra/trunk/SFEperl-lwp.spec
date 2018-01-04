#
# spec file for package: SFEperl-lwp
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

%define tarball_version 6.26
#%define tarball_name    LWP
%define tarball_name    libwww-perl

Name:		SFEperl-lwp
#IPS_package_name: library/perl-5/lwp
IPS_Package_Name:	library/perl-5/libwww-perl-lwp
Version:	6.26
IPS_component_version: 6.26
Group:          Development/Libraries                    
Summary:	LWP - LWP
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~oalders/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/libwww-perl-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

#e.g. OmniOS has perl 5.24 with those modules included
%if %( expr %{perl_version_padded}.0 '<' 0005002400000000.0 )
BuildRequires:  SFEperl-encode
Requires:       SFEperl-encode
BuildRequires:  SFEperl-encode-locale
Requires:       SFEperl-encode-locale
BuildRequires:	SFEperl-io-compress
Requires:	SFEperl-io-compress
%else
#included in runtime/perl@5.24.1
%endif

BuildRequires:  SFEperl-http-message	
Requires:       SFEperl-http-message	
BuildRequires:	SFEperl-html-parser
Requires:	SFEperl-html-parser
BuildRequires:	SFEperl-uri
Requires:	SFEperl-uri
BuildRequires:  SFEperl-net-http
Requires:       SFEperl-net-http

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Olaf Alders <olaf@wundersolutions.com>
Meta(info.upstream_url):        http://search.cpan.org/~oalders/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
LWP
Libwww-perl

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
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3


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
- Thu Jan  4 2018 - Thomas Wagner
- change (Build)Requires active only for old perl version < 5.24.0 for SFEperl-encode SFEperl-encode-locale SFEperl-io-compress (OM)
* Fri Aug 12 2017 - Thomas Wagner
- reworked / renewed version 6.15 -> 6.26
- note: IPS_Component_Name different from what automatic script experimental/make_perl_cpan_settings.pl calculates
* Fri Mar 11 2016 - Thomas Wagner
- reworked / renewed version 6.05 -> 6.15
* Sat Oct  5 2013 - Thomas Wagner
- add (Build)Requires SFEperl-net-http
* Fri Oct  4 2013 - Thomas Wagner
- add (Build)Requires SFEperl-http-message, SFEperl-encode, SFEperl-encode-locale
* Thu Sep 26 2013 - Thomas Wagner
- bump to 6.05
* Fri Feb 01 2013 - Thomas Wagner
- change (Build)Requires to SFEperl-io-compress (now includes Zlib.pm from older SFEperl-compress-zlib)
* Sun May 27 2012 - Milan Jurik
- bump to 6.04, all except LWP:: went to separate packages
* Tue Feb  1 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
* Sun Jul 19 2009 - matt@greenviolet.net
- bumped verion to 5.829
- Added missing Requires
* Wed Nov 28 2007 - Thomas Wagner
- renamed package and if necessary (Build-)Requires
* Sat Nov 24 2007 - Thomas Wagner
- moved from site_perl to vendor_perl
- released into the wild
* Wed, 19 July 2007  - Thomas Wagner
- Initial spec file
