#
# spec file for package xmlrpc-c
#
# includes module(s): xmlrpc-c
#

Name:                   xmlrpc-c
Summary:                A lightweight RPC library based on XML and HTTP (super stable version)
URL:                    http://xmlrpc-c.sourceforge.net/
Version:                1.25.26
IPS_component_version:	1.25.26
Source:                 %{sf_download}/%{name}/Xmlrpc-c%%20Super%%20Stable/%{version}/%{name}-%{version}.tgz
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-cplusplus		\
	    --disable-werror		\
	    --disable-warnings

make -j1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Oct 13 2013 - Thomas Wagner
- bump to 1.25.26
- IPS bring back IPS_component_version to regular format (needs manual 
  removal of version 1.632 IPS Packages from repo and system)
* Sat Mar 31 2012 - tropikhajma@gmail.com
- fix ips version and download location
* Thu Jan 15 2009 - halton.huo@sun.com
- Bump to 1.06.32
* Tue Jun 24 2008 - trisk@acm.jhu.edu
- Disable C++ compilation since results are not used
- Disable parallel make
* Sat May 24 2008 - trisk@acm.jhu.edu
- Initial base spec
