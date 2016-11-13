#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc

%define srcname stunnel
%define runuser stunnel
#use random number by userid tool %define runuserid stunnel
%define runusergroup other

Name:                SFEstunnel
IPS_Package_Name:    sfe/service/security/stunnel
Summary:             An SSL client/server encryption wrapper
Version:             5.37
#remove leading "0"s. 5.09 -> 5.9
IPS_Component_Version: $( echo %{version} | sed -e 's?\.0*?.?g' )
Source:              http://www.usenix.org.uk/mirrors/stunnel/archive/5.x/stunnel-%{version}.tar.gz
Source2:             stunnel.xml

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires:          %{pnm_buildrequires_SUNWopenssl_include}
Requires:               %{pnm_requires_SUNWopenssl_libraries}

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n stunnel-%version
cp %{SOURCE2} stunnel.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=gcc
export CXX=g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"
export LIBS="/usr/lib/values-xpg4.o"
export CPPFLAGS="-D_XOPEN_SOURCE -D_XOPEN_SOURCE_EXTENDED=1 -D__EXTENSIONS__"

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-ssl=/usr

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

install -D src/stunnel $RPM_BUILD_ROOT%{_sbindir}/stunnel
install -D src/.libs/libstunnel.so $RPM_BUILD_ROOT%{_libdir}/libstunnel.so
install -D doc/stunnel.8 $RPM_BUILD_ROOT%{_mandir}/man8/stunnel.8
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/stunnel
sed -e 's|/usr/|/|g' -e 's|nobody|stunnel|g' tools/stunnel.conf-sample > $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.conf-sample

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp stunnel.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

mkdir -p ${RPM_BUILD_ROOT}/var/lib/stunnel

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Stunnel Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/stunnel"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for stunnel)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/stunnel %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for stunnel)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/stunnel %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c STUNNEL

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man*/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/stunnel/stunnel.conf-sample
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/stunnel.xml
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, stunnel, other) /var/lib/stunnel

%changelog
* Sun Nov 13 2016 - Thomas Wagner
- bump to 5.37
- fix download URL to read vom permanent location /archive/
* Sun Oct 30 2016 - Thomas Wagner
- fix download URL
- bump to 5.36
* Fri Aug  5 2016 - Thomas Wagner
- bump to 5.35
* Wed May 11 2016 - Thomas Wagner
- bump to 5.32
* Sun Feb 14 2016 - Thomas Wagner
- bump to 5.30
* Sat Jan 10 2015 - Thomas Wagner
- bump to 5.09 (5.9 on IPS)
- remove typo in %files root
* Sat Oct 25 2014 - Thomas Wagner
- fix preserve for config files
* Mon Arp 14 2014 - Thomas Wagner
- bump to 5.01 (5.1 on IPS)
* Sun Apr  6 2014 - Thomas Wagner
- add %iclass(renamenew) for %{_sysconfdir}/stunnel
* Thu Mar 21 2013 - Logan Bruns <logan@gedanken.org>
- updated to 4.55
* Sat Jan 12 2013 - Logan Bruns <logan@gedanken.org>
- bump to 4.54
- added IPS name
- added smf service and stunnel user
* Sat May  3 2008 - river@wikimedia.org
- 4.22
- change source location to stunnel.org
- build in XPG4v2 standards mode for CMSG macros
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 4.21
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Jan  7 2007 - laca@sun.com
- bump to 4.20
* Mon Dec 18 2006 - Eric Boutilier
- Initial spec
