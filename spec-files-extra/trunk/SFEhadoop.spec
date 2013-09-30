#
# spec file for package SFEhadoop
#
# includes module(s): hadoop
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define srcname hadoop
%define runuser hadoop
#use random number by userid tool %define runuserid hadoop
%define runusergroup other

Name:                    SFEhadoop
IPS_Package_Name:	 developer/distributed/hadoop
Summary:                 Hadoop - Open-source software for reliable, scalable, distributed computing.
Group:                   Utility
Version:                 2.0.2
URL:		         http://hadoop.apache.org
Source:		         http://www.us.apache.org/dist/hadoop/core/hadoop-%{version}-alpha/hadoop-%{version}-alpha-src.tar.gz
Source2:                 hadoop.xml
Patch3:                  hadoop-03-fix-file-flags.diff
Patch4:                  hadoop-04-errlist.diff
Patch5:                  hadoop-05-limits.diff
Patch6:                  hadoop-06-libast.diff
Patch7:                  hadoop-07-getpwnam.diff
Patch8:                  hadoop-08-nslsocket.diff
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:      SFEmaven
BuildRequires:      %{pnm_buildrequires_SUNWant}
BuildRequires:      SFEcmake
BuildRequires:      SFEgcc
BuildRequires:      %{pnm_requires_java_runtime_default}
BuildRequires:      SFEsnappy
BuildRequires:      SFEprotobuf-devel
#make package dependency resolver happy (autobuild)
Requires:           SFEprotobuf
Requires:           SFEgccruntime
Requires:           %{pnm_requires_java_runtime_default}
Requires:           SFEsnappy

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
The Apache Hadoop software library is a framework that allows for the
distributed processing of large data sets across clusters of computers
using a simple programming model. It is designed to scale up from
single servers to thousands of machines, each offering local
computation and storage. Rather than rely on hardware to deliver
high-avaiability, the library itself is designed to detect and handle
failures at the application layer, so delivering a highly-availabile
service on top of a cluster of computers, each of which may be prone
to failures.

%prep
rm -rf %{srcname}-%{version}-alpha-src
%setup -q -n %{srcname}-%{version}-alpha-src
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
find . -name "*.sh" -exec chmod a+x {} \;
cp %{SOURCE2} hadoop.xml

%build

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS"
#export LDFLAGS="%_ldflags"
export LDFLAGS="-L/usr/jdk/latest/jre/lib/i386/"
export JAVA_HOME=/usr/java
mvn -B package -Pdist,native -DskipTests -Dtar -Dversion=%{version}-alpha -Drequire.snappy

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp hadoop.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/hadoop
mkdir -p $RPM_BUILD_ROOT/var/lib/hadoop

cd hadoop-dist/target/%{srcname}-%{version}-alpha

mv etc $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mv lib include $RPM_BUILD_ROOT/usr/
mkdir -p $RPM_BUILD_ROOT/usr/share
mv share/doc $RPM_BUILD_ROOT/usr/share
mkdir -p $RPM_BUILD_ROOT/usr/share/hadoop
mv bin sbin libexec share $RPM_BUILD_ROOT/usr/share/hadoop
mkdir $RPM_BUILD_ROOT/usr/bin
for f in hadoop hdfs mapred yarn ; do
  ln -s /usr/share/hadoop/libexec/$f-config.sh $RPM_BUILD_ROOT/usr/bin/$f-config.sh
  sed 's|DEFAULT_LIBEXEC_DIR=.*|DEFAULT_LIBEXEC_DIR=/usr/share/hadoop/libexec|g' < $RPM_BUILD_ROOT/usr/share/hadoop/bin/$f > $RPM_BUILD_ROOT/usr/bin/$f
  chmod a+x $RPM_BUILD_ROOT/usr/bin/$f
done

echo "export HADOOP_CONF_DIR=/etc/hadoop" > $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
cat $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh >> $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
echo "export HADOOP_HOME=/usr/share/hadoop" >> $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
cp $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh
rm $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
echo "export JAVA_HOME=/usr/java" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh
echo "export HADOOP_LOG_DIR=/var/log/hadoop" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh
echo "export YARN_LOG_DIR=/var/log/hadoop" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh
echo "export HADOOP_MAPRED_LOG_DIR=/var/log/hadoop" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh
echo "export HTTPFS_LOG_DIR=/var/log/hadoop" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Hadoop Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/hadoop"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for hadoop)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hadoop %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for hadoop)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hadoop %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c HADOOP


%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/hadoop
%{_datadir}/hadoop/*
%dir %attr(0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, other) %{_datadir}/doc/hadoop
%{_datadir}/doc/hadoop/*

%files root
%defattr (-, root, sys)
/etc/hadoop/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, hadoop, other) /var/log/hadoop
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, hadoop, other) /var/lib/hadoop
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/hadoop.xml

%changelog
* Sun Aug 11 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWant}, %{pnm_requires_java_runtime_default}, %{pnm_requires_java_runtime_default}
- add Requires: SFEprotobuf to make autobuild happy
* Mon Dec 10 2012 - Thomas Wagner
- run maven in batch mode (exits in case of problems instead waiting indefinitly)
* Sun Nov 11 2012 - Logan Bruns <logan@gedanken.org>
- Bumped to 2.0.2-alpha. Updated patches, dependencies and packaging rules.
* Mon Jun 18 2012 - Logan Bruns <logan@gedanken.org>
- bumped to 1.0.3
* Sun Jun 10 2012 - Logan Bruns <logan@gedanken.org>
- Increased the startup and shutdown timeouts. It can take longer with
  a lot of data in the cluster.
* Thu May 3 2012 - Logan Bruns <logan@gedanken.org>
- Replaced linux file flags with solaris ones
* Sat Apr 28 2012 - Logan Bruns <logan@gedanken.org>
- Added snappy to requires (really optional)
- Put home directory back to hold ssh keys
- Moved out of experimental
* Fri Apr 27 2012 - Logan Bruns <logan@gedanken.org>
- Fixes for building native task-controller, better directory usage and such.
* Wed Apr 25 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
