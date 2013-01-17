#
# spec file for package SFEfunambol
#
# includes module(s): funambol
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%include packagenamemacros.inc

%define srcname funambol
%define runuser funambol
#use random number by userid tool %define runuserid funambol
%define runusergroup other

Name:                    SFEfunambol
IPS_Package_Name:	 network/syncml/funambol
Summary:                 Funambol - SyncML based mobile application platform
Group:                   Utility
Version:                 10.0.2
URL:		         http://www.funambol.com
Source:		         http://downloads.sourceforge.net/project/funambol/bundle/v10/funambol-%{version}.tgz
Source2:                 funambol.xml
License: 		 GNU Affero General Public License
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /var
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %pnm_requires_java_runtime_default

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
Funambol, your SyncML based mobile application platform:

 - Funambol Data Synchronization Server - a Java SyncML 
server, that you can use with any SyncML client (e. g. to synchronize the 
address book on your phone through a pre-installed SyncML client)

 - Funambol CTP Server - a CTP Server to support CTP notification

 - Funambol Administration Tool - a standalone visual 
interface to administer the Funambol Data Synchronization Server

 - Funambol Java Demo Client - a stand-alone visual
interface to test the synchronization of PIM data (contacts and calendar) 
with the Funambol Data Synchronization Server

 - Funambol Inbox Listener -  a component to perfom push email
 
 - Funambol Pim Listener -  a component to perfom push pim information

 - Web Demo Client - a demo web interface to visualize PIM data.

%prep
rm -rf %name-%version
mkdir %name-%version
tar xvzf %{SOURCE}
rm -rf Funambol/tools/jre-1.6.0
rm Funambol/bin/*.cmd Funambol/bin/*.exe
gsed -i -e 's|.FUNAMBOL_HOME/tools/jre-1.6.0/jre|/usr/jdk/instances/jdk1.6.0|g' Funambol/bin/funambol
cp %{SOURCE2} funambol.xml

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib
mv Funambol $RPM_BUILD_ROOT/var/lib/funambol
mkdir -p $RPM_BUILD_ROOT/var/log/funambol
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp funambol.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Funambol Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/funambol"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for funambol)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/funambol %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for funambol)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/funambol %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c FUNAMBOL


%files
%defattr (-, root, other)
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, funambol, other) /var/lib/funambol
%defattr (-, funambol, other)
/var/lib/funambol/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, funambol, other) /var/log/funambol


%files root
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/funambol.xml

%changelog
* Thu Jan 17 2013- Logan Bruns <logan@gedanken.org>
- Initial spec.
