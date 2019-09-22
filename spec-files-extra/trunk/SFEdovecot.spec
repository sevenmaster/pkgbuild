##TODO## Hinweis einbauen!
#dovecot auth - postfix wenn Versionen unterschiedlich sind, lieber setzen: version_ignore=yes in dovecot.conf
#Sonst der Effekt, dass ein neues smtp diesen Fehler zeigt, bei SSL Verbindung bricht es ab mit:
#250 8BITMIME
#read:errno=0
#(then connection closes)
#
#log:
#Oct  5 23:45:10 mailrouter postfix/smtpd[14020]: [ID 197553 mail.info] connect from unknown[46.182.137.63]
#Oct  5 23:45:10 mailrouter postfix/smtpd[14020]: [ID 197553 mail.info] Anonymous TLS connection established from unknown[46.182.137.63]: TLSv1.2 with cipher ECDHE-RSA-AES256-GCM-SHA384 (256/256 bits)
#Oct  5 23:45:10 mailrouter dovecot: [ID 583609 mail.crit] auth: Fatal: Dovecot version mismatch: Master is v2.3.1, auth is v2.3.3 (if you don't care, set version_ignore=yes)
#Oct  5 23:45:10 mailrouter dovecot: [ID 583609 mail.error] master: Error: service(auth): command startup failed, throttling for 8 secs
#Oct  5 23:45:10 mailrouter postfix/smtpd[14020]: [ID 947731 mail.crit] fatal: no SASL authentication mechanisms
#Oct  5 23:45:11 mailrouter postfix/master[657]: [ID 947731 mail.warning] warning: process /usr/lib/postfix/smtpd pid 14020 exit status 1
#Oct  5 23:45:11 mailrouter postfix/master[657]: [ID 947731 mail.warning] warning: /usr/lib/postfix/smtpd: bad command startup -- throttling




##TODO## check --with-ioloop=poll if apropriate for Solaris

##TODO## set better location (w/o /usr in it)
#root@mail:~# ls -l /usr/var/lib/dovecot
#total 3
##-rw-r--r--   1 root     other         62 Jan 18 21:30 instances
#-rw-r--r--   1 root     other        230 Jan 11 18:13 ssl-parameters.dat
#root@mailrouter:~# cat /usr/var/lib/dovecot/instances 
#1516307458      dovecot /var/run/dovecot        /etc/dovecot/dovecot.conf


#
# spec file for package SFEdovecot
#
# works: snv105 / pkgbuild 1.3.91 / Sun Ceres C 5.10 SunOS_i386 2008/10/22

# NOTE: READ THE WIKI page for SFEdovecot.spec : http://pkgbuild.wiki.sourceforge.net/SFEdovecot.spec


##TODO## move this to pnm_macros in include/packagenamemacros.inc
##Note: this will be automaticly overruled once it appears in packagenamemacros.inc and below
%define pnm_buildrequires_openldap_default SFEopenldap-gnu
%define pnm_requires_openldap_default SFEopenldap-gnu

#defaults to _off_ . use pkgtool --with-clucene to get 
#the nice server side search extension
#note: needs boost, libstemmer, libtextcat, switches to gcc/g++
%define with_clucene %{!?_with_clucene:0}%{?_with_clucene:1}

%define src_name dovecot

%define  daemonuser  dovecot
%define  daemonuid   111
%define  daemongcosfield dovecot Reserved UID
%define  daemongroup dovecot
#%define  daemongid   1
%define  daemongid  111
#starting with version 2.0.0  -  adds one more user
%define  daemonloginuser  dovenull
#inspired by http://slackbuilds.org/uid_gid.txt
##TODO## check if this id is a good choice in Solaris
%define  daemonloginuid   248
%define  daemonloginusergcosfield dovecot Reserved UID login user
##TODO## check if this should be nogroup or nobody group
#READ! if you change from nogroup (65534) then *ENABLE* group creation below, twice
%define  daemonlogingroup nogroup
%define  daemonlogingid   65534

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc


Name:		SFEdovecot
IPS_Package_Name:	service/network/imap/dovecot
Group:		System/Services
Summary:	A Maildir based pop3/imap email daemon
URL:		http://www.dovecot.org
Version:	2.3.7.2
%define downloadversion	  %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
License:	LGPLv2.1+ and MIT
SUNW_Copyright:	dovecot.copyright
Source:		http://dovecot.org/releases/%{downloadversion}/%{src_name}-%{version}.tar.gz
Source2:	dovecot.xml

Patch1:		dovecot-01-raise-soft-fd-limit.patch
#retired 2.2.29 Patch2:		dovecot-02-void-cannot-return-value-ldap-compare.c.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%if %{with_clucene}
BuildRequires:      SFEgcc
Requires:           SFEgccruntime
%endif
BuildRequires: %{pnm_buildrequires_openldap_default}
Requires:      %{pnm_requires_openldap_default}
BuildRequires: %{pnm_buildrequires_SUNWbzip}
BuildRequires: %{pnm_buildrequires_SUNWzlib}
Requires:      %{pnm_requires_SUNWzlib}
BuildRequires: %{pnm_buildrequires_SUNWbzip}
Requires:      %{pnm_requires_SUNWbzip}
BuildRequires: %{pnm_buildrequires_SUNWlexpt}
Requires:      %{pnm_requires_SUNWlexpt}
BuildRequires: %{pnm_buildrequires_SUNWgnu_idn}
Requires:      %{pnm_requires_SUNWgnu_idn}
BuildRequires: %{pnm_buildrequires_SUNWcurl}
Requires:      %{pnm_requires_SUNWcurl}
BuildRequires: %{pnm_buildrequires_SUNWopenssl_include}
Requires:      %{pnm_requires_SUNWopenssl_libraries}
BuildRequires: SFElibsodium
Requires:      SFElibsodium
%if %{with_clucene}
BuildRequires: SFElibstemmer-devel
Requires: SFElibstemmer
BuildRequires: SFElibtextcat-devel
Requires: SFElibtextcat
BuildRequires: SFEclucene-gpp-devel
Requires: SFEclucene-gpp
%endif

#with newer solr and dovecot-plugin there is no need for SFEclucene* and SFElibstemmer
#needs libexpat installed to enable the --with-solr plugin
BuildRequires: %{pnm_buildrequires_library_expat}
Requires:      %{pnm_requires_library_expat}
#later 
#BuildRequires: SFEsolr
#Requires:      SFEsolr

%include default-depend.inc

Requires: %name-root
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
Dovecot IMAP and POP3 Email Server. Also usable for SMTP_AUTH.
See the wiki page for SFEdovecot.spec for installation guidance:
  http://pkgbuild.wiki.sourceforge.net/SFEdovecot.spec

%prep
%setup -q -n %{src_name}-%{version}
cp -p %{SOURCE2} dovecot.xml

%patch1 -p1
#retired 2.2.29 %patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
export LD=gcc
%endif

export CFLAGS="-I/usr/include/openssl/fips-140 %optflags -I/usr/gnu/include -I/usr/include/kerberosv5 -D__EXTENSIONS__"
#find SFE openldap in /usr/gnu/include/ldap
export CXXFLAGS="%cxx_optflags-I/usr/gnu/include -I/usr/include/kerberosv5 "
#gnu_lib_path to find SFE openldap
export LDFLAGS="%_ldflags %{gnu_lib_path}"
#g++_lib_path to find our icu first and not the osdistro provided in /usr/lib. Needs gcc5-runtime on S12
export CFLAGS="-I/usr/g++/include $CFLAGS"
export CXXFLAGS="$CXXFLAGS -I/usr/g++/include"
export LDFLAGS="$LDFLAGS -L/usr/g++/lib -R/usr/g++/lib"

#needs bash (for parsing krb5-config call)
bash ./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --with-moduledir=%{_libexecdir}/%{src_name}/modules \
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
            --with-rundir=%{_localstatedir}/run/%{src_name} \
            --localstatedir=%{_localstatedir} \
            --with-ioloop=poll \
	    --with-ssl=openssl \
	    --with-gssapi=plugin  \
%if %{with_clucene}
	    --with-lucene \
            --with-stemmer \
%endif
            --with-solr \
	    --with-zlib \
	    --with-bzlib \
	    --with-ldap=plugin  \
	    --with-libwrap \
	    --disable-static \
	    --with-notify=none \
            --enable-hardening=no \

#--with-gssapi=plugin
 #--with-ldap=plugin
#--with-sql=plugin
#--with-pgsql
 #--with-zlib
 #--with-bzlib
#--with-libwrap
#--with-ssl=openssl

##TODO## try on omnios with 2.3.1 if the following is still necessary:
#error in detection of inotify, so we need to patch it off again
##define HAVE_INOTIFY_INIT 1
#possibly other OS Distro might as well get stuck here
%if %{omnios}
gsed -i.bak -e '/^#define HAVE_INOTIFY_INIT 1/ s?^?// we do not have this ?' config.h
%endif


gmake -j$CPUS

%install
%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
export LD=gcc
%endif
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -rf $RPM_BUILD_ROOT/usr/include

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp dovecot.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} \;

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


#IPS
##TODO## is is possible to predefine the numeric GID and UID?
%actions
%if %( expr '0' '+' 0'%{daemongid}' '>' 0 )
group groupname="%{daemongroup}" gid="%{daemongid}"
%else
group groupname="%{daemongroup}"
%endif
user ftpuser=false gcos-field="%{daemongcosfield}" username="%{daemonuser}" uid=%{daemonuid} password=NP group="%{daemongroup}"
#not needed _if_ group is nogroup  (65534)
# group groupname="%{daemonlogingroup}" gid="%{daemonlogingid}"
user ftpuser=false gcos-field="%{daemonloginusergcosfield}" username="%{daemonloginuser}" uid=%{daemonloginuid} password=NP group="%{daemonlogingroup}"


#SVR4 (e.g. Solaris 10, SXCE)
#must run immediately to create the needed userid and groupid to be assigned to the files
#NOTE: if given GID or UID is already engaged, the next free ID is chosen automaticly
%pre root
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo 'getent group %{daemongroup} || groupadd -g %{daemongid} %{daemongroup} ';
  echo 'getent passwd %{daemonuser} || useradd -d /tmp -g %{daemongroup} -c "%{daemongcosfield}" -s /bin/false  -u %{daemonuid} %{daemonuser}';
  echo '#not needed _if_ group is nogroup  (65534) because the group is altready there!'
  echo '# getent group %{daemonlogingroup} || groupadd -g %{daemonlogingid} %{daemonlogingroup} ';
  echo 'getent passwd %{daemonloginuser} || useradd -d /tmp -g %{daemonlogingroup} -c "%{daemonloginusergcosfield}" -s /bin/false  -u %{daemonloginuid} %{daemonloginuser}';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

#%postun root
#( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
#  echo 'getent passwd %{daemonuser} && userdel %{daemonuser}';
#  echo 'getent group %{daemongroup} && groupdel %{daemongroup}';
#  echo 'getent passwd %{daemonloginuser} && userdel %{daemonloginuser}';
#  echo 'getent group %{daemonlogingroup} && groupdel %{daemonlogingroup}';
#  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

%post
%restart_fmri dovecot
%restart_fmri postfix


#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr(-, root, bin)
%doc README ChangeLog COPYING INSTALL NEWS AUTHORS TODO 
%dir %attr (0755,root,bin) %{_bindir}
%ips_tag(restart_fmri="svc:/site/dovecot:*") %{_bindir}/*
%dir %attr (0755,root,bin) %{_sbindir}
%ips_tag(restart_fmri="svc:/site/dovecot:*") %{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%ips_tag(restart_fmri="svc:/site/dovecot:*") %{_libdir}/%{src_name}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_docdir}/%{src_name}/*
%{_datadir}/%{src_name}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*



%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{src_name}
%config %{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%ips_tag(restart_fmri="svc:/site/dovecot:*") %config %attr(0444, root, sys)/var/svc/manifest/site/dovecot.xml


%changelog
* Sun Sep 22 2019 - Thomas Wagner
- bump to 2.3.7.2 - https://dovecot.org/doc/NEWS-2.3 CVE-2019-11500: IMAP protocol parser does not properly handle NUL byte
  when scanning data in quoted strings, leading to out of bounds heap
  memory writes. Found by Nick Roessler and Rafi Rubin.
* Tue Jul 16 2019 - Thomas Wagner
- bump to 2.3.7 - https://dovecot.org/doc/NEWS-2.3
* Fri Jul  5 2019 - Thomas Wagner
- bump to 2.3.6 - https://dovecot.org/doc/NEWS-2.3
* Thu Apr 18 2019 - Thomas Wagner
- S11 complains about 
     FMRI-Muster entspricht eventuell implizit mehreren Serviceinstanzen.
     Aktuatoren für restart_fmri werden nicht für svc:/site/dovecot ausgeführt.
  set %ips_tag(restart_fmri="svc:/site/dovecot/*") - use :*
* Wed Apr 17 2019 - Thomas Wagner
- set %ips_tag(restart_fmri="svc:/site/dovecot") - to get binaries reloaded of they change on pkg update
- now send restart to postfix if dovecot gets reloaded - to get auth_pipe for SMTP_AUTH refreshed propperly,
  see dovecot.xml postfix_multi-user-server
* Sun Apr 14 2019 - Thomas Wagner
- bump to 2.3.5.1 - https://dovecot.org/list/dovecot-news/2019-March/000401.html
* Sun Dec  2 2018 - Thomas Wagner
- add missing package dependency on libsodium (would make auth process fail)
- bump to 2.3.4 - https://www.dovecot.org/list/dovecot-news/2018-November/000391.html
* Wed Oct  3 2018 - Thomas Wagner
- bump to 2.3.3 - https://dovecot.org/list/dovecot-news/2018-October/000389.html
* Tue Apr 17 2018 - Thomas Wagner
- bump to 2.3.1 for all OS!
- SFEpigeonhole 0.5.1 needs function call to array_idx_get_space -> 2.3.1 provides
- needs default group created (group=dovecot, create with next free group-ID or you set daemongid in this spec file)
- use gcc only for all OS
- set --localstatedir=%{_localstatedir} (or get wrong /usr/var/lib/dovecot)
- --with-ioloop=poll  (was: best)
- remove HAVE_INOTIFY_INIT - wrong detected on OmniOS (OM)
- tie gid to 111
* Fri Mar  2 2018 - Thomas Wagner
- bump to 2.2.34 for older Solaris 11.3 GA (S11)
* Tue Jan  2 2018 - Thomas Wagner
- bump to 2.3.0 (if new OSDISTRO with openssl EC), S11.3 GA w/o SRU gets version 2.2.33.2
- switch to gcc on OmniOS, --disble-hardening (or get -fstack-protector-strong lib call __stack_chk_fail_local not found)
* Wed Nov  8 2017 - Thomas Wagner
- fix compilation, false detection of HAVE_INOTIFY_INIT 1 on OmniOS (OM)
* Mon Oct 23 2017 - Thomas Wagner
- bump to 2.2.33.2
* Fri Jul 28 2017 - Thomas Wagner
- bump to 2.2.31
* Sun Jun  4 2017 - Thomas Wagner
- bump to 2.2.30.1
* Mon May 22 2017 - Thomas Wagner
- bump to 2.2.29
- retired patch2 dovecot-02-void-cannot-return-value-ldap-compare.c.diff
* Wed Jan  4 2017 - Thomas Wagner
- bump to 2.2.27
* Sat Dec 17 2016 - Thomas Wagner
- add temporary definition for an pnm_requires_openldap_default
- add (Build)Requires pnm_buildrequires_openldap_default
* Sun Dec 11 2016 - Thomas Wagner
- link to SFEicu-gpp in any case
* Thu Dec  1 2016 - Thomas Wagner
- add patch dovecot-01-raise-soft-fd-limit.patch
- add to CFLAGS / LDFLAGS to find SFEopenldap in /usr/gnu (OM)
- rework logic with_clucene and cc_is_gcc
* Sun Nov 13 2016 - Thomas Wagner
- bump to 2.2.26.0 (this is the second version of 2.2.26 see website)
* Thu Jan  7 2016 - Thomas Wagner
- bump to 2.2.21
* Wed Oct 14 2015 - Thomas Wagner
- bump to 2.2.19
* Tue Jun  2 2015 - Thomas Wagner
- bump to 2.2.18
* Sat Oct 25 2014 - Thomas Wagner
- fix preserve for config files s/%iclass(renamenew)/%config/g
- bump to 2.2.15
* Thu Aug  7 2014 - Thomas Wagner
- bump to 2.2.13
* Mon Apr 21 2014 - Thomas Wagner
- add %iclass renamenew
- bump to 2.2.12
* Fri Jan 10 2014 - Thomas Wagner
- bump to 2.2.10
* Sun Nov  3 2013 - Alex Viskovatoff <herzen@imapmail.org>
- fix packaging of documentation
* Thu Oct 24 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- bump to 2.2.6
* Mon Sep 9 2013 - Logan Bruns <logan@gedanken.org>
- updated to 2.2.5
* Fri Jun 21 2013 - Logan Bruns <logan@gedanken.org>
- updated to 2.2.3
* Sat Jun  8 2013 - Thomas Wagner
- bump to 2.2.2
- use bash configure
- use quotes with daemongcosfield
- add options zlib, bzlib, ldap, libwrap, gssapi=plugin
- remove *.la static files
* Wed Jun  5 2013 - Thomas Wagner
- fix typo in daemon* variable, remove quotes
* Sat Apr  6 2013 - Thomas Wagner
- make clucene optional (--with-clucene)
- bump to 2.1.16 (needs -D__EXTENSIONS__) 
* Mon Apr  1 2013 - Thomas Wagner
- make purpose of created userids more clear, mind re-installing SFEdovecot-root package if upgrading from 1.x.x
- remove %action group, no more then one package may deliver this (for group other/1)
* Mon Feb 25 2013 - Ken Mays <kmays2000@gmail.com>
- bump to 2.1.15
* Tue Feb 5 2013 - Logan Bruns <logan@gedanken.org>
- updated to 2.1.14
- enabled lucene full text search indexing plug-in
* Thu Dec  4 2012 - Thomas Wagner
- bump to 2.1.12 (auth. user can DoS)
* Sat Aug 25 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 2.1.9
* Thu May 31 2012 - Milan Jurik
- bump to 2.1.7
* Sat Apr  1 2012 - Thomas Wagner
- bump to 2.1.2
- add user dovenull with group nogroup (needed since 2.0.0 for login process)
- added notes to enable group creation if is it changed from nogroup (65534)
* Sat Mar 17 2012 - Thomas Wagner
- remove Requires: %name from the SFEdovecot-root package to get correct install order
* Fri Feb 24 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 2.1.1
* Mon Feb 6 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 2.0.17
* Thu Nov 24 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 2.0.16
* Tue Sep 27 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 2.0.15
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jul 03 2011 - Knut Anders Hatlen
- bump to 2.0.13
* Wed Mar 16 2011 - Thomas Wagner
- add dependencies (Build)Requires SUNWbzip SUNWlexpt SUNWgnu-idn SUNWcurl
* Tue Mar 15 2011 - Thomas Wagner
- bump to 2.0.11
- add missing predefined numeric gid="%{daemongid}" to %actions
- use packagenammacros.inc for (Build)Requires SUNWopenssl*
* Mon Feb 28 2011 - Thomas Wagner
- bump to 2.0.9
* Thr Feb 03 2011 - Thomas Wagner
- /var/run is under core system control, removed from spec and to be created at runtime
- add %action and %pre to create dovecot userid
- adjust --sysconfdir=%{_sysconfdir}, subdirectory dovecot by configure
- extra commit: set %action uid to predefine numeric userid. See man -a pkg
* Tue Dec 14 2010 - Thomas Wagner
- bump to 2.0.8 and svn copy to experimental
- fix %files (bindir, mandir, aclocal)
* Wed Nov 17 2010 - Knut Anders Hatlen
- bump to 1.2.16
* Tue Oct 12 2010 - Knut Anders Hatlen
- bump to 1.2.15
* Tue Aug 24 2010 - Milan Jurik
- bump to 1.2.13
* Mon Jun 29 2010 - Thomas Wagner
- bump to 1.2.12
* Wed May 19 2010 - Thomas Wagner
- migrate experimental/SFEdovecot.spec to regular spec directory (w/o svn history form experimental)
- add note and description pointing to dovecot wiki page
* Thu Feb 04 2010 - Albert Lee <trisk@opensolaris.org>
- Set CFLAGS
- Fix /var/run permissions
* Thu Jan 07 2010 - Thomas Wagner
- bump to 1.2.9
- adjust _libexexdir
* Fri Jan 01 2010 - Thomas Wagner
- bump to 1.1.20
- add --with-rundir=%{_localstatedir}/run/%{src_name}  since /usr/var/run/dovecot is wrong, add new location to %files
- add header files to the package by --enable-header-install, add to %files, don't rm header file location
- add full-text search --with-solr
* Sat Oct 03 2009  - Thomas Wagner
- bump to 1.1.19
* Sun Feb 07 2009  - Thomas Wagner
- bump to 1.1.11
* Wed Jan  7 2009 - Thomas Wagner
- remove %post, %preun, %postun
- adjust files in %doc, adjust wildcard for %{_docdir}/%{src_name}/*
- bump to 1.1.7
* Mon Oct 06 2008  - Thomas Wagner
- bump to 1.1.4
- add SMF FMRI / manifest for site/dovecot
* Thu May 22 2008  - Thomas Wagner
- Initial spec
