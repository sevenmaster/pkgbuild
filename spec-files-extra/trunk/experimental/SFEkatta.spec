#
# spec file for package SFEkatta
#
# includes module(s): katta
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# TODO: either use a separate zookeeper package or require hbase

%include Solaris.inc

%include packagenamemacros.inc

%define srcname katta
%define runuser katta
#use random number by userid tool %define runuserid katta
%define runusergroup other

Name:                    SFEkatta
IPS_Package_Name:	 developer/distributed/katta
Summary:                 Katta - distributed lucene
Group:                   Utility
Version:                 0.6.4
URL:		         http://katta.sourceforge.net
Source:		         http://downloads.sourceforge.net/project/katta/katta/katta-%{version}/katta-core-%{version}.tar.gz
Source2:                 katta.xml
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           %pnm_requires_java_runtime_default
Requires:           SFEhadoop

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
Katta is a scalable, failure tolerant, distributed, data storage for
real time access.  Katta serves large, replicated, indices as shards
to serve high loads and very large data sets. These indices can be of
different type. Currently implementations are available for Lucene and
Hadoop mapfiles.

  - Makes serving large or high load indices easy
  - Serves very large Lucene or Hadoop Mapfile indices as index shards on many servers
  - Replicate shards on different servers for performance and fault-tolerance
  - Supports pluggable network topologies
  - Master fail-over
  - Fast, lightweight, easy to integrate
  - Plays well with Hadoop clusters
  - Apache Version 2 License

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-core-%{version}
cp %{SOURCE2} katta.xml

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp katta.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/katta
mkdir -p $RPM_BUILD_ROOT/var/lib/katta

mkdir -p $RPM_BUILD_ROOT/etc
mv conf $RPM_BUILD_ROOT/etc/katta
mkdir -p $RPM_BUILD_ROOT/usr/share/katta
mv bin docs lib *.jar *.txt $RPM_BUILD_ROOT/usr/share/katta
mkdir $RPM_BUILD_ROOT/usr/bin
ln -s /usr/share/katta/bin/katta-config.sh $RPM_BUILD_ROOT/usr/bin/katta-config.sh
ln -s /usr/share/katta/bin/katta $RPM_BUILD_ROOT/usr/bin/katta

# remove old hadoop library
rm $RPM_BUILD_ROOT/usr/share/katta/lib/hadoop-0.20.2-core.jar

echo "export KATTA_CONF_DIR=/etc/katta" > $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh-new
cat $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh >> $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh-new
echo "export KATTA_HOME=/usr/share/katta" >> $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh-new
cp $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh-new $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh
rm $RPM_BUILD_ROOT/usr/share/katta/bin/katta-config.sh-new
echo "export JAVA_HOME=/usr/java" >> $RPM_BUILD_ROOT/etc/katta/katta-env.sh
echo "export KATTA_LOG_DIR=/var/log/katta" >> $RPM_BUILD_ROOT/etc/katta/katta-env.sh
echo "export KATTA_CLASSPATH=/usr/share/hadoop/share/hadoop/common/hadoop-common-2.0.2-alpha.jar:/usr/share/hadoop/share/hadoop/common/lib/commons-configuration-1.6.jar:/usr/share/hadoop/share/hadoop/common/lib/commons-codec-1.4.jar:/usr/share/hadoop/share/hadoop/common/lib/commons-lang-2.5.jar:/usr/share/hadoop/share/hadoop/common/lib/hadoop-auth-2.0.2-alpha.jar:/usr/share/hadoop/share/hadoop/common/lib/slf4j-api-1.6.1.jar:/usr/share/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.6.1.jar:/usr/share/hadoop/share/hadoop/common/lib/protobuf-java-2.4.0a.jar" >> $RPM_BUILD_ROOT/etc/katta/katta-env.sh

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Katta Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/katta"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for katta)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/katta %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for katta)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/katta %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c KATTA


%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/katta
%{_datadir}/katta/*

%files root
%defattr (-, root, sys)
/etc/katta/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, katta, other) /var/log/katta
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, katta, other) /var/lib/katta
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/katta.xml

%changelog
* Thu Nov 15 2012 - Logan Bruns <logan@gedanken.org>
- Updated for hadoop2 compatibility.
* Thu July 12 2012 - Logan Bruns <logan@gedanken.org>
- Replaced hadoop client library with reference to more recent hadoop
  from hadoop pkg.
* Fri July 6 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
