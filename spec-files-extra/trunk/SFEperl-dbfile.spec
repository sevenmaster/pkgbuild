#
# spec file for package: SFEperl-db_file SFEperl-dbfile
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
#%define _use_internal_dependency_generator 0

%define tarball_version 1.843
%define tarball_name    DB_File

Name:		SFEperl-dbfile
IPS_package_name: library/perl-5/db_file
Version:	1.843
IPS_component_version: 1.843
Group:          Development/Libraries                    
Summary:	DB_File - DB_File
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~pmqs/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/DB_File-%{tarball_version}.tar.gz
Patch1:                  perl-dbfile-01-config.in-include_gnu.diff

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
Requires:                SFEbdb
BuildRequires:           SFEbdb

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Paul Marquess <pmqs@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~pmqs/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
DB_File
DB_File

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build

#perl -V | grep gcc
#    config_args='-de -Dmksymlinks -Ulocincpth= -Uloclibpth= -Dbin=/usr/perl5/5.24/bin -Dcc=/usr/gcc/4.9/bin/gcc -m64 -Dcf_email=oi-dev@openindiana.org -Dcf_by=perl-bugs -Dlibperl=libperl.so -Dmyhostname=localhost -Dprefix=/usr/perl5/5.24 -Dprivlib=/usr/perl5/5.24/lib -Dsitelib=/usr/perl5/site_perl/5.24 -Dsiteprefix=/usr/perl5/5.24 -Dvendorlib=/usr/perl5/vendor_perl/5.24 -Dvendorprefix=/usr/perl5/5.24 -Duse64bitall -Duseshrplib -Dusedtrace -Dusethreads -Dlibpth=/lib/64 /usr/lib/64'
#    cc='/usr/gcc/4.9/bin/gcc -m64', ccflags ='-D_REENTRANT -m64 -fwrapv -fno-strict-aliasing -pipe -fstack-protector-strong -D_LARGEFILE64_SOURCE -D_FORTIFY_SOURCE=2 -DPERL_USE_SAFE_PUTENV',
#    ccversion='', gccversion='4.9.4', gccosandvers=''
#    ld='/usr/gcc/4.9/bin/gcc -m64', ldflags =' -m64 -fstack-protector-strong '
#    libpth=/lib/64 /usr/lib/64 /usr/gcc/4.9/lib /usr/lib /usr/ccs/lib
#fix hipster used /usr/gcc/4.9/bin/gcc and we in SFE have different path
#solution 1) remove path compoment from cc and ld

PERL_CC=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | sed -e 's?cc=.??' -e 's?.;$??' )
if [ ! -x "${PERL_CC}" ]; then
  echo "ALARM es ist nicht vorhanden/ausfuehrbar  >>>${PERL_CC}<<<"
   #hipster '/usr/gcc/4.9/bin/gcc -m64'
   PERL_CC=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | sed -e 's?cc=.??' -e 's?.;$??' )
   #hipster  '/usr/gcc/4.9/bin/gcc -m64'
   PERL_LD=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:ld | sed -e 's?ld=.??' -e 's?.;$??' )
   #PERL_CC=$( /usr/bin/basename $PERL_CC )
   #PERL_LD=$( /usr/bin/basename $PERL_LD )
   #test: (echo "/usr/gnu/bin/gcc -m64" ; echo "gcc -m64" ; echo "gcc") | sed -e 's?.*/??'
   PERL_CC=$( echo "${PERL_CC}" | sed -e 's?.*/??' )
   PERL_LD=$( echo "${PERL_LD}" | sed -e 's?.*/??' )
   echo "PERL CC:  >>>${PERL_CC}<<<"
   echo "PERL LD:  >>>${PERL_LD}<<<"
fi

%if %{perl_bitness_64}
echo "perl_bitness is %{perl_bitness}"
%define gnu_lib_path %( echo -L%{gnu_lib} -R%{gnu_lib} | sed -e 's?/lib?/lib/%{_arch64}?g' )
#omnios  -  perl -V:lddlflags
#64-bit, missing /amd64:  lddlflags='-G -64 -shared -m64 -L/usr/gnu/lib ';
#solaris 11.3
#32-bit                :  lddlflags='-G -L/usr/lib -L/usr/ccs/lib  -L/lib -L/usr/gnu/lib';
LDDLFLAGS=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:lddlflags | sed -e 's?lddlflags=.??' -e 's?.;$??' )
#omnios  -  perl -V:cccdlflags
# cccdlflags='-fPIC';
CCCDLFLAGS=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cccdlflags | sed -e 's?cccdlflags=.??' -e 's?.;$??' )

#(echo "-L/usr/gnu/lib"; echo "-L/lib/64"; echo "-L/usr/lib/amd64"; echo "-L/usr/lib/sparcv9"); echo ; (echo "-L/usr/gnu/lib"; echo "-L/lib/64"; echo "-L/usr/lib/amd64"; echo "-L/usr/lib/sparcv9") | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g"
#echo " -G -m64 -L/lib/64" ; echo "-G -64 -shared -m64 -L/usr/gnu/lib " )| gegrep -- "-L/.*(/64|/%{_arch64})"

if echo ${LDDLFLAGS} | egrep -- "-L/.*(/64|/%{_arch64})" >/dev/null; then
LDDLFLAGS=$(  echo "${LDDLFLAGS}"  | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g" )
CCCDLFLAGS=$( echo "${CCCDLFLAGS}" | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g" )
echo "Modified LDDLFLAGS and CCCDLFLAGS to print libdir for 64-bit)"
echo "LDDLFLAGS:  >>>${LDDLFLAGS}<<<"
echo "CCCDLFLAGS: >>>${CCCDLFLAGS}<<<"
fi
%endif

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
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \



#note: %{gnu_lib_path} is modified above to match the %{_arch} corresponding to perl's bitness
%if %( perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null && echo 1 || echo 0 )
  make CCCDLFLAGS="${CCCDLFLAGS} -I%{gnu_inc} %{gnu_lib_path}" LDDLFLAGS="${LDDLFLAGS} %{gnu_lib_path}" CC="${PERL_CC}" LD="${PERL_LD}" 

%else
  # make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC
  make  CC=$CC CCCDLFLAGS="${CCCDLFLAGS} -I%{gnu_inc}" LDDLFLAGS="${LDDLFLAGS} %{gnu_lib_path}" LD=$CC
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
    --destdir $RPM_BUILD_ROOT \



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
* Thu Jan 10 2019 - Thomas Wagner
- bump 1.820 to 1.843
- keep name without "_" (packaging complains)
- for spamassassin -> sa-learn -> bayes db
- reworked from SFEperl-dbfile.spec
- removed OPTIMIZE="%optflags" argument o make, as it carries e.g. xarch=pentium and this disables -m64 (S11.4/S12)
* Tue Mar 02 2010 - matt@greenviolet.net
- Updated dependencies
* Mon, 28 Apr 2009  - Thomas Wagner
- initial spec
