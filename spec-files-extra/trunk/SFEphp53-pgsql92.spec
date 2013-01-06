#
# spec file for package SFEphp53-pgsql92
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc

%define _prefix /usr
%define tarball_version  5.3.14
%define tarball_name     php

Name:                    SFEphp53-pgsql92
IPS_package_name:	 web/php-53/extension/php-pgsql92
Summary:                 PHP 5.3 module for PostgreSQL 92
Version:                 5.3.14
License:		 PHP License
Url:                     http://www.php.net/
Source:			 http://museum.php.net/php5/%{tarball_name}-%{tarball_version}.tar.gz
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            /
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: web/php-53
BuildRequires: text/gnu-sed
BuildRequires: database/postgres-92/library
BuildRequires: database/postgres-92/developer
BuildRequires: SFEre2c

Requires: database/postgres-92/library
Requires: web/php-53

%description
The SFEphp53-pgsql92 package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL-9.2 database
support to PHP. PostgreSQL-9.2 is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL-9.2, you should install this package in addition to the main
php package.

%prep
%setup -c -n %name-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="%_ldflags"
export CC=cc
pwd
cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

pushd ext/pgsql/
/usr/php/5.3/bin/phpize
./configure \
 --prefix=%{_prefix}\
 --exec-prefix=%{_prefix}\
 --sysconfdir=%{_sysconfdir} \
 --libdir=%{_libdir} \
 --bindir=%{_bindir} \
 --includedir=%{_includedir} \
 --with-php-config=/usr/php/5.3/bin/php-config \
 --with-pgsql=/usr/postgres/9.2
gmake -j$CPUS
popd

pushd ext/pdo_pgsql/
/usr/php/5.3/bin/phpize
./configure \
 --prefix=%{_prefix}\
 --exec-prefix=%{_prefix}\
 --sysconfdir=%{_sysconfdir} \
 --libdir=%{_libdir} \
 --bindir=%{_bindir} \
 --includedir=%{_includedir} \
 --with-php-config=/usr/php/5.3/bin/php-config \
 --with-pdo-pgsql=/usr/postgres/9.2
gmake -j$CPUS
popd


%install

cd %{tarball_name}-%{tarball_version}
mkdir -p $RPM_BUILD_ROOT/etc/php/5.3/conf.d

for mod in pgsql pdo_pgsql; do
 pushd ext/${mod}/
  make install INSTALL_ROOT=$RPM_BUILD_ROOT PECL_EXTENSION_DIR=%{_prefix}/php/5.3/modules PECL_INCLUDE_DIR=%{_prefix}/php/5.3/include
 popd
 cat > $RPM_BUILD_ROOT/etc/php/5.3/conf.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
done

#mkdir -p $RPM_BUILD_ROOT/%{_prefix}/php/5.3/modules/
#mkdir -p  $RPM_BUILD_ROOT/etc/php/5.3/conf.d

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_prefix}
%dir %attr(0755, root, bin) %{_prefix}/php/5.3/modules
%{_prefix}/php/5.3/modules/*
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/php/5.3/conf.d/*

%changelog
* Mon Jan  7 2013 TAKI,Yasushi <taki@justplayer.com>
- fix version number
- fix package name
* Sat Dec 15 2012 Fumihisa TONAKA <fumi.ftnk@gmail.com>
- initial commit
