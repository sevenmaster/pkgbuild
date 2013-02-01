#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFErblcheck
IPS_Package_Name:    mail/rblcheck
Summary:             rblcheck - a simple tool for performing lookups in DNSBL.
Version:             1.5
URL:                 http://rblcheck.sourceforge.net
Source:              http://sourceforge.net/projects/rblcheck/files/rblcheck/%{version}/rblcheck-%{version}.tar.gz
License:      	     GPLv2
SUNW_Copyright:      SFErblcheck.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
rblcheck is a simple tool for performing lookups in DNS-based IP
address blacklist databases (DNSBL).This project continues the
development of that tool and helpful subsidiary tools (email filters,
etc).

%prep
%setup -q -n rblcheck-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Thu Jan 31 2012 - Logan Bruns <logan@gedanken.org>
- initial version
