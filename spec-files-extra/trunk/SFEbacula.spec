# 
# spec file for package SFEbacula 
# 

%include Solaris.inc
%include packagenamemacros.inc

%define src_name bacula
%define mysql_version %(pkg mediator -H mysql | awk '{print $3}')
%define mysql_pkg_version %(echo %{mysql_version} | sed -e 's/\.//g')

Name:                SFEbacula
IPS_Package_Name:	 backup/bacula
License:             AGPLv3
Summary:             The Bacula Open Source Network Backup Solution
Version:             9.0.4
Source:              http://downloads.sourceforge.net/sourceforge/bacula/bacula-%{version}.tar.gz
Source1:			 bacula.xml
URL:                 http://www.bacula.org/
# SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      bacula.copyright
Group:		    	 Applications/System
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: database/mysql-%{mysql_pkg_version}
BuildRequires: database/mysql-%{mysql_pkg_version}/library
Requires: database/mysql-%{mysql_pkg_version}
Requires: database/mysql-%{mysql_pkg_version}/library
Requires: SFEmtx

%prep
echo %{_sysconfdir}
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# Using the standard flags results in several problems with default values at runtime
# Similar to http://bacula.10910.n7.nabble.com/bconsole-can-t-talk-to-bacula-dir-td84578.html

#export CFLAGS="%{optflags}"
#export CXXFLAGS="%{cxx_optflags}"
#export LDFLAGS="%{_ldflags}"

./configure				\
	--prefix=%{_prefix} \
	--with-mysql=/usr/mysql/%{mysql_version} \
	--sysconfdir=%{_sysconfdir}/bacula \
	--with-scriptdir=%{_sysconfdir}/bacula/scripts \
	--with-working-dir=/var/bacula \
	--with-logdir=/var/bacula \
	--mandir=%{_datadir}/man \
	--enable-batch-insert=no \
	--enable-tray-monitor

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/application/bacula
cp %{SOURCE1} ${RPM_BUILD_ROOT}/var/svc/manifest/application/bacula/

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE: the scripts mtx-changer and disk-changer (*changer) in /etc/bacula
# are marked as %config because they sometimes need to be modified to
# properly support different media changer models. When upgrading,
# check *changer.new for any changes.

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%attr (0555, root, bin) %{_sbindir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/bacula
%config(noreplace) %{_sysconfdir}/bacula/*.conf
%dir %attr (0755, root, sys) %{_sysconfdir}/bacula/scripts
%{_sysconfdir}/bacula/scripts/bacula
%{_sysconfdir}/bacula/scripts/*ctl*
%{_sysconfdir}/bacula/scripts/bacula_config
%{_sysconfdir}/bacula/scripts/bconsole
%{_sysconfdir}/bacula/scripts/btraceback.*
%{_sysconfdir}/bacula/scripts/*backup*
%{_sysconfdir}/bacula/scripts/*.desktop
%config(noreplace) %{_sysconfdir}/bacula/scripts/*changer
%config(noreplace) %{_sysconfdir}/bacula/scripts/*changer.conf
%{_sysconfdir}/bacula/scripts/*database
%{_sysconfdir}/bacula/scripts/*privileges
%{_sysconfdir}/bacula/scripts/*tables
%{_sysconfdir}/bacula/scripts/tapealert
%{_sysconfdir}/bacula/scripts/*.sql
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/bacula
%{_datadir}/doc/bacula/*
%dir %{_datadir}/man/man1
%{_datadir}/man/man1/*
%dir %{_datadir}/man/man8
%{_datadir}/man/man8/*
%dir %attr (1777, root, sys) /tmp
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/bacula
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/application
%dir %attr (0755, root, sys) /var/svc/manifest/application/bacula
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/application/bacula/bacula.xml

%changelog
* Wed Oct 18 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- Remove standard flags to fix runtime issues with default values
* Fri Oct 06 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- Bump to 9.0.4
* Wed Apr 02 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Restrict %config tag to actual config files and changer scripts
* Tue Apr 01 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Fix SUNW_Copyright
* Tue Apr 01 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add %config(noreplace) to configuration files in %files
* Mon Mar 03 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add SMF manifest
- Add CFLAGS and LDFLAGS
* Wed Nov 20 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Added Requires: %{pnm_requires_SUNWmtx}
* Thu Nov 14 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 5.2.13
