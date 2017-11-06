



##TODO## Auto-detect, ob perl ein 64-bit-perl ist oder nicht ---  -m64 dazu schreiben.
# perl -V hat vielleicht ein -64 oder -m64 drin, dann ist es 64 bit. oder "file libperl.so" im CORE Verzeichnis







#
# spec file for package: SFEperl-encode-detect
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%if %omnios
#perl built with gcc / g++
%define cc_is_gcc 1
%include base.inc
%endif

#consider switching off dependency_generator to speed up packaging step
#if there are no binary objects in the package which link to external binaries
%define _use_internal_dependency_generator 0

%define tarball_version 1.01
%define tarball_name    Encode-Detect

Name:		SFEperl-encode-detect
IPS_package_name: library/perl-5/encode-detect
Version:	1.01
IPS_component_version: 1.1
Group:          Development/Libraries                    
Summary:	Encode::Detect - Encode::Detect
#License:	Artistic
License:	mozilla1.1
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~jgmyers/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/J/JG/JGMYERS/Encode-Detect-%{tarball_version}.tar.gz
Patch1:	                 encode-detect-01-sunpro.diff

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
#from former spec file
BuildRequires:           %{pnm_buildrequires_SUNWsfwhea}
BuildRequires:           %{pnm_buildrequires_SFEperl_extutils_cbuilder}
#pkgtool doesn't detect this otherwise
Requires:                %{pnm_requires_SFEperl_extutils_cbuilder}
BuildRequires:           SFEperl-module-build

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            John Gardiner Myers <jgmyers@proofpoint.com>
Meta(info.upstream_url):        http://search.cpan.org/~jgmyers/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Encode::Detect
Encode::Detect

%prep
%setup -q -n %{tarball_name}-%{tarball_version}
chmod +w Detector.xs
%patch1 -p1

%build
%if %cc_is_gcc
export CC=gcc
export CXX=g++
%else
export CXX="${CXX} -norunpath"
%endif

echo "remove Makefile.PL  -  because it is broken in terms of installing into the correct taget directories."
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
#or get:
# error building src/nsCharSetProber.o from 'src/nsCharSetProber.cpp' at /usr/perl5/5.12/lib/ExtUtils/CBuilder/Base.pm line 112.
export CC=$CXX
  make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD="$CC"
%endif

else
  # style "Build.PL"
%if %{omnios}
echo "setting paramters for OmniOS"
export CC=$CXX
export EXTRA="--config cc=$CC --config ld=$CC --config $( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:lddlflags | sed -e 's?-64?-m64?' -e 's?;$??' )"
export EXTRA="${EXTRA} --extra_linker_flags -G --extra_linker_flags -m64"
%else
# hack: use C++ compiler because it tries with cc otherwise
export CC=$CXX
export EXTRA="--config cc=$CC --config ld=$CC"
%endif
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT

echo "EXTRA: >$EXTRA<"

  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build build \
    --extra_compiler_flags "-Iinclude" \
    ${EXTRA}
fi

%install
rm -rf $RPM_BUILD_ROOT
##raus #or get:
##raus # error building src/nsGB2312Prober.o from 'src/nsGB2312Prober.cpp' at /usr/perl5/5.12/lib/ExtUtils/CBuilder/Base.pm line 112.
##raus export CC=$CXX
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
* Sa Aug 12 2017 - Thomas Wagner
- reworked, same version 1.01
- kept extra tweaks from previous spec
- remove Makefile.PL as this leads to install into wrong target directories
* Wed Nov 28 2012 - Thomas Wagner
- re-create spec file by script
- use "Build" to build
* Sat May 12 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SFEperl_extutils_cbuilder}
- fix building with C++ on perl 5.8.4 and 5.12 (5.10)
* Sat Jul  2 2011 - Thomas Wagner
- fix Version: %{perl_version}.%{module_version}
- use full path to perl intepreter (still wrong interpreter used by Makefile (perl 5.12))
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- BuildRequires: %{pnm_buildrequires_SUNWsfwhea}
- make %build look more like the other spec files, old commands commented for history
- BuildRequires: SFEperl-modules-build
- use absolute path the perl interpreter (avoid wrong hit by searchpath)
* Thr Apr 30 2009 - Thomas Wagner
- bump to 1.01
- rework patch1
- make version number IPS capable
* Tue Apr 08 2008 - trisk@acm.jhu.edu
- Initial spec
