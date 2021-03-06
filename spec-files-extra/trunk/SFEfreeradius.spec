##TODO## rework patch3 or remove it once it comes with the source distro

##TODO## check dependencies with check-deps(.pl) script
##TODO## what is the right thing to do in %postun, remove user/group or not
##TODO## change startscript to read SF property for command-line-switches
#        or make a boolean flag for running radiusd -X and let svc-freeradius
#        svc script do the initialization once if usefull criteria is met

%include Solaris.inc
%include packagenamemacros.inc
%define  radiususer  freerad
%define  radiusuid   110
%define  radiusgroup freerad
%define  radiusgid   128

Name:                SFEfreeradius
Summary:             FreeRADIUS - modular, high performance and feature-rich RADIUS suite
IPS_Package_Name:    service/network/freeradius
Group:               System/Services
Version:             3.0.15
Source:              ftp://ftp.freeradius.org/pub/freeradius/freeradius-server-%{version}.tar.bz2
Source2:	     freeradius.xml
Source3:             svc-freeradius
#Patch1:              freeradius-01-types.diff
#Patch2:              freeradius-02-makefiles.diff
#should be obsolete some day
#obsolete with 3.x.x Patch3:              freeradius-03-libradius.h_sig_t.diff
URL:                 http://www.freeradius.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#  *** /usr/bin/radsniff (SFEfreeradius) requires /usr/lib/libpcap.so which
#      is found in SUNWlibpcap, but that is not listed as a package
#      dependency.
#      /usr/perl5/5.8.4/bin/perl5.8.4 which is found in SUNWperl584core, but
#      that is not listed as a package dependency.
#  *** /usr/sbin/radiusd (SFEfreeradius) requires /usr/lib/libltdl.so.3 which
#      is found in SUNWltdl, but that is not listed as a package dependency.
#  *** /usr/sbin/radmin (SFEfreeradius) requires /usr/lib/libreadline.so.5
#      which is found in SUNWgnu-readline,SFEreadline, but that is not listed
#      /usr/sfw/lib/libmysqlclient_r.so.12 which is found in SUNWmysqlu, but
#      that is not listed as a package dependency.
#      /usr/lib/libz.so.1 which is found in SUNWzlib, but that is not listed
#      as a package dependency.
#  *** /usr/lib/rlm_sql_mysql-2.1.10.so (SFEfreeradius) requires
#      /usr/lib/libm.so.2 which is found in SUNWlibms, but that is not listed
#      as a package dependency.
#  *** /usr/lib/rlm_python-2.1.10.so (SFEfreeradius) requires
#      /usr/lib/libpython2.4.so.1.0 which is found in SUNWPython, but that is
#      not listed as a package dependency.

BuildRequires: %{pnm_buildrequires_SUNWkrb}
BuildRequires: %{pnm_buildrequires_SUNWopenssl_include}
BuildRequires: %{pnm_buildrequires_SUNWgnu_dbm}
#BuildRequires: %{pnm_buildrequires_SUNWmysql_base_devel}
%define PERLpath /usr/perl%{perl_major_version}/bin/perl

BuildRequires: %{pnm_buildrequires_perl_default}
BuildRequires: %{pnm_buildrequires_SUNWltdl_devel}
BuildRequires: %{pnm_buildrequires_library_readline}
Requires: %{pnm_requires_SUNWkrb}
Requires: %{pnm_requires_SUNWopenssl_libraries}
Requires: %{pnm_requires_SUNWgnu_dbm}
#Requires: %{pnm_requires_SUNWmysql_base}
Requires: %{pnm_buildrequires_perl_default}
Requires: %{pnm_requires_SUNWltdl}
Requires: %{pnm_requires_library_readline}

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n freeradius-server-%version
cp %{SOURCE2} freeradius.xml
cp %{SOURCE3} svc-freeradius
#%patch1 -p1
#%patch2 -p1
#should be obsolete some day
#obsolete with 3.x.x %patch3 -p1

#or skip defining struct utmp in rlm_unix.c -> error
gsed -i.bak -e 's?(_sun)?(__sun)?' src/include/sysutmp.h src/include/libradius.h

#change all /bin/sh to /bin/bash since some scripts (certs/bootstrap) aren't 
#working with old /bin/sh - /etc/raddb/certs/"random" file doesn't get created, read
#http://freeradius.1045715.n5.nabble.com/Problem-running-radiusd-X-tp2787672p2787676.html
#error message tells errors while loading "eap" 
#run command below with "-pi.bak" if you want backup files be created, otherwise only "-pi"
#perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec egrep -q "^#\! */bin/sh" {} \; -print| egrep -v "/configure|/config.status|CONFIG_SHELL|>conf.*.sh"`

#rewrite shell interpreter
#*only* for configure step
##TODO## check other shell scripts in this pacakge on the shell interpreter used
perl -w -pi -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec egrep -q "^#\! */bin/sh" {} \; -print| egrep -v "/configure|/config.status|CONFIG_SHELL|>conf.*.sh"`

#rewrite perl interpreter
perl -w -pi -e "s,^#\!\s*/usr/bin/perl,#\!/usr/perl%{perl_major_version}/bin/perl," `find . -type f -exec grep -q "^#\!.*/usr/bin/perl" {} \; -print`

perl -w -pi -e "s,^#user = radius,user = %{radiususer},; s,^#group = radius,group = %{radiusgroup},;" raddb/radiusd.conf.in


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -I/usr/mysql/include/mysql `krb5-config --cflags` -I/usr/include/openldap -I/usr/sfw/include"
export CFLAGS="${CFLAGS} -Dlt__PROGRAM__LTX_preloaded_symbols=lt_libltdl_LTX_preloaded_symbols"
export LDFLAGS="%_ldflags -I/usr/mysql/include/mysql -L/usr/mysql/lib -R/usr/mysql/lib `krb5-config --libs` -L/usr/sfw/lib -R/usr/sfw/lib"
export PERL=%{PERLpath}

#put preferred mysql_config in front of the path (else sfw version would be detected)

export PATH=/usr/mysql/bin:$PATH
./configure --prefix=%{_prefix}               \
            --bindir=%{_bindir}               \
            --sbindir=%{_sbindir}             \
            --mandir=%{_mandir}               \
            --libdir=%{_libdir}               \
            --datadir=%{_datadir}             \
            --libexecdir=%{_libexecdir}       \
            --sysconfdir=%{_sysconfdir}       \
            --localstatedir=%{_localstatedir} \
            --with-openssl-includes=/usr/sfw/include \
            --with-openssl-libraries=/usr/sfw/lib \
            --with-ldap                       \
            --with-mysql                      \
            --with-system-libltdl             \
            --disable-static                  \

#            --enable-dynamic                  \

#fix wrong linking against /usr/sfw/lib/libmysql* for the rlm_sql_mysql module
#Modify freeradius-server-2.1.10/src/modules/rlm_sql/drivers/rlm_sql_mysql/Makefile
#to no longer contain /sfw/ in LDFLAGS (and CFLAGS). This doesn't break openssl for mysqlclient?
#copy the Make.inc to Make-without-sfw.inc and change the rlm_sql_mysql/Makefile
# to include the new include file
#cat Make.inc | sed -e 's#-\(R\|L\)/usr/sfw/lib##g' -e 's#-I/usr/sfw/include##g' > Make-without-sfw.inc
#sed -i 's#/Make.inc#/Make-without-sfw.inc#' src/modules/rlm_sql/drivers/rlm_sql_mysql/Makefile
cat Make.inc | sed -e '/^LDFLAGS/ s#-\(R\|L\)/usr/sfw/lib##g' > Make-without-sfw.inc
sed -i 's#/Make.inc#/Make-without-sfw.inc#' src/modules/rlm_sql/drivers/rlm_sql_mysql/Makefile

#doesn't succeed if built in parallel
gmake -j1

%install
rm -rf "$RPM_BUILD_ROOT"
#DESTDIR is overwritten in the Makefile by content of $R
R="$RPM_BUILD_ROOT" gmake install

#move libs/header files out of the way in case freeradius's libltdl has been built
[ -e $RPM_BUILD_ROOT%{_includedir}/ltdl.h ] && mv $RPM_BUILD_ROOT%{_includedir}/ltdl.h $RPM_BUILD_ROOT%{_includedir}/ltdl_freeradius.h

for file in `ls -1 $RPM_BUILD_ROOT%{_libdir}/libltdl.so*`
   do
   mv $file $file.freeradius
   done
#check that RPM_BUILD_ROOT is not empty (not save if it is "/")
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a"  -exec rm -f {} ';'

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site
cp freeradius.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p ${RPM_BUILD_ROOT}/lib/svc/method
cp svc-freeradius ${RPM_BUILD_ROOT}/lib/svc/method/

#remove directory, will be created at runtime by svc-freeradius script
[ -d ${RPM_BUILD_ROOT}/%{_localstatedir}/run/radiusd ] && rmdir ${RPM_BUILD_ROOT}/%{_localstatedir}/run/radiusd
[ -d ${RPM_BUILD_ROOT}/%{_localstatedir}/run         ] && rmdir ${RPM_BUILD_ROOT}/%{_localstatedir}/run

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

#IPS
%actions
group groupname="%{radiusgroup}" gid="%{radiusgid}"
user ftpuser=false gcos-field="freeradius" username="%{radiususer}" uid="%{radiusuid}" password=NP group="%{radiusgroup}"


#SVR4 (e.g. Solaris 10, SXCE)
#must run immediately to create the needed userid and groupid to be assigned to the files
#NOTE: if given GID or UID is already engaged, the next free ID is chosen automaticly
%pre root
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo 'getent group %{radiusgroup} || groupadd -g %{radiusgid} %{radiusgroup} ';
  echo 'getent passwd %{radiususer} || useradd -d /etc/raddb -g %{radiusgroup} -s /bin/false  -u %{radiusuid} %{radiususer}';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

#%postun root
#( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
#  echo 'getent passwd %{radiususer} && userdel %{radiususer}';
#  echo 'getent group %{radiusgroup} && groupdel %{radiusgroup}';
#  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/freeradius
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (1700, %{radiususer}, %{radiusgroup}) %dir %{_sysconfdir}/raddb
%attr (1700, %{radiususer}, %{radiusgroup}) %dir %{_sysconfdir}/raddb/certs
%attr (1700, %{radiususer}, %{radiusgroup}) %dir %{_sysconfdir}/raddb/sites-available
%attr (1700, %{radiususer}, %{radiusgroup}) %dir %{_sysconfdir}/raddb/sites-enabled
%attr (1700, %{radiususer}, %{radiusgroup}) %dir %{_sysconfdir}/raddb/modules
%attr (1700, %{radiususer}, %{radiusgroup}) %dir %{_sysconfdir}/raddb/sql
%defattr (0700, %{radiususer}, %{radiusgroup})
%dir %defattr (0700, %{radiususer}, %{radiusgroup})
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/acct_users*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/attrs*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/certs/*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/clients.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/dictionary
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/eap.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/example.pl
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/experimental.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/hints
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/huntgroups
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/ldap.attrmap
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/modules/*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/policy.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/policy.txt
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/preproxy_users
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/proxy.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/radiusd.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/sites-available/*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/sites-enabled/*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/sqlippool.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/sql.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/sql/*
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/templates.conf
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/users
%class(renamenew) %attr (0700, %{radiususer}, %{radiusgroup}) %{_sysconfdir}/raddb/panic.gdb
%dir %defattr (-, root, sys)
#removed %dir %attr (0755, root, sys) %{_localstatedir}/run
#removed %dir %attr (0755, %{radiususer}, %{radiusgroup}) %{_localstatedir}/run/radiusd
%dir %attr (0755, root, sys) %{_localstatedir}/log
%attr (0755, %{radiususer}, %{radiusgroup}) %{_localstatedir}/log/radius
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/svc-freeradius
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/freeradius.xml


%changelog
* Sun Nov  5 2017 - Thomas Wagner
- remove obsolete patch3 freeradius-03-libradius.h_sig_t.diff
* Mon Oct 30 2017 - Thomas Wagner
- bump to 3.0.15
* Mon Oct 30 2017 - Thomas Wagner
- bump to 2.2.10
* Wed May 31 2017 - Thomas Wagner
- bump to 2.2.9
* Tue Jun 17 2014 - Thomas Wagner
- add IPS_Package_Name and Group
* Mon Jun 16 2014 - Thomas Wagner
- bump to 2.2.5
- add patch3 sig_t
- add -I/usr/include/openldap (define LDAP_OPT_X_TLS_HARD not found)
- change define(_sun) to define(__sun) for sysutmp.h libradius.h (else possibly not detected right -> ut.ut_host undefined and more)
- help linker with  -Dlt__PROGRAM__LTX_preloaded_symbols=lt_libltdl_LTX_preloaded_symbols or get symbol not found in modules.o
- add new %files  %{_sysconfdir}/raddb/panic.gdb
* Wed Sep 18 2013 - Thomas Wagner
- bump to 2.2.1
* Sat Dec 15 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWltdl-devel}
  as renamed package SUNWltdl can't be detected as installed on IPS
- change (Build)Requires to %{pnm_buildrequires_library_readline}
* Tue Sep 11 2011 - Thomas Wagner
- bump to 2.2.0 - needs testing
* Mon Aug  1 2011 - Thomas Wagner
- bump to 2.1.10
- add (Build)Requires as pnm_macros: SUNWkrbu/SUNWkrb/SUNWopenssl_include/%{pnm_buildrequires_perl_default}
- rewrite perl interpreter to be /usr/perl%{perl_major_version}/bin/perl
* Tue Mar 17 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWgnu_dbm}
* Tue Mar 15 2011 - Thomas Wagner
- add missing predefined numeric gid="%{daemongid}" and uid="%{radiusuid} to %actions
- typo: s/raidusuid/radiusuid/
* Tue Jan 18 2011 - Thomas Wagner
- tweaked drivers/rlm_sql_mysql/Makefile and Make.inc to not catch the wrong
  mysql /usr/sfw/lib/libmysqlclient_r.so.12 from sfw
- remove *.a files from /usr/lib/
- enhance svc-freeradius startscript to create and chown /var/run/radiusd directory
  according to the "user =" value in the configuration file.
  Know the SMF config/debug property and set "-X" for fulldebug.
- freeradius.xml manifest: add SMF runtime config property for "-X" fulldebug 
  switch. Default is "false". Examples:
  svccfg -s freeradius setprop config/debug = boolean: true
  svcadm refresh freeradius
  svcprop freeradius | grep debug
  next service start will use new value (remember the refesh subcommand)
  ##TODO## needs improvement to know more fine grained debug settings
  ##TODO## improve "exec" string to explicitly set the configuration script set in SMF
- SMF manifest, change runuser for startscript to root, let radiusd step down the
  permissions to configured user in /etc/raddb/radiusd.conf
- pause %postun, don't remove user/group at uninstall of root package
- removed /var/run/radiusd - makes troubles at package upgrades (possible runtime owner mismatch)
* Sat Jan  1 2011 - Thomas Wagner
- bump to 2.1.10
- remove patch1 patch2
- adjusted Source URL
- try mysql-base as (Build)Requires via pnm_macros (TBD: which mysql version to default to depending on the osbuild)
- move ltdl.h aside, use system supplied SUNWltdl
- enhance %files for freeradius include files
- --with-system-libltdl  to avoid clush with system provided include file an library
- set PERL path to satisfy the ON Perl Style Guidelines.
- make config files in root package all %class(renamenew) to preserve important data
- add options --with-udpfromto --with-mysql --with-ldap (untested!)
* Tue Jun 01 2010 - Milan Jurik
- SFEgdbm replaced by SUNWgnu-dbm
* Sun 19 Aug 2007 - trisk@acm.jhu.edu
- Initial version
