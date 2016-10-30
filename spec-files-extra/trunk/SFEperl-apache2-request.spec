##TODO## find a way to specify apach 2.2 or 2.4, config helper "apxs" is only a mediated symlink /usr/bin/apxs, therefore out of control of our dependecy checks
#        specify full path instead? /usr/apache2/2.2/bin/apxs or /usr/apache2/2.4/bin/apxs and require this depdendent of the pnm macro apache2_default?

##NOTE## Non-Standard Perl module! configure / Makefile.PL works differently then for a usual perl module

##TODO## make default apache 32 or 64-bit version numbers and paths a pnm_macro and use it here (search for string "22" and "2\.2")


#
# spec file for package: SFEperl-apache2-request
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

%define tarball_version 2.13
%define tarball_name    libapreq2 

Name:		SFEperl-apache2-request
IPS_package_name: library/perl-5/apache2-request
Version:	2.13
IPS_component_version: 2.13
Group:          Development/Libraries                    
Summary:	Apache2::Request - Apache2::Request
License:	Apache
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~joesuf/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/I/IS/ISAAC/libapreq2-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

#mod_perl2: 2.000004 ok
#Apache::Test: 1.31 ok
#ExtUtils::MakeMaker: 7.18 ok
#ExtUtils::XSBuilder: 0.28 ok
#Test::More: 0.98 ok

BuildRequires:  web/server/apache-22/module/apache-perl
Requires:       web/server/apache-22/module/apache-perl

BuildRequires:  SFEperl-extutils-makemaker
Requires:       SFEperl-extutils-makemaker
BuildRequires:  SFEperl-extutils-xsbuilder
Requires:       SFEperl-extutils-xsbuilder
BuildRequires:  SFEperl-parse-recdescent
Requires:       SFEperl-parse-recdescent


Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Joe Schaefer <apreq-dev@httpd.apache.org>
Meta(info.upstream_url):        http://search.cpan.org/~joesuf/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Apache2::Request

currenlty only works with apache in 32-bit, as the libraries used by perl are 32-bit as well.


%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

#do not remove!
##TODO## make this a full path to /usr/apache2/2.2/bin/apxs or /usr/apache2/2.4/bin/apxs and require this depdendent of the pnm macro apache2_default
##paused## APACHE2_APXS=/usr/bin/apxs

##temporaritly, we only can work with apache 2.2 in 32-bit!
APACHE2_APXS=/usr/apache2/2.2/bin/apxs

#if we have a 32-bit perl and a 64-bit apache httpd, then we need to tweak the apxs output, or we can't link the library (arch mismatch)
##paused## mkdir bin
##paused## cat - > bin/apxs_wrapper << EOF
##paused## #!/usr/bin/bash
##paused## ${APACHE2_APXS} \${@}| gsed -e 's?/%{_arch64}??g'
##paused## EOF
##paused## APACHE2_APXS=`pwd`/bin/apxs_wrapper
##paused## chmod a+rx ${APACHE2_APXS}


#find ModPerl/MM.pm
#(1/2)
export PERL5LIB=/usr/apache2/2.2/lib/perl


%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Makefile.PL \
 --with-apache2-apxs=${APACHE2_APXS} \
 --with-perl-opts="PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3     \
    INSTALLDIRS=vendor"
 
#replace all occurences of site_perl with vendor_perl. looks like variables from outsite are not honored
gsed -i -e '/INSTALL/ s?site_perl?vendor_perl?' -e '/SITE/ s?site_perl?vendor_perl?' `ggrep  -l -r /site_perl/`

#man3 goes into unusual place 
#/usr/perl5/5.12/man/man3 - not chaning


%if %( perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null && echo 1 || echo 0 )
  make
%else
  make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC PERL5LIB=${PERL5LIB}
%endif


%install
rm -rf $RPM_BUILD_ROOT

#find ModPerl/MM.pm
#(2/2)
export PERL5LIB=/usr/apache2/2.2/lib/perl

if test -f Makefile.PL
   then
   # style "Makefile.PL"
   make install DESTDIR=${RPM_BUILD_ROOT} PERL5LIB=${PERL5LIB} INSTALLDIRS=vendor
else
   # style "Build.PL"
   %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build install
fi

#replaced by gsed in %build# echo "installing into vendor_perl is not honored, so move it manually"
#replaced by gsed in %build# echo "mv ${RPM_BUILD_ROOT}/%{_prefix}/%{perl_path_site_perl_version} $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}"
#replaced by gsed in %build# mv ${RPM_BUILD_ROOT}/%{_prefix}/%{perl_path_site_perl_version} $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

#left over, empty directory /usr/perl5/5.12/lib/i86pc-solaris-64int
[ -d $RPM_BUILD_ROOT/%{_prefix}/perl%{perl_major_version}/%{perl_version}/lib ] && echo "removing empty %{_prefix}/perl%{perl_major_version}/%{perl_version}/lib" && rm -r $RPM_BUILD_ROOT/%{_prefix}/perl%{perl_major_version}/%{perl_version}/lib

#remove "*.la" static libs
find $RPM_BUILD_ROOT/usr \( -name \*.la -o -name \*.a \) -exec  %{__rm} {} \;



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
#%dir %attr(0755,root,bin) %{_bindir}
#%{_bindir}/*
#%dir %attr(0755,root,sys) %{_datadir}
#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
#%{_mandir}/*/*

#NOTE: installs into unusual place /usr/perl5/5.12/man/man3/
%{_prefix}/perl%{perl_major_version}/%{perl_version}/man/*/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%defattr(-,root,bin)
/usr/apr-util/*
        #/usr/apr-util/1.5/include
        #/usr/apr-util/1.5/lib
        #/usr/apr-util/1.5/bin

/usr/apache2/*
        #/usr/apache2/2.2/include
        #/usr/apache2/2.2/libexec

%changelog
* Mon Aug  8 2016 - Thomas Wagner
- add missing (Build)Requires SFEperl-parse-recdescent
* Mon Jun  6 2016 - Thomas Wagner
- initial spec - note: non-standard build and install (this is no not the default spec file produced by make_perl_cpan_settings.pl)
