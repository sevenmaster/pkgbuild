#
# spec file for package: SFEperl-razor2-client-agent
#
# This file and all modifications and additions to the pristine
# package are 
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

#consider switching off dependency_generator to speed up packaging step
#if there are no binary objects in the package which link to external binaries
%define _use_internal_dependency_generator 0

%define tarball_version 2.84
%define tarball_name    Razor2-Client-Agent

Name:		SFEperl-razor2-client-agent
IPS_package_name: library/perl-5/razor2-client-agent
Version:	2.84
IPS_component_version: 0
Group:          Development/Libraries                    
Summary:	Razor2::Client::Agent - Razor2::Client::Agent
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~toddr/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/Razor2-Client-Agent-%{tarball_version}.tar.gz
#Source:                  http://downloads.sourceforge.net/razor/razor-agents-%{module_version}.tar.bz2
Patch1:         razor2-client-agent-01-Makefile-quoting.diff

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Todd Rinaldo <toddr@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~toddr/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Razor2::Client::Agent
Razor2::Client::Agent

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

%include perl-bittness.inc

#fix quoting for MAN5 in Makefile
[ -f Makefile ] && rm Makefile

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
    INSTALLSITEMAN5DIR=$RPM_BUILD_ROOT%{_mandir}/man5 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN5DIR=$RPM_BUILD_ROOT%{_mandir}/man5 \


%include perl-bittness-make.inc


#correct (seen with MakeMaker 6.56 on S11.3 GA perl 5.12)
#   $(INST_MAN5DIR) $(DESTINSTALLMAN5DIR) \
#wrong (seen with MakeMaker 7.1002 on OmniOSce perl 5.24) - one >"< is lost
#  "$(INST_MAN1DIR)" "$(DESTINSTALLMAN1DIR) \
#  $(INST_MAN5DIR) $(INSTALLMAN5DIR)" \
#fix quoting for MAN5 in Makefile - if we see an opening but no closing >"<
grep '"$(DESTINSTALLMAN1DIR) ' Makefile > /dev/null && patch -p0 < %{PATCH1}



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
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
%{_mandir}/*/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Mon Jan 28 2019 - Thomas Wagner
- fix compile with 64-bit perl  (%include perl-bittness.inc)
* Sat Jan  6 2017 - Thomas Wagner
- add patch1 fix quoting in Makefile for MAN5 path
* Sun Aug 13 2017 - Thomas Wagner
- reworked, version 2.84
* Wed Nov 28 2012 - Thomas Wagner
- bump to 2.85
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- take care of special moving around of mis-layed directories (as well now with parametrized perl location/version)
* Tue Feb  1 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
* Sun Mai 03 2009  - Thomas Wagner
- initial spec
