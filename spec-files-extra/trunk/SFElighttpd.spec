##TODO## mkdir -p /var/lighttpd/1.4/logs
##TODO##  537  sudo chown webservd:webservd /var/lighttpd/1.4/logs


#
# Copyright (c) 2011 Oracle Corporation
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%define _gpp g++
%include base.inc

Name:                SFElighttpd
Summary:             Lighttpd Web Server
IPS_package_name:    sfe/web/server/lighttpd-14
Version:             1.4.48
Source:              http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-%{version}.tar.gz 
Source2:             lighttpd-auth_attr
Source3:             lighttpd-prof_attr
Source4:             lighttpd-fcgi-php.conf
Source5:             lighttpd-http-lighttpd14.xml
Source6:             lighttpd-lighttpd.8.sunman
Source7:             lighttpd-ssl.conf

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Patch1:              lighttpd-01-drop_privileges.patch
Patch2:              lighttpd-02-sslv3-disable.patch
Patch3:              lighttpd-03-lighttpd.conf.patch
Patch4:              lighttpd-04-manpage.patch
Patch8:              lighttpd-08-fix-mysql-sock-location.patch
#onbsolete# Patch20:             lighttpd-20-Bug2752.patch
Patch21:             lighttpd-21-studio.patch
#disabled# Patch22:             lighttpd-22-tests-perlver.patch
Patch31:             lighttpd-31-pollin.patch

#lighttpd-http-lighttpd14.xml
#lighttpd-lighttpd.8.sunman
#lighttpd-prof_attr
#lighttpd-ssl.conf

#checking for PgSQL support... no
#checking for LibDBI support... no



%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWpcre}
Requires: %{pnm_requires_SUNWpcre}

BuildRequires: %{pnm_buildrequires_library_file_monitor_gamin}
Requires: %{pnm_requires_library_file_monitor_gamin}

%prep
%setup -q -n lighttpd-%version

%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch8 -p0
#onbsolete# %patch20 -p0
%patch21 -p0
#disabled# %patch22 -p0
%patch31 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --with-openssl=/usr --with-attr --with-fam --with--gdbm \
            --with-kerberos5 --with-ldap \
--with-memcache \
%if %{omnios}
%else
--with-lua \
            --with-mysql=%{_prefix}/%{mysql_default_prefix}/bin/mysql_config \
%endif
            --without-attr \
	    --with-pcre --with-webdav-locks --with-webdav-props

	    # --with-mysql=/usr/mysql/5.1/bin/mysql_config \

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/mod_*.la

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lighttpd/1.4/logs
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lighttpd/1.4/docroot
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lighttpd/1.4/vhosts
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lighttpd/1.4/cache
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lighttpd/1.4/sockets


ESCAPED_PKG_NAME=$( echo %{ips_package_name} | sed -e 's?/?_?g' )
mkdir -p $RPM_BUILD_ROOT/etc/security/auth_attr.d/
#Source2:             lighttpd-auth_attr
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/security/auth_attr.d/${ESCAPED_PKG_NAME}

mkdir -p $RPM_BUILD_ROOT/etc/security/prof_attr.d/
#Source3:             lighttpd-prof_attr
cp -p  %{SOURCE3} $RPM_BUILD_ROOT/etc/security/prof_attr.d/${ESCAPED_PKG_NAME}

mkdir -p $RPM_BUILD_ROOT/lib/svc/manifest/network
#Source5:             lighttpd-http-lighttpd14.xml
cp -p %{SOURCE5} ${RPM_BUILD_ROOT}/lib/svc/manifest/network/http-lighttpd14.xml

#Source6:             lighttpd-lighttpd.8.sunman
cp -p %{SOURCE6} ${RPM_BUILD_ROOT}%{_mandir}/man8/lighttpd.8.sunman


#populate the config directory (will be tagged "renamenew" in IPS)
TARGETDIR=${RPM_BUILD_ROOT}%{_sysconfdir}/lighttpd/1.4
mkdir -p ${TARGETDIR}
[ -d doc/config/conf.d ] && cp -pr doc/config/conf.d ${TARGETDIR}
cp -p doc/config/lighttpd.conf doc/config/modules.conf  ${TARGETDIR}


#Source4:             lighttpd-fcgi-php.conf
cp -p %{SOURCE4} ${TARGETDIR}/conf.d/lighttpd-fcgi-php.conf 

#Source7:             lighttpd-ssl.conf
cp -p %{SOURCE7} ${TARGETDIR}/conf.d/lighttpd-ssl.conf 


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/lighttpd*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/lighttpd
%{_sbindir}/lighttpd-angel
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mod*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man8/*
%dir %attr (0755, root, sys) /etc/security
%dir %attr (0755, root, sys) /etc/security/auth_attr.d
%attr (0644, root, sys) /etc/security/auth_attr.d/*
%dir %attr (0755, root, sys) /etc/security/prof_attr.d
%attr (0644, root, sys) /etc/security/prof_attr.d/*


%dir %attr (0755, root, sys) /lib/svc/manifest
%dir %attr (0755, root, sys) /lib/svc/manifest/network
%class(manifest) %attr(0444, root, sys)/lib/svc/manifest/network/*.xml

%dir %attr (0700, webservd, webservd) %{_localstatedir}/lighttpd/1.4/logs

%dir %attr (0755, webservd, webservd) %{_localstatedir}/lighttpd/1.4/docroot
%dir %attr (0755, webservd, webservd) %{_localstatedir}/lighttpd/1.4/vhosts
%dir %attr (0755, webservd, webservd) %{_localstatedir}/lighttpd/1.4/cache
%dir %attr (0755, webservd, webservd) %{_localstatedir}/lighttpd/1.4/sockets


%changelog
* Sat Nov 18 2017 - Thomas Wagner
- add (Build)Requires pnm_buildrequires_library_file_monitor_gamin
- add lighttpd.conf modules.conf to package
- add directories logs docroot vhosts cache sockets
* Fri Nov 17 2017 - Thomas Wagner
- change IPS_Package_Name to sfe/web/server/lighttpd-14 (avoid clush with OS consolidation)
* Thu Nov 16 2017 - Thomas Wagner
- bump to 1.4.48
- use pnm_macros for finding mysql_config 
- change (Build)Requires to pnm_buildrequires_SUNWpcre, %include packagenamemacros.inc
- import patches thanks to solaris userland (github)
* Fri Aug  7 2015 - Thomas Wagner
- bump to 1.4.36
* Fri Oct 16 2011 - Ken Mays <kmays2000@gmail.com>
- Updated for MySql 5.1 package.
* Fri Oct 14 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4.29
* Wed May 14 2008 - Ananth Shrinivas <ananth@sun.com>
- Lighty has moved light years ahead. Bump to 1.4.19 
* Sun Mar 04 2007 - Eric Boutilier
- Initial spec
