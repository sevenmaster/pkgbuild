#
# spec file for package SFEfail2ban
#

#TODO# might get removed some day
%define _use_internal_dependency_generator 0

%include Solaris.inc
%include packagenamemacros.inc

#description of this download method:
#https://fedorahosted.org/fpc/attachment/ticket/233/slask

#fail2ban
%define githubowner1  jamesstout
%define githubproject1 fail2ban-0.8.4-OpenSolaris
#for github commits see link on the right with the shortened commitid on the Webpage
#  -> https://github.com/jamesstout/fail2ban-0.8.4-OpenSolaris/commit/e065f64b14699758a28fdbf4622fca884753e68f
%define commit1 e065f64b14699758a28fdbf4622fca884753e68f
#remember to increas with every changed commit1 value
%define increment_version_helper 2
%define shortcommit1 %(c=%{commit1}; echo ${c:0:7})
#

%define svcdir /var/svc/manifest/network
%define src_name fail2ban


Name:                    SFEfail2ban
IPS_Package_Name:        package/fail2ban
Group:                   Network
Summary:                 monitor logfiles for invalid login attempts and ban source IP-addresses - (github version %{commit1})
Version:                 0.0.0.0.0.%{increment_version_helper}
Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{shortcommit1}/%{githubproject1}-%{commit1}.tar.gz
Patch1:                  fail2ban-01-create-var-run-fail2ban.diff
URL:                     https://github.com/quattor/fail2ban
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{src_version}-build


%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_python_default}
Requires:	%{pnm_requires_python_default}

Requires: %name-root
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/


%description
Fail2Ban monitors log files like /var/log/pwdfail or /var/log/apache/error_log
and bans failure-prone addresses. It updates firewall rules to reject the IP
address or executes user defined commands.
(currently: /etc/hosts.deny is updated)

NOTE: You need to configure syslog.conf to get necessary login log entries
==========================================================================

INSTALLATION ON SOLARIS

-> Read the file /usr/share/doc/SFEfail2ban/README.Solaris

Note from SFE maintainer for this package:
If you do not follow the above README.Solaris (files already copied!)
then you will not get a working fail2ban setup!


%prep
%setup -q -n %{githubproject1}-%{commit1}

%patch1 -p1

#remove /usr/local/bin: from SMF manifest file
gsed -i.bak1 -e 's,/usr/local/bin:\?,,'  files/opensolaris-svc-fail2ban
gsed -i.bak1 -e 's,/usr/local/bin:\?,,'  files/solaris-10-svc-fail2ban


%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=%{buildroot} --prefix=%{_prefix} --no-compile

mkdir -p "${RPM_BUILD_ROOT}/var/svc/manifest/network"
cp files/solaris-fail2ban.xml ${RPM_BUILD_ROOT}/var/svc/manifest/network

#note: opensolaris-svc-fail2ban is patched to use /usr/local/bin/python, we don't want this right now for SFE
mkdir -p "${RPM_BUILD_ROOT}/lib/svc/method/"
cp files/solaris-10-svc-fail2ban "${RPM_BUILD_ROOT}/lib/svc/method/svc-fail2ban"

#TODO# check if fail2ban can create its directory /var/run/fail2ban on its own
rm -r $RPM_BUILD_ROOT/var/run



%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr(-, root, bin)
%doc COPYING ChangeLog PKG-INFO README README.Solaris README.md TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, bin) /lib/svc/method/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
%dir %attr (0755, root, other) %{_docdir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{src_name}
%class(renamenew) %{_sysconfdir}/%{src_name}/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%class(manifest) %attr (0444, root, sys) %{svcdir}/*
%define svcdir /var/svc/manifest/network/fail2ban
#              /var/svc/manifest/site/dovecot.xml


%changelog
* Sat Nov 30 2013 - Thomas Wagner
- Initial spec
