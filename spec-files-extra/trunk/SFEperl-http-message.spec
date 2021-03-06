#
# spec file for package: SFEperl-http-message
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

%define tarball_version 6.11
%define tarball_name    HTTP-Message

Name:		SFEperl-http-message
IPS_package_name: library/perl-5/http-message
Version:	6.11
IPS_component_version: 6.11
Group:          Development/Libraries                    
Summary:	HTTP::Message - Base class for Request/Response
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~lwwwp/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/HTTP-Message-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:  SFEperl-http-date
Requires:       SFEperl-http-date
BuildRequires:  SFEperl-uri
Requires:       SFEperl-uri
BuildRequires:  SFEperl-lwp-mediatypes
Requires:       SFEperl-lwp-mediatypes
#e.g. OmniOS has perl 5.24 with those modules included
#e.g. Hipsterhas perl 5.22 with those modules included
%if %( expr %{perl_version_padded}.0 '<' 0005002200000000.0 )
#get Encode::Alias
BuildRequires:  SFEperl-encode
Requires:       SFEperl-encode
BuildRequires:  SFEperl-encode-locale
Requires:       SFEperl-encode-locale
%else
#included in runtime/perl@5.24.1
%endif
BuildRequires:  SFEperl-io-html
Requires:       SFEperl-io-html

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            The libwww-perl mailing list <libwww@perl.org>
Meta(info.upstream_url):        http://search.cpan.org/~lwwwp/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
HTTP::Message
Base class for Request/Response

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
- Sat Jan 20 2018 - Thomas Wagner
- change (Build)Requires active only for old perl version < 5.22.0 for SFEperl-encode SFEperl-encode-locale (OIH)
- Thu Jan  4 2018 - Thomas Wagner
- change (Build)Requires active only for old perl version < 5.24.0 for SFEperl-encode SFEperl-encode-locale (OM)
* Fri Mar 11 2016 - 
- initial spec
- rework / renew version 6.11
* Fri Oct  4 2013 - Thomas Wagner
- bump to 6.06 (6.6 on IPS)
* Sun May 27 2012 - Milan Jurik
- initial spec
