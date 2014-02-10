#
# spec file for package SFEsiege
#

%include Solaris.inc

Name:		SFEsiege
IPS_Package_Name:	 diagnostic/siege
Summary:	HTTP load testing and benchmarking tool
Group:		Applications/Internet
URL:		http://www.joedog.org/siege-home/
Vendor:		Joe Dog Software (Jeff Fulmer)
Version:	3.0.5
License:	GPL
Source0:	http://www.joedog.org/pub/siege/siege-%{version}.tar.gz	

%define _prefix /usr

SUNW_Copyright:	siege.copyright
SUNW_BaseDir:	/
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

%description
Siege is an http load testing and benchmarking utility. It was designed to let web developers measure their code under duress, to see how it will stand up to load on the internet. Siege supports basic authentication, cookies, HTTP and HTTPS protocols. It lets its user hit a web server with a configurable number of simulated web browsers. Those browsers place the server “under siege.”

%prep
%setup -q -n siege-%{version}

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
./configure \
	--prefix=%{_prefix}

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=%buildroot
mkdir %buildroot%{_datadir}
mv %buildroot/usr/man %buildroot%{_datadir}
mv %buildroot/usr/etc %buildroot/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_sysconfdir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Sun Feb 09 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec at version 3.0.5
