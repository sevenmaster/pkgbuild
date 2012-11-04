#
# spec file for package SFEnagios-plugins
#
# includes module(s): nagios-plugins
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEnagios-plugins
Version:	1.4.16
Summary:	Nagios plugins
Group:		Applications/System
License:	GPLv2
URL:		http://www.nagios.org/
Source:		%{sf_download}/nagiosplug/nagios-plugins-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWsndm_devel}
Requires:	%{pnm_requires_SUNWsndm}
BuildRequires:	SFEnagios-devel
Requires:	SFEnagios
BuildRequires:	%{pnm_buildrequires_SUNWntp_devel}
Requires:	%{pnm_requires_SUNWntp}
BuildRequires:	SUNWbip
Requires:	SUNWbip
BuildRequires:	SUNWbindc
Requires:	SUNWbindc
BuildRequires:	SUNWnet-snmp-utils
Requires:	SUNWnet-snmp-utils
BuildRequires:	%{pnm_buildrequires_SUNWsmba_devel}
Requires:	%{pnm_requires_SUNWsmbau}
BuildRequires:	SFEperl-net-snmp
Requires:	SFEperl-net-snmp

%description
Provides Nagios plugins

%prep
%setup -q -n nagios-plugins-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch sparcv9
export CFLAGS="-I/usr/include/kerberosv5"
%else
export CFLAGS="%{optflags} -I/usr/include/kerberosv5"
export LDFLAGS="%{_ldflags}"
%endif

./configure \
	--with-cgiurl=/nagios/cgi-bin \
	--libexecdir=%{_libdir}/nagios/plugins \
	--with-libiconv-prefix=/usr/gnu \
	--disable-static \
	--enable-extra-opts

make -j$CPUS all

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

rm -r %{buildroot}%{_prefix}/local

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_libdir}

%changelog
* Sat Aug  4 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWsndm_devel}, %{pnm_buildrequires_SUNWntp_devel}, %{pnm_buildrequires_SUNWsmba_devel}, %include packagenamemacros.inc
* Sun Mar 06 2011 - Milan Jurik
- fix Solaris build
* Sat Mar 05 2011 - Milan Jurik
- initial spec
