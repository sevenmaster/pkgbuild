#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include usr-gnu.inc
%include packagenamemacros.inc

#Attention!
%define _prefix %{_basedir}/gnu/squid

Name:                SFEsquid
IPS_Package_Name:    web/proxy/gnu/squid 
Summary:             proxy caching server for web clients (/usr/gnu) - gnutls nettle - basic compile time options only
Version:             3.5.10
Source:              http://www.squid-cache.org/Versions/v3/3.5/squid-%{version}.tar.bz2
Patch1:              patches/squid-01-Makefile.in.diff
Patch2:              patches/squid-02-negotiate_kerberos.diff
Patch3:              patches/squid-03-wno-write-strings.diff
Patch4:              squid-04-ext_time_quota_acl.cc__BIT_TYPES_DEFINED__.diff


##TODO## dependencies aren't complete!

BuildRequires: SFEgnutls
BuildRequires: SFEnettle-gnu


SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
squid proxy cache
this version uses gnutls and nettle

placed in /usr/gnu to let it co-exist with osdistro squid. For testing you may choose ln -s /etc/squid/ /etc/gnu/squid/ and ln -s /var/squid /var/gnu/squid if osdistro squid is off.

designed to co-exist with osdistro provided squid. 
Keep in mind, you can't share the IP-Addres:Port pairs.

confdir: /etc/gnu/squid/
vardir:  /var/gnu/squid/

SMF-Name: site/network/squid:default

%prep
%setup -q -n squid-%version

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++

#vfork -> deprecated -> allow with defined(__EXTENSIONS__)
export CFLAGS="%optflags -I%{gnu_inc} -I/usr/include/kerberosv5 -I/usr/include -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D__EXTENSIONS__"
export CXXFLAGS="%optflags -I%{gnu_inc} -I/usr/include/kerberosv5 -I/usr/include -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D__EXTENSIONS__"
export LDFLAGS="%_ldflags %{gnu_lib_path} -ldb"

#find pod2man
export PATH=/usr/perl5/bin:$PATH

##TODO## try enabling extra features later!
#export CONFIGURE_OPTIONS="--enable-arp-acl
#--enable-storeio='aufs,diskd,ufs'
#--enable-removal-policies='heap,lru'
#--enable-auth-basic='DB,NCSA,NIS,LDAP,PAM,getpwnam,MSNT-multi-domain,POP3,SMB,SMB_LM,SASL'
#--enable-cache-digests
#--enable-carp
#--enable-coss-aio-ops
#--enable-delay-pools
#--enable-auth-digest='file,LDAP'
#--enable-external-acl-helpers='file_userip,unix_group,LDAP_group,wbinfo_group'
#--enable-follow-x-forwarded-for
#--enable-forward-log
#--enable-forw-via-db
#--enable-htcp
#--enable-icmp
#--enable-large-cache-files
#--enable-multicast-miss
#--enable-auth-negotiate='kerberos'
#--enable-auth-ntlm='smb_lm,fake'
#--enable-ntlm-fail-open
#--enable-snmp
#--enable-ssl
#--enable-x-accelerator-vary
#--with-aio
#--with-aufs-threads=8
#--with-build-environment=POSIX_V6_ILP32_OFFBIG
#--with-pthreads
#--without-nettle
#--enable-silent-rules"

export CONFIGURE_OPTIONS="--enable-arp-acl
--enable-cache-digests
--enable-carp
--enable-coss-aio-ops
--enable-delay-pools
--enable-follow-x-forwarded-for
--enable-forward-log
--enable-forw-via-db
--enable-htcp
--enable-icmp
--enable-large-cache-files
--enable-multicast-miss
--enable-snmp
--enable-ssl
--enable-x-accelerator-vary
--with-aio
--with-aufs-threads=8
--with-build-environment=POSIX_V6_ILP32_OFFBIG
--with-pthreads
--enable-silent-rules
--with-gnutls
--with-nettle=/usr/gnu
"

#--disable-arch-native https://bugzilla.redhat.com/show_bug.cgi?id=1173946

#complaining about deprecated vfork in /usr/include/unistd.h line 531
export CONFIGURE_OPTIONS="${CONFIGURE_OPTIONS} --disable-strict-error-checking"

#find gnutls in /usr/gnu
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig:$PKG_CONFIG_PATH

bash ./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --libexecdir=%{_libexecdir} \
            --disable-arch-native \
            --sysconfdir=%{_sysconfdir}/squid \
            --localstatedir=%{_localstatedir}/squid \
            --sharedstatedir=%{_localstatedir}/squid \
            ${CONFIGURE_OPTIONS}

#            --sysconfdir=%{_std_sysconfdir}/squid \
#            --localstatedir=%{_std_localstatedir}/squid \
#            --sharedstatedir=%{_std_localstatedir}/squid \

#'--enable-auth=basic,digest,negotiate,ntlm' '--enable-basic-auth-helpers=DB,NCSA,YP,LDAP,PAM,getpwnam,MSNT,POP3,multi-domain-NTLM,SMB,SASL' '--enable-cache-digests' '--enable-carp' '--enable-coss-aio-ops' '--enable-delay-pools' '--enable-digest-auth-helpers=ldap,password' '--enable-external-acl-helpers=ip_user,unix_group,ldap_group,wbinfo_group' '--enable-follow-x-forwarded-for' '--enable-forward-log' '--enable-forw-via-db' '--enable-htcp' '--enable-icmp' '--enable-large-cache-files' '--enable-multicast-miss' '--enable-negotiate-auth-helpers=squid_kerb_auth' '--enable-ntlm-auth-helpers=SMB,fakeauth,no_check' '--enable-ntlm-fail-open' '--enable-referer-log' '--enable-removal-policies=heap,lru' '--enable-snmp' '--enable-ssl' '--enable-storeio=aufs,coss,diskd,ufs,null' '--enable-useragent-log' '--enable-x-accelerator-vary' '--libexecdir=/usr/squid/libexec' '--localstatedir=/var/squid' '--prefix=/usr/squid' '--sharedstatedir=/var/squid' '--sysconfdir=/etc/squid' '--with-aio' '--with-aufs-threads=8' '--with-large-files' '--with-build-environment=POSIX_V6_ILP32_OFFBIG' '--with-pthreads' 'CC=/opt/SUNWspro.40/SS12/bin/cc' 'CFLAGS= -xO3 -m32 -xchip=pentium -xspace -Xa  -xildoff -xc99=all  -D__BIG_ENDIAN__ -DSOLARIS_11 -I /usr/include/kerberosv5 ' 'LDFLAGS=-R/usr/sfw/lib -L/usr/sfw/lib '



gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}/squid
%{_sysconfdir}/squid/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/squid
%{_localstatedir}/squid/*

%changelog
* Fri Oct 23 2015 - Thomas Wagner
- important: NO openssl, uses gnutls / nettle
- placed in /usr/gnu to let it co-exist with osdistro squid. For testing you may choose ln -s /etc/squid/ /etc/gnu/squid/ and ln -s /var/squid /var/gnu/squid if osdistro squid is off.
- limited compile time options, needs improvement. Basic service works
- bump to 3.5.10
- use patch1/2/3 and SMF method script from userland gate 
- add patch4 squid-04-ext_time_quota_acl.cc__BIT_TYPES_DEFINED__.diff as only db_185.h later defines u_int32_t
* Tue Nov 07 2006 - Eric Boutilier
3 Initial spec
