#
# spec file for package SFEphp-pecl-geoip
#
# includes module(s): php pecl geoip
#
# modeled after https://github.com/remicollet/remirepo/raw/master/php/pecl/php-pecl-geoip/php-pecl-geoip.spec


# SFE-webstack

%include Solaris.inc
%include packagenamemacros.inc

%define php_version   5.4
##not defined %define php_major_version   5
%define php_major_minor_version   5.4
##not defined %define php_major_minor_micro_version 5.4.11

%define pecl_name geoip
%define php_inidir /etc/php/%{php_major_minor_version}/conf.d
%define pecl_xmldir /var/php/%{php_major_minor_version}/pear/.pkgxml

Name:                    SFEphp54-pecl-geoip
IPS_package_name:	 web/php-54/pecl/geoip
Summary:                 php pecl geoi, pecl extension module geoip
Version:                 1.0.8
Source:                  http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
URL:                     http://pecl.php.net/package/%{pecl_name}
##TODO## License:                 PHP
SUNW_BaseDir:            /
Patch1:                  php-pecl-geoip-01-geoip-tests.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEphp54
Requires:      SFEphp54

#libgeoip
BuildRequires: SFEgeoip
Requires:      SFEgeoip

%description
This PHP extension allows you to find the location of an IP address 
City, State, Country, Longitude, Latitude, and other information as 
all, such as ISP and connection type. It makes use of Maxminds geoip
database

%prep
%setup -q -c -n %{pecl_name}-%{version}

cd %{pecl_name}-%{version}
%patch1 -p0 -b .tests
cd ..

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc %{pecl_name}-%{version}/{README,ChangeLog}
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_prefix}/php/%{php_major_minor_version}/*

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/php/%{php_major_minor_version}/pear/.pkgxml/*

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/php/%{php_major_minor_version}/conf.d/%{pecl_name}.ini


%changelog
* Sun Jan 20 2013 - Thomas Wagner
- initial spec
  modeled after https://github.com/remicollet/remirepo/raw/master/php/pecl/php-pecl-geoip/php-pecl-geoip.spec
