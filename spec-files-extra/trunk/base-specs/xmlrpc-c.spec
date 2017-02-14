#
# spec file for package xmlrpc-c
#
# includes module(s): xmlrpc-c
#

Name:                   xmlrpc-c
Summary:                A lightweight RPC library based on XML and HTTP (super stable version)
URL:                    http://xmlrpc-c.sourceforge.net/
Version:                1.39.12
IPS_component_version:	1.39.12
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
* Mon Feb 13 2017 - Thomas Wagner
- bump to 1.39.12 (IPS: 1.39.12)
* Tue Aug 23 2016 - Thomas Wagner
- bump to 1.39.10 (IPS: 1.39.10)
* Sun Jun  5 2016 - Thomas Wagner
- bump to 1.39.08 (IPS: 1.39.8)
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Thu Jan  1 2015 - Thomas Wagner
- bump to 1.33.15
* Sun Oct 13 2013 - Thomas Wagner
- bump to 1.25.26
- IPS bring back IPS_component_version to regular format (needs manual 
  removal of version 1.632 IPS Packages from repo and system)
- add -std=c99
- relocate to /usr/gnu (S11 has own xmlrpc-c), add IPS_Package_Name
* Sat Mar 31 2012 - tropikhajma@gmail.com
- fix ips version and download location
* Thu Jan 15 2009 - halton.huo@sun.com
- Bump to 1.06.32
* Tue Jun 24 2008 - trisk@acm.jhu.edu
- Rename to SFExmlrpc-c since we don't distribute C++ libs
- Add CFLAGS_PERSONAL for Studio
- Disable C++ compilation since results are not used
- Disable parallel make
* Sat May 24 2008 - trisk@acm.jhu.edu
- Initial base spec
