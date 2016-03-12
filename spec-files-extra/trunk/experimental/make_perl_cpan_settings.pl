#!/usr/bin/perl
#


#potential for improvement: use the dependency solver from here: https://github.com/DrHyde/CPANdeps/pull/3
#it is used on this website where you can see modules and theirs build results
#http://deps.cpantesters.org/?module=Error;perl=latest


##visit license detection, should not write Artistic without checking files


#http://cpansearch.perl.org/src/NIERLEIN/Monitoring-Generator-TestConfig-0.42/META.yml
# ---
# abstract: 'generate monitoring configurations (nagios/icinga/shinken)'
# author:
#   - 'Sven Nierlein, <nierlein@cpan.org>'
# build_requires:
#   ExtUtils::MakeMaker: 6.42
#   Test::More: 0.87
# configure_requires:
#   ExtUtils::MakeMaker: 6.42
# distribution_type: module
# generated_by: 'Module::Install version 1.01'
# license: gpl3
# meta-spec:
#   url: http://module-build.sourceforge.net/META-spec-v1.4.html
#   version: 1.4
# name: Monitoring-Generator-TestConfig
# no_index:
#   directory:
#     - inc
#     - t
# requires:
#   File::Which: 0
#   perl: 5.005
# resources:
#   bugtracker: https://github.com/sni/Monitoring-Generator-TestConfig/issues
#   homepage: https://github.com/sni/Monitoring-Generator-TestConfig
#   license: http://opensource.org/licenses/gpl-3.0.html
#   repository: https://github.com/sni/Monitoring-Generator-TestConfig
# version: 0.42
# 

use strict;
use warnings;

use CPAN;

&help() unless($ARGV[0]);
use Data::Dumper;
sub p { print Dumper shift }

my $ModuleName = $ARGV[0];

sub help {
    print <<__HELP;
  make_cpan_settings <ModuleName>

Example:
  make_cpan_settings Unicode::Japanese

__HELP
    exit;
}


sub get_distriute_uri{
    my ($mod)=@_;
    my $uri='';
    foreach my $site(@{$CPAN::Config->{urllist}}) {
	$uri=$site . 'authors/id/'.$mod->{RO}->{CPAN_FILE};
	last;
    }
    return $uri;
}


#sub make_defines{
    #my ($mod) = @_;
    #my @filename=split(/\//,$mod->{RO}->{CPAN_FILE});
    #my $progs1=$filename[@filename-1];
    #my $progs1_dir=$progs1;
    #$progs1_dir=~s/\.tar\.[bg]z2?$//;
    #my $uri=get_distriute_uri($mod);
    #my $pkg=$mod->{ID};
    #$pkg=~ s/::/-/g;
    #my $result= <<__END;
#PROG1=$progs1
#PROG1_DIR=$progs1_dir
#PROG1_SITE=$uri
#TARGET=perl584-$pkg.pkg
#__END
    #return $result;
#}


# Main

my $mod = CPAN::Shell->expand('Module', $ModuleName);

unless($mod){
    print "\n'$ModuleName' is not found in CPAN module\n\n";
    print "Explain:\n";
    &help();
}

p $mod;
# p $CPAN::META;
my $pkg=$mod->{ID};
$pkg=~ s/::/-/g;
my $module_name=$pkg;
$pkg=~ tr/A-Z/a-z/;
my $pkgdir=$mod->{ID};
$pkgdir=~ s/::/\//g;
my $arch=`uname -p`;
chomp($arch);

my $vendor=$CPAN::META->instance("CPAN::Author", $mod->{RO}->{CPAN_USERID})->as_glimpse();
chomp($vendor);
$vendor=~s/^.*?\((.+?)\).*?$/$1/;
$vendor=~s/\"//g;

my $logname=`logname`;
chomp($logname);

my $userid=$mod->{RO}->{CPAN_USERID};
$userid=~ tr/A-Z/a-z/;

# ex) 1.01.1 -> 1.1.1
my $ips_version="";
foreach my $num (split(/\./,$mod->{RO}->{CPAN_VERSION})) {
    $ips_version.=int($num).".";
}
chop($ips_version);

# replace version number.
my $version=$mod->{RO}->{CPAN_VERSION};
my $cpan_file=$mod->{RO}->{CPAN_FILE};
$cpan_file=~s/$version/\%\{tarball_version\}/;

# get license file
my $license_url="http://search.cpan.org/src/".$mod->{RO}->{CPAN_USERID}."/".$module_name."-".$mod->{RO}->{CPAN_VERSION}."/LICENSE";
if (system("wget -O copyright/SFEperl-$pkg.copyright $license_url"))  { 
   print "copyright file could not be loaded, please check license information\n";
   open HANDLE, ">>copyright/SFEperl-$pkg.copyright" or print "failed to touch copyright/SFEperl-$pkg.copyright: $!\n";
   close HANDLE; 
   }

##TODO## check if the license is artitic perl license, if yes, default "SUNW_Copyright: %{license}.copyright" and "License: Artistic"

# work around for empty description (might depend on older CPAN module version!)
#Summary:	$mod->{RO}->{description}

#  DB<3> use CPAN;
#  DB<4> $mod = CPAN::Shell->expand('Module', "IO:Socket:SSL");
#Always commit changes to config variables to disk? [no]
#
#  DB<<5>> $mod = CPAN::Shell->expand('Module', "IO:Socket:SSL");
#CPAN: Storable loaded ok (v2.18)
#  DB<<6>> print $mod->id . "\n";
#IO::Socket::SSL
#  DB<<7>> print $mod->description . "\n";
#
#  DB<<8>> use Data::Dumper
#  DB<<9>> print Dumper $mod;
#$VAR1 = bless( {
#                 'ID' => 'IO::Socket::SSL',
#                 'RO' => {
#                           'CPAN_FILE' => 'S/SU/SULLR/IO-Socket-SSL-1.77.tar.gz',
#                           'CPAN_USERID' => 'SULLR',
#                           'CPAN_VERSION' => '1.77'
#                         }
#               }, 'CPAN::Module' );
#

#temporary solution is to just place the module name into spec files Summary and %description
$mod->{RO}->{description} = $mod->{ID} unless defined $mod->{RO}->{description};
 
if (-f "SFEperl-".$pkg.".spec") {
   print STDERR "Spec file already exists! SFEperl-$pkg.spec\n" ;
   exit 1;
   }

# out spec files
open (OUT,">SFEperl-$pkg.spec") or die ("cannot write SFEperl-$pkg.spec");

print OUT <<_END ;
#
# spec file for package: SFEperl-$pkg
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
\%include Solaris.inc
\%include packagenamemacros.inc

#consider switching off dependency_generator to speed up packaging step
#if there are no binary objects in the package which link to external binaries
#\%define _use_internal_dependency_generator 0

\%define tarball_version $mod->{RO}->{CPAN_VERSION}
\%define tarball_name    $module_name

Name:		SFEperl-$pkg
IPS_package_name: library/perl-5/$pkg
Version:	$mod->{RO}->{CPAN_VERSION}
IPS_component_version: $ips_version
Group:          Development/Libraries                    
Summary:	$mod->{ID} - $mod->{RO}->{description}
License:	Artistic
#Distribution:   OpenSolaris
#Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~$userid/\%{tarball_name}-\%{tarball_version}
SUNW_Basedir:	\%{_basedir}
SUNW_Copyright: \%{license}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/$cpan_file

BuildRequires:	\%{pnm_buildrequires_perl_default}
Requires:	\%{pnm_requires_perl_default}

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin\@justplayer.com>
Meta(info.upstream):            $vendor
Meta(info.upstream_url):        http://search.cpan.org/~$userid/\%{tarball_name}-\%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

\%description
$mod->{ID}
$mod->{RO}->{description}

\%prep
\%setup -q -n \%{tarball_name}-\%{tarball_version}

\%build

if test -f Makefile.PL
  then
  # style "Makefile.PL"
  \%{_prefix}/perl\%{perl_major_version}/\%{perl_version}/bin/perl Makefile.PL \\
    PREFIX=\$RPM_BUILD_ROOT\%{_prefix} \\
    LIB=\$RPM_BUILD_ROOT\%{_prefix}/\%{perl_path_vendor_perl_version} \\
    INSTALLSITELIB=\$RPM_BUILD_ROOT\%{_prefix}/\%{perl_path_vendor_perl_version} \\
    INSTALLSITEARCH=\$RPM_BUILD_ROOT\%{_prefix}/\%{perl_path_vendor_perl_version}/\%{perl_dir} \\
    INSTALLARCHLIB=\$RPM_BUILD_ROOT\%{_prefix}/\%{perl_path_vendor_perl_version}/\%{perl_dir} \\
    INSTALLSITEMAN1DIR=\$RPM_BUILD_ROOT\%{_mandir}/man1 \\
    INSTALLSITEMAN3DIR=\$RPM_BUILD_ROOT\%{_mandir}/man3 \\
    INSTALLMAN1DIR=\$RPM_BUILD_ROOT\%{_mandir}/man1 \\
    INSTALLMAN3DIR=\$RPM_BUILD_ROOT\%{_mandir}/man3


\%if \%( perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null \&\& echo 1 \|\| echo 0 )
  make
\%else
  make CC=\$CC CCCDLFLAGS="\%picflags" OPTIMIZE="\%optflags" LD=\$CC
\%endif

else
  # style "Build.PL"
  \%{_prefix}/perl\%{perl_major_version}/\%{perl_version}/bin/perl Build.PL \\
    --installdirs vendor --makefile_env_macros 1 \\
    --install_path lib=\%{_prefix}/\%{perl_path_vendor_perl_version} \\
    --install_path arch=\%{_prefix}/\%{perl_path_vendor_perl_version}/\%{perl_dir} \\
    --install_path bin=\%{_bindir} \\
    --install_path bindoc=\%{_mandir}/man1 \\
    --install_path libdoc=\%{_mandir}/man3 \\
    --destdir \$RPM_BUILD_ROOT

  \%{_prefix}/perl\%{perl_major_version}/\%{perl_version}/bin/perl Build build
fi

\%install
rm -rf \$RPM_BUILD_ROOT
if test -f Makefile.PL
   then
   # style "Makefile.PL"
   make install
else
   # style "Build.PL"
   \%{_prefix}/perl\%{perl_major_version}/\%{perl_version}/bin/perl Build install
fi

find \$RPM_BUILD_ROOT -name .packlist -exec \%{__rm} {} \\; -o -name perllocal.pod  -exec \%{__rm} {} \\;

\%clean
rm -rf \$RPM_BUILD_ROOT

\%files
\%defattr(-,root,bin)
\%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
\%{_prefix}/%{perl_path_vendor_perl_version}/*
\#\%dir \%attr(0755,root,bin) \%{_bindir}
\#\%{_bindir}/*
\%dir \%attr(0755,root,sys) \%{_datadir}
\%dir %attr(0755, root, bin) %{_mandir}
#\%dir %attr(0755, root, bin) %{_mandir}/man1
#\%{_mandir}/man1/*
\%{_mandir}/*/*
#\%dir %attr(0755, root, bin) %{_mandir}/man3
#\%{_mandir}/man3/*

\%changelog
##TODO## add changelog
_END

close(OUT);

print "1st, check SFEperl-$pkg.spec and copyright/SFEperl-$pkg.copyright.\n";
print "License parameter is always Artistic. You'll have to check it and change\n";
print "to the right copyright string and file in case this module uses other licensing.\n";
print "2nd,\n../bin/specbuild.sh SFEperl-$pkg.spec\n";
print "3nd,\nremove or add lines form the \%files section\n";


__DATA__
%changelog
* Sat Mar 12 2016 - Thomas Wagner
- fix build for packages with binaries on OmniOS amd64/perl and OIH i86pc/perl (both use gcc) (remove all broken options for studio on make command line) (OM OIH)
* Wed Mar  9 2016 - Thomas Wagner
- use default license as %{license}.copyright (matches most modules, still check each one until automated from meta.yml
* Mon Mar  7 2016 - Thomas Wagner
- try simpler %files entry for %{_mandir}/*/*
* Sun Jan 21 2016 - Thomas Wagner
- add module name to target package Summary and to package %description
- add build trough "Build.PL" and test for presence of "Makefile.PL". If absent, go for "Build.PL"
- use absolute path to perl executable when building
- see also script testbuildperlmodule which does a test-build, edits "man1", "man3" and "bin", then re-runs the build, adds $changelog and then adds spec to SVN
* Sun Dec  8 2013 - Thomas Wagner
- add INSTALLARCHLIB as it is sometimes empty on perl 5.10.x on OI, make complains on recoursive variable
* Sun Nov  4 2012 - Thomas Wagner
- add workaround to place module ID into description unless defined : Summary %description
* Wed Oct 24 2012 - Thomas Wagner
- add removal for .packlist and perllocal.pod
* Tue Aug 14 2012 - Thomas Wagner
  add  LIB=\$RPM_BUILD_ROOT\%{_prefix}/\%{perl_path_vendor_perl_version} \\
* Sat Aug 11 2012 - Thomas Wagner
- adapt to the current standards used for updates perl modules in sfe
* Wed Jul 20 2011 - Thomas Wagner
- use pnm_macros, prepare for perl versions other then 5.8.4
- adujst notes at the end
