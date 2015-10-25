#
# spec file for package SFEdovecot
#
# works: snv105 / pkgbuild 1.3.91 / Sun Ceres C 5.10 SunOS_i386 2008/10/22

# NOTE: READ THE WIKI page for SFEdovecot.spec : http://pkgbuild.wiki.sourceforge.net/SFEdovecot.spec

#defaults to _off_ . use pkgtool --with-clucene to get 
#the nice server side search extension
#note: needs boost, libstemmer, libtextcat, switches to gcc/g++
%define with_clucene %{!?_with_clucene:0}%{?_with_clucene:1}

%define src_name dovecot
# maybe set to nullstring outside release-candidates (example: 1.1/rc  or just 1.1)
#%define downloadversion	 1.1/rc
%define downloadversion	 2.2

%define  daemonuser  dovecot
%define  daemonuid   111
%define  daemongcosfield dovecot Reserved UID
%define  daemongroup other
%define  daemongid   1
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
%include packagenamemacros.inc

%if %{with_clucene}
%define cc_is_gcc 1
%include base.inc
%endif

Name:		SFEdovecot
IPS_Package_Name:	service/network/imap/dovecot
Group:		System/Services
Summary:	A Maildir based pop3/imap email daemon
URL:		http://www.dovecot.org
#note: see downloadversion 22 above
Version:	2.2.19
License:	LGPLv2.1+ and MIT
SUNW_Copyright:	dovecot.copyright
Source:		http://dovecot.org/releases/%{downloadversion}/%{src_name}-%{version}.tar.gz
Source2:	dovecot.xml


SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%if %{with_clucene}
BuildRequires:      SFEgcc
Requires:           SFEgccruntime
%endif
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
%if %{with_clucene}
BuildRequires: SFElibstemmer-devel
Requires: SFElibstemmer
BuildRequires: SFElibtextcat-devel
Requires: SFElibtextcat
BuildRequires: SFEclucene-gpp-devel
Requires: SFEclucene-gpp
%endif

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
%setup -q -n %{src_name}-%version
cp -p %{SOURCE2} dovecot.xml


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %{with_clucene}
export CC=gcc
export CXX=g++
%endif
export CFLAGS="%optflags -D__EXTENSIONS__"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
%if %{with_clucene}
export CXXFLAGS="$CXXFLAGS -I/usr/g++/include"
export LDFLAGS="$LDFLAGS -L/usr/g++/lib -R/usr/g++/lib"
%endif

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
            --with-ioloop=best \
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
	    --disable-static		

#--with-gssapi=plugin
 #--with-ldap=plugin
#--with-sql=plugin
#--with-pgsql
 #--with-zlib
 #--with-bzlib
#--with-libwrap
#--with-ssl=openssl



gmake -j $CPUS

%install
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
#no more then one package may deliver this: group groupname="%{daemongroup}" gid="%{daemongid}"
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

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr(-, root, bin)
%doc README ChangeLog COPYING INSTALL NEWS AUTHORS TODO 
%dir %attr (0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/%{src_name}/*
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
%config %attr(0444, root, sys)/var/svc/manifest/site/dovecot.xml


%changelog
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
