#
# spec file for package SFEspamassassin
#
#

#TODO# re-work perl specific prerequisites...

%define src_name spamassassin
%define module_version 3.3.2
%define rules_version 3.3.2-r1104058
%define rules_version_IPS $( echo %{rules_version} | sed -e 's/-r/./' )
%define module_name Mail-Spamassassin
%define module_name_major Mail
%define module_package_name mail-spamassassin
#still unused: %define module_name_minor spamassassin

%include Solaris.inc
%include packagenamemacros.inc

%define perlmodulepkgnameprefix SFEperl
%define contact_address_spamreport postmaster@localhost

Name:                    SFEspamassassin
IPS_package_name:        service/network/smtp/spamassassin
Group:			 Applications/Internet
Summary:                 spamassassin - a spam filter for email which can be invoked from mail delivery agents
URL:                     http://spamassassin.apache.org/
Version:                 %{module_version}
Source:                  http://ftp.uni-erlangen.de/pub/mirrors/apache/spamassassin/source/Mail-SpamAssassin-%{version}.tar.bz2
#                        example: Mail-SpamAssassin-rules-3.3.2-r1104058.tar.gz
Source1:                 http://ftp.uni-erlangen.de/pub/mirrors/apache/spamassassin/source/Mail-SpamAssassin-rules-%{rules_version}.tar.gz
Source2:		 spamassassin.xml
#Patch1:			 spamassassin-sa-compile-env-cc.diff
Patch1:			 spamassassin-01-3.3.1-sa-compile-env-cc.diff
License: Apache License 2.0

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:		%{pnm_buildrequires_perl_default}
Requires:		%{pnm_requires_perl_default}
##TODO## check if necessary: BuildRequires:           %{pnm_buildrequires_SUNWsfwhea}


#Absolutely necessary perl modules
BuildRequires: SFEperl-digest-sha1
Requires: SFEperl-digest-sha1
BuildRequires: SFEperl-html-parser
Requires: SFEperl-html-parser
BuildRequires: SFEperl-net-dns
Requires: SFEperl-net-dns
#INSTALL file says this is required, build/check_dependencies does not complain..
BuildRequires: SFEperl-lwp
Requires: SFEperl-lwp

BuildRequires: SFEperl-encode-detect
Requires: SFEperl-encode-detect
BuildRequires: SFEperl-mail-spf
Requires: SFEperl-mail-spf

Requires: SFEperl-razor-agents
#http://www.opensourcehowto.org/how-to/postfix/fighting-spam-with-spamassassin-pyzor-dcc-razor--rules-du-jour.html#Rules Du Jour
#8. Next make a razor user
#useradd -d /bin/null -s /bin/bash razor
#9. now change into the razor user and
#su razor
#razor-admin -create
#exit
#10. Register your Razor install with the Razor servers. Replace the address with your admin’s e-mail address:
#razor-admin -register -user= admin@mydomain.comThis e-mail address is being protected from spam bots, you need JavaScript enabled to view it This email address is being protected from spam bots, you need Javascript enabled to view it
#11.  comming soon ... 


#TODO# make the spec file for that: Requires: SFEperl-pyzor

#optional perl modules for improvements/special features

BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

#obsolete pkgbuild: Requires: SFEperl-mail-spf-query
#pkgbuild: Requires: SFEperl-ip-country


#we *want* this one   (Note: this is the output of a pkgbuild run of *this* spec file, just in case you want to refresh the list below by copy&paste)
#pkgbuild: Requires: SFEperl-net-ident
#pkgbuild: Requires: SFEperl-io-socket-sl
#pkgbuild: Requires: SFEperl-mail-domainkeys
#pkgbuild: Requires: SFEperl-mail-dkim
#pkgbuild: Requires: SFEperl-lwp-useragent
#pkgbuild: Requires: SFEperl-htp-date
#pkgbuild: Requires: SFEperl-archive-tar
#pkgbuild: Requires: SFEperl-io-zlib

#we have in SFE a special naming mess for the perl modules. :)
Requires: SFEperl-io-compress
Requires: SFEperl-archive-tar
#Requires: SFEperl-io-zlib
#for sa-update we need more
Requires: SFEperl-package-constants
Requires: %{pnm_requires_SFEgnupg2}

BuildRequires: SFEperl-netaddr-ip
Requires: SFEperl-netaddr-ip

#INSTALL file says this is highly recommended:
#DB_File
#MIME::Base64
#Net::SMTP
#IP::Country::Fast
#Mail::DKIM
#Mail::DomainKeys
#Net::SMTP
#Time::HiRes
#Razor2 (If you do not plan to use this plugin, be sure to comment out its loadplugin line in /etc/spamassassin/v310.pre)

#from http://advosys.ca/papers/email/53-postfix-filtering.html
#install MIME::Base64
#install MIME::QuotedPrint
#install Net::DNS
#install DB_File


#from: http://www.opensourcehowto.org/how-to/postfix/fighting-spam-with-spamassassin-pyzor-dcc-razor--rules-du-jour.html#Rules Du Jour
# 5. Once it has installed change the local.cf configuration file
# nano /etc/mail/spamassassin/local.cf
# local.cf:
# dcc_path /usr/local/bin/dccproc
# dcc_body_max 999999
# dcc_timeout 10
# dcc_fuz1_max 999999
# dcc_fuz2_max 999999 

%include default-depend.inc

#from the original spamassassin.spec in the source tarball
%description
SpamAssassin provides you with a way to reduce, if not completely eliminate,
Unsolicited Bulk Email (or "spam") from your incoming email.  It can be
invoked by a MDA such as sendmail or postfix, or can be called from a procmail
script, .forward file, etc.  It uses a perceptron-optimized scoring system
to identify messages which look spammy, then adds headers to the message so
they can be filtered by the user's mail reading software.  This distribution
includes the spamc/spamc components which considerably speeds processing of
mail.

%prep
%setup -q -n Mail-SpamAssassin-%{version}

#we have gpg2 in requirements, but sa-update only knows the gpg binary
perl -w -pi.bak -e "s,GPGPath = \'gpg\' ,GPGPath = \'gpg2\' ," sa-update.raw

#use ENV{CC} since we not necessarily have "cc" in $PATH
#
%patch1 -p1

# below: not rock solid detection of missing perl modules because manually installed perl modules would not"
# result in complete (Build)Requires entries (package dependencies) in this spec file
# it uses the spamassassin provided check script in build/check_dependencies

REQUIREDPERLMODULES=`build/check_dependencies 2>/dev/null| grep -i "REQUIRED module missing: " | sed -e 's/^.*missing: //' -e 's/::/-/g' | tr '[:upper:]' '[:lower:]'`

if echo $REQUIREDPERLMODULES | grep -v "^$" 
  then
  echo "Required missing: $REQUIREDPERLMODULES"
  echo "ERROR: missing required Spamassassin Perl Module(s). Requirements of SFEspamassassin.spec seem to have changes and must be extended in SFEspamassassin.spec."
  echo "ERROR: required perl modules missing, you need to add them to BuildRequires: and Requires: in the spec file."
  echo "ERROR: eventually you need to write a new spec file to get the required perl module."
  echo "NOTE: you may use script make_perl_cpan_settings.pl in SFE spec-files-extra repository to create new packages for missing perl modules"
  for PERLMODULE in $REQUIREDPERLMODULES
   do
   echo "BuildRequires: %perlmodulepkgnameprefix-$PERLMODULE"
   echo "Requires: %{perlmodulepkgnameprefix}-$PERLMODULE"
   done #REQUIREDPERLMODULES
  exit 1
fi #$REQUIREDPERLMODULES

#below: only tell about the optional modules. e.g. Archive::Tar for having sa-update working
WANTEDPERLMODULES=`build/check_dependencies 2>/dev/null| grep -i " module missing: " | sed -e 's/^.*missing: //' -e 's/::/-/g' | tr '[:upper:]' '[:lower:]'`

if echo $WANTEDPERLMODULES | grep -v "^$" 
  then
  echo "suggested perl modules missing, consider adding them to BuildRequires: and Requires: in the spec file"
  echo "suggestion for this spec build recipe: add or write and add required perl modules with this syntax:"
  echo "NOTE: you may use script make_perl_cpan_settings.pl in SFE spec-files-extra repository to create new packages for missing perl modules"
  for PERLMODULE in $WANTEDPERLMODULES
   do
   echo "BuildRequires: %{perlmodulepkgnameprefix}-$PERLMODULE"
   echo "Requires: %{perlmodulepkgnameprefix}-$PERLMODULE"
   done #WANTEDPERLMODULES
fi #$WANTEDPERLMODULES


#smapassassin manifest
cp -p %{SOURCE2} spamassassin.xml

%build

#NOTE# special to this module: --no-online-tests

##DEVEL## perl Makefile.PL \
##DEVEL##	PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} DESTDIR=$RPM_BUILD_ROOT \
##DEVEL##	CONFDIR=%{_sysconfdir}/%{src_name} \
##DEVEL##        INSTALLSITELIB=%{_prefix}/%{perl_path_vendor_perl_version} \
##DEVEL##        INSTALLSITEARCH=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
##DEVEL##        INSTALLSITEMAN1DIR=%{_mandir}/man1 \
##DEVEL##        INSTALLSITEMAN3DIR=%{_mandir}/man3 \
##DEVEL##        INSTALLMAN1DIR=%{_mandir}/man1 \
##DEVEL##        INSTALLMAN3DIR=%{_mandir}/man3 \
##DEVEL##	ENABLE_SSL=yes \
##DEVEL##	CONTACT_ADDRESS=%{contact_address_spamreport} \
##DEVEL##	--no-online-tests
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    CONFDIR=%{_sysconfdir}/%{src_name} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    ENABLE_SSL=yes \
    CONTACT_ADDRESS=%{contact_address_spamreport} \
    --no-online-tests

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

#TODO# check if the make libspamc.so is needed
[ -f spamd/libspamc.so ] && cp -p spamd/libspamc.so spamd/libspamc.so.$$
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC \
      spamc/libspamc.so


%install
rm -rf $RPM_BUILD_ROOT
make install

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp spamassassin.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{src_name}

#remove perllocal.pod 
find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
#%doc README Changes sample-nonspam.txt sample-spam.txt INSTALL LICENSE TRADEMARK USAGE UPGRADE
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/%{src_name}
%{_datadir}/%{src_name}/*
#%dir %attr(0755, root, other) %{_docdir}
#%{_docdir}/%{src_name}/*
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%class(renamenew) %{_sysconfdir}/%{src_name}/*
%dir %attr (0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, sys) %{_localstatedir}
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/spamassassin.xml

%changelog
* Thu Oct  3 2013 - Thomas Wagner
- svn add missing patch spamassassin-01-3.3.1-sa-compile-env-cc.diff
* Fri Feb 01 2013 - Thomas Wagner
- change (Build)Requires to SFEperl-io-compress (now includes Zlib.pm from older SFEperl-compress-zlib)
- add (Build)Requires: SFEperl-netaddr-ip
* Mon Nov 26 2012 - Thomas Wagner
- bump to 3.3.2
- align perl Makefile.PL and other places to standard settings
- add IPS_package_name, add Group
- fix (Build)Requires for renamed package SFEperl-libwww-perl -> SFEperl-lwp.spec
* Thu May 17 2012 - Thomas Wagner
- change Requires to %{pnm_requires_SUNWgnupg}
* Sat May 12 2012 - Thomas Wagner
- Change (Build)Requires to %{pnm_buildrequires_perl_default}, %include packagenamemacros.inc
* Fri May 11 2012 - Thomas Wagner
- bump to 3.3.1
- rework patch1 spamassassin-01-3.3.1-sa-compile-env-cc.diff
- inserted Source1 to fetch the rules bundle
##TODO## split out rules bundle into a new package to enable updates of only the rules
* Sat Aug  7 2010 - Thomas Wagner
- remove BuildRequires: SUNWsfwhea
- add patch1 to let sa-compile read $ENV{CC} - in crontab use CC=/opt/SUNWspro/bin/cc sa-compile; svcadm restart svc:/site/spamassassin:default
* Sat Jul 11 2009 - Thomas Wagner
- add Requires: SFEperl-archive-tar, SFEperl-io-zlib, SFEgnupg2.spec to have sa-update working
- add patch to sa-update (use /usr/bin/gpg2 instead /usr/bin/gpg)
- add Requires: SFEperl-compres-zlib
- adjust paths in sa-update/sa-compile/sa-learn by complete refresh of the "make" parameters. The
  spamassassin.spec form the source tarball was of great help
- add Requires: SFEperl-razor-agents
* Sat Mai 02 2009 - Thomas Wagner
- add (Build)Requires: SFEperl-encode-detect and (Build)Requires: SFEperl-mail-spf
* Sun Apr 26 2009  - Thomas Wagner
- add %iclass(renamenew) for /etc/spamassassin/*
* Sun Apr 19 2009  - Thomas Wagner
- add manifest for SMF
* Sat Apr 18 2009  - Thomas Wagner
- Initial spec
