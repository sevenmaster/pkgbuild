#
# spec file for package: SFEperl-io-compress
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 2.062
%define tarball_name    IO-Compress

Name:		SFEperl-io-compress
IPS_package_name: library/perl-5/io-compress
Version:	2.062
IPS_component_version: 2.62
Summary:	IO::Compress
License:	perl
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~pmqs/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/IO-Compress-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Paul Marquess <pmqs@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~pmqs/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Note: IO::Compress includes sub modules
IO::Compress::Base
new package name is SFEperl-io-compress library/perl-5/io-compress (IPS)
old package name was SFEperl-io-compress-base library/perl-5/io-compress-base (IPS)


%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLVENDORLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLVENDORARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLVENDORMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLVENDORMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC


%install
rm -rf $RPM_BUILD_ROOT
make pure_install

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sun Dec  8 2013 - Thomas Wagner
- add INSTALLARCHLIB as it is sometimes empty on perl 5.10.x on OI, make complains on recoursive variable
* Thu Sep 26 2013 - Thomas Wagner
  bump to 2.062 (2.62 on IPS)
* Mon Dec 10 2012 - Thomas Wagner
- re-create spec file by script
  bump to 2.058 (2.58 on IPS)
- now includes Gzip, RawDeflate, Zip, Deflate, Bzip2, FAW, Base - obsoletes 
  IO-Compress-Base-2.015, IO-Compress-Bzip2-2.015, IO-Compress-Zlib-2.015 from SFE
- current consuming other spec files need updates: (Build)Requires: 
  SFEperl-io-compress-base instead of -zip -gzip -bzip2,
  known consumers: SFEperl-compress-zlib.spec (change is done)
- spec file renamed to SFEperl-io-compress to match the source tarball name
- include shared perl license file (perl + artistic)
- package new file /usr/bin/zipdetails
- add extra variabled to get module installed into vendor_lib
* Mon May 14 2012 - Thomas Wagner
- simplify %files
- add missing INSTALLVENDORLIB to get path vendor_perl work on perl 5.12
- bump to 2.015 (2.15 on IPS)
- add IPS_package_name library/perl-5/%{module_package_name}
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- BuildRequires: %{pnm_buildrequires_SUNWsfwhea}
- make version number IPS capable
* Tue Nov 13 2007 - trisk@acm.jhu.edu
- Initial spec
