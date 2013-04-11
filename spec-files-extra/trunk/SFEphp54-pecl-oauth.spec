#
# spec file for package SFEphp-pecl-oauth
#
# includes module(s): php pecl oauth
#
# modeled after https://github.com/remicollet/remirepo/raw/master/php/pecl/php-pecl-oauth/php-pecl-oauth.spec


# SFE-webstack

%include Solaris.inc
%include packagenamemacros.inc

%define php_version   5.4
##not defined %define php_major_version   5
%define php_major_minor_version   5.4
##not defined %define php_major_minor_micro_version 5.4.11

%define pecl_name oauth
%define php_inidir /etc/php/%{php_major_minor_version}/conf.d
%define pecl_xmldir /var/php/%{php_major_minor_version}/pear/.pkgxml

Name:                    SFEphp54-pecl-oauth
IPS_package_name:	 web/php-54/pecl/oauth
Summary:                 php pecl oauth - OAuth 1.0 consumer and provider extension
Version:                 1.2.3
Source:                  http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
URL:                     http://pecl.php.net/package/%{pecl_name}
License:                 BSD
SUNW_Copyright:          %{pecl_name}license.copyright
SUNW_BaseDir:            /
#Patch1:                  php-pecl-oauth-01-oauth-tests.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEphp54
Requires:      SFEphp54

%description
This PHP extension allows you to use OAuth 1.0
OAuth is an authorization protocol built on top of HTTP which allows
applications to securely access data without having to store user-
names and passwords.

This package provides an API for fetching and serving OAuth protected
resources.

%prep
%setup -q -c -n %{pecl_name}-%{version}

#cd %{pecl_name}-%{version}
#%patch1 -p0 -b .tests
#cd ..

gsed -ibak -e 's,CFLAGS="$CFLAGS -Wall -g",,' %{pecl_name}-%{version}/config.m4


cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig:$PKG_CONFIG_PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
export CFLAGS="$CFLAGS -I %{gnu_inc}"
export LDFLAGS="$LDFLAGS %{gnu_lib_path}"

#from OS Makefile (php5.2)
export CFLAGS="$CFLAGS -xjobs=16 -fsimple=2 -xnorunpath -xO4 -xalias_level=basic -xipo=0"
export CFLAGS="$CFLAGS -xlibmopt -xprefetch_level=1 -xprefetch=auto -xstrconst -zlazyload"

PHP_REL=%{php_major_minor_version}
TOP_DIR=%{_prefix}/php/%{php_major_minor_version}
MODULES_DIR=%{_prefix}/php/%{php_major_minor_version}/modules
CONF_DIR=/etc/php/${PHP_REL}
MODULES_CONF_DIR=${CONF_DIR}/conf.d
PEAR_DIR=/var/php/${PHP_REL}/pear
SAMPLES_DIR=%{_prefix}/php/%{php_major_minor_version}/samples

#NOTE: the following variables are ENV variables to configure
PHP_PEAR_CACHE_DIR=/var/tmp/pear/cache \
PHP_PEAR_DOWNLOAD_DIR=/var/tmp/pear/cache \
PHP_PEAR_EXTENSION_DIR=/var/php/${PHP_REL}/modules \
PHP_PEAR_INSTALL_DIR=/var/php/${PHP_REL}/pear \
PHP_PEAR_SIG_BIN=/usr/gnu/bin/gpg \

cd %{pecl_name}-%{version}
$TOP_DIR/bin/phpize
./configure  \
            --with-php-config=%{_prefix}/php/%{php_major_minor_version}/bin/php-config

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

cd %{pecl_name}-%{version}
make install INSTALL_ROOT=%{buildroot}
cd ..
# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

#rm ${RPM_BUILD_ROOT}%{_sysconfdir}/php/%{php_major_minor_version}/pear.conf

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/php%{php_version}-%{pecl_name}-%{version}
cp -pr %{pecl_name}-%{version}/examples ${RPM_BUILD_ROOT}%{_docdir}/php%{php_version}-%{pecl_name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%doc %{pecl_name}-%{version}/{README,ChangeLog}
%dir %attr (0755, root, sys) %{_prefix}
%{_prefix}/php/%{php_major_minor_version}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/php%{php_version}-%{pecl_name}-%{version}/*

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/php/%{php_major_minor_version}/pear/.pkgxml/*

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/php/%{php_major_minor_version}/conf.d/%{pecl_name}.ini

%changelog
* Tue Feb 19 2013 - Thomas Wagner
- initial spec
