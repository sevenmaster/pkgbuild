# 
# spec file for package SFEbacula 
# 
%include Solaris.inc
%include packagenamemacros.inc

%define src_name bacula

Name:                SFEbacula
IPS_Package_Name:	 backup/bacula
License:             AGPLv3
Summary:             The Bacula Open Source Network Backup Solution
Version:             5.2.13
Source:              http://downloads.sourceforge.net/sourceforge/bacula/bacula-5.2.13.tar.gz
Source1:			 bacula.xml
URL:                 http://www.bacula.org/
# SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
Group:		    	 Applications/System
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_mysql_default}
Requires: %{pnm_requires_mysql_default}
Requires: %{pnm_requires_SUNWmtx}

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure				\
	--prefix=%{_prefix} \
	--with-mysql=/usr/mysql/5.1 \
	--sysconfdir=/etc/bacula \
	--with-working-dir=/var/bacula \
	--mandir=%{_datadir}/man \
	--enable-tray-monitor

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/application/bacula
cp %{SOURCE1} ${RPM_BUILD_ROOT}/var/svc/manifest/application/bacula/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%attr (0555, root, bin) %{_sbindir}/*
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, sys) /etc/bacula
%config(noreplace) /etc/bacula/*
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
* Tue Apr 01 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add %config(noreplace) to configuration files in %files
* Mon Mar 03 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add SMF manifest
- Add CFLAGS and LDFLAGS
* Wed Nov 20 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Added Requires: %{pnm_requires_SUNWmtx}
* Thu Nov 14 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 5.2.13
