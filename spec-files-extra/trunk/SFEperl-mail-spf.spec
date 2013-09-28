#
# spec file for package: SFEperl-mail-spf
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version v2.8.0
%define tarball_name    Mail-SPF

Name:		SFEperl-mail-spf
IPS_package_name: library/perl-5/mail-spf
Version:	v2.8.0
IPS_component_version: 0.8.0
Summary:	Sender Permitted From - Object Oriented
License:	BSD
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~shevek/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}license.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/J/JM/JMEHNLE/mail-spf/Mail-SPF-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:           SFEperl-module-build

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Shevek <cpan@anarres.org>
Meta(info.upstream_url):        http://search.cpan.org/~shevek/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Sender Permitted From - Object Oriented

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
#NOTE: this module might need more parameters set to place files in the place
#/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL installdirs=vendor
#
#CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC ./Build

/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT

/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build build \
    --config "cc=$CXX" --config "ld=$CXX" \
    --extra_compiler_flags "-Iinclude" --extra_linker_flags ""

%install
rm -rf $RPM_BUILD_ROOT
#./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build install \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \

mkdir $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT/%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/spfquery $RPM_BUILD_ROOT/%{_bindir}/spfquery.pl
rmdir  $RPM_BUILD_ROOT/%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin
rmdir  $RPM_BUILD_ROOT/%{_prefix}/perl%{perl_major_version}/%{perl_version}

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755,root,bin) %{_sbindir}
%{_sbindir}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Fri Sep 27 2013 - Thomas Wagner
- rename query tools /usr/bin/spfquery -> spfquery.pl (avoid file conflict with SFElibsp2.spec)
* Wed Nov 28 2012 - Thomas Wagner
- re-create spec file by script, change back to Build.PL, fix placement of bin and man
- use IPS_Package_Name
* Sat May 12 2012 - Thomas Wagner
- bump tp 2.8.0
- re-work Build system because old method failed to use correct locations
  for target directories completely
* Fri May 11 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_perl_default}
* Thr Apr 30 2009 - Thomas Wagner
- Initial spec file
