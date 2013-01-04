#
# spec file for package SFEphp
#
# includes module(s): php
#

# SFE-webstack

%include Solaris.inc
%include packagenamemacros.inc

%define php_version   5.4
##not defined%define php_major_version   5
%define php_major_minor_version   5.4
%define php_major_minor_micro_version 5.4.10


Name:                    SFEphp54
IPS_package_name:	 web/php-54
Summary:                 php - Hypertext Preprocessor - general-purpose scripting language for Web development
Version:                 %{php_major_minor_micro_version}
Source:                  http://www.php.net/distributions/php-%{version}.tar.bz2
URL:                     http://www.php.net/
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#fetch this platform default apache2 version
BuildRequires: %{pnm_buildrequires_apache2_default}
Requires:      %{pnm_requires_apache2_default}
BuildRequires: %{pnm_buildrequires_SUNWgnu_gettext_devel}
##TODO##
#is at runtime gnu_gettext really required?
Requires:      %{pnm_requires_SUNWgnu_gettext}
#fetch SUNWpostgr-84-devel
BuildRequires: %{pnm_buildrequires_postgres_default}
#fetch SUNWpostgr-84-libs
Requires:      %{pnm_requires_postgres_default}


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -c -n php-%version
cp -pr php-%version php-%{version}-fastcgi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig:$PKG_CONFIG_PATH
export CFLAGS="%optflags -I %{gnu_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

#	PHP_PEAR_CACHE_DIR=/var/tmp/pear/cache \
#	PHP_PEAR_DOWNLOAD_DIR=/var/tmp/pear/cache \
#	PHP_PEAR_EXTENSION_DIR=/var/php/$(PHP_REL)/modules \
#	PHP_PEAR_INSTALL_DIR=/var/php/$(PHP_REL)/pear \
#	PHP_PEAR_SIG_BIN=/usr/gnu/bin/gpg \

PHP_REL=%{php_major_minor_version}
TOP_DIR=%{_prefix}/php/%{php_major_minor_version}
MODULES_DIR=%{_prefix}/php/%{php_major_minor_version}/modules
CONF_DIR=/etc/php/${PHP_REL}
MODULES_CONF_DIR=${CONF_DIR}/conf.d
PEAR_DIR=/var/php/${PHP_REL}/pear
SAMPLES_DIR=%{_prefix}/php/%{php_major_minor_version}/samples

cd php-%{version}-fastcgi
#NOTE: the following variables are ENV variables to configure
PHP_PEAR_CACHE_DIR=/var/tmp/pear/cache \
PHP_PEAR_DOWNLOAD_DIR=/var/tmp/pear/cache \
PHP_PEAR_EXTENSION_DIR=/var/php/${PHP_REL}/modules \
PHP_PEAR_INSTALL_DIR=/var/php/${PHP_REL}/pear \
PHP_PEAR_SIG_BIN=/usr/gnu/bin/gpg \
PHP_LIBXML_DIR=/usr/gnu \
./configure --prefix=%{_prefix}/php/%{php_major_minor_version} \
	    --bindir=%{_prefix}/php/%{php_major_minor_version}/bin \
	    --sbindir=%{_prefix}/php/%{php_major_minor_version}/sbin \
	    --datadir=%{_prefix}/php/%{php_major_minor_version}/share \
            --localstatedir=%{_localstatedir}/php \
            --libexecdir=%{_prefix}/php/%{php_major_minor_version}/modules \
            --mandir=%{_prefix}/php/%{php_major_minor_version}/man \
            --oldincludedir=%{_prefix}/php/%{php_major_minor_version}/share \
	    --sysconfdir=%{_sysconfdir}/php/%{php_major_minor_version} \
	    --with-config-file-path=${CONF_DIR} \
	    --with-config-file-scan-dir=${MODULES_CONF_DIR} \
	    --enable-fastcgi                    \
	    --enable-pdo=shared \
	    --with-bz2                          \
	    --with-zlib                         \
	    --enable-mbstring                   \
	    --with-gettext=/usr/gnu             \
	    --with-layout=PHP \
	    --with-pear=${PEAR_DIR} \
            --with-pdo-pgsql=shared,%{_prefix}/%{postgres_default_prefix} \
            --with-pgsql=shared,%{_prefix}/%{postgres_default_prefix} \
	    --with-sqlite=shared \
            --with-pdo-sqlite=shared \
            --enable-sqlite-utf8 \
            --disable-static \
            --with-cdb \
	    --with-freetype \
	    --with-jpeg \
	    --with-kerberos \
	    --with-mcrypt=shared \
	    --with-pcre \
	    --with-pcre-regex \
	    --with-png \
	    --with-xmlrpc \
	    --with-xpm \
	    --with-xsl \
	    --enable-discard-path \
	    --enable-ftp=shared \
	    --with-curl \
	    --with-curlwrappers \
	    --with-gd=shared \
	    --with-iconv \
	    --with-ldap=shared \

#	    --datadir=%{_datadir}		\
#	    --mandir=%{_mandir}			\
#	    --libexec=%{_libexecdir}		\
#	    --sysconfdir=%{_sysconfdir}		\


gmake -j$CPUS
cd ..

cd php-%version
#NOTE: the following variables are ENV variables to configure
PHP_PEAR_CACHE_DIR=/var/tmp/pear/cache \
PHP_PEAR_DOWNLOAD_DIR=/var/tmp/pear/cache \
PHP_PEAR_EXTENSION_DIR=/var/php/${PHP_REL}/modules \
PHP_PEAR_INSTALL_DIR=/var/php/${PHP_REL}/pear \
PHP_PEAR_SIG_BIN=/usr/gnu/bin/gpg \
PHP_LIBXML_DIR=/usr/gnu \
./configure --prefix=%{_prefix}/php/%{php_major_minor_version} \
	    --bindir=%{_prefix}/php/%{php_major_minor_version}/bin \
	    --sbindir=%{_prefix}/php/%{php_major_minor_version}/sbin \
	    --datadir=%{_prefix}/php/%{php_major_minor_version}/share \
            --localstatedir=%{_localstatedir}/php \
            --libexecdir=%{_prefix}/php/%{php_major_minor_version}/modules \
            --mandir=%{_prefix}/php/%{php_major_minor_version}/man \
            --oldincludedir=%{_prefix}/php/%{php_major_minor_version}/share \
	    --sysconfdir=%{_sysconfdir}/php/%{php_major_minor_version} \
	    --with-config-file-path=${CONF_DIR} \
	    --with-config-file-scan-dir=${MODULES_CONF_DIR} \
	    --enable-fastcgi                    \
	    --enable-pdo=shared \
	    --with-bz2                          \
	    --with-zlib                         \
	    --enable-mbstring                   \
	    --with-gettext=/usr/gnu             \
	    --with-layout=PHP \
	--with-pear=${PEAR_DIR} \
            --with-pdo-pgsql=shared,%{_prefix}/%{postgres_default_prefix} \
            --with-pgsql=shared,%{_prefix}/%{postgres_default_prefix} \
	    --with-sqlite=shared \
            --with-pdo-sqlite=shared \
            --enable-sqlite-utf8 \
            --with-apxs2=%{_prefix}/%{apache2_default_apxs} \
            --disable-static \
            --with-cdb \
	    --with-freetype \
	    --with-jpeg \
	    --with-kerberos \
	    --with-mcrypt=shared \
	    --with-pcre \
	    --with-pcre-regex \
	    --with-png \
	    --with-xmlrpc \
	    --with-xpm \
	    --with-xsl \
	    --enable-discard-path \
	    --enable-ftp=shared \
	    --with-curl \
	    --with-curlwrappers \
	    --with-gd=shared \
	    --with-iconv \
	    --with-ldap=shared \


##TODO##	    ## --with-imap \ --with-imap=shared,/builds2/sfwnv-gate/usr/src/cmd/php5/imap-2007e --with-imap-ssl=shared,/builds2/sfwnv-gate/proto/root_i386/usr

          

#TODO#
#--with-freetype-dir=/usr/sfw --with-jpeg-dir=/usr --with-kerberos --with-mcrypt=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-pcre-dir=/builds2/sfwnv-gate/proto/root_i386/usr --with-pcre-regex --with-png-dir=/usr --with-xmlrpc --with-xpm-dir=/usr/openwin --with-xsl --with-zend-vm=CALL
	    ## --with-zend-vm=CALL \
#--with-iconv=shared --with-imap=shared,/builds2/sfwnv-gate/usr/src/cmd/php5/imap-2007e --with-imap-ssl=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-ldap=shared 


#	    --datadir=%{_datadir}		\
#	    --mandir=%{_mandir}			\
#	    --libexec=%{_libexecdir}		\
#	    --sysconfdir=%{_sysconfdir}		\
#cp .libs/libphp5.lai /var/tmp/pkgbuild-tom/SFEphp54-5.4.8-build/usr/apache2/2.2/libexec/libphp5.la
#libtool: install: warning: remember to run `libtool --finish /localhomes/tom/packages/BUILD/php-5.4.8/php-5.4.8/libs'
#chmod 755 /var/tmp/pkgbuild-tom/SFEphp54-5.4.8-build/usr/apache2/2.2/libexec/libphp5.so
#apxs:Error: Config file /var/tmp/pkgbuild-tom/SFEphp54-5.4.8-build/etc/apache2/2.2/conf.d/modules-32.load not found.
#make: *** [install-sapi] Error 1


#build pgsql in a separate module

#http://blog.experimentalworks.net/2012/05/canonical-way-to-build-php-5-4-on-solaris-11/
gsed -i.bak 's,\-mt,,' Makefile
gsed -i.bak 's,\-i \-a \-n php5 libphp5\.la,-i -n php5 libphp5.la,' Makefile

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

# Create a dummy httpd.conf that apxs will populate.
mkdir -p $RPM_BUILD_ROOT/etc/apache2/%{apache2_version}
echo >${RPM_BUILD_ROOT}/etc/apache2/%{apache2_version}/httpd.conf
echo "LoadModule /usr/dummy.so" >>${RPM_BUILD_ROOT}/etc/apache2/%{apache2_version}/httpd.conf

cd php-%version
make install INSTALL_ROOT=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/php/%{php_major_minor_version}/
cp php.ini-production $RPM_BUILD_ROOT/etc/php/%{php_major_minor_version}/php.ini

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/php/%{php_major_minor_version}/sessions

# Remove the dummy line and rename the file.
awk '!/dummy/ {print}' ${RPM_BUILD_ROOT}/etc/apache2/%{apache2_version}/httpd.conf > ${RPM_BUILD_ROOT}/etc/apache2/%{apache2_version}/httpd-php.conf
# Remove the generated files.
rm ${RPM_BUILD_ROOT}/etc/apache2/%{apache2_version}/httpd.conf*

# Remove files and dirs that should probably be re-generated on the destination
# machine and not simply installed.
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/php/%{php_major_minor_version}/pear.conf
rm -r ${RPM_BUILD_ROOT}/.registry
rm -r ${RPM_BUILD_ROOT}/.channels
rm -r ${RPM_BUILD_ROOT}/.filemap
rm -r ${RPM_BUILD_ROOT}/.lock
rm -r ${RPM_BUILD_ROOT}/.depdblock
rm -r ${RPM_BUILD_ROOT}/.depdb


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) /usr
#%{_prefix}/php/%{php_major_minor_version}/.*
%{_prefix}/php/%{php_major_minor_version}/*
%{_prefix}/apache2/*

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
##%dir %attr (0755, root, bin) %{_localstatedir}/php/%{php_major_minor_version}/pear
##%{_localstatedir}/php/%{php_major_minor_version}/pear
%{_localstatedir}/php/%{php_major_minor_version}/pear
####TODO## look if those files are really necessary or can be re-generated
##%{_localstatedir}/php/%{php_major_minor_version}/pear/.*
%dir %attr (0755, webservd, bin) %{_localstatedir}/php/%{php_major_minor_version}/sessions

%files root
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/apache2
%{_sysconfdir}/php

%changelog

/var/sadm/pkg/SUNWphp52d/save/pspool/SUNWphp52d/pkgmap:1 d none usr 0755 root sys
/var/sadm/pkg/SUNWphp52d/save/pspool/SUNWphp52d/pkgmap:1 d none usr/php 0755 root bin
/var/sadm/pkg/SUNWphp52d/save/pspool/SUNWphp52d/pkgmap:1 d none usr/php/5.2 0755 root bin
/var/sadm/pkg/SUNWphp52d/save/pspool/SUNWphp52d/pkgmap:1 d none usr/php/5.2/doc 0755 root bin
/var/sadm/pkg/SUNWphp52d/save/pspool/SUNWphp52d/pkgmap:1 d none usr/php/5.2/doc/html 0755 root bin
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none etc 0755 root sys
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none etc/php 0755 root bin
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none etc/php/5.2 0755 root bin
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none etc/php/5.2/conf.d 0755 root bin
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none var 0755 root sys
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none var/php 0755 root bin
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none var/php/5.2 0755 root bin
/var/sadm/pkg/SUNWphp52r/save/pspool/SUNWphp52r/pkgmap:1 d none var/php/5.2/sessions 0750 webservd bin

                              /usr/php/5.2/bin/php-config
Usage: /usr/php/5.2/bin/php-config [OPTION]
Options:
  --prefix            [/usr/php/5.2]
  --includes          [-I/usr/php/5.2/include/php -I/usr/php/5.2/include/php/main -I/usr/php/5.2/include/php/TSRM -I/usr/php/5.2/include/php/Zend -I/usr/php/5.2/include/php/ext -I/usr/php/5.2/include/php/ext/date/lib]
  --ldflags           [ -L/usr/ucblib]
  --libs              [
           -lcrypt   -lz 
             -lexslt   
             -lresolv 
            -lm -lsocket -lnsl 
             -ldl 
            -lposix4 
               -lxml2 -lz -lm -lsocket -lnsl 
            -lxslt 
  --extension-dir     [/usr/php/5.2/modules]
  --include-dir       [/usr/php/5.2/include/php]
  --php-binary        [/usr/php/5.2/bin/php]
  --php-sapis         [cli apache2handler]
  --configure-options [--bindir=/usr/php/5.2/bin --datadir=/usr/php/5.2/share 
--enable-bcmath --enable-calendar --enable-ctype --enable-cli --enable-dom --enable-dtrace --enable-exif --enable-flatfile --enable-filter --enable-gd-jis-conv --enable-gd-native-ttf --enable-hash --enable-inifile --enable-ipv6 --enable-json --enable-magic-quotes --enable-mbregex --enable-mbstring --enable-mod-charset --enable-pcntl --enable-posix --enable-reflection --with-libxml-dir=/usr --enable-libxml --enable-sqlite-utf8 --enable-session --enable-shared --enable-shmop --enable-short-tags --enable-simplexml --enable-soap --enable-sockets --enable-spl --enable-sysvmsg --enable-sysvsem --enable-sysvshm --enable-tokenizer --enable-xml --enable-xmlreader --enable-xmlwriter --enable-zend-multibyte --enable-zip --exec-prefix=/usr/php/5.2 --includedir=/usr/php/5.2/include --libdir=/usr/php/5.2/lib --libexecdir=/usr/php/5.2/modules --mandir=/usr/php/5.2/man --oldincludedir=/usr/php/5.2/share --prefix=/usr/php/5.2 --sbindir=/usr/php/5.2/sbin --sysconfdir=/etc/php/5.2 --with-cdb --with-config-file-path=/etc/php/5.2 --with-config-file-scan-dir=/etc/php/5.2/conf.d --with-exec-dir=/usr/php/5.2/bin --with-freetype-dir=/usr/sfw --with-jpeg-dir=/usr --with-kerberos --with-layout=PHP --with-mcrypt=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-pcre-dir=/builds2/sfwnv-gate/proto/root_i386/usr --with-pcre-regex --with-png-dir=/usr --with-xmlrpc --with-xpm-dir=/usr/openwin --with-xsl --with-zend-vm=CALL 
--enable-discard-path --enable-ftp=shared --enable-pdo=shared --with-apxs2=/builds2/sfwnv-gate/proto/root_i386/usr/apache2/2.2/bin/apxs --with-bz2=shared --with-curl=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-curlwrappers --with-gd=shared --with-gettext=shared --with-iconv=shared --with-imap=shared,/builds2/sfwnv-gate/usr/src/cmd/php5/imap-2007e --with-imap-ssl=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-ldap=shared --with-mysql=shared,/builds2/sfwnv-gate/proto/root_i386/usr/mysql/5.1 --with-mysql-sock=/tmp/mysql.sock --with-mysqli=shared,/builds2/sfwnv-gate/proto/root_i386/usr/mysql/5.1/bin/mysql_config --with-openssl=shared --with-pear=/var/php/5.2/pear --with-pdo-mysql=shared,/builds2/sfwnv-gate/proto/root_i386/usr/mysql/5.1 --with-pdo-pgsql=shared,/builds2/sfwnv-gate/proto/root_i386/usr/postgres/8.3 --with-pdo-sqlite=shared --with-pgsql=shared,/builds2/sfwnv-gate/proto/root_i386/usr/postgres/8.3 --with-snmp=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-sqlite=shared --with-tidy=shared,/builds2/sfwnv-gate/proto/root_i386/usr --with-zlib=shared 

--disable-cgi --disable-fastcgi 
--disable-dbase --disable-debug --disable-dmalloc --disable-inline-optimization --disable-libgcc --disable-libtool-lock --disable-rpath --disable-static 
--without-dbm --without-t1lib 
--without-tsrm-pthreads]
  --version           [5.2.11]
  --vernum            [50211]

VON ZWISCHENDURCH:
 ~/packages/PKGS/SFEphp54/reloc/usr/php/5.4/bin ./php-config 
Usage: ./php-config [OPTION]
Options:
  --prefix            [/usr/php/5.4]
  --includes          [-I/usr/php/5.4/include/php -I/usr/php/5.4/include/php/main -I/usr/php/5.4/include/php/TSRM -I/usr/php/5.4/include/php/Zend -I/usr/php/5.4/include/php/ext -I/usr/php/5.4/include/php/ext/date/lib]
  --ldflags           [ -L/usr/ucblib]
  --libs              [  -lresolv -lrt -lintl -lbz2 -lz -lrt -lm -lnsl -lsocket  -lxml2 -lz -lm -lsocket -lnsl -lxml2 -lz -lm -lsocket -lnsl -lxml2 -lz -lm -lsocket -lnsl -lxml2 -lz -lm -lsocket -lnsl -lxml2 -lz -lm -lsocket -lnsl -lxml2 -lz -lm -lsocket -lnsl ]
  --extension-dir     [/usr/php/5.4/lib/php/extensions/no-debug-non-zts-20100525]
  --include-dir       [/usr/php/5.4/include/php]
  --man-dir           [/usr/php/5.4/man]
  --php-binary        [/usr/php/5.4/bin/php]
  --php-sapis         [ apache2handler cli cgi]
  --configure-options [--prefix=/usr/php/5.4 --bindir=/usr/php/5.4/bin --sbindir=/usr/php/5.4/sbin --datadir=/usr/php/5.4/share --localstatedir=/var/php --libexecdir=/usr/php/5.4/modules --mandir=/usr/php/5.4/man --oldincludedir=/usr/php/5.4/share --sysconfdir=/etc/php/5.4 --with-config-file-path=/etc/php/5.4 --with-config-file-scan-dir=/etc/php/5.4/conf.d --enable-fastcgi --with-bz2 --with-zlib --enable-mbstring --with-gettext=/usr/gnu --with-layout=PHP --with-pear= --with-pdo-pgsql=shared,/usr/postgres/8.4 --with-sqlite=shared --with-apxs2=/usr/apache2/2.2/bin/apxs]
  --version           [5.4.10]
  --vernum            [50410]


* Tue Jan  1 2013 - Thomas Wagner
- bump to 5.4.10

