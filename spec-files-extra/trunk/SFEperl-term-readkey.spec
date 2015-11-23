#
# spec file for package: SFEperl-term-readkey
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

#%define _use_internal_dependency_generator 0

%define tarball_version 2.33
%define tarball_name    Term-ReadKey

Name:		SFEperl-term-readkey
IPS_package_name: library/perl-5/term-readkey
Version:	2.33
IPS_component_version: 2.33
Group:          Development/Libraries                    
Summary:	Read keystrokes and change terminal modes
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~jstowe/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/J/JS/JSTOWE/TermReadKey-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Jonathan Stowe <jns@gellyfish.co.uk>
Meta(info.upstream_url):        http://search.cpan.org/~jstowe/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Read keystrokes and change terminal modes

%prep
#%setup -q -n %{tarball_name}-%{tarball_version}
%setup -q -n TermReadKey-%{tarball_version}

%build
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
* Mon Nov 23 2015 - Thomas Wagner
- initial spec
- needs a SFEgcc with present libssp_nonshared.a or fail linking with gcc with options -shared -fstack-protector (gcc based distro like OIH)
