#From: Dieter Klünter <dieter@dkluenter.de>
#Reply-To: Discussion list for OpenIndiana <openindiana-discuss@openindiana.org>
#Subject: [OpenIndiana-discuss] Problem with openldap_24 package
#To: OpenIndiana Discuss <openindiana-discuss@openindiana.org>
#
#Hi,
#I face some problems with the existing openldap_24 package.
#The file '/lib/svc/method/ldap-olslapd' contains information that
#obsolete. Thus I modified this file to be in accordance with slapd(8).
#The databases back-bdb and back-hdb are obsolete, thus BerkleyDB-Tools
#(db_recover etc.) are not required anymore.
#
#These are my modifications of ldap-olslapd
#
#
#typeset -r CONFDIR=/etc/openldap/slapd.d
#typeset -r LDAP_URL=ldap:///
#typeset -r LDAPS_URL=ldaps:///
#typeset -r LDAPI_URL=ldapi:///
#typeset -r SLAPD="/usr/lib/64/slapd -h "${LDAP_URL} ${LDAPI_URL}" -u
#${LDAPUSR} -g ${LDAPGRP} -f ${CONF_FILE} -F ${CONFDIR}"
#
#As I mentioned in an earlier mail, I face some property problems with
#IPC socket.
#
#Some instance, unknown to me, is checking the file ldap-olslapd as the
#flag '-h' is ignored, according to the logs.
#
#lib/svc/method/ldap-olslapd[21]: typeset: ldapi:/// -u openldap -g
#openldap -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d: invalid
#variable name
#[ Juli 16 15:16:29 Method "stop" exited with status 1. ]
#
#Is there somebody who may have a look at this issues?
#
#-Dieter
#
#--
#Dieter Klünter | Directory Service
#http://sys4.de
#
#
#siehe https://www.illumos.org/issues/10069
#--enable-bdb=mod
#--enable-hdb=mod

# Date: Mon, 17 Dec 2018 21:54:30 +0100
# From: D      K       <d     @d        .  >
# Reply-To: Discussion list for OpenIndiana <openindiana-discuss@openindiana.org>
# Subject: [OpenIndiana-discuss] OpenLDAP and BerkeleyDB
# To: Openindiana <openindiana-discuss@openindiana.org>
# 
# Hi,
# I'm trying to get OpenLDAP running, but a BDB library mismatch prevents it :-(
# 
# bdb_back_initialize: BDB library version mismatch: expected Berkeley DB
# 5.3.21: (May 11, 2012), got Berkeley DB 5.3.28: (September  9, 2013
# 
# OpenLDAP: slapd 2.4.44 (Feb 11 2018 07:52:01) $
# @hipster.openindiana.org:/jenkins/jobs/oi-userland/workspace/components/network/openldap/build/amd64/servers/slapd
# 
# Whoever built this package,  PLEASE either stick to library conformance or,                                                        h
# even better, refrain from building slapd with BerkeleyDB, as this is
# deprecated, the announcement has been made at LDAPCon 2007.
# If you have to stick to BerkeleyDB build back_bdb and back_hdb as modules.
# 
# -Dxxxxx
 
 
 

%define _use_internal_dependency_generator 0

#
# spec file for package SFEopenldap.spec
#

# NOTE: some distributions provide theyr own openldap package,
#       you only want his package here in case you need special
#       options set/compiled in

# for now:  32-bit *only*, 32/64-bit can be added on request

%include Solaris.inc
%include osdistro.inc
%define cc_is_gcc 1

#avoid ovelapping with SUNWhea and SUNWman
%include usr-gnu.inc
%include base.inc
%include pkgbuild-features.inc

# usr-gnu.inc sets _sysconfdir to /etc/gnu but base.inc resets this to /etc if run after usr-gnu.inc
%define _sysconfdir /etc/%{_subdir}

%define src_name openldap


Name:                    SFEopenldap-gnu
IPS_package_name:	sfe/library/gnu/openldap
Group:			System/Services
Summary:                 OpenLDAP - LDAP Server, Tools and Libraries (/usr/gnu)
URL:                     http://www.openldap.org
Version:                 2.4.48
Source:                  http://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source2:		ldap-olslapd.xml
Source3:		openldap-exec_attr
Source4:		openldap-prof_attr
SUNW_Copyright:		 openldap.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

##TODOä## make (Build)Requires complete
BuildRequires:   SFEbdb
Requires:        SFEbdb
#BuildRequires:   SFEgcc
#Requires:        SFEgcc-runtime

#if not using usr-gnu.inc, then
#Conflicts: SUNWopenldap,SUNWopenldapu,SUNWopenldapr

Requires: %name-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /



#START automatic renamed package  (remember %actions)
# create automatic package with old name and "renamed=true" in it
%include pkg-renamed.inc

#STRONG NOTE:
#remember to set in this spec file the %action which
#adds the depend rule in a way that the new package 
#depends on the old package in a slightly updated branch
#version and has the flag "renamed=true" in it

%package 1ni
#if oldname is same as the "Name:"-tag in this spec file:
#example_ab# %define renamed_from_oldname      %{name}
#example_ab# %define renamed_from_oldname      SFEstoneoldpkgname
#
#example_a#  %define renamed_to_newnameversion category/newpackagename = *
#or
#example_b#  %define renamed_to_newnameversion category/newpackagename >= 1.1.1
#
#do not omit version equation!
%define renamed_from_oldname      SFEopenldap
%define renamed_to_newnameversion sfe/library/gnu/openldap = *
%include pkg-renamed-package.inc

%package 2ni
%define renamed_from_oldname      SFEopenldap-root
%define renamed_to_newnameversion sfe/library/gnu/openldap = *
%include pkg-renamed-package.inc

##TODO##
##TODO## %define NEED_IPS_NAME_AS_INPUT_HERE_renamed_from_oldname      sfe/library/openldap
##TODO## example problem: pkgbuild: failed to create file /localhomes/tom/packages/PKGMAPS/pkginfo/sfe/library/openldap.pkginfo



#example# %package %{name}-2-noinst
#example# #add more and different old names here (increment the counter at the end)
#example# %define renamed_from_oldname      SFEstoneoldpkgname
#example# %define renamed_to_newnameversion terminal/urxvt >= 1.23
#example# %include pkg-renamed-package.inc

#END automatic renamed package

%description
OpenLDAP Server, Tools and Libraries
Replaces distro provided LDAP Server package


%prep
%setup -q -n %{src_name}-%version

cp -p %{SOURCE2}  ldap-olslapd.xml
cp -p %{SOURCE3}  openldap-exec_attr
cp -p %{SOURCE4}  openldap-prof_attr

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#we use SFEbdb

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I%{gnu_inc} -D_POSIX_PTHREAD_SEMANTICS"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc} -D_POSIX_PTHREAD_SEMANTICS"
export CPPFLAGS=${CXXFLAGS}
export LDFLAGS="%_ldflags %{gnu_lib_path}"

export RUNDIR="%{_std_localstatedir}/run/%{src_name}"

#if gcc defauls to 64-bit but we need a 3-2bit build, then we workaround
#building slapdS.c where the Makefile leaves out the CFLAGS, result is ELF bittness error
echo "${CFLAGS}" | grep -- "-m32" && export CC="${CC} -m32"
echo "${CFLAGS}" | grep -- "-m64" && export CC="${CC} -m64"

#note: at the moment %install section moves binaries from %{_bindir} over to %{gnu_bin}
#note: at the moment %install section moves one library from %{_libdir} over to %{gnu_lib}
./configure --prefix=%{_prefix}				\
            --libexecdir=%{_libexecdir}			\
            --sysconfdir=%{_sysconfdir}			\
            --localstatedir=%{_localstatedir}/%{src_name}\
            --enable-wrappers		\
            --enable-modules \
            --enable-bdb=mod \
            --enable-hdb=mod \
            --disable-static

##TODO## choose options, add (Build)Requires and then remove the comments below
#    --enable-dynacl	  enable run-time loadable ACL support (experimental) [no]
#    --enable-aci	  enable per-object ACIs (experimental) no|yes|mod [no]
#    --enable-cleartext	  enable cleartext passwords [yes]
#    --enable-crypt	  enable crypt(3) passwords [no]
#    --enable-lmpasswd	  enable LAN Manager passwords [no]
#    --enable-spasswd	  enable (Cyrus) SASL password verification [no]
#    --enable-modules	  enable dynamic module support [no]
#    --enable-rewrite	  enable DN rewriting in back-ldap and rwm overlay [auto]
#    --enable-rlookups	  enable reverse lookups of client hostnames [no]
#    --enable-slapi        enable SLAPI support (experimental) [no]
#    --enable-slp          enable SLPv2 support [no]
#    --enable-wrappers	  enable tcp wrapper support [no]

#SLAPD Backend Options:
#    --enable-backends	  enable all available backends no|yes|mod
#    --enable-bdb	  enable Berkeley DB backend no|yes|mod [yes]
#    --enable-dnssrv	  enable dnssrv backend no|yes|mod [no]
#    --enable-hdb	  enable Hierarchical DB backend no|yes|mod [yes]
#    --enable-ldap	  enable ldap backend no|yes|mod [no]
#    --enable-meta	  enable metadirectory backend no|yes|mod [no]
#    --enable-monitor	  enable monitor backend no|yes|mod [yes]
#    --enable-ndb	  enable MySQL NDB Cluster backend no|yes|mod [no]
#    --enable-null	  enable null backend no|yes|mod [no]
#    --enable-passwd	  enable passwd backend no|yes|mod [no]
#    --enable-perl	  enable perl backend no|yes|mod [no]
#    --enable-relay  	  enable relay backend no|yes|mod [yes]
#    --enable-shell	  enable shell backend no|yes|mod [no]
#    --enable-sock	  enable sock backend no|yes|mod [no]
#    --enable-sql	  enable sql backend no|yes|mod [no]

#SLAPD Overlay Options:
#    --enable-overlays	  enable all available overlays no|yes|mod
#    --enable-accesslog	  In-Directory Access Logging overlay no|yes|mod [no]
#    --enable-auditlog	  Audit Logging overlay no|yes|mod [no]
#    --enable-collect	  Collect overlay no|yes|mod [no]
#    --enable-constraint	  Attribute Constraint overlay no|yes|mod [no]
#    --enable-dds  	  Dynamic Directory Services overlay no|yes|mod [no]
#    --enable-deref	  Dereference overlay no|yes|mod [no]
#    --enable-dyngroup	  Dynamic Group overlay no|yes|mod [no]
#    --enable-dynlist	  Dynamic List overlay no|yes|mod [no]
#    --enable-memberof	  Reverse Group Membership overlay no|yes|mod [no]
#    --enable-ppolicy	  Password Policy overlay no|yes|mod [no]
#    --enable-proxycache	  Proxy Cache overlay no|yes|mod [no]
#    --enable-refint	  Referential Integrity overlay no|yes|mod [no]
#    --enable-retcode	  Return Code testing overlay no|yes|mod [no]
#    --enable-rwm       	  Rewrite/Remap overlay no|yes|mod [no]
#    --enable-seqmod	  Sequential Modify overlay no|yes|mod [no]
#    --enable-sssvlv	  ServerSideSort/VLV overlay no|yes|mod [no]
#    --enable-syncprov	  Syncrepl Provider overlay no|yes|mod [yes]
#    --enable-translucent  Translucent Proxy overlay no|yes|mod [no]
#    --enable-unique       Attribute Uniqueness overlay no|yes|mod [no]
#    --enable-valsort      Value Sorting overlay no|yes|mod [no]


#Optional Packages:
#  --with-PACKAGE[=ARG]    use PACKAGE [ARG=yes]
#  --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
#  --with-subdir=DIR       change default subdirectory used for installs
#  --with-cyrus-sasl	  with Cyrus SASL support [auto]
#  --with-fetch		  with fetch(3) URL support [auto]
#  --with-threads	  with threads [auto]
#  --with-tls		  with TLS/SSL support auto|openssl|gnutls|moznss [auto]
#  --with-yielding-select  with implicitly yielding select [auto]
#  --with-mp               with multiple precision statistics auto|longlong|long|bignum|gmp [auto]
#  --with-odbc             with specific ODBC support iodbc|unixodbc|odbc32|auto [auto]
#  --with-gnu-ld           assume the C compiler uses GNU ld [default=no]
#  --with-pic              try to use only PIC/non-PIC objects [default=use
#                          both]
#  --with-tags[=TAGS]      include additional configurations [automatic]

#adjust, if younger distrelnumber can't run gsoelim
#NPOTE This appears in %build and in %install
%if %( expr %{omnios} '=' 1 '&' %{distrelnumber} '<=' 151014 )
#gsoelim can't find its libstdc++.so.6, as omnios doesn't carry it (only lib-files with full version in the filename)
#try using our runtime. Might break if out gcc version <= omnios gcc version
export LD_LIBRARY_PATH=/usr/gcc-sfe/lib:/usr/gcc/lib
%endif


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

#adjust, if younger distrelnumber can't run gsoelim
#NPOTE This appears in %build and in %install
%if %( expr %{omnios} '=' 1 '&' %{distrelnumber} '<=' 151014 )
#gsoelim can't find its libstdc++.so.6, as omnios doesn't carry it (only lib-files with full version in the filename)
#try using our runtime. Might break if out gcc version <= omnios gcc version
export LD_LIBRARY_PATH=/usr/gcc-sfe/lib:/usr/gcc/lib
%endif

gmake install DESTDIR=$RPM_BUILD_ROOT

[ -d $RPM_BUILD_ROOT%{_datadir}/doc/%{src_name} ] || mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{src_name}
cp [A-Z][A-Z]* $RPM_BUILD_ROOT%{_datadir}/doc/%{src_name}

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network/ldap/
cp ldap-olslapd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/network/ldap/

mkdir -p $RPM_BUILD_ROOT%{_std_sysconfdir}/security/exec_attr.d
mkdir -p $RPM_BUILD_ROOT%{_std_sysconfdir}/security/prof_attr.d
cp  openldap-exec_attr $RPM_BUILD_ROOT%{_std_sysconfdir}/security/exec_attr.d/%{name}
cp  openldap-prof_attr $RPM_BUILD_ROOT%{_std_sysconfdir}/security/prof_attr.d/%{name}

#clean from static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

#relocate a few binaries, relocate one basic client library to usr_gnu
#mkdir -p $RPM_BUILD_ROOT%{gnu_bin}/
#mv $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT/%{gnu_bin}/
#rmdir $RPM_BUILD_ROOT%{_bindir}
#mkdir -p $RPM_BUILD_ROOT%{gnu_lib}/
#mv $RPM_BUILD_ROOT%{_libdir}/libldap.so* $RPM_BUILD_ROOT/%{gnu_lib}/
#not moving, instead remove the symlink (let OS ldap package's symlink in place)
#rm $RPM_BUILD_ROOT%{_libdir}/libldap.so

%clean
rm -rf $RPM_BUILD_ROOT


# automatic uninstall oldpkg on upgrade or on install newpkg

#list *all* old package names here which could be installed on
#user's systems
#stay in sync with section above controlling the "renamed" packages
#SFEopenldap@9.18-5.11,0.0.175.0.0.0.2.1 (note: last digit is incremented calculated
#on the branch version printed by pkg info release/name
%actions
depend fmri=SFEopenldap@%{ips_version_release_renamedbranch} type=optional
#depend fmri=SFEotheroldnamesgohere@%{ips_version_release_renamedbranch} type=optional


%files
%defattr(-, root, bin)
#moved to /usr/gnu/bin
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%dir %attr (0755, root, bin) %{gnu_bin}
#%{gnu_bin}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
#see %install, paused - symlink removed
#%dir %attr (0755, root, bin) %{gnu_lib}
#%{gnu_lib}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files root
%defattr (-, root, bin)
#/etc/gnu/
%dir %attr (0755, root, bin) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{src_name}
%defattr (-, openldap, openldap)
##TODO## do we have user-editable config files? protect them with %config
%{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
#/etc/
%dir %attr (0755, root, sys) %{_std_sysconfdir}
%dir %attr (0755, root, sys) %{_std_sysconfdir}/security
%{_std_sysconfdir}/security/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%defattr (-, openldap, openldap)
%dir %attr (0700, openldap, openldap) %{_localstatedir}/%{src_name}
%{_localstatedir}/%{src_name}/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_std_localstatedir}
%dir %attr (0755, root, sys) %{_std_localstatedir}/svc
%dir %attr (0755, root, sys) %{_std_localstatedir}/svc/manifest
%class(manifest) %attr(0444, root, sys)%{_std_localstatedir}/svc/manifest/network/ldap/ldap-olslapd.xml

%changelog
* Sun Sep 22 2019 - Thomas Wagner
- bump to 2.4.48
- add workaround to build slapdS.c if compiler defaults to 64-bit but we want 32-bit openldap
* Tue Dec 18 2018 - Thomas Wagner
- Testing with: --enable-modules --enable-bdb=mod --enable-hdb=mod as suggested in https://www.illumos.org/issues/10069
* Sun Dec 10 2017 - Thomas Wagner
- bump to 2.4.45
- add -D_POSIX_PTHREAD_SEMANTICS or get error wrong number of arguments to sigwait
* Thu Dec  1 2016 - Thomas Wagner
- add workaround to find gcc runtime for "gsoelim" (called in %install by gmake install) (OM <= 151014)
* Mon Nov 21 2016 - Thomas Wagner
- bump to 2.4.44
* Tue Sep 20 2016 - pjama
- hard set _sysconfdir to /etc/gnu because base.inc run after usr-gnu.inc overwrites _sysconfdir to be /etc and breaks %files paths
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Fri Jan 16 2015 - Thomas Wagner
- add IPS_Package_Name and Group
- Name / IPS_Package_Name add "gnu" to indicate install location in /usr/gnu/
* Mon Dec 15 2014 - Thomas Wagner
- bump to 2.4.40
* Tue Jan 21 2014 - Thomas Wagner
- bump to 2.4.38
- remove typo in CXXLAGS -> CXXFLAGS (no finds right BDB db.h in %{gnu_inc}, export CPPFLAGS=${CXXFLAGS}
- remove depenency on %name in package %name-root
* Sat Oct  8 2011 - Thomas Wagner
- add SMF manifest (copied from distro, modified), add security/ RBAC info (copied from distro, modified)
* Fri Oct  7 2011 - Thomas Wagner
- Initial spec
