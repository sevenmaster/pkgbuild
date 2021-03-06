

%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#root@ldap:~# grep -i munin /etc/passwd
#munin:x:835:835::/var/lib/munin:/bin/false
#root@ldap:~# grep -i munin /etc/group
#munin:x:835:
#root@ldap:~# 

%define  daemonuser  munin

#Subject to change!
%define  daemonuser  munin
%define  daemonuid   835
%define  daemongcosfield munin Reserved UID
%define  daemongroup munin
%define  daemongid   835

%define         dbdir   %{_localstatedir}/lib/munin

Name: SFEmunin
IPS_Package_Name: monitoring/munin
Version: 2.0.19
Source:         %{sf_download}/munin/stable/%{version}/munin-%{version}.tar.gz
Source2:        munin-node.xml
Source3:        munin.conf.example

##TODO## Source1:  smf manfest .xml
#recreate patch with diff -u Makefile.config.orig Makefile.config in BUILD dir
Patch1:		munin-01-Makefile.config.diff

#from OS (or SFE?)
#from SFE! the OS rrdtool misses the Perl modules we need
#SFErrdtool uses --prefix=/usr/gnu
BuildRequires: SFErrdtool
Requires: SFErrdtool

%include perl-depend.inc
BuildRequires: SFEperl-net-server
Requires: SFEperl-net-server
BuildRequires: SFEperl-net-cidr
Requires: SFEperl-net-cidr
BuildRequires: SFEperl-net-snmp
Requires: SFEperl-net-snmp
#delivers /usr/perl5/vendor_perl/5.12/Log/Log4perl/Appender/RRDs.pm
BuildRequires: SFEperl-log-log4perl
Requires: SFEperl-log-log4perl
#hm. some day included in more fresh perl version? maybe a pnm_macro
BuildRequires: SFEperl-module-build
Requires: SFEperl-module-build
BuildRequires: SFEperl-html-template
Requires: SFEperl-html-template
##TODO## maby only requiure the top-level module and let dependencies be installed by resolver 
BuildRequires: SFEperl-io-socket-inet6
Requires: SFEperl-io-socket-inet6
BuildRequires: SFEperl-socket6
Requires: SFEperl-socket6
BuildRequires: SFEperl-uri
Requires: SFEperl-uri
BuildRequires: SFEperl-file-copy-recursive
Requires: SFEperl-file-copy-recursive
BuildRequires: SFEperl-date-manip
Requires: SFEperl-date-manip
BuildRequires: SFEperl-digest-hmac
Requires: SFEperl-digest-hmac
BuildRequires: SFEperl-mail-sender
Requires: SFEperl-mail-sender
BuildRequires: SFEperl-mail-sendmail
Requires: SFEperl-mail-sendmail


##TODO##
#fuer quoted emailsn add this optional module
#SFEperl-mime-base64

##TODO## below, cover all OSDIST with its net-ssleay package (or: manage to get our own net-ssleay)
# this is a mediator on Solaris 11.2 ? there is as well package net-ssleay-584 and net-ssleay-512
%if %( expr %{solaris11} '+' %{solaris11express} '+' %{solaris12} '>=' 1 )
BuildRequires: library/perl-5/net-ssleay
%else
#older Solaris with perl 5.8.4
%if %SXCE
#not working, says "n_a" not found
%else
BuildRequires: SFEperl-net-ssleay
%endif
%endif
##TODO## Requires:
##TODO## Requires:
##TODO## Requires:
##TODO## Requires:
##TODO## Requires:


%description

%prep
%setup -q -n munin-%{version}
#- RRD with Perl support - this means that RRDs.pm must be available
#  and "perl -MRRDs -e ':;'" must run without errors.
perl -MRRDs -e ':;' || exit 1
cp Makefile.config Makefile.config.ORIG
%patch1 -p0 

gsed -i.bak_site_vendor_perl -e '/^PERLLIB/ s?/site_perl/?/vendor_perl/?' Makefile.config

perl -w -pi.bak -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," getversion

#copy example apache config
cp -p %{SOURCE3} .

%build

#let pod2man be found by $PATH
export PATH=/usr/perl%{perl_major_version}/bin:$PATH

#dirty hack
##TODO## file not found, maybe not generated propperly: Munin::Master::HTMLOld.pm3
#for now, just touch it or remove it from Makefile
make clean
mkdir -p  "master/blib/libdoc"
touch "master/blib/libdoc/Munin::Master::HTMLOld.3pm"

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC build \
    DESTDIR=${RPM_BUILD_ROOT} \
    PREFIX=%{_prefix} \
    CONFDIR=%{_sysconfdir}/munin \
    BINDIR=%{_prefix}/munin/bin \
    SBINDIR=%{_prefix}/munin/sbin \
    DOCDIR=%{_prefix}/munin/doc \
    MANDIR=%{_prefix}/munin/man \
    LIBDIR=%{_prefix}/munin/lib \
    HTMLDIR=%{_localstatedir}/munin/docs \
    CGIDIR=%{_localstatedir}/munin/cgi \
    LOGDIR=%{_localstatedir}/log/munin \
    STATEDIR=%{_localstatedir}/munin \
    DBDIR=%{dbdir} \
    build \



%install
rm -rf ${RPM_BUILD_ROOT}
#let pod2man be found by $PATH
export PATH=/usr/perl%{perl_major_version}/bin:$PATH

##TODO## re-visit and double check if the make install CHOWN=/bin/true already solves the chown issues on our build-environment
#install doesn't really implement $DESTDIR right ... wants to chown to nobody, munin and so on
#as well tries to chown root:root!
#should be done by %files section. Keep Makefile's chown in sync with %files!
gsed -i.bak1 -e '/CHOWN.*root.*PLUGSTATE/ s?^?##PAUSED## ?' Makefile

##TODO##
#somehow we don't have that file Munin::Master::HTMLOld.3pm in our build
gsed -i -e 's?./master/blib/libdoc/Munin::Master::HTMLOld.3pm??' Makefile

#gmake install DESTDIR=${RPM_BUILD_ROOT} USER=tom CGIUSER=tom PLUGINUSER=tom
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC build \
    DESTDIR=${RPM_BUILD_ROOT} \
    PREFIX=%{_prefix} \
    CONFDIR=${RPM_BUILD_ROOT}%{_sysconfdir}/munin \
    BINDIR=${RPM_BUILD_ROOT}%{_prefix}/munin/bin \
    SBINDIR=${RPM_BUILD_ROOT}%{_prefix}/munin/sbin \
    DOCDIR=${RPM_BUILD_ROOT}%{_prefix}/munin/doc \
    MANDIR=${RPM_BUILD_ROOT}%{_prefix}/munin/man \
    LIBDIR=${RPM_BUILD_ROOT}%{_prefix}/munin/lib \
    HTMLDIR=${RPM_BUILD_ROOT}%{_localstatedir}/munin/docs \
    CGIDIR=${RPM_BUILD_ROOT}%{_localstatedir}/munin/cgi \
    LOGDIR=${RPM_BUILD_ROOT}%{_localstatedir}/log/munin \
    STATEDIR=${RPM_BUILD_ROOT}%{_localstatedir}/munin \
    DBDIR=${RPM_BUILD_ROOT}%{dbdir} \
    CHECKUSER="echo Skipping user check" CHECKGROUP="echo Skipping group check" CHOWN=/bin/true CHGRP=/bin/true \
    install-node install-node-plugins \
    install-doc install-man \
    install-master \
    install \
    

    #clean install-node-prime install-node-plugins


mkdir -p ${RPM_BUILD_ROOT}%{dbdir}


install -d 0755 %{buildroot}%/var/svc/manifest/application
install -m 0644 %{SOURCE2} %{buildroot}%/var/svc/manifest/application


mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_major_version}/%{apache2_version}/samples-conf.d/
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/apache%{apache2_major_version}/%{apache2_version}/samples-conf.d/%{name}.conf

[ -d ${RPM_BUILD_ROOT}%{_localstatedir}/run ] && rm -r ${RPM_BUILD_ROOT}%{_localstatedir}/run


##Fix wrong paths in some files
# s{(BINDIR     \s+=\s).*}{\1q{/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/usr/munin/bin};}x;      \
#/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/usr/perl5/vendor_perl/5.12/Munin/Common/Defaults.pm:our $MUNIN_PREFIX     = q{/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/usr/munin};
#gsed -i.bak -e '/our.*MUNIN_/ s?/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build??' ${RPM_BUILD_ROOT}/usr/perl5/vendor_perl/5.12/Munin/Common/Defaults.pm
#gsed -i.bak -e '/our.*MUNIN_/ s?/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build??' ${RPM_BUILD_ROOT}%{_prefix}/%{perl_path_vendor_perl_version}/Munin/Common/Defaults.pm
gsed -i -e '/our.*MUNIN_/ s?/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build??' ${RPM_BUILD_ROOT}%{_prefix}/%{perl_path_vendor_perl_version}/Munin/Common/Defaults.pm

#tom/SFEmunin-2.0.19-build/ | grep -v "pm.bak"
#/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/usr/perl5/vendor_perl/5.12/Munin/Common/Defaults.pm:our $MUNIN_CONFDIR    = q{/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/etc/munin};
#/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/usr/munin/bin/munin-check:norec=yes owner_ok /var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/var/munin-node/plugin-state nobody
#/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/usr/munin/bin/munin-check:norec=yes perm_ok /var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build/var/munin-node/plugin-state 775
#gsed -i.bak -e '/norec.*_ok / s?/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build??' ${RPM_BUILD_ROOT}/usr/munin/bin/munin-check
gsed -i -e '/norec.*_ok / s?/var/tmp/pkgbuild-tom/SFEmunin-2.0.19-build??' ${RPM_BUILD_ROOT}/usr/munin/bin/munin-check

#remove the hostname of the compiling computer
#gsed -i.bak -e 's/'`uname -n`'/yourhostname_here/' /etc/munin/munin-node.conf
#gsed -i.bak_hostname -e 's/'`uname -n`'/yourhostname_here/'  ${RPM_BUILD_ROOT}/usr/perl5/vendor_perl/5.12/Munin/Common/Defaults.pm ${RPM_BUILD_ROOT}/etc/munin/munin.conf ${RPM_BUILD_ROOT}/etc/munin/munin-node.conf
#gsed -i.bak_hostname -e 's/'`uname -n`'/yourhostname_here/'  ${RPM_BUILD_ROOT}%{_prefix}/%{perl_path_vendor_perl_version}/Munin/Common/Defaults.pm ${RPM_BUILD_ROOT}/etc/munin/munin.conf ${RPM_BUILD_ROOT}/etc/munin/munin-node.conf
gsed -i -e 's/'`uname -n`'/yourhostname_here/'  ${RPM_BUILD_ROOT}%{_prefix}/%{perl_path_vendor_perl_version}/Munin/Common/Defaults.pm ${RPM_BUILD_ROOT}/etc/munin/munin.conf ${RPM_BUILD_ROOT}/etc/munin/munin-node.conf

#the SMF manifest
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/application/
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}/var/svc/manifest/application/



%clean
rm -rf %{buildroot}


#IPS
%actions
#no more then one package may deliver this: group groupname="%{daemongroup}" gid="%{daemongid}"
user ftpuser=false gcos-field="%{daemongcosfield}" username="%{daemonuser}" uid=%{daemonuid} password=NP group="%{daemongroup}"
group groupname="%{daemongroup}" gid="%{daemongid}"

##TODO## SVR4 create user


#SVR4 (e.g. Solaris 10, SXCE)
#must run immediately to create the needed userid and groupid to be assigned to the files
#NOTE: if given GID or UID is already engaged, the next free ID is chosen automaticly
%pre root
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo 'getent group %{daemongroup} || groupadd -g %{daemongid} %{daemongroup} ';
  echo 'getent passwd %{daemonuser} || useradd -d /tmp -g %{daemongroup} -c "%{daemongcosfield}" -s /bin/false  -u %{daemonuid} %{daemonuser}';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

#%postun root
#( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
#  echo 'getent passwd %{daemonuser} && userdel %{daemonuser}';
#  echo 'getent group %{daemongroup} && groupdel %{daemongroup}';
#  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew



%files
%defattr(-, root, sys)
%dir %attr(0750, root, munin) %{_sysconfdir}/munin
%class(renamenew) %{_sysconfdir}/munin/*

%dir %attr(0755, root, sys) %{_sysconfdir}
%dir %attr(0755, root, bin) %{_sysconfdir}/apache2
%dir %attr(0755, root, bin) %{_sysconfdir}/apache2/2.2
%dir %attr(0755, root, bin) %{_sysconfdir}/apache2/2.2/samples-conf.d
%class(renamenew) %{_sysconfdir}/apache2/2.2/samples-conf.d/%{name}.conf
%dir %attr(0755, munin, munin) %{_localstatedir}/munin
%dir %attr(0755, munin, munin) %{_localstatedir}/munin/docs
%{_localstatedir}/munin/docs/.htaccess
%dir %attr(0755, munin, munin) %{_localstatedir}/munin/cgi
%{_localstatedir}/munin/cgi/*
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0755, munin, munin) %{_localstatedir}/log/munin
#%{_localstatedir}/log/*
%dir %attr (0755, root, other) %{_localstatedir}/lib
%{_localstatedir}/lib/*
%dir %attr(0755, munin, munin) %{_localstatedir}/munin-node
%{_localstatedir}/munin-node/*

%dir %attr(0755, root, sys) %{_prefix}
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%{_prefix}/munin/*

%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/application/munin-node.xml

%changelog
* Fri Aug  8 2014 - Thomas Wagner
- change dependencies to SFErrdtool in /usr/gnu to get the perl modules
- fix %files %class
* Sun Jun  8 2014 - Thomas Wagner
- initial spec version 2.0.19
