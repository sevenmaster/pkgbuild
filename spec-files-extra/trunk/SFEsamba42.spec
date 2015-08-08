##TODO##
# sed /usr/local/... ....>>> /var/gnu/ oder so
# root@s12:/etc/gnu/samba# grep local *
# grep: private: Is a directory
# smb.conf:# connections to machines which are on your local network. The
# smb.conf:   log file = /usr/local/samba/var/log.%m
# smb.conf:;   include = /usr/local/samba/lib/smb.conf.%m
# smb.conf:;   path = /usr/local/samba/lib/netlogon
# smb.conf:;    path = /usr/local/samba/profiles
# smb.conf.default:# connections to machines which are on your local network. The
# smb.conf.default:   log file = /usr/local/samba/var/log.%m
# smb.conf.default:;   include = /usr/local/samba/lib/smb.conf.%m
# smb.conf.default:;   path = /usr/local/samba/lib/netlogon
# smb.conf.default:;    path = /usr/local/samba/profiles
# root@s12:/etc/gnu/samba# pkg contents -r -m samba42 > /tmp/samba42contents
# grep smb.conf root@s12:/etc/gnu/samba# grep smb.conf /tmp/samba42contents
# file 345752fa9f6eb1bcefd4ca636da703db4c2b7f80 chash=4640204ce2ff10eb540782a056d7a7f1e840f556 group=bin mode=0644 owner=root path=etc/gnu/samba/smb.conf.default pkg.csize=3138 pkg.size=7932
# 

# --with-modulesdir=$PREFIX/lib/samba
#--with-statedir=/var/samba/lib
#--with-piddir=/var/samba/run
#/var/gnu/samba/locks (alter 3er
#--with-cachedir=/var/samba/cache
#--with-sockets-dir=/var/samba/run
#--with-privileged-socket-dir=/var/samba/lib

#
# spec file for package SFEsamba
#

%include Solaris.inc
%define cc_is_gcc 1
#rely on $PATH to find the right g++
%define _gpp g++
%include base.inc

#avoid clush with /usr/bin/profiles of SUNWcsu Solaris package
%include usr-gnu.inc

%include packagenamemacros.inc

%define src_name samba
%define major_version 4

Name:                    SFEsamba42
IPS_package_name:	 sfe/service/network/samba42
Summary:                 samba - CIFS Server, AD and Domain Controller
URL:                     http://samba.org/
Version:                 4.2.3
Copyright:               GPLv3
SUNW_Copyright:          GPLv3.copyright
##TODO## License: 
Url:                     http://www.samba.org
Source:                  http://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.gz
Source5:		addmachinescript-samba3
Source6:		domain-samba3.reg
Source7:                samba42gnu.xml
#Patch1:                 samba-01-oi-2172.diff
#Patch2:                  samba-02-eliminate-selftest-bcs-buildroot-not-recognized.diff
#Patch3:                  samba-03-Makefile-add-DESTDIR_RPM_BUILD_ROOT.diff
#Patch4:                  samba-04-ext-sources-manifest-gnu-names.diff
##TODO## check if this patch should go in again:
#Patch5:                  samba-05-smb.conf.default-add-machine-script-useradd.diff
#Patch6:                 samba-06-remove-attr_get-configure.in.diff
#Patch6:                 samba4-06-remove-attr_get-configure.diff
#Patch7:                 samba4-06b-remove-attr_get-configure.diff
#replaced with sed in %prep
#Patch8:                 samba4-08-fix-multiline-waf-rule.diff



SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

##TODO## better
#BuildRequires: SUNWgcc
#Requires:      SUNWgccruntime
BuildRequires: %{pnm_buildrequires_SUNWbash}
Requires:      %{pnm_requires_SUNWbash}
BuildRequires: SFEopenldap-gnu
Requires:      SFEopenldap-gnu

#to build certificates for an AD Domain:
Requires:       SFEgnutls

%include default-depend.inc


%package doc
Summary:                 %{summary} - documentation and manpages
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name



%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%description
Samba SMB/CIFS server with network file and print services
to SMB/CIFS clients


%prep
#can't be build while /usr/gnu/include/tdb.h is present from older samba version
test -f /usr/gnu/include/tdb.h && exit 1

%setup -q -n samba-%version
#%patch1 -p1
#%patch2 -p1

%if %{SXCE}
perl -w -pi.bak -e "s,^SHELL=/bin/sh,SHELL=/usr/bin/bash," source*/Makefile.in source*/Makefile
perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure `find source* -type f -exec grep -q "^#\!.*/bin/sh" {} \; -print`
%endif

#extra scripts, registry input files
cp -p %{SOURCE5} addmachinescript
cp -p %{SOURCE6} domain.reg
#samba manifest
cp -p %{SOURCE7} .
#%patch4 -p0

#solaris useradd smb.conf.default
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#replaced with sed
#%patch8 -p1
gsed -i.bak -e '/XSLTPROC.*xinclude.*stringparam.*noreference.*nonet.*SAMBA_EXPAND_XSL.*SRC/ s?$?;?' buildtools/wafsamba/wafsamba.py

##TODO##
#@INC in Perl Script so aendern, dass /usr/gnu/perl5 includiert wird

#script/autobuild.py:               ("configure", "perl Makefile.PL PREFIX=${PREFIX_DIR}", "text/plain"),
#script/autobuild.py:               ("configure", "perl Makefile.PL PREFIX=${PREFIX_DIR} ", "text/plain"),

#perl -pe 's?PREFIX.*\",?huuuu"? if /configure.*perl Makefile.PL PREFIX=/' < script/autobuild.py | grep Makefile.PL
##TODO## check ob das wirklich wirkt... offenbar nicht.
##PAUSE## perl -i.bakperlpath -pe 's?PREFIX.*\",?LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}"? if /configure.*perl Makefile.PL PREFIX=/' script/autobuild.py 

#./bin/default/docs-xml/smbdotconf/parameters.all.xml
#<!ENTITY pathconfig.PERL_LIB_INSTALL_DIR   '/usr/gnu/share/perl5'>
##PAUSE## perl -i.bakperlpath -pe 's?/usr/gnu/share/perl5?%{_prefix}/%{perl_path_vendor_perl_version}? if /ENTITY pathconfig.PERL_LIB_INSTALL_DIR/' bin/default/docs-xml/smbdotconf/parameters.all.xml

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CPP=cpp

%if %{omnios}
#export CPP=/usr/gnu/bin/cpp
#export CPP=$( dirname `which $CC` )/cpp
export CPP=/usr/gcc/bin/cpp
%endif

##TODO## which ranlib, which ar? defaults to /usr/gnu/bin/ranlib /usr/gnu/bin/ar
#are they used?
#RANLIB=/usr/bin/ranlib
#AR=/usr/bin/ar




#compile time might have much never samba libs then the installed one on the disk
LIBSCOMPILETIME=`pwd`/nsswitch:`pwd`/source%{major_version}/bin
export LD_LIBRARY_PATH=$LIBSCOMPILETIME

#export CFLAGS="%optflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib -lncurses -ltermcap"
#export CXXFLAGS="%cxx_optflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib"
#export LDFLAGS="%_ldflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib"
#export LDFLAGS="$LDFLAGS -lncurses -ltermcap"
##TEST-AUS## export CFLAGS="%optflags -L$LIBSCOMPILETIME"
##TEST-AUS## export CXXFLAGS="%cxx_optflags -L$LIBSCOMPILETIME"
##TEST-AUS## export LDFLAGS="%_ldflags -L$LIBSCOMPILETIME -L/usr/gnu/lib -R/usr/gnu/lib"
##TEST-AUS## export LDFLAGS="$LDFLAGS -lncurses -ltermcap"

##NEU##
##TODO## find openldap on other way then including the whole /usr/gnu/include (old samba install might deliver tdb.h, fails the build eventually)
export CFLAGS="%optflags -I/usr/gnu/include"
export CXXFLAGS="%cxx_optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="$LDFLAGS"

#xsltproc fails 
export XSLTPROC=/usr/gnu/bin/xsltproc

#find libgnutls in /usr/gnu
#export PKG_CONFIG_PATH=%{_prefix}/gnu/lib/pkgconfig:%{_prefix}/lib/pkgconfig

#python_version_package_string e.g. "26" or "27" for Python 2.6 or 2.7
#CFLAGS="$CFLAGS -I/usr/lib/python%{python_version_package_string}/include"


##REMOVETHIS## cd source3
##REMOVETHIS## ./autogen.sh
#+CONFIGURE_OPTIONS +=   --with-shared-modules=vfs_zfsacl,vfs_prealloc,vfs_cacheprime,vfs_commit,idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex
#+CONFIGURE_OPTIONS +=   --with-readline
#+CONFIGURE_OPTIONS +=   --with-aio-support
#+CONFIGURE_OPTIONS +=   --with-acl-support
#+CONFIGURE_OPTIONS +=   --with-ads
#+CONFIGURE_OPTIONS +=   --with-krb5
#+CONFIGURE_OPTIONS +=   --with-ldap
#+CONFIGURE_OPTIONS +=   --with-automount
#+CONFIGURE_OPTIONS +=   --with-dnsupdate
#+CONFIGURE_OPTIONS +=   --with-pam
#+CONFIGURE_OPTIONS +=   --with-winbind
#
#+CONFIGURE_OPTIONS +=   CPP=/usr/sfw/bin/cpp
#+CONFIGURE_OPTIONS +=   CPPFLAGS="$(CPPFLAGS)"
#+CONFIGURE_OPTIONS +=   CFLAGS="$(CFLAGS)"
#+CONFIGURE_OPTIONS +=   CUPS_CONFIG=/usr/bin/cups-config
#+CONFIGURE_OPTIONS +=   INSTALLCMD=/usr/bin/ginstall
#+CONFIGURE_OPTIONS +=   LIBREPLACE_NETWORK_LIBS=" -lsocket -lnsl"

#Dynconfig[SCRIPTSBINDIR]:                                                         : '/usr/gnu/sbin'
#Dynconfig[SETUPDIR]:                                                              : '/usr/gnu/share/samba/setup'
#Dynconfig[PYTHONDIR]:                                                             : '/usr/gnu/lib/python2.4/site-packages'
#Dynconfig[CACHEDIR]:                                                              : '/var/gnu/samba/cache/samba'
#Dynconfig[LOGFILEBASE]:                                                           : '/var/gnu/samba/log/samba'
#Dynconfig[CONFIGFILE]:                                                            : '/etc/gnu/samba/smb.conf'
#Dynconfig[WINBINDD_PRIVILEGED_SOCKET_DIR]:                                        : '/var/gnu/samba/lib/samba/winbindd_privileged'
#Dynconfig[LIBDIR]:                                                                : '/usr/gnu/lib/samba'
#Dynconfig[PKGCONFIGDIR]:                                                          : '/usr/gnu/lib/samba/pkgconfig'
#Dynconfig[NMBDSOCKETDIR]:                                                         : '/var/gnu/samba/run/samba/nmbd'
#Dynconfig[INCLUDEDIR]:                                                            : '/usr/gnu/include/samba-4.0'
#Dynconfig[LOCKDIR]:                                                               : '/var/gnu/samba/lock/samba'
#Dynconfig[PRIVILEGED_SOCKET_DIR]:                                                 : '/var/gnu/samba/lib/samba'
#Dynconfig[LIBEXECDIR]:                                                            : '/usr/gnu/lib/samba'
#Dynconfig[SMB_PASSWD_FILE]:                                                       : '/etc/gnu/samba/private/smbpasswd'
#Dynconfig[BINDIR]:                                                                : '/usr/gnu/bin'
#Dynconfig[STATEDIR]:                                                              : '/var/gnu/samba/lib/samba'
#Dynconfig[PAMMODULESDIR]:                                                         : '/usr/gnu/lib/samba/security'
#Dynconfig[WINBINDD_SOCKET_DIR]:                                                   : '/var/gnu/samba/run/samba/winbindd'
#Dynconfig[PRIVATE_DIR]:                                                           : '/etc/gnu/samba/private'
#Dynconfig[DATADIR]:                                                               : '/usr/gnu/share'
#Dynconfig[SBINDIR]:                                                               : '/usr/gnu/sbin'
#Dynconfig[NCALRPCDIR]:                                                            : '/var/gnu/samba/run/samba/ncalrpc'
#Dynconfig[LMHOSTSFILE]:                                                           : '/etc/gnu/samba/lmhosts'
#Dynconfig[SWATDIR]:                                                               : '/usr/gnu/share/samba/swat'
#Dynconfig[PYTHONARCHDIR]:                                                         : '/usr/gnu/lib/python2.4/site-packages'
#Dynconfig[PIDDIR]:                                                                : '/var/gnu/samba/run/samba'
#Dynconfig[NTP_SIGND_SOCKET_DIR]:                                                  : '/var/gnu/samba/lib/samba/ntp_signd'
#Dynconfig[SOCKET_DIR]:                                                            : '/var/gnu/samba/run/samba'
#Dynconfig[MODULESDIR]:                                                            : '/usr/gnu/lib/samba/samba'
#Dynconfig[LOCALEDIR]:                                                             : '/usr/gnu/share/locale'
#Dynconfig[CODEPAGEDIR]:                                                           : '/usr/gnu/share/samba/codepages'
#Dynconfig[CONFIGDIR]:                                                             : '/etc/gnu/samba'
#Dynconfig[PRIVATELIBDIR]:                                                         : '/usr/gnu/lib/samba/samba'

export XSLTPROC_MANPAGES=True

#CC=/usr/gnu/bin/gcc CXX=/usr/gnu/bin/g++ CPP=/usr/gnu/bin/cpp \
PERL_ARCH_INSTALL_DIR=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
PERL_LIB_INSTALL_DIR=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
PKG_CONFIG_PATH=%{_prefix}/gnu/lib/pkgconfig:%{_prefix}/lib/pkgconfig \
CC=gcc CXX=g++ CPP=cpp \
       python buildtools/bin/waf -v configure \
            --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --bindir=%{_bindir}         \
            --sbindir=%{_sbindir}         \
            --libdir=%{_libdir}/samba         \
            --libexecdir=%{_libexecdir}/samba \
            --sysconfdir=%{_sysconfdir}/samba \
	    --with-configdir=%{_sysconfdir}/samba \
	    --with-privatedir=%{_sysconfdir}/samba/private \
	    --sharedstatedir=%{_localstatedir}/samba \
	    --localstatedir=%{_localstatedir}/samba \
            --with-logfilebase=%{_localstatedir}/samba/log \
	    --datadir=%{_datadir} \
            --enable-fhs \
--with-aio-support \
--with-ads \
--with-ldap \
--with-automount \
--with-dnsupdate \
--with-pam \
--with-acl-support   \
--without-systemd    \
--with-shared-modules=nfs4_acls,vfs_zfsacl,idmap_ad,idmap_ldap,idmap_rid,idmap_tdb2 \

#unknown --enable-socket-wrapper \
#unknown --enable-nss-wrapper \


#--without-acl-support \
##CHECKTHIS##            --with-shared-modules=vfs_zfsacl,vfs_prealloc,vfs_cacheprime,vfs_commit,idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex \
##CHECKTHIS##--with-acl-support \

##REMOVETHIS##              CFLAGS="$CFLAGS"        \
##REMOVETHIS##              CXXFLAGS="$CXXFLAGS"    \
##REMOVETHIS##              LDFLAGS="$LDFLAGS"      \
##REMOVETHIS##              CC="$CC"                \
##REMOVETHIS##              CXX="$CXX"              

##CHECKTHIS##von kmays' 4	    --enable-socket-wrapper \
##CHECKTHIS##von kmays' 4	    --enable-nss-wrapper
##REMOVETHIS##	    --with-swatdir=%{_datadir}/samba/swat \
##REMOVETHIS##   --with-krb5 \
            #PROBE RAUS TERMLIBS=-ltermcap \  dann immer noch correct ein ncurses oder curses eingelinkt? ldd -u -r smbclient

#https://www.illumos.org/attachments/276/fix-samba-termcap.patch
#            TERMLIBS=-ltermcap \
#do not specify this, it would disturb detecting the ncurses location --with-readline \
#            --with-shared-modules=vfs_zfsacl,vfs_prealloc,vfs_cacheprime,vfs_commit,idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex \
#--with-readline \
#--with-aio-support \
#--with-acl-support \
#--with-ads \
#--with-krb5 \
#--with-ldap \
#--with-automount \
#--with-dnsupdate \
#--with-pam \
#  # --datarootdir=DIR      read-only arch.-independent data root [PREFIX/share]
  #--localedir=DIR        locale-dependent data [DATAROOTDIR/locale]

#%patch3 -p2

#perl -pe 's?PREFIX.*\",?huuuu"? if /configure.*perl Makefile.PL PREFIX=/' < script/autobuild.py | grep Makefile.PL
##TODO## check ob das wirklich wirkt... offenbar nicht.
##PAUSE## perl -i.bakperlpath -pe 's?PREFIX.*\",?LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}"? if /configure.*perl Makefile.PL PREFIX=/' script/autobuild.py 

#./bin/default/docs-xml/smbdotconf/parameters.all.xml
#<!ENTITY pathconfig.PERL_LIB_INSTALL_DIR   '/usr/gnu/share/perl5'>
##PAUSE## perl -i.bakperlpath -pe 's?/usr/gnu/share/perl5?%{_prefix}/%{perl_path_vendor_perl_version}? if /ENTITY pathconfig.PERL_LIB_INSTALL_DIR/' bin/default/docs-xml/smbdotconf/parameters.all.xml

#./bin/config.log:'/usr/gnu/share/perl5'
#./bin/c4che/default.cache.py:PERL_LIB_INSTALL_DIR = '/usr/gnu/share/perl5'
# PERL_ARCH_INSTALL_DIR:                                                            : '${LIBDIR}/perl5' 
# PERL_LIB_INSTALL_DIR:                                                             : '${DATADIR}/perl5' 



##TEST AUS##CC=/usr/gnu/bin/gcc CXX=/usr/gnu/bin/g++ CPP=/usr/gnu/bin/cpp python buildtools/bin/waf -v build -j$CPUS
python buildtools/bin/waf -v build -j$CPUS
#gmake -j1

%install
rm -rf $RPM_BUILD_ROOT
##REMOVETHIS## cd source3
#SHELL=/usr/bin/bash gmake install DESTDIR=$RPM_BUILD_ROOT
python buildtools/bin/waf -v install --destdir=$RPM_BUILD_ROOT

  	
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/samba/private
##REMOVETHIS##cp -p ../examples/smb.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/samba/
cp -p examples/smb.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/samba/

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
#cp samba4gnu-samba.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp samba42gnu.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/
cp -p addmachinescript ${RPM_BUILD_ROOT}%{_bindir}/
chmod a+rx  ${RPM_BUILD_ROOT}%{_bindir}/addmachinescript
[ -d ${RPM_BUILD_ROOT}%{_docdir}/%{name}/ ] || mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}/
cp -p domain.reg ${RPM_BUILD_ROOT}%{_datadir}/%{src_name}/setup/

#/data/netlogon/
#/localhomes/tom/packages/BUILD/samba-3.5.20/docs-xml/registry/Win7_Samba3DomainMember.reg

for OLDNAME in `find ${RPM_BUILD_ROOT}%{_datadir} -name '*=*ldif' -print`
  do 
  NEWNAME=$( echo $OLDNAME | sed -e 's?=?-?g' )
  mv $OLDNAME $NEWNAME
  done

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc COPYING README README.Coding WHATSNEW.txt
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
#swat see below
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
#for doc section from above
%dir %attr (0755, root, sys) %{_datadir}
#%if %{_share_locale_group_changed}
#%dir %attr (0755, root, %{_share_locale_group}) %{_datadir}/locale
#%defattr (-, root, %{_share_locale_group})
#%else
#%dir %attr (0755, root, other) %{_datadir}/locale
#%defattr (-, root, other)
#%endif
#%{_datadir}/locale/*
%dir %attr (0755, root, other) %{_docdir}
#%dir %attr (0755, root, other) %{_docdir}/%{src_name}
#perl5
#%{_datadir}/perl5
#/var/tmp/pkgbuild-sfe/SFEsamba42-4.2.2-build/usr/perl5
#/usr/perl5
%{_prefix}/share/perl5
%{_datadir}/samba

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
##TODO##%dir %attr (0755, root, bin) %{_mandir}
##TODO##%dir %attr (0755, root, bin) %{_mandir}/*
##TODO##%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*
#%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/samba4gnu-samba.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/samba42gnu.xml



%changelog
* Tue Aug  4 2015 - Thomas Wagner
- to build certificates for an AD Domain add Requires: SFEgnutls
- bump to 4.2.3
* Wed Jun  3 2015 - Thomas Wagner
- svn copy to SFEsamba42.spec
- bump to 4.2.2
* Wed Mar  4 2015 - Thomas Wagner
- bump to 4.1.12
- add (Build)Requires: SFEopenldap-gnu
- find SFEopenladp-gnu with -I/usr/gnu/include in CFLAGS
- --with-acl-support --without-systemd --with-shared-modules=nfs4_acls,vfs_zfsacl,idmap_ad,idmap_ldap,idmap_rid,idmap_tdb2
- --with-logfilebase=%{_localstatedir}/samba/log \
* Sat Feb  9 2013 - Thomas Wagner
- use waf build, rename files with "=" to "-", use SFE xsltproc (fix multiline), enable some supporting files *reg, SMF manifest 
* Sat Jan  5 2013 - Thomas Wagner
- initial spec file, merged from SFEsamba35.spec and SFEsamba4.spec (kmays)
* Thu Dec 27 2012 - Thomas Wagner
- bump to 3.5.20
- use auto-switch for changing group owner of /usr/gnu/share/locale
- add package description
* Sun Oct  7 2012 - Thomas Wagner
- use separate names f/e daemon in SMF dependent group
* Fri Jun 15 2012 - Thomas Wagner
- reworked, usw old sfw gcc-3, changed *FLAGS
- add -ln curses to LDFLAGS to solve libreadline not finding symbol tgetent (*curses)
- add patches patches/samba-01-oi-2172.diff patches/samba-06-remove-attr_get-configure.in.diff
* Wed May 30 2012 - Thomas Wagner
- bump to 3.5.15
- enable parallel build
* Mon Apr 23 2012 - Thomas Wagner
- derived 3.5.14 from 3.6.4
- add IPS_package_name with sfe/ prefix
##TODO## test addmachinescript, PDC, roaming profiles.
## Is this version better then 3.6.4 as a AD member?
* Tue Apr 17 2012 - Thomas Wagner
- bump to 3.6.4 (trigger was CVE-2012-1182 "root" credential remote code execution.)
- remove -L /usr/gnu/lib/samba to avoid build time errors by old incompatible libs
* Wed Jan  4 2012 - Thomas Wagner
- bump to 3.6.1
* Tue Apr 19 2011 - Thomas Wagner
- bump to 3.5.8
- new Download-URL
* Sun Mar 14 2010 - Thomas Wagner
- bump to 3.4.7
* Thr Nov 11 2009 - Thomas Wagner
- bump to 3.4.3, corrected download-URL
- add manifest for nmbd and winbindd, renamed manifest for smbd, new FMRI for samba and it's helper daemons, 3 in total
- add ext-sources addmachinescript to workaround "$" in machine-name to exit tools != 0 
* Thr Sep 24 2009 - Thomas Wagner
- bump / change series to version 3.4.1
* Thr Sep 24 2009 - Thomas Wagner
- bump to version 3.2.14  --- NOTE: seems to be discontinued
* Wed Jan  7 2009 - Thomas Wagner
- remove %post, %preun, %postun
- bump to version 3.2.7 to solve CVE-2009-0022 and CVE-2008-4314
- clean %doc, add mkdir %{_docdir} for compatibility to older pkgbuild/pkgtool
* Mon Oct 13 2008 - Thomas Wagner
- typo at mkdir for samba log
* Fri Oct 03 2008 - Thomas Wagner
- derive new SMF instance from samba.xml and add postinstall for import
* Sat Sep 13 2008 - Thomas Wagner
- Initial spec - derived from LSB/lsb-samba.spec


