#
# spec file for package SFEkestrel
#
# includes module(s): kestrel
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include packagenamemacros.inc

%define srcname kestrel
%define runuser kestrel
#use random number by userid tool %define runuserid kestrel
%define runusergroup other

Name:                    SFEkestrel
IPS_Package_Name:	 developer/distributed/kestrel
Summary:                 Kestrel - a simple, distributed message queue
Group:                   Utility
Version:                 2.4.1
URL:		         http://robey.github.com/kestrel/
Source:		         http://robey.github.com/kestrel/download/kestrel-%{version}.zip
Source2:                 kestrel.xml
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%define SFEopenjdk7     %(/usr/bin/pkginfo -q SFEopenjdk7  2>/dev/null && echo 1 || echo 0)

# Use openjdk7 if present instead of OI's older version of java
%if %SFEopenjdk7
Requires: SFEopenjdk7
%define java_home /usr/jdk/instances/openjdk1.7.0
%else
Requires:           %pnm_requires_java_runtime_default
%define java_home /usr/java
%endif

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
Kestrel is a simple, distributed message queue written on the JVM,
based on Blaine Cook's "starling".

Each server handles a set of reliable, ordered message queues, with no
cross communication, resulting in a cluster of k-ordered ("loosely
ordered") queues. Kestrel is fast, small, and reliable.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}
cp %{SOURCE2} kestrel.xml

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp kestrel.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/kestrel
mkdir -p $RPM_BUILD_ROOT/var/spool/kestrel
mkdir -p $RPM_BUILD_ROOT/var/lib/kestrel

mkdir -p $RPM_BUILD_ROOT/usr/share/kestrel
mv * $RPM_BUILD_ROOT/usr/share/kestrel

mkdir -p $RPM_BUILD_ROOT/etc/kestrel
echo "export JAVA_HOME=%java_home" > $RPM_BUILD_ROOT/etc/kestrel/kestrel-env.sh

gsed -i -e 's|/etc/sysconfig/kestrel|/etc/kestrel/kestrel-env.sh|g' \
     -e 's|/usr/local/$APP_NAME/current|/usr/share/kestrel|g' \
     -e 's|/var/run|/var/lib|g' \
     -e 's|-server|-d64 -server|g' \
  `find $RPM_BUILD_ROOT/usr/share/kestrel/scripts/* -type f -print`

chmod a+x $RPM_BUILD_ROOT/usr/share/kestrel/scripts/*

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Kestrel Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/kestrel"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for kestrel)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/kestrel %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for kestrel)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/kestrel %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c KESTREL


%files
%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/kestrel
%{_datadir}/kestrel/*

%files root
%defattr (-, root, sys)
/etc/kestrel/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, kestrel, other) /var/log/kestrel
%dir %attr(0755, root, bin) /var/spool
%dir %attr(0700, kestrel, other) /var/spool/kestrel
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, kestrel, other) /var/lib/kestrel
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/kestrel.xml

%changelog
* Tue Feb 26 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
