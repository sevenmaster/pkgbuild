#
# spec file for package SFEjena-fuseki
#
# includes module(s): jena-fuseki
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%include packagenamemacros.inc

%define srcname jena-fuseki
%define runuser fuseki
#use random number by userid tool %define runuserid jena-fuseki
%define runusergroup other

Name:                    SFEjena-fuseki
IPS_Package_Name:	 database/jena-fuseki
Summary:                 Fuseki - the Jena SPARQL server
Group:                   System/Databases
Version:                 1.0.0
URL:		         http://jena.apache.org
Source:		         http://www.apache.org/dist/jena/binaries/jena-fuseki-%{version}-distribution.tar.gz
Source2:                 jena-fuseki.xml
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /var
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%define SFEopenjdk7     %(/usr/bin/pkginfo -q SFEopenjdk7  2>/dev/null && echo 1 || echo 0)

# Use openjdk7 if present instead of OI's older version of java
%if %SFEopenjdk7
Requires: SFEopenjdk7
%define java_home /usr/jdk/instances/openjdk1.7.0
%else
Requires:           %pnm_requires_java_runtime_default
%define java_home /usr/java
%endif

%description
Jena-Fuseki: serving RDF data over HTTP

Jena-Fuseki is a SPARQL server. It provides REST-style SPARQL HTTP Update, SPARQL Query, and SPARQL Update using the SPARQL protocol over HTTP.

The relevant SPARQL standards are:

    SPARQL 1.1 Query
    SPARQL 1.1 Update
    SPARQL 1.1 Protocol
    SPARQL 1.1 Graph Store HTTP Protocol

These are work-in-progress by the SPARQL working group; although the general designs are stable, details may change. Jena-Fuseki will track the draft standards.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
cp %{SOURCE2} jena-fuseki.xml

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/jena-fuseki
cp -r * $RPM_BUILD_ROOT/var/lib/jena-fuseki
mkdir -p $RPM_BUILD_ROOT/var/log/jena-fuseki
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp jena-fuseki.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/etc/default
cat > $RPM_BUILD_ROOT/etc/default/fuseki <<EOF
JAVA=%{java_home}/bin/java
FUSEKI_HOME=/var/lib/jena-fuseki
FUSEKI_ARGS="--update --loc=/var/lib/jena-fuseki/DB /ds"
FUSEKI_LOGS=/var/log/jena-fuseki
EOF
mkdir -p $RPM_BUILD_ROOT/usr/bin
chmod a+x $RPM_BUILD_ROOT/var/lib/jena-fuseki/s-*
for f in $RPM_BUILD_ROOT/var/lib/jena-fuseki/s-* ; do 
  ln -s /var/lib/jena-fuseki/`basename $f` $RPM_BUILD_ROOT/usr/bin/`basename $f`
done

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Jena-Fuseki Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/jena-fuseki"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for jena-fuseki)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/jena-fuseki %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for jena-fuseki)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/jena-fuseki %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c JENA-FUSEKI


%files
%defattr (-, root, other)
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, fuseki, other) /var/lib/jena-fuseki
%defattr (-, fuseki, other)
/var/lib/jena-fuseki/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, fuseki, other) /var/log/jena-fuseki


%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/jena-fuseki.xml
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, sys) /etc/default
/etc/default/*
%defattr (-, root, other)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Thu Jan 2 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
