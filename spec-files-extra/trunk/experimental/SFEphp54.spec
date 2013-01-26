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
%define php_major_minor_micro_version 5.4.11

#1 use xml2 from gnu location in new version, 0 use system supplied xml2
%define usexml2gnu 1


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
%if %{usexml2gnu}
BuildRequires: SFElxml-gnu
Requires:      SFElxml-gnu
%endif
BuildRequires: SFEgmp
Requires:      SFEgmp
BuildRequires: SFEre2c
Requires:      SFEre2c


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -c -n php-%version
cp -pr php-%version php-%{version}-fastcgi

#do not run apxs with -a (it would try to install/activate the module instantly)
gsed -i.bak1 -e 's#APXS -i -a -n php5#APXS -i -n php5#' php-%version*/configure

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig:$PKG_CONFIG_PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
export CFLAGS="$CFLAGS -I %{gnu_inc}"
export LDFLAGS="$LDFLAGS %{gnu_lib_path} -liconv -lxml2"

#from OS Makefile (php5.2)
#export CFLAGS="$CFLAGS -xjobs=16 -fsimple=2 -xnorunpath -xO4 -xalias_level=basic -xipo=0"
export CFLAGS="$CFLAGS -xjobs=16 -fsimple=2 -xO4 -xalias_level=basic -xipo=0"
export CFLAGS="$CFLAGS -xlibmopt -xprefetch_level=1 -xprefetch=auto -xstrconst -zlazyload"
export LDFLAGS="$LDFLAGS -xlibmopt -xprefetch_level=1 -xprefetch=auto -xstrconst -zlazyload -liconv"

#maybe not necessary to find the mysql libs? export LDFLAGS="$LDFLAGS -L%{_prefix}/%{mysql_default_libdir}"

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

#find libtool from our own build directory, not from the OS (oi libtool tried /usr/ucb/echo, not installed by default)
PATHSAVED=$PATH
export PATH=`pwd`:$PATHSAVED

###TODO### check obsolete/misspelled/wrong options:
#configure: WARNING: unrecognized options: --enable-fastcgi, --with-sqlite, --enable-sqlite-utf8, --with-freetype, --with-jpeg, --with-pcre, --with-png, --with-libxml, --with-xpm, --enable-discard-path

#NOTE: the following variables are ENV variables to configure
PHP_PEAR_CACHE_DIR=/var/tmp/pear/cache \
PHP_PEAR_DOWNLOAD_DIR=/var/tmp/pear/cache \
PHP_PEAR_EXTENSION_DIR=/var/php/${PHP_REL}/modules \
PHP_PEAR_INSTALL_DIR=/var/php/${PHP_REL}/pear \
PHP_PEAR_SIG_BIN=/usr/gnu/bin/gpg \
%if %{usexml2gnu}
PHP_LIBXML_DIR=/usr/gnu \
%endif
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
	    --with-mysql=shared,%{_prefix}/%{mysql_default_prefix} \
	    --with-mysql-sock=/tmp/mysql.sock \
	    --with-mysqli=shared,%{_prefix}/%{mysql_default_prefix}/bin/mysql_config \
	    --with-pear=${PEAR_DIR} \
	    --with-pdo-mysql=shared,%{_prefix}/%{mysql_default_prefix} \
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
%if %{usexml2gnu}
            --with-libxml-dir=/usr/gnu/%{base_isa} \
%endif
            --with-libxml \
	    --with-xmlrpc \
	    --with-xpm \
	    --with-xsl \
	    --enable-discard-path \
	    --enable-ftp=shared \
	    --with-curl \
	    --with-curlwrappers \
	    --with-gd=shared \
	    --with-iconv \
	    --with-iconv-dir=/usr/gnu \
	    --with-ldap=shared \
            --with-openssl=shared \
            --enable-bcmath \
            --with-gmp=/usr/gnu \

gmake -j$CPUS
cd ..

cd php-%version
#find libtool from our own build directory, not from the OS (oi libtool tried /usr/ucb/echo, not installed by default)
export PATH=`pwd`:$PATHSAVED

#NOTE: the following variables are ENV variables to configure
PHP_PEAR_CACHE_DIR=/var/tmp/pear/cache \
PHP_PEAR_DOWNLOAD_DIR=/var/tmp/pear/cache \
PHP_PEAR_EXTENSION_DIR=/var/php/${PHP_REL}/modules \
PHP_PEAR_INSTALL_DIR=/var/php/${PHP_REL}/pear \
PHP_PEAR_SIG_BIN=/usr/gnu/bin/gpg \
%if %{usexml2gnu}
PHP_LIBXML_DIR=/usr/gnu \
%endif
##TODO## disable-fastcgi disable-cgi ... siehe php 5.2 makefiles
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
	    --with-mysql=shared,%{_prefix}/%{mysql_default_prefix} \
	    --with-mysql-sock=/tmp/mysql.sock \
	    --with-mysqli=shared,%{_prefix}/%{mysql_default_prefix}/bin/mysql_config \
	    --with-pear=${PEAR_DIR} \
	    --with-pdo-mysql=shared,%{_prefix}/%{mysql_default_prefix} \
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
%if %{usexml2gnu}
            --with-libxml-dir=/usr/gnu/%{base_isa} \
%endif
            --with-libxml \
	    --with-xmlrpc \
	    --with-xpm \
	    --with-xsl \
	    --enable-discard-path \
	    --enable-ftp=shared \
	    --with-curl \
	    --with-curlwrappers \
	    --with-gd=shared \
	    --with-iconv \
	    --with-iconv-dir=/usr/gnu \
	    --with-ldap=shared \
            --with-openssl=shared \
            --enable-bcmath \
            --with-gmp=/usr/gnu \



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
#find libtool from our own build directory, not from the OS (oi libtool tried /usr/ucb/echo, not installed by default)
PATHSAVED=$PATH
export PATH=`pwd`:$PATHSAVED

make install INSTALL_ROOT=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/php/%{php_major_minor_version}/
cp php.ini-production $RPM_BUILD_ROOT/etc/php/%{php_major_minor_version}/php.ini

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/php/%{php_major_minor_version}/sessions
mkdir -p $RPM_BUILD_ROOT/etc/php/%{php_major_minor_version}/conf.d

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

#create simple default config files for the modules delivered
EXTDIR=`${RPM_BUILD_ROOT}/%{_prefix}/php/%{php_major_minor_version}/bin/php-config --extension-dir`

for MODULE in `cd ${RPM_BUILD_ROOT}/$EXTDIR && find . -type f -name \*so`
 do
 MODULESOFILE=$( basename $MODULE )
 MODULEINIFILE=$( echo $MODULESOFILE | sed -e 's?\.so?.ini?' )
 echo "creating module ini file $MODULEINIFILE for module $MODULESOFILE"
 echo "extension=$MODULESOFILE" > $RPM_BUILD_ROOT/etc/php/%{php_major_minor_version}/conf.d/$MODULEINIFILE
done # MODULE


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) /usr
#%{_prefix}/php/%{php_major_minor_version}/.*
%{_prefix}/php/%{php_major_minor_version}/*
%{_prefix}/apache2/*

%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_docdir}
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
changelog incomplete, under development, stay tuned
open: check imap client
open: modify lib name libphp5.so and make it mod_php5.4.so
open: add notes in description for how to activate this php5.4 in apache2
* Sat Jan 26 2013 - Thomas Wagner
- add (Build)Requires: SFEre2c
- remove -xnorunpath from CFLAGS, add LDFLAGS similar to the ones from php 5.2 in ON
- make PATH search for libtool in our build directory (not find OS provided libtool on OI)
- generate /etc/php/5.4/conf.g/<modulename>.ini and by default enable all modules compiled
  fixed finding modules
- add mysql
* Fri Jan 18 2013 - Thomas Wagner
- bump to 5.4.11
* Thu Jan 10 2013 - Thomas Wagner
- add --with-openssl=shared to get smtp encrypted transfers
* Tue Jan  1 2013 - Thomas Wagner
- bump to 5.4.10

