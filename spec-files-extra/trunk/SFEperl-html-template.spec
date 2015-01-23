#
# spec file for package: SFEperl-html-template
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 2.95
%define tarball_name    HTML-Template

Name:		SFEperl-html-template
IPS_package_name: library/perl-5/html-template
Version:	2.95
IPS_component_version: 2.95
Summary:	a simple HTML templating system
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~samtregar/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: perl.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/W/WO/WONKO/HTML-Template-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Sam Tregar <sam@tregar.com>
Meta(info.upstream_url):        http://search.cpan.org/~samtregar/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
a simple HTML templating system

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
#on older perl, e.g. 5.8.4
#NOTE: we need fresh extutils::makemaker, so search it in site_perl (it installs there in an exception)
#export PERL5LIB=%{_prefix}/%{perl_path_site_perl_version}
perl Makefile.PL \
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


%install
rm -rf $RPM_BUILD_ROOT
#on older perl, e.g. 5.8.4
#NOTE: we need fresh extutils::makemaker, so search it in site_perl (it installs there in an exception)
#export PERL5LIB=%{_prefix}/%{perl_path_site_perl_version}
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
* Fri Jan 23 2015 - Thomas Wagner
- fix copyright tag
* Mon Jun 30 2014 - Thomas Wagner
- bump to 2.95, re-create, tested only on S11.2
* Sat Aug 17 2013 - Thomas Wagner
- initial spec (2.94)
