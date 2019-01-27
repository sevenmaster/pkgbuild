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

#consider switching off dependency_generator to speed up packaging step
#if there are no binary objects in the package which link to external binaries
%define _use_internal_dependency_generator 0

%define tarball_version v2.9.0
%define tarball_name    Mail-SPF

Name:		SFEperl-mail-spf
IPS_package_name: library/perl-5/mail-spf
Version:	v2.9.0
IPS_component_version: 0.9.0
Group:          Development/Libraries                    
Summary:	Mail::SPF - Mail::SPF
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~jmehnle/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/J/JM/JMEHNLE/mail-spf/Mail-SPF-%{tarball_version}.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:	SFEperl-module-build
Requires:	SFEperl-module-build

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Julian Mehnle <julian@mehnle.net>
Meta(info.upstream_url):        http://search.cpan.org/~jmehnle/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Mail::SPF
Mail::SPF

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build


echo "removing Makefile.PL - installs into the wrong target directories"
rm -f Makefile.PL

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
#%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
%{_mandir}/*/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Sat Jan 26 2019 - Thomas Wagner
- add (Build)Requires:  SFEperl-module-build
* Sat Aug 12 2017 - Thomas Wagner
- reworked, bump version 2.8.0 -> 2.9.0 
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
