#
# spec file for package SFEejabberd
#
# includes module(s): ejabberd
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define srcname ejabberd
%define runuser ejabberd
#use random number by userid tool %define runuserid ejabberd
%define runusergroup other

Name:                    SFEejabberd
IPS_Package_Name:	 service/network/xmpp/ejabberd
Summary:                 ejabberd - the Erlang Jabber/XMPP daemon
Group:                   Utility
Version:                 2.1.11
URL:		         http://www.ejabberd.im
Source:		         http://www.process-one.net/downloads/%{srcname}/%{version}/%{srcname}-%{version}.tgz
Source2:                 ejabberd.xml
License: 		 GPLv2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgcc
BuildRequires:          %{pnm_buildrequires_SUNWopenssl_include}
Requires:               %{pnm_requires_SUNWopenssl_libraries}
BuildRequires: SFEerlang
Requires: SFEerlang
BuildRequires: SUNWlexpt
Requires: SUNWlexpt
BuildRequires: SFEimagemagick
Requires: SFEimagemagick

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
ejabberd is a Jabber/XMPP instant messaging server, licensed under
GPLv2 (Free and Open Source), written in Erlang/OTP. Among other
features, ejabberd is cross-platform, fault-tolerant, clusterable and
modular.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

cp %{SOURCE2} ejabberd.xml

# Move the lock file from /var/lock to ~ejabberd
gsed -i 's|@localstatedir@/lock/ejabberdctl|@localstatedir@/lib/ejabberd/ejabberdctl|g' src/Makefile.in

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

cd src
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
mkdir -p $RPM_BUILD_ROOT/var/lib/ejabberd
mkdir -p $RPM_BUILD_ROOT/var/log/ejabberd
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ejabberd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

gsed -i 's/INSTALLUSER=/INSTALLUSER=ejabberd/g' $RPM_BUILD_ROOT/usr/sbin/ejabberdctl
chmod a+rx $RPM_BUILD_ROOT/usr/sbin/ejabberdctl

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="ejabberd Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/ejabberd"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for ejabberd)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/ejabberd %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for ejabberd)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/ejabberd %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c EJABBERD


%files
%defattr (-, root, bin)
%{_sbindir}
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr(0755, ejabberd, other) %{_localstatedir}/lib/%{srcname}
%{_localstatedir}/lib/%{srcname}/*
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr(0755, ejabberd, other) %{_localstatedir}/log/%{srcname}

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/ejabberd.xml

%changelog
* Tue Jan 22 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
