##TODO##
#ld.so.1: smbd: fatal: relocation error: file /usr/gnu/lib/samba/samba/libsmbd-base-samba4.so: symbol FamErrlist: referenced symbol not found
#[ Nov 10 12:05:20 Method "start" failed due to signal KILL. ]
#root@mailrouter:/etc/samba# ls -l /usr/gnu/lib/samba/samba/libsmbd-base-samba4.so:
#/usr/gnu/lib/samba/samba/libsmbd-base-samba4.so:: No such file or directory
#root@mailrouter:/etc/samba# ls -l /usr/gnu/lib/samba/samba/libsmbd-base-samba4.so 
#-rwxr-xr-x   1 root     bin      4251684 Nov 10 11:58 /usr/gnu/lib/samba/samba/libsmbd-base-samba4.so
#root@mailrouter:/etc/samba# pkg search libfam.so.0
#INDEX      ACTION VALUE                     PACKAGE
#basename   link   usr/lib/libfam.so.0       pkg:/library/file-monitor/gamin@0.1.10-0.0.151022
#basename   link   usr/lib/amd64/libfam.so.0 pkg:/library/file-monitor/gamin@0.1.10-0.0.151022
#basename   link   usr/lib/libfam.so.0       pkg:/library/file-monitor/gamin@0.1.10-0.0.151022
#basename   link   usr/lib/amd64/libfam.so.0 pkg:/library/file-monitor/gamin@0.1.10-0.0.151022


##TODO## Pfad in Muster smb.conf anpassen:
# solaris-11.3-0.175.3.35.0.6.0

##TODO## update auf samba 4.7 !!!

#
#     Planung: Aktionen werden zusammengeführt ... Fertig (0.051s)
#     Planung: Es wird auf widersprüchliche Aktionen geprüft ... Fertig (9.301s)
#
#pkg update: Folgende Pakete stellen Aktionen des Typs file für etc/samba/smb.conf.default bereit:
#
#  pkg://solaris/service/network/samba@4.7.6,5.11-0.175.3.32.0.4.0:20180426T185303Z
#  pkg://localhosts11/sfe/service/network/samba46@4.6.14,5.11-0.0.175.3.1.0.5.0:20180316T233648Z
#
#Diese Pakete dürfen nicht zusammen installiert werden. Sofern die Pakete nicht widersprüchlich sind, dürfen
#sie gemeinsam installiert werden. Andernfalls müssen die Pakete vor der Installation berichtigt werden.
#
#Folgende Pakete stellen Aktionen des Typs file für usr/share/man/man3/talloc.3 bereit:
#
#  pkg://localhosts11/library/libtalloc@2.1.10,5.11-0.0.175.3.1.0.5.0:20180315T215352Z
#  pkg://solaris/service/network/samba@4.7.6,5.11-0.175.3.32.0.4.0:20180426T185303Z
#
#Diese Pakete dürfen nicht zusammen installiert werden. Sofern die Pakete nicht widersprüchlich sind, dürfen
#


##TODO## enable builds without internet connection. load docbook.xsl from local disk
##TODO2## omnos doesn't have it in the public repo as of 201803xx (only in extra)

# https://github.com/omniosorg/omnios-build/pull/597/commits/c4bb8a1ecc4b724cdcee979bbaf341b3cf336d12
# 
#  16 build/ntpsec/patches/nonet.patch
# @@ -0,0 +1,16 @@
# +
# +Always pass --nonet to xsltproc to avoid it checking for updated
# +stylesheets.
# +
# +diff -pruN '--exclude=*.orig' ntpsec-1.0.0~/wscript ntpsec-1.0.0/wscript
# +--- ntpsec-1.0.0~/wscript	2017-10-10 03:54:39.000000000 +0000
# ++++ ntpsec-1.0.0/wscript	2017-12-27 14:20:06.985213252 +0000
# +@@ -207,6 +207,8 @@
# +     if not ctx.options.enable_a2x_xmllint:
# +         ctx.env.A2X_FLAGS += ["--no-xmllint"]
# + 
# ++    ctx.env.A2X_FLAGS += ["--xsltproc-opts=--nonet"]
# ++
# +     # Disable manpages within build()
# +     if ctx.options.disable_manpage:
# +         ctx.env.DISABLE_MANPAGE = True



##TODO## just in case we have none, provide a copy of docbook.xsl in ext-sources and copy it over in the %prep section
##       location for the copy is to be determined. e.g. could make gsed pattern use packages/BUILD/samba-4.6.13/ for the local copy - set the replace pattern accordingly
# s11175 sfe ~/packages/BUILD/samba-4.6.13 ggrep -r ".http://docbook.sourceforge.net.*docbook.xsl"                                                                                                                                                
# 
# lib/ldb/docs/builddocs.sh:MANXSL="http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl"
# lib/ldb/docs/builddocs.sh:HTMLXSL="http://docbook.sourceforge.net/release/xsl/current/html/docbook.xsl"
# .pkgbuild.build.sh:#bld.env.MAN_XSL = 'http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl'
# .pkgbuild.build.sh:   -e '/bld.env.MAN_XSL = / s?http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl?' \
# buildtools/wafsamba/samba_conftests.py:    s='http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl'
# Binary file buildtools/wafsamba/samba_conftests.pyc matches
# buildtools/wafsamba/wafsamba.py.bak:    bld.env.MAN_XSL = 'http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl'
# buildtools/wafsamba/wafsamba.py.bak.docbook.xsl:    bld.env.MAN_XSL = 'http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl'
# bin/config.log:Checking for stylesheet http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl
# bin/config.log:Checking for stylesheet http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl
# docs-xml/xslt/man.xsl:<xsl:import href="http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl"/>
# docs-xml/xslt/html.xsl:<xsl:import href="http://docbook.sourceforge.net/release/xsl/current/html/docbook.xsl"/>
# 








#plain omnios

#
#Paketcache wird aktualisiert                     2/2
#root@drsnt05:/lib/svc/manifest/system# /usr/gnu/bin/smbclient \\\\servername\\renodat -U Administrator
#ld.so.1: smbclient: fatal: libpopt.so.0: open failed: No such file or directory
#ld.so.1: smbclient: fatal: relocation error: file /usr/gnu/bin/smbclient: symbol poptHelpOptions: referenced symbol not found
#Killed
#root@drsnt05:/lib/svc/manifest/system# LD_PRELOAD=/^Csr/gnu/bin/smbclient \\\\servername\\renodat -U Administrator
#root@drsnt05:/lib/svc/manifest/system# pkg list | grep popt
#root@drsnt05:/lib/svc/manifest/system# pkg install -v libpopt
#
#
#-rwxr-xr-x   1 root     bin       438336 Aug 20 18:05 /usr/lib/libncurses.so.6.0
#-rw-r--r--   1 root     bin       183892 Aug 20 18:05 /usr/lib/libncurses++.a
#root@drsnt05:/lib/svc/manifest/system# LD_PRELOAD=/usr/lib/libncurses.so.6.0 /usr/gnu/bin/smbclient \\\\servername\\renodat -U Administrator
#Enter WORKGROUP\Administrator's password: 
#Domain=[SERVERNAME] OS=[Windows Server 2012 R2 Standard Evaluation 9600] Server=[Windows Server 2012 R2 Standard Evaluation 6.3]
#smb: \> 
#
#
#
#




















#This might be a default smb.conf to be used when provisioning a AD domain!
#contains the ZFS acl settings.
#/localhomes/sfe/smb.conf_sysvolshare-samba-domain
#     
#     # start with no smb.conf. Important: compiled --without-ntvfs (or just not specify --with-ntvfs ... this module core dumps!)
#     
#     # samba-tool domain provision --realm="youradname.yourdomainname" --use-rfc2307 --interactive
#     # this first run will fail with ACL errors, but then add the parameters from below:
#     # the block sysvol -> merge the whole block, you may erase the path given by the samba-tool and use the example
#     # re-run the same provision command again and it will happily create the ACLs
#     
#     # start the samba server in foreground for more details:
#     # /usr/gnu/sbin/samba -i -d 5 
#     
#     # set your client PC to use the DNS of the AD Server Machine
#     # set your client IPv4 / IPv6 config to have DHCP deliver
#     # or have manually set: DNS-Server "the AD Server Machine IP" and  This connection DNS suffix: "youradname.yourdomainname"
#     # join the domain with the user: Administrator and the password you gave at provisioning with samba-tool
#     
#     
#     
#     
#     
#     # zfs create rpool/sysvol
#     # zfs set mountpoint=/var/tmp/sysvol rpool/sysvol
#     # 
#     # zfs set aclmode=passthrough rpool/sysvol
#     # zfs set aclinherit=passthrough rpool/sysvol
#     
#     [sysvol]
#        path = /var/tmp/sysvol
#        vfs objects = zfsacl
#        nfs4:mode = special
#        nfs4:acedup = merge
#        nfs4:chown = yes
#        zfsacl: acesort = dontcare
#        
#     [homes]
#        comment = Home Directories
#        browseable = no
#        writable = yes
#        guest ok = no
#     ##(1) initial
#       wide links = yes
#       hide files = /outlook*.lnk/*Briefcase*/
#        vfs objects = zfsacl
#        nfs4:mode = special
#        nfs4:acedup = merge
#        nfs4:chown = yes
#        zfsacl: acesort = dontcare
#     
#       























#https://github.com/OpenIndiana/oi-userland/pull/3758





#Upgrade-path:
# within a series upgrade is with the same package name
# e.g. samba46 in version 4.6.2 upgrades to 4.6.3
#
# if support ends, then the last released package in sfe
# has a renamed-to action and the target package name
# obsletes the old package name
#
# e.g. samba46 version 4.6.3-plus has renamed-to once
# the upgrade is mandatory and redirects resolver to
# samba 49 version x.y.z

%define _use_internal_dependency_generator 0

##TODO## try winbind separately in 32/64 bit


#
# spec file for package SFEsamba
#

%include Solaris.inc
%define cc_is_gcc 1
#rely on $PATH to find the right g++
%define _gpp g++

#avoid clush with /usr/bin/profiles of SUNWcsu Solaris package
%include usr-gnu.inc
%include base.inc

%include packagenamemacros.inc

%define src_name samba

##TODO## below test with python 3.4
%if %{solaris11}
%define python_major_minor_version 2.7
%endif

#%if %{omnios}
#%define python_major_minor_version 3.5
#%endif

Name:                    SFEsamba49
IPS_package_name:	 sfe/service/network/samba49
Summary:                 samba - CIFS Server, AD and Domain Controller
URL:                     http://samba.org/
Version:                 4.9.8
%define major_version %( echo %{version} | awk -F'.' '{print $1}' )
%define minor_version %( echo %{version} | awk -F'.' '{print $2}' )
Copyright:               GPLv3
SUNW_Copyright:          GPLv3.copyright
##TODO## License: 
Url:                     http://www.samba.org
Source:                  http://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.gz
Source2:		sambagnu-smbd.xml
Source3:		sambagnu-nmbd.xml
Source4:		sambagnu-winbindd.xml
Source5:		addmachinescript-samba3
Source6:		domain-samba3.reg
Source7:                samba%{major_version}%{minor_version}gnu.xml
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

#obsolete Patch9:			samba46-09-ifndef-MSG_NOSIGNAL-messages_dgm.c.diff

#imported from Solaris Userland Gate (samba 4.4.8)
patch10:		samba44-10-25511645.patch
#check# patch11:		samba44-11-MITkrb5-Solaris.patch
patch12:		samba44-12-hcrypto.patch
patch13:		samba44-13-ldap-libs.patch
patch14:		samba44-14-mech_krb5-oids4solaris.patch
#obsolete patch15:		samba44-15-samba_autoconf.py.patch
#check# patch16:		samba44-16-source3-krb5-build.patch
patch17:		samba44-17-source3-winbind-krb5-build.patch

#sfe patches
patch31:		samba44-31-gss_mech_krb5.diff
patch32:		samba49-32-remove-libiconv.diff
patch33:		samba46-33-provision-add-smb.conf-extra-defaults.diff
patch34:		samba49-34-provision-remove-check-have_posix_acls.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

##TODO## better
#BuildRequires: SUNWgcc
#Requires:      SUNWgccruntime
BuildRequires: SFEgcc-49
Requires: SFEgccruntime-49
BuildRequires: %{pnm_buildrequires_SUNWbash}
Requires:      %{pnm_requires_SUNWbash}
BuildRequires: SFEopenldap-gnu
Requires:      SFEopenldap-gnu

#to build certificates for an AD Domain:
BuildRequires:  SFEgnutls
Requires:       SFEgnutls

#https://wiki.samba.org/index.php/Operating_system_requirements/Dependencies_-_Libraries_and_programs
BuildRequires: SFEpython%{python_version_package_string}-pycrypto
Requires:      SFEpython%{python_version_package_string}-pycrypto

BuildRequires: SFEtalloc
Requires:      SFEtalloc
BuildRequires: %{pnm_buildrequires_library_popt}
Requires:      %{pnm_requires_library_popt}

#change to read library/jansson here and in include/packagename*inc
BuildRequires: %{pnm_buildrequires_SFElibjansson}
Requires:      %{pnm_requires_SFElibjansson}

#change to read library/archive here and in include/packagename*inc
BuildRequires: %{pnm_buildrequires_SFElibjansson}
Requires:      %{pnm_requires_SFElibarchive}

#change to read ..../gpgme here and in include/packagename*inc
BuildRequires: %{pnm_buildrequires_SFEgpgme}
Requires:      %{pnm_requires_SFEgpgme}

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
. 
See CVE notes here: https://www.samba.org/samba/history/security.html
See Samba Release notes here: https://www.samba.org/samba/history/
. 
Configure an AD:  (Attention: more instructions to get a ZFS dataset with pass-through for ACLs will follow. See SFE website)
samba-tool domain provision --use-rfc2307 --interactive --use-xattrs=yes
svcadm enable samba%{major_version}%{minor_version}
. 
(more options: /usr/gnu/bin/samba-tool domain provision --help )

Notes:
  use for AD domains use SMF service: samba49
  use for non-AD modes use SMF services: smbd, nmbd, winbindd

If you want to run an EXE from a share, add to the share:
acl allow execute always = True


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
#old mode samba3 with smbd and nmbd winbindd SMF manifests - NOT AUTO IMPORTED!
cp -p %{SOURCE2} sambagnu-smbd.xml
cp -p %{SOURCE3} sambagnu-nmbd.xml
cp -p %{SOURCE4} sambagnu-winbindd.xml
cp -p %{SOURCE5} addmachinescript
cp -p %{SOURCE6} domain.reg
#samba SMF manifest for operating as AD controller
cp -p %{SOURCE7} .
#%patch4 -p0

#solaris useradd smb.conf.default
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#replaced with sed
#%patch8 -p1
#obsolete %patch9 -p1
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


#obsolete with samba 4.4.10
#%patch10 -p1
##check## %patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
#obsolete %patch15 -p1
##check## %patch16 -p1
%patch17 -p1

perl -pi -e 's:^#! */usr/bin/env *python:#!/usr/bin/python%{python_major_minor_version}:'  `ggrep -r -l "env python"`

%if %{oihipster}
#or get 
# ../source4/heimdal/lib/gssapi/gssapi/gssapi_krb5.h:64:29: error: expected identifier or '(' before '&' token
# #define GSS_KRB5_MECHANISM (&__gss_krb5_mechanism_oid_desc)
%patch31 -p1
%endif


%if %{solaris12}
## vim auth/kerberos/gssapi_pac.c
#den "if 1" auf "if 0" aendern im Falle Solaris12
#braucht auf solari12 nicht definiert werden, sonst Fehler:
#../auth/kerberos/gssapi_pac.c:35:27: error: static declaration of 'krb5_gss_oid_array' follows non-static declaration
# static const gss_OID_desc krb5_gss_oid_array[] = {
#                           ^
#In file included from ../lib/replace/system/gssapi.h:43:0,
#                 from ../lib/krb5_wrap/gss_samba.h:27,
#                 from ../auth/kerberos/pac_utils.h:27,
#                 from ../auth/kerberos/gssapi_pac.c:24:
#/usr/include/kerberosv5/gssapi/gssapi_krb5.h:87:38: note: previous declaration of 'krb5_gss_oid_array' was here
# GSS_DLLIMP extern const gss_OID_desc krb5_gss_oid_array[];
%patch31 -p1

#lib/texpect/texpect.c"
gsed -i.bak -e '/#include <popt.h>/ a\
#include "termios.h"
' lib/texpect/texpect.c
%endif

#dito omnios
%if %{omnios}
%patch31 -p1
%endif

#dito s11
%if %{solaris11}
%patch31 -p1
%endif

#remove iconv
%patch32 -p1

%patch33 -p1
%patch34 -p1

%build
#export PYTHON="/usr/bin/python%{python_major_minor_version}"
#if it can't find param, then is effectively looks for param.so and that is 32 or 64 bit.
#Omnios by default uses 64-bit python, so no param.so object in 64-bit is available by samba
%if %{omnios}
export PYTHON="/usr/bin/i386/python%{python_major_minor_version}"
%else
export PYTHON="/usr/bin/i86/python%{python_major_minor_version}"
%endif
%if %{s110400}
export PYTHON="/usr/bin/python%{python_major_minor_version}"
%endif

#parked ifeq ($(MACH), sparc)
#parked WAFOPT1	= -j64 
#parked override studio_OPT = -xO1
#parked WAF_PATH	=	PATH=$(BUILD_DIR)/samba/buildtools/bin:$(PROTO_DIR)/usr/bin:$$PATH
#parked CFLAGS.studio	+=	$(studio_C99_ENABLE)
#parked LIBS +=		-lrt -lsec -lcrypt -lmd5 -lsocket -lnsl
#parked LIBS +=		-lrt -lsec -lcrypt -lmd5 -lsocket -lnsl
# More libs needed by smbd (libavahi, libgamin, ...)
#parked LIBS4SMBD =	-lsendfile -lavahi-common -lavahi-core
#parked CPPFLAGS +=	$(CPP_LARGEFILES)
#parked CPPFLAGS +=	$(CPP_XPG6MODE)
#parked CPPFLAGS +=	-I/usr/include/openldap
#parked 
# MIT kerberos uses different enctype defs.
#parked CPPFLAGS += -DCKSUMTYPE_HMAC_SHA1_96_AES_128=CKSUMTYPE_HMAC_SHA1_96_AES128
#parked CPPFLAGS += -DCKSUMTYPE_HMAC_SHA1_96_AES_256=CKSUMTYPE_HMAC_SHA1_96_AES256
# Enable adiheap and adistack security extensions
#parked ADIHEAP_MODE =	$(ADIHEAP_ENABLE)
#parked ADISTACK_MODE =	$(ADISTACK_ENABLE)
#parked LDFLAGS +=	-m$(BITS)
#parked LDFLAGS +=	-R/usr/lib/samba$(MACHLIBDIR)
#parked LDFLAGS +=	-R/usr/lib/samba/private$(MACHLIBDIR)
#parked LDFLAGS +=	$(LIBS)
#parked $(BUILD_DIR_SMB)/.configured:	LDFLAGS +=	$(LIBS4SMBD)
#parked LD_OPTIONS += 	$(LD_B_DIRECT)
#parked 
##TODO## alle statischen Module ausfinden und dann explizt wieder einschalten
# Whenever getfacl is found HAVE_SOLARIS_UNIXWARE_ACLS is set and
# vfs_solarisacl is placed into the list of the static modules
#parked CONFIGURE_OPTIONS +=	--with-static-modules=
#parked --with-shared-modules=vfs_worm,vfs_zfsacl,vfs_prealloc,vfs_cacheprime,vfs_commit,idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex
#parked 	--with-shared-modules=idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex
#parked --with-ads
#parked --with-winbind
#parked --with-ldap
#parked --with-libldap=ldap_r
#parked --with-system-mitkrb5
#NICHT# parked --without-ad-dc

#parked --nocache
#parked --nopyo
#parked --disable-rpath
#NICHT# parked --disable-gnutls
#parked --bundled-libraries=ALL
#parked export PYTHONDIR="$(PYTHON_VENDOR_PACKAGES)"
#parked export PYTHONARCHDIR="$(PYTHON_VENDOR_PACKAGES)/samba"
#parked 
#parked export PERL=$(PERL)
#parked export PYTHONDIR="$(PYTHON_VENDOR_PACKAGES)"
#parked export PYTHONARCHDIR="$(PYTHON_VENDOR_PACKAGES)/samba"
#parked export LD="$(LD)"
#parked export CFLAGS="$(CFLAGS)"
#parked export C	rkedONFIGURE_ENV +=	CPPFLAGS="$(CPPFLAGS) -I$(PROTO_DIR)/usr/include -I$(COMPONENT_DIR)/Solaris/include"
#parked export LINKFLAGS="$(LD_OPTIONS) $(LDFLAGS)"
#parked export CONFIGURE_ENV.64 +=	MACH64="$(MACH64)"
#parked export LD_EXEC_OPTIONS="$(LD_EXEC_OPTIONS)"
#parked export CUPS_CONFIG=$(USRBINDIR)/cups-config
#parked 
## Propagation of smb.conf with default settings.
#$(PROTO_DIR)/etc/samba/smb.conf-example: $(BUILD_DIR_SMB)/.built
#	$(MKDIR) $(@D)
#	sed -f $(COMPONENT_DIR)/Solaris/smbconf.sed > $@ \
#	   $(BUILD_DIR_SMB)/examples/smb.conf.default
#parked 
#parked 
#parked $(PYTHON) -m compileall $(PROTO_DIR)/$(PYTHON_VENDOR_PACKAGES)/
#parked 
#parked ACHTUNG: winbind in 32 und 64 bit bauen siehe Makefile solaris userland
#parked 
#parked 	# set version of python interpreter for pkglint
#parked 	find $(PROTO_DIR) -name \*.py -print0 | \
#parked 	   while IFS= read -r -d $$'\0' file; do \
#parked 		/usr/bin/sed -e '1,1s&^#!.*python[:blank:]\{0,\}$$&#!$(PYTHON.$(PYTHON_VERSION))&' \
#parked 		   $$file > $$file.pyverset ; \
#parked 	   done
#parked 	find $(PROTO_DIR) -name \*.py.pyverset -print0 | \
#parked 	   while IFS= read -r -d $$'\0' file; do \
#parked 		$(MV) $$file `echo $$file | sed -e 's/[.]pyverset$$//'` ; \
#parked 	   done
#parked 
#parked 
#parked 


CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')


export CC=/usr/gcc-sfe/4.9/bin/gcc
export CXX=/usr/gcc-sfe/4.9/bin/g++
export CPP="$CC -E"
export AR=/usr/bin/ar

##TODO## which ranlib, which ar? defaults to /usr/gnu/bin/ranlib /usr/gnu/bin/ar
#are they used?
#RANLIB=/usr/bin/ranlib
#AR=/usr/bin/ar

export LD=/usr/bin/ld


#compile time might have much never samba libs then the installed one on the disk
##PAUSE## LIBSCOMPILETIME=`pwd`/nsswitch:`pwd`/source%{major_version}/bin
##PAUSE## export LD_LIBRARY_PATH=$LIBSCOMPILETIME

#export CFLAGS="%optflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib -lncurses -ltermcap"
#export CXXFLAGS="%cxx_optflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib"
##TEST-AUS## export CFLAGS="%optflags -L$LIBSCOMPILETIME"
##TEST-AUS## export CXXFLAGS="%cxx_optflags -L$LIBSCOMPILETIME"

##NEU##
##TODO## find openldap on other way then including the whole /usr/gnu/include (old samba install might deliver tdb.h, fails the build eventually)
#export CFLAGS="%optflags -I/usr/gnu/include -D_XPG6 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
#getpagesize needs -D__EXTENSIONS__
export CFLAGS="%optflags -I/usr/gcc/include/openldap -I/usr/gnu/include -D__EXTENSIONS__ -D_XPG6 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
export CPPFLAGS="-I/usr/gcc/include/openldap -I/usr/gnu/include -D__EXTENSIONS__ -D_XPG6 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DCKSUMTYPE_HMAC_SHA1_96_AES_128=CKSUMTYPE_HMAC_SHA1_96_AES128 -DCKSUMTYPE_HMAC_SHA1_96_AES_256=CKSUMTYPE_HMAC_SHA1_96_AES256"

#-gdwarf-2 

#export CXXFLAGS="%cxx_optflags -I/usr/gnu/include  -D_XPG6 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="%cxx_optflags"
#export LDFLAGS="%_ldflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib"
#export LDFLAGS="$LDFLAGS -lncurses -ltermcap"
##TEST-AUS## export LDFLAGS="%_ldflags -L$LIBSCOMPILETIME -L/usr/gnu/lib -R/usr/gnu/lib"
##TEST-AUS## export LDFLAGS="$LDFLAGS -lncurses -ltermcap"
export LDFLAGS="%_ldflags -m32 -R/usr/gnu/lib/samba/samba  -L/usr/gnu/lib -R/usr/gnu/lib"
#probe#export LDFLAGS="$LDFLAGS -lrt -lsec -lcrypt -lmd5 -lsocket -lnsl -Bzignore -Bzcombreloc -Bdirect"
export LDFLAGS="$LDFLAGS -lrt -lsec -lcrypt -lmd5 -lsocket -lnsl"
export LDFLAGS="$LDFLAGS -lncurses -ltermcap"
#probe#export LDFLAGS="$LDFLAGS -z nodeferred -z verbose -z now"
#aus https://github.com/sjorge/pkgsrc-blackdot/blob/master/samba-pbd/Makefile
export LDFLAGS="$LDFLAGS -lintl"
#probe#export EXTRA_LDFLAGS=" -B zignore -B zcombreloc -B direct -B symbolic "
#probe#export EXTRA_LDFLAGS="$EXTRA_LDFLAGS -z nodeferred -z verbose -z now"
export EXTRA_LDFLAGS="-lncurses"
export LINKFLAGS="$EXTRA_LDFLAGS"


#probe#export CFLAGS="$CFLAGS -g -Og -gdwarf-4 -fvar-tracking-assignments"
#probe#export CXXFLAGS="$CXXFLAGS -g -Og -gdwarf-4 -fvar-tracking-assignments"

#aus https://github.com/sjorge/pkgsrc-blackdot/blob/master/samba-pbd/Makefile
export CFLAGS="$CFLAGS -DHAVE_SOLARIS_GETGRENT_R"
export CXXFLAGS="$CXXFLAGS -DHAVE_SOLARIS_GETGRENT_R"

#xsltproc fails 
export XSLTPROC=/usr/gnu/bin/xsltproc

#find libgnutls in /usr/gnu
export PKG_CONFIG_PATH=%{_prefix}/gnu/lib/pkgconfig:%{_prefix}/lib/pkgconfig

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

export LIBS4SMBD="-lsendfile -lavahi-common -lavahi-core"

%if %{solaris11}
# --with-system-mitkrb5 needs:
#-version_string="Solaris Kerberos based on MIT Kerberos 5 release 1.8.3"
#+version_string="Solaris Kerberos (based on MIT Kerberos 5 release 1.8.3)"
mkdir -p bin/
cp -p /usr/bin/krb5-config bin/
gsed -i.bak -e '/^version_string=/ s?[()]??g' bin/krb5-config
export KRB5_CONFIG=`pwd`/bin/krb5-config
%endif

#avoid loading docbook.xml from sourceforge every time
#bld.env.MAN_XSL = 'http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl'
#evaluate current path
%if %{omnios}
#if necessary, then provide a local package for docbook.xsl (e.g. pkg:/data/docbook/docbook-style-xsl)
%else
gsed -i.bak.docbook.xsl \
   -e '/bld.env.MAN_XSL = / s?http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl?' \
   buildtools/wafsamba/wafsamba.py \

gsed -i.bak.docbook.xsl \
   -e '/MANXSL=/ s?http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl?' \
   -e '/HTMLXSL=/ s?http://docbook.sourceforge.net/release/xsl/current/html/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/html/docbook.xsl?' \
   lib/ldb/docs/builddocs.sh

gsed -i.bak.docbook.xsl \
   -e '/s=.http:\/\/docbook.sourceforge.net\/release\/xsl\/current\/manpages\/docbook.xsl./ s?http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl?' \
   buildtools/wafsamba/samba_conftests.py

gsed -i.bak.docbook.xsl \
   -e '/xsl:import href=/ s?http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl?' \
   docs-xml/xslt/man.xsl

gsed -i.bak.docbook.xsl \
   -e '/xsl:import href=/ s?http://docbook.sourceforge.net/release/xsl/current/html/docbook.xsl?file:///usr/share/sgml/docbook/xsl-stylesheets/html/docbook.xsl?' \
   docs-xml/xslt/html.xsl
%endif


##TODO## scheint nicht zu klappen
#aus http://midnight-commander.org/attachment/ticket/1943/01_namelen.patch
#ABER:
##TODO## kontrollieren ob das ein geegneter Wert ist (kann z.B. 512 statt 255 sein)
%if %( expr %{solaris11} '+' %{s110400} '>=' 1 )
#gsed -i.bak -e 's?NAME_MAX?MAXNAMLEN?' source3/modules/vfs_glusterfs.c source3/modules/vfs_glusterfs_fuse.c
gsed -i.bak -e 's?[^_]NAME_MAX?MAXNAMLEN?' source3/modules/vfs_glusterfs.c source3/modules/vfs_glusterfs_fuse.c
%endif

            # --enable-debug \
#CC=/usr/gnu/bin/gcc CXX=/usr/gnu/bin/g++ CPP=/usr/gnu/bin/cpp \
PERL_ARCH_INSTALL_DIR=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
PERL_LIB_INSTALL_DIR=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
PKG_CONFIG_PATH=%{_prefix}/gnu/lib/pkgconfig:%{_prefix}/lib/pkgconfig \
PYTHONDIR='%{_libdir}/python%{python_major_minor_version}/site-packages:/usr/lib//python%{python_major_minor_version}' \
PYTHONARCHDIR='%{_libdir}/python%{python_major_minor_version}/site-packages/samba' \
CC=$CC CXX=$CXX CPP=$CPP CPPFLAGS=$CPPFLAGS CXXFLAGS=$CXXFLAGS CFLAGS=$CFLAGS \
LDFLAGS=$LDFLAGS \
EXTRA_LDFLAGS=$EXTRA_LDFLAGS \
LINKFLAGS=$LINKFLAGS \
       $PYTHON buildtools/bin/waf -v configure \
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
--with-ads \
--with-ldap \
--with-libldap=ldap_r \
--with-automount \
--with-dnsupdate \
--with-pam \
--with-acl-support   \
--without-systemd    \
--disable-glusterfs  \
--with-static-modules=vfs_default,vfs_zfsacl,auth_builtin,auth_sam,auth_winbind,vfs_solarisacl,pdb_smbpasswd,pdb_tdbsam,auth_unix,pdb_samba_dsdb,auth_samba4,vfs_dfs_samba4,pdb_ldapsam \
--with-shared-modules=vfs_prealloc,vfs_cacheprime,vfs_commit,idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex,idmap_passdb,vfs_fruit \
--with-pie \
--enable-gccdeps \
--symbol-check \
--gdbtest \
--nocache \


#--without-ntvfs \

#--without-winbind \
#mit samba46? --with-ntvfs \
#mal raus aus shared-modules  ,idmap_nss \
#mal raus aus static-modules  ,nss_info_template

#compiled nicht: vfs_posixacl (../source3/modules/vfs_posixacl.c:27:33: error: unknown type name 'acl_entry_t' und viele mehr)

#das geht nicht --address-sanitizer \
#--disable-rpath \

#ausprobieren:
# --with-pie --with-relro --with-relro --enable-gccdeps --disable-rpath --address-sanitizer --symbol-check --gdbtest 
#das klappt nicht: --with-relro \
#ld: fatal: option '-z' has illegal argument 'relro'


#--with-static-modules=vfs_default,auth_domain,auth_builtin,auth_sam,auth_winbind,vfs_solarisacl \
#--with-shared-modules=nfs4_acls,vfs_zfsacl,idmap_ad,idmap_ldap,idmap_rid,idmap_tdb2,vfs_prealloc,vfs_cacheprime,vfs_commit,\
#pdb_smbpasswd,pdb_tdbsam,pdb_wbc_sam,auth_unix,auth_wbc,nss_info_template,idmap_tdb,idmap_passdb,idmap_nss,pdb_samba_dsdb,auth_samba4,vfs_dfs_samba4,pdb_ldapsam \
#--with-ntvfs \


#%if %{solaris12}
#--with-system-mitkrb5 \
#--without-ntvfs \
#%else
#--with-ntvfs \
#%endif

#smbd -b | gegrep -A10  -i "modu"
#Builtin modules:
#   vfs_default auth_domain auth_builtin auth_sam auth_winbind vfs_solarisacl pdb_smbpasswd pdb_tdbsam pdb_wbc_sam auth_unix auth_wbc nss_info_template idmap_tdb idmap_passdb idmap_nss pdb_samba_dsdb auth_samba4 vfs_dfs_samba4 pdb_ldapsam
#above: with trick --with-static-modules= (empty) and then add all except vfs_solarisacl to the shared modules we can avoid having vfs_solarisacl (errm, why? ... from solaris userland-gate)


#,vfs_solarisacl,
#unknown --enable-socket-wrapper \
#unknown --enable-nss-wrapper \

#removed from 4.4.0 --with-aio-support \

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


##unwind
##TODO## /localhomes/sfe/packages/BUILD/samba-4.4.9
##TODO## pkgbuild@s11175> find /usr/gcc -name libgcc-unwind.map
##TODO## /usr/gcc/4.9/lib/libgcc-unwind.map
##TODO## pkgbuild@s11175> cat /usr/gcc/4.9/lib/libgcc-unwind.map
##TODO## {
##TODO##         _Unwind_Backtrace = EXTERN DIRECT;
##TODO##         _Unwind_DeleteException = EXTERN DIRECT;
##TODO##         _Unwind_FindEnclosingFunction = EXTERN DIRECT;
##TODO##         _Unwind_Find_FDE = EXTERN DIRECT;
##TODO##         _Unwind_ForcedUnwind = EXTERN DIRECT;
##TODO##         _Unwind_GetCFA = EXTERN DIRECT;
##TODO##         _Unwind_GetDataRelBase = EXTERN DIRECT;
##TODO##         _Unwind_GetGR = EXTERN DIRECT;
##TODO##         _Unwind_GetIP = EXTERN DIRECT;
##TODO##         _Unwind_GetIPInfo = EXTERN DIRECT;
##TODO##         _Unwind_GetLanguageSpecificData = EXTERN DIRECT;
##TODO##         _Unwind_GetRegionStart = EXTERN DIRECT;
##TODO##         _Unwind_GetTextRelBase = EXTERN DIRECT;
##TODO##         _Unwind_RaiseException = EXTERN DIRECT;
##TODO##         _Unwind_Resume = EXTERN DIRECT;
##TODO##         _Unwind_Resume_or_Rethrow = EXTERN DIRECT;
##TODO##         _Unwind_SetGR = EXTERN DIRECT;
##TODO##         _Unwind_SetIP = EXTERN DIRECT;
##TODO##         _Unwind_SjLj_ForcedUnwind = EXTERN DIRECT;
##TODO##         _Unwind_SjLj_RaiseException = EXTERN DIRECT;
##TODO##         _Unwind_SjLj_Register = EXTERN DIRECT;
##TODO##         _Unwind_SjLj_Resume = EXTERN DIRECT;
##TODO##         _Unwind_SjLj_Resume_or_Rethrow = EXTERN DIRECT;
##TODO##         _Unwind_SjLj_Unregister = EXTERN DIRECT;
##TODO## };
##TODO## 

#sed -i.bak_add_samba-hostconfig -e "s?deps='?deps='samba-hostconfig ?" source4/ntvfs/wscript_build 
#VARIANTE
#gsed -i.bak_add_samba-hostconfig -e "s?deps='?deps='hostconfig ?" /source4/ntvfs/wscript_build 

#miss-detected HAVE_ATTR_
#/* #define HAVE_ATTR_GET 1 */
#/* #undef HAVE_ATTR_GETF */
#/* #undef HAVE_ATTR_LIST */
#/* #undef HAVE_ATTR_LISTF */
#/* #undef HAVE_ATTR_REMOVE */
#/* #undef HAVE_ATTR_REMOVEF */
#/* #define HAVE_ATTR_SET 1 */
#/* #undef HAVE_ATTR_SETF */
gsed -i.bak_undefine_HAVE_ATTR_ \
    -e '/#define HAVE_ATTR_GET 1/ s?^?// ?' \
    -e '/#define HAVE_ATTR_SET 1/ s?^?// ?' \
    bin/default/include/config.h


##TEST AUS##CC=/usr/gnu/bin/gcc CXX=/usr/gnu/bin/g++ CPP=/usr/gnu/bin/cpp python buildtools/bin/waf -v build -j$CPUS
$PYTHON buildtools/bin/waf -v build -j$CPUS
#gmake -j1

#from solaris userland gate
#/usr/gnu/lib/python2.7/site-packages/samba/third_party/dns/renderer.py
#or
#/usr/lib/python2.7/site-packages/samba/third_party/dns/renderer.py
$PYTHON -m compileall `find . -type f -name \*.py -print` || true

%install
rm -rf $RPM_BUILD_ROOT

export PYTHON="/usr/bin/python%{python_major_minor_version}"

$PYTHON buildtools/bin/waf -v install --destdir=$RPM_BUILD_ROOT

  	
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/samba/private
cp -p examples/smb.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/samba/smb.conf.default.sfe

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/

#new mode as samba4
cp -p samba%{major_version}%{minor_version}gnu.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

#old mode as samba3
cp -p sambagnu-smbd.xml      ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp -p sambagnu-nmbd.xml      ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp -p sambagnu-winbindd.xml  ${RPM_BUILD_ROOT}/var/svc/manifest/site/

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

#if docbook.xsl is unavailable, then we have no manpages. make %files doc happy with an empty directory
[ -d ${RPM_BUILD_ROOT}%{_mandir}/man1 ] || { mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1; touch ${RPM_BUILD_ROOT}%{_mandir}/man1/samba.temp.dummy; }

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
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/samba/smb.conf.default.sfe
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%attr (0500, root, bin) %dir %{_sysconfdir}/%{src_name}/private
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*
#%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/samba4gnu-samba.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/samba%{major_version}%{minor_version}gnu.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu-smbd.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu-nmbd.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu-winbindd.xml

%changelog
* Sat May 25 2019 - Thomas Wagner
- bump to 4.9.8 - CVE-2018-16860 Samba AD DC S4U2Self/S4U2Proxy unkeyed checksum
- add --disable-glusterfs, fix sed regex for MAXNAMLEN
* Fri Apr 19 2019 - Thomas Wagner
- add patch patches/samba49-34-provision-remove-check-have_posix_acls.diff to get AD Domain provision work
  run /usr/gnu/bin/samba-tool domain provision (and enter realm mytestdom.mydomain and domain mytestdom and a Admin password, then svcadm enable samba49
* Thu Apr 11 2019 - Thomas Wagner
- bump to 4.9.6
* Wed Mar 13 2019 - Thomas Wagner
- bump to 4.9.5
* Sun Mar  3 2019 - Thomas Wagner
- bump to 4.9.4 - svn copy from 4.6.16
- add BuildRequires: %{pnm_buildrequires_SFElibjansson}
* Sun Aug 26 2018 - Thomas Wagner
- bump to 4.6.16 - security fixes (CVE)
* Sun May 27 2018 - Thomas Wagner
- bump to 4.6.15
* Sat May 26 2018 - Thomas Wagner
- rename to etc/samba/smb.conf.default.sfe to not conflict with Solaris delivered samba 4
* Fri Mar 16 2018 - Thomas Wagner
- enable patch31 samba44-31-gss_mech_krb5.diff for Hipster (OIH)
* Tue Mar 13 2018 - Thomas Wagner
- bump to 4.6.14 - CVE-2018-1057: Unprivileged user can change any user (and admin) password
* Wed Mar  7 2018 - Thomas Wagner
- change dependent SMF service pg name to 'samba4-multi-user-server' in samba46gnu.xml or get badly broken multi-user-server with "Instance has conflicts" (needs magic or BE rollback to fix, I'm sorry)
* Thu Mar  1 2018 - Thomas Wagner
- bump to 4.6.13
* Mon Dec 25 2017 - Thomas Wagner
- bump to 4.6.10 - CVE-2017-14746, CVE-2017-15275
- update (Build)Requires from python crypto to SFEpython27-pycrypto (all)
* Thu Nov 23 2017 - Thomas Wagner
- add patch32 samba46-32-remove-libiconv.diff
* Thu Nov 16 2017 - Thomas Wagner
- add back old samba3 SMF manifests to let user decide which one is to be enabled
* Tue Oct 31 2017 - Thomas Wagner
- bump to 4.6.8 (downgrade, compile error "ace->aceMask" undefined with version 4.6.9)
* Tue Oct 31 2017 - Thomas Wagner
- bump to 4.6.9
* Sun Jul 30 2017 - Thomas Wagner
- bump to 4.6.4
- re-add SMF manifest for non-AD modes sambagnu-smbd.xml sambagnu-nmbd.xml sambagnu-winbindd.xml
  use for AD domains: SMF samba46
  use for non-AD modes smbd/nmbd/winbindd : SMF smbd, nmbd, winbindd
* Sun May 28 2017 - Thomas Wagner
- bump to 4.6.4
- add patch9 samba46-09-ifndef-MSG_NOSIGNAL-messages_dgm.c.diff https://bugzilla.samba.org/show_bug.cgi?id=12502
* Wed May 24 2017 - Thomas Wagner
- bump to 4.4.14
* Thu Mar 23 2017 - Thomas Wagner
- bump to 4.4.10
- remove patch10 samba44-10-25511645.patch (obsolete)
* Fri Jan  6 2017 - Thomas Wagner
- bump to 4.4.9
* Sun Oct 30 2016 - Thomas Wagner
- bump to 4.4.7
* Sun Jul 31 2016 - Thomas Wagner
- add missing (Build)Requires SFEgnutls
* Sat Jul 16 2016 - Thomas Wagner
- bump to 4.4.5 - CVE-2016-2119 Client side SMB2/3 required signing can be downgraded
* Wed Apr 13 2016 - Thomas Wagner
- bump to 4.4.2
* Fri Apr  8 2016 - Thomas Wagner
- add RPATH to smbclient/net/..
- add --with-ntvfs to get AD samba-tool domain provision stop complaining
* Fri Mar 25 2016 - Thomas Wagner
- bump to 4.4.0
* Wed Jan 14 2016 - Thomas Wagner
- bump to 4.3.5
* Wed Jan 14 2016 - Thomas Wagner
- bump to 4.2.3
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
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


