#
# spec file for package: SFEperl-io-socket-ssl
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

%define tarball_version 2.024
%define tarball_name    IO-Socket-SSL

Name:		SFEperl-io-socket-ssl
IPS_package_name: library/perl-5/io-socket-ssl
Version:	2.024
IPS_component_version: 2.24
Group:          Development/Libraries                    
Summary:	IO::Socket::SSL - IO::Socket::SSL
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~sullr/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

BuildRequires:  SFEperl-net-ssleay
Requires:       SFEperl-net-ssleay


Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Steffen Ullrich <Steffen_Ullrich@genua.de>
Meta(info.upstream_url):        http://search.cpan.org/~sullr/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
IO::Socket::SSL
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

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
* Tue Mar 22 2016 - Thomas Wagner
- remove (Build)Requires SFEperl-io-socket
* Wed Mar 16 2016 - Thomas Wagner
- renew / rework version 1.77 -> 2.024 (IPS 2.24)
* Sun Nov  4 2012 - Thomas Wagner
- bump to 1.77 (from 1.33)
- create new spec file with make_perl_cpan_settings.pl (align with other perl module spec files)
* Thu Sep 02 2010 - Milan Jurik
- Initial spec based on Fedora
