#
# spec file for package: SFEperl-test-script
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 1.07
%define tarball_name    Test-Script

Name:		SFEperl-test-script
IPS_package_name: library/perl-5/test-script
Version:	1.07
IPS_component_version: 1.7
Summary:	Test::Script
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~adamk/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Test-Script-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Adam Kennedy <adamk@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~adamk/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
The intent of this module is to provide a series of basic tests for 80%
of the testing you will need to do for scripts in the script (or bin as
is also commonly used) paths of your Perl distribution.
Further, it aims to provide this functionality with perfect
platform-compatibility, and in a way that is as unobtrusive as possible.
That is, if the program works on a platform, then Test::Script should
always work on that platform as well. Anything less than 100% is
considered unacceptable.
In doing so, it is hoped that Test::Script can become a module that you
can safely make a dependency of all your modules, without risking that
your module won't on some platform because of the dependency.
Where a clash exists between wanting more functionality and maintaining
platform safety, this module will err on the side of platform safety.

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC


%install
rm -rf $RPM_BUILD_ROOT
make install

#remove $RPM_BUILD_ROOT/usr/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/auto/File/Which/.packlist
#..../i86pc-solaris-64int/perllocal.pod
rm -r $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} 

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
* Fri Nov  2 2012 - Thomas Wagner
- add description
* Tue Aug 14 2012 - Thomas Wagner
- initial spec
