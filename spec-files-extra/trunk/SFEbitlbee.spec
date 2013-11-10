#
# spec file for package SFEbitlbee
#
# includes module(s): bitlbee
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%include pkgbuild-features.inc

%define srcname bitlbee

##TODO## put username:group into bitlbee.xml at build time
%define  daemonuser  bitlbee
#inspired by http://slackbuilds.org/uid_gid.txt
##TODO## check if this id is a good choice in Solaris
%define  daemonuid   250
%define  daemongcosfield BitlBee Reserved UID
%define  daemongroup other
%define  daemongid   1

Name:                    SFEbitlbee
IPS_Package_Name:	 network/chat/bitlbee
Group:                   Utility
%define bzr_revision	998
Version:                 3.2.0.0.%{bzr_revision}
%define download_version %{bzr_revision}
Summary:                 BitlBee - An IRC to other chat networks gateway (bzr_revision %{bzr_revision})
URL:		         http://www.bitlbee.org
#Source:		         http://get.bitlbee.org/src/bitlbee-%{download_version}.tar.gz
Source:		         http://code.bitlbee.org/lh/bitlbee/tarball/%{download_version}/bitlbee-develsnapshot-%{download_version}.tar.gz
Source2:                 bitlbee.xml
License: 		 GPLv2
Patch1:                  bitlbee-01-ipc.diff
Patch2:                  bitlbee-02-irc_im.diff
Patch3:                  bitlbee-03-irc_commands.diff
Patch4:                  bitlbee-04-irc_user.diff
Patch6:                  bitlbee-06-configure-find-libotr-in-usr-gnu.diff 
##TODO## check which osbuild brought us strcasestr
%if %{os2nnn}
#Solaris 11 has strcasestr
%else
Patch7:                  bitlbee-07-998-add_strcasestr.diff
%endif

SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:          %{pnm_buildrequires_SUNWopenssl_include}
Requires:               %{pnm_requires_SUNWopenssl_libraries}
BuildRequires:		%{pnm_buildrequires_SUNWglib2_devel}
Requires:		%{pnm_requires_SUNWglib2}
BuildRequires:		SFElibotr
Requires:		SFElibotr
#build docs
BuildRequires:		SFExmlto

#%config %class(preserve)
%if %{os2nnn}
%else
Requires: SUNWswmt
%endif

Requires: %name-root
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

#example 'category/newpackagename = *'
#example 'category/newpackagename >= 1.1.1'
#do not omit version equation!
%define renamed_from_oldname_1      %{name}
%define renamed_to_newnameversion_1 '%{IPS_Package_Name} = *'
#add more and different old names here
#%define renamed_from_oldname_2      %{name}
#%define renamed_to_newnameversion_2 ''

%include pkg-renamed.inc

%description
BitlBee brings IM (instant messaging) to IRC clients. It is a great
solution for people who have an IRC client running all the time and
do not want to run an additional MSN/AIM/whatever client.

BitlBee currently supports the following IM networks/protocols:
XMPP/Jabber (including Google Talk), MSN Messenger, Yahoo! Messenger,
AIM and ICQ, and the Twitter microblogging network (plus all other
Twitter API compatible services like identi.ca and status.net).

%prep
rm -rf %name-%version
#%setup -q -n %srcname-%version
#don't unpack please
%setup -q -c -T -n %srcname-%version
gzip -d < %SOURCE0 | (cd ${RPM_BUILD_DIR}/%srcname-%version; tar xf -)
cd bitlbee
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
##TODO## check which osbuild brought us strcasestr
%if %{os2nnn}
#Solaris 11 has strcasestr
%else
%patch7 -p1
%endif

#below: work into bitbee.xml the currently defined userid %{daemonuser}
#bitlbee manifest
cp -p %{SOURCE2} bitlbee.xml

%build
cd bitlbee
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#below: search first in /usr/gnu: e.g. /usr/gnu/lib/pkgconfig:/usr/lib/pkgconfig
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:$PKG_CONFIG_PATH
export CFLAGS="%optflags -I%{gnu_inc} %{gnu_lib_path} -L/usr/lib -R/usr/lib"
export LDFLAGS="/usr/lib/0@0.so.1 %_ldflags %{gnu_lib_path} -L/usr/lib -R/usr/lib `pkg-config --libs glib-2.0` -lgcrypt"
bash ./configure --prefix=%{_prefix}		\
            --etcdir=%{_sysconfdir}/%{srcname}  \
	    --mandir=%{_mandir}                 \
            --ssl=openssl                       \
            --otr=1

#doc is only built if the source looks like a bzr checkout
mkdir .bzr
make -j$CPUS LDFLAGS_BITLBEE="/usr/lib/0@0.so.1 %_ldflags %{gnu_lib_path} -L/usr/lib -R/usr/lib -lgcrypt"

%install
cd bitlbee
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-etc DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/bitlbee/

#mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{srcname}
#mv $RPM_BUILD_ROOT/%{_datadir}/%{srcname} $RPM_BUILD_ROOT/%{_docdir}/%{srcname}

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp bitlbee.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#no more then one package may deliver this: group groupname="%{daemongroup}" gid="%{daemongid}"
user ftpuser=false gcos-field="%{daemongcosfield}" username="%{daemonuser}" uid=%{daemonuid} password=NP group="%{daemongroup}"

#SVR4 (e.g. Solaris 10, SXCE)
#must run immediately to create the needed userid and groupid to be assigned to the files
#NOTE: if given GID or UID is already engaged, the next free ID is chosen automaticly
%pre root
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo 'getent group %{daemongroup} || groupadd -g %{daemongid} %{daemongroup} ';
  echo 'getent passwd %{daemonuser} || useradd -d /tmp -g %{daemongroup} -s /bin/false -c %{daemongcosfield} -u %{daemonuid} %{daemonuser}';
  echo '#not needed _if_ group is nogroup  (65534) because the group is altready there!'
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

#%postun root
#( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
#  echo 'getent passwd %{daemonuser} && userdel %{daemonuser}';
#  echo 'getent group %{daemongroup} && groupdel %{daemongroup}';
#  echo 'getent passwd %{daemonuser} && userdel %{daemonuser}';
#  echo 'getent group %{daemonlogingroup} && groupdel %{daemonlogingroup}';
#  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -c SFE

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{srcname}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
#%dir %attr (0755, root, other) %{_docdir}
#%dir %attr (0755, root, sys) %{_docdir}/%{srcname}
#%{_docdir}/%{srcname}/*

%dir %attr(0755, root, sys) %{_localstatedir}
%dir %attr(0755, root, other) %{_localstatedir}/lib
%dir %attr(0755, bitlbee, root) %{_localstatedir}/lib/%{srcname}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/bitlbee.xml

%files root
%defattr (-, root, bin)
%dir %attr(0755, root, sys) /etc
%dir %attr(0755, root, bin) /etc/bitlbee
%class(renamenew) /etc/bitlbee/*

%changelog
* Sun Nov 10 2013 - Thomas Wagner
- bump to 998 (development version 998, tarball download from bzr scm)
  (%change unpack, trigger doc preparation
- add patch7 for missing strcasestr bitlbee-07-998-add_strcasestr.diff
- preserve old config file
- link with 0@0.so.1 to prevent core dump when accessing a nullpointer
- add BuildRequires: SFExmlto to build docs
* Thu Jan 17 2013 - Logan Bruns <logan@gedanken.org>
- Updated to 3.2
* Thu Jan 17 2013 - Thomas Wagner
- remove too much quotes from daemongcosfield
- leave help.txt in /usr/share/bitlbee for online help
##TODO## consider adding the user-guide as well
* Sat Dec 15 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWopenssl_include}, 
  %{pnm_buildrequires_SUNWglib2_devel}, %include packagenamemacros.inc
- add root package for config and early enough userid creation on SVR4,
  default to numeric UID 250 for user bitlbee
- move configuration to /etc/bitlbee
- make bitlbee find SFElibotr in /usr/gnu/
- add SVR4 useradd
- add patch6 bitlbee-06-configure-find-libotr-in-usr-gnu.diff
* Sun Nov 5 2012 - Logan Bruns <logan@gedanken.org>
- Updated to 3.0.6 and removed a patch.
* Sat May 12 2012 - Logan Bruns <logan@gedanken.org>
- Made some more permissions explicit.
* Sat Apr 28 2012 - Logan Bruns <logan@gedanken.org>
- Fixed another permission and also changed to no longer enable service by default.
* Tue Apr 17 2012 - Logan Bruns <logan@gedanken.org>
- Fixed some permissions.
* Fri Mar 2 2012- Logan Bruns <logan@gedanken.org>
- New smf manifest, use a different runtime model and switch from gnutls to openssl.
* Thu Mar 1 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
