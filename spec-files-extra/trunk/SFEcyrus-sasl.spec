#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc

Name:		SFEcyrus-sasl
IPS_Package_Name:	library/security/cyrus-sasl
Summary:	Simple Authentication and Security Layer library
Version:	2.1.26
Source0:	ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-%{version}.tar.gz
Source1:	saslauthd.xml
Patch0:		saslutil.c.patch
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3
Requires: %{pnm_requires_openssl}
BuildRequires: %{pnm_buildrequires_openssl}
# Requires: SFElibntlm
# BuildRequires: SFElibntlm-devel

%prep
%setup -q -n cyrus-sasl-%{version}
%patch0 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# needed to prevent an error during configure - strip whitespace
CFLAGS="%optflags -I/usr/gnu/include -I/usr/include/gssapi"
export CFLAGS="`echo $CFLAGS`"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"

./configure -prefix %{_prefix} \
           --enable-shared=yes \
           --enable-static=no \
           --with-dbpath=%{_sysconfdir}/sasldb2 \
           --with-plugindir=%{_libdir}/sasl2 \
           --sysconfdir=%{_sysconfdir} \
           --mandir %{_mandir} \
           --with-ipctype=doors

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/sasl2/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

mkdir -p $RPM_BUILD_ROOT/var/state/saslauthd
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/network
cp %{SOURCE1} $RPM_BUILD_ROOT/var/svc/manifest/network/saslauthd.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/sbin
%{_prefix}/sbin/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/sasl2
%{_libdir}/sasl2/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libsasl2.pc
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/sasl
%{_includedir}/sasl/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, sys) /var/state/
%dir %attr (0755, root, sys) /var/state/saslauthd

%defattr(-,root,sys)
%dir %attr (0755, root, sys) /var/svc
%class(manifest) %attr(0444, root, sys) /var/svc/manifest/network/saslauthd.xml

%changelog
* Tue Dec 08 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Include packagenamemacros.inc
- Change (Build)Requires SUNWopenssl-* to %{pnm_buildrequires_openssl}
* Wed Sep 05 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add saslauthd SMF manifest
- Add statedir lines
- Change basedir to /
* Wed Sep 04 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 2.1.26
- Update source URL
- Change legacy dependencies to IPS names
- Remove dependency on SFElibntlm
* Mon Dec 12 2011 - Milan Jurik
- bump to 2.1.25
* Sun Feb 13 2011 - Milan Jurik
- bump to 2.1.23
* Fri Oct 24 2008 - jedy.wang@sun.com
- Fixes plugindir problem.
* Fri Jun 06 2008 - river@wikimedia.org
- strip whitespace from $CFLAGS otherwise autoconf gets upset
* Sun Feb 03 2008 - moinak.ghosh@sun.com
- Add dependency on SFElibntlm.
* Tue Jan 15 2008 - moinak.ghosh@sun.com
- Initial spec.
