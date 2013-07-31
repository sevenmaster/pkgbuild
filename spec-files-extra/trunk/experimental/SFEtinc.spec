#
# spec file for package SFEtinc
#
# includes module(s): tinc
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define srcname tinc

Name:                    SFEtinc
IPS_Package_Name:	 system/network/tinc
Summary:                 tinc - a Virtual Private Network (VPN) daemon
Group:			 System/Security
Version:                 1.0.21
URL:		         http://www.tinc-vpn.org
Source:		         http://www.tinc-vpn.org/packages/tinc-%{version}.tar.gz
License: 		 GPLv2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:      SFEgcc
Requires:           SFEgccruntime
BuildRequires:      SUNWzlib
Requires:           SUNWzlib
BuildRequires:      SFElzo
Requires:           SFElzo
BuildRequires:      SFEtun
Requires:           SFEtun

%description
tinc is a Virtual Private Network (VPN) daemon that uses tunnelling
and encryption to create a secure private network between hosts on the
Internet. tinc is Free Software and licensed under the GNU General
Public License version 2 or later. Because the VPN appears to the IP
level network code as a normal network device, there is no need to
adapt any existing software. This allows VPN sites to share
information with each other over the Internet without exposing any
information to others.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_localstatedir}   \

echo "#include <limits.h>" >> config.h

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Wed July 31 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
