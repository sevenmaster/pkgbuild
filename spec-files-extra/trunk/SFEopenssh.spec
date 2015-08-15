# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# TODO:
#   fix manpages
#   ssh-http-proxy-connect
#   ssh-socks5-proxy-connect
#   RBAC
#   PAM

%include Solaris.inc

%include packagenamemacros.inc

%define as_optional %{?_with_optional_sshd:1}%{?!_with_optional_sshd:0}

%define	src_name	openssh

Name:		SFEopenssh-server
IPS_Package_Name:	service/network/openssh
Summary:	Secure Shell protocol Server
Version:	6.9p1
IPS_Component_Version:	6.9.1
URL:		http://www.openssh.org/
Source:		http://ftp5.usa.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{src_name}-%{version}.tar.gz
Source1:	ssh.xml
Source2:	sshd
Source3:	ssh-askpass
Source4:	openssh.xml
Source5:	opensshd
Patch1:		openssh-01-motd.diff
Patch2:		openssh-002-pam_support.diff
Patch3:		openssh-003-last_login.diff
Patch4:		openssh-004-broken_bsm_api.diff
Patch5:		openssh-005-openssh_krb5_build_fix.diff
Patch8:		openssh-008-deprecate_sunssh_opt.diff
Group:		System/Security
License:	BSD
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}_%{version}-build

%include default-depend.inc

BuildRequires:	SFEldns-devel
Requires:	SFEldns
BuildRequires:  %{pnm_buildrequires_SUNWopenssl_include}
Requires:	%{pnm_requires_SUNWopenssl_libraries}
BuildRequires:	%{pnm_buildrequires_SUNWopenssl_fips_140_devel}
Requires:	%{pnm_requires_SUNWopenssl_fips_140}
%if %{os2nnn}
BuildRequires:	library/libedit
Requires:	library/libedit
%else
BuildRequires:	SFEeditline-devel
Requires:	SFEeditline
%endif

%description
OpenSSH is a FREE version of the SSH connectivity tools that technical users of the Internet rely on. Users of telnet, rlogin, and ftp may not realize that their password is transmitted across the Internet unencrypted, but it is. OpenSSH encrypts all traffic (including passwords) to effectively eliminate eavesdropping, connection hijacking, and other attacks. Additionally, OpenSSH provides secure tunneling capabilities and several authentication methods, and supports all SSH protocol versions.

%package -n SFEopenssh-client
IPS_package_name:	network/openssh
Summary:	SSH Client and utilities
SUNW_BaseDir:	/
%include default-depend.inc
BuildRequires:	SFEldns-devel
Requires:	SFEldns
BuildRequires:  %{pnm_buildrequires_SUNWopenssl_include}
Requires:	%{pnm_requires_SUNWopenssl_libraries}
BuildRequires:	%{pnm_buildrequires_SUNWopenssl_fips_140_devel}
Requires:	%{pnm_requires_SUNWopenssl_fips_140}

%package -n SFEopenssh-common
IPS_package_name:	network/openssh/ssh-key
Summary:	Secure Shell protocol common Utilities
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch8 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %as_optional
%define path_suffix openssh
%else
%define path_suffix ssh
%endif

export CFLAGS="%{optflags}"

#which build exactly?
%if %{solaris11} %{solaris12}
export CFLAGS="${CFLAGS} -DS11_BSM_API"
%endif

export LDFLAGS="%{_ldflags} -B direct -z nolazyload"

./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir}/%{path_suffix}	\
	--libexecdir=%{_libdir}/%{path_suffix}	\
	--sbindir=%{_libdir}/%{path_suffix}	\
	--with-audit=bsm	\
	--with-ssl-engine	\
	--with-pam		\
	--with-kerberos5	\
	--with-solaris-contracts	\
	--with-solaris-projects	\
	--with-tcp-wrappers	\
	--with-4in6	\
	--enable-strip=no	\
	--with-xauth=/usr/bin/xauth	\
	--with-libedit		\
	--with-ldns

make -j$CPUS

%install
rm -rf %{buildroot}

gmake install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/lib/svc/manifest/network/
mkdir -p %{buildroot}/lib/svc/method/
%if %as_optional
cp %{SOURCE4} %{buildroot}/lib/svc/manifest/network/
cp %{SOURCE5} %{buildroot}/lib/svc/method/
%else
cp %{SOURCE1} %{buildroot}/lib/svc/manifest/network/
cp %{SOURCE2} %{buildroot}/lib/svc/method/
%endif

cp %{SOURCE3} %{buildroot}/%{_libdir}/%{path_suffix}/ssh-askpass

# section 8 is not valid for Solaris
(cd %{buildroot}/%{_mandir}
    for i in `ls -1 man8/*`; do mv $i $(echo $i | sed 's/\.8/\.1m/g'); done
    mv man8 man1m
)

# section 5 is not valid for Solaris
(cd %{buildroot}/%{_mandir}
    for i in `ls -1 man5/*`; do mv $i $(echo $i | sed 's/\.5/\.4/g'); done
    mv man5 man4
)

%if %as_optional
rm %{buildroot}/%{_mandir}/man1m/sftp-server.1m
rm %{buildroot}/%{_mandir}/man1m/sshd.1m
rm %{buildroot}/%{_mandir}/man4/sshd_config.4
mv %{buildroot}/%{_bindir}/ssh-keygen %{buildroot}/%{_bindir}/%{path_suffix}-keygen
mv %{buildroot}/%{_bindir}/ssh-keyscan %{buildroot}/%{_bindir}/%{path_suffix}-keyscan
mv %{buildroot}/%{_libdir}/%{path_suffix}/ssh-keysign %{buildroot}/%{_libdir}/%{path_suffix}/%{path_suffix}-keysign
mv %{buildroot}/%{_mandir}/man1/ssh-keygen.1 %{buildroot}/%{_mandir}/man1/%{path_suffix}-keygen.1
mv %{buildroot}/%{_mandir}/man1/ssh-keyscan.1 %{buildroot}/%{_mandir}/man1/%{path_suffix}-keyscan.1
mv %{buildroot}/%{_mandir}/man1m/ssh-keysign.1m %{buildroot}/%{_mandir}/man1m/%{path_suffix}-keysign.1m
%endif


%clean
rm -rf %{buildroot}

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/useradd -d /var/empty -s /bin/true -g sys sshd';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel sys';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions -n SFEopenssh-server
legacy desc="Secure Shell protocol Server" name="SSH Server, (Root)" pkg=SUNWsshdr
legacy desc="Secure Shell protocol Server" name="SSH Server, (Usr)" pkg=SUNWsshdu
user ftpuser=false gcos-field="sshd Reserved UID" username="sshd" password=NP group="sys" home-dir="/var/empty"

%actions -n SFEopenssh-client
legacy desc="Secure Shell protocol Client and associated Utilities" name="SSH Client and utilities, (Root)" pkg=SUNWsshr
legacy desc="Secure Shell protocol Client and associated Utilities" name="SSH Client and utilities, (Usr)" pkg=SUNWsshu

%actions -n SFEopenssh-common
legacy desc="Secure Shell protocol common Utilities" name="SSH Common, (Usr)" pkg=SUNWsshcu

%files -n SFEopenssh-server 
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}
%if %as_optional
%class(preserve) %config %attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}/sshd_config
%else
%class(preserve) %config %ips_tag(original_name=SUNWsshd:%{@}) %attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}/sshd_config
%endif
%dir %attr (0755, root, sys) /lib/svc/manifest
%dir %attr (0755, root, sys) /lib/svc/manifest/network
%class(manifest) %attr (0444, root, sys) /lib/svc/manifest/network/%{path_suffix}.xml
%attr (0555, root, bin) /lib/svc/method/%{path_suffix}d
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/%{path_suffix}/sftp-server
%{_libdir}/%{path_suffix}/sshd
%if %as_optional
%else
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1m/sftp-server.1m
%{_mandir}/man1m/sshd.1m
%{_mandir}/man4/sshd_config.4
%endif
%dir %attr (0755, root, sys) %{_localstatedir}
%attr (0755, root, sys) %{_localstatedir}/empty

%files -n SFEopenssh-client
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}
%attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}/moduli
%if %as_optional
%class(preserve) %config %attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}/ssh_config
%else
%class(preserve) %config %ips_tag(original_name=SUNWssh:%{@}) %attr (0755, root, sys) %{_sysconfdir}/%{path_suffix}/ssh_config
%endif
%dir %attr (0755, root, sys) %{_prefix}
%{_bindir}/scp
%{_bindir}/sftp
%{_bindir}/slogin
%{_bindir}/ssh
%{_bindir}/ssh-add
%{_bindir}/ssh-agent
%attr (0555, root, bin) %{_libdir}/%{path_suffix}/ssh-askpass
%{_libdir}/%{path_suffix}/ssh-pkcs11-helper
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/scp.1
%{_mandir}/man1/sftp.1
%{_mandir}/man1/slogin.1
%{_mandir}/man1/ssh.1
%{_mandir}/man1/ssh-add.1
%{_mandir}/man1/ssh-agent.1
%{_mandir}/man1m/ssh-pkcs11-helper.1m
%{_mandir}/man4/moduli.4
%{_mandir}/man4/ssh_config.4

%files -n SFEopenssh-common
%defattr (-, root, bin)
%{_bindir}/%{path_suffix}-keygen
%{_bindir}/%{path_suffix}-keyscan
%{_libdir}/%{path_suffix}/%{path_suffix}-keysign
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/%{path_suffix}-keygen.1
%{_mandir}/man1/%{path_suffix}-keyscan.1
%{_mandir}/man1m/%{path_suffix}-keysign.1m

%changelog
* Mon Aug 10 2015 - Thomas Wagner
- bump to 6.9p1
* Tue Feb 24 2015 - Thomas Wagner
- bump to 6.7p1, rework patch3 patch8
* Sun May 04 2014 - Milan Jurik
- bump to 6.6p2
- add openssh as optional to system ssh
* Mon Sep 09 2013 - Milan Jurik
- bump to 6.2p2
* Fri Oct 12 2012 - Milan Jurik
- bump to 6.1p1
- force use of editline
* Fri Jun 8 2012 - Logan Bruns <logan@gedanken.org>
- Added a missing with_editline conditional which prevented compilation without editline
* Sat Jun 02 2012 - Milan Jurik
- Initial spec
