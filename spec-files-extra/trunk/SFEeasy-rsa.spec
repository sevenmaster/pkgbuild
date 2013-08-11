#
# spec file for package SFEeasy-rsa
#
# includes module(s): easy-rsa
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname easy-rsa

Name:                    SFEeasy-rsa
IPS_Package_Name:	 system/security/easy-rsa
Summary:                 Easy-Rsa - a small RSA key management package
Group:			 System/Security
Version:                 2.2.0
URL:		         http://www.openvpn.net
Source:		         http://github.com/OpenVPN/easy-rsa/archive/v%{version}.tar.gz
License: 		 GPLv2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
This is a small RSA key management package, based on the openssl
command line tool, that can be found in the easy-rsa subdirectory
of the OpenVPN distribution.  While this tool is primary concerned
with key management for the SSL VPN application space, it can also
be used for building web certificates.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

autoreconf -i
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_localstatedir}   \

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, bin)
%{_datadir}/%{srcname}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{srcname}

%changelog
* Sun Aug 11 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
