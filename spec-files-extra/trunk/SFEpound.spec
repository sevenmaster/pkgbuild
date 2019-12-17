##TODO## OpenSSL 1.1.x ... http://www.apsis.ch/pound/pound_list/archive/2018/2018-01/1515081171000#1515091575000

##
# spec file for package: pound
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

##TODO## make SMF manifest more nice, check for /etc/pound.cfg present

%include Solaris.inc
%include packagenamemacros.inc

Name:           SFEpound
IPS_Package_Name: web/proxy/pound
Group:		WebServices/ApplicationandWebServers
Summary:        The Pound program is a reverse proxy, load balancer and HTTPS front-end for Web server(s)
Version:        2.8
IPS_Component_Version: 2.8.0.1.0
License:        GPLv3
URL:            http://www.apsis.ch/pound/
Source:         http://www.apsis.ch/pound/Pound-%{version}.tgz
Source1:	%{name}-manifest.xml
Source2:	%{name}.cfg
Patch1:		pound-01-Makefile.in.diff
Patch2:		pound-02-BIO_read-cpu-load.diff
Distribution:	OpenSolaris
Vendor:		OpenSolaris Community

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): Robert Segall <roseg@apsis.ch>
Meta(info.maintainer): Thomas Wagner <tom68@users.sourceforge.net>
Meta(info.classification): org.opensolaris.category.2008:Applications/Internet


BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   /
SUNW_Copyright: %{name}.copyright


#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
#BuildRequires: SUNWbtool
#BuildRequires: SUNWggrp
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
Requires:      %{pnm_requires_SUNWopenssl}
Requires:      %{pnm_requires_SUNWlibms}
Requires:      %{pnm_requires_SUNWpcre}
Requires:      %{pnm_requires_SUNWzlib}
Requires:      %{pnm_requires_SUNWbzip}
BuildRequires: %{pnm_buildrequires_SUNWzlib}
Requires:      %{pnm_requires_SUNWzlib}
BuildRequires: %{pnm_buildrequires_SUNWbzip}
Requires:      %{pnm_requires_SUNWbzip}



%description
The Pound program is a reverse proxy, load balancer and
HTTPS front-end for Web server(s). Pound was developed
to enable distributing the load among several Web-servers
and to allow for a convenient SSL wrapper for those Web
servers that do not offer it natively.

%prep
%setup -q -n Pound-%{version}
%patch1 -p0
%patch2 -p1


%build
export CC=cc
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lmtmalloc"
export CFLAGS="%{optflags} -I/usr/sfw/include -I/usr/include/pcre"
./configure --prefix=%{_prefix} --sysconfdir=/etc || (cat config.log; false)

# regexec() in libpcreposix behaves differently than in libc
# libc version works properly with pound
#perl -pi -e 's/-lpcreposix//g' Makefile
#change hard-coded "gcc" binary to the  
#perl -pi -e 's/gcc/\${CC}/g' Makefile
gsed -i.bak -e '/^CC=/ d' Makefile

gmake V=2


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Install example config file
mkdir "${RPM_BUILD_ROOT}/etc/"
cp "%{SOURCE2}" "${RPM_BUILD_ROOT}/etc/pound.cfg.example"

#Install manifest
%define svcdir /var/svc/manifest/application/proxy
mkdir -p "${RPM_BUILD_ROOT}/%{svcdir}"
cp "%{SOURCE1}" "${RPM_BUILD_ROOT}/%{svcdir}/%{name}.xml"



%clean
rm -rf %{buildroot}

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif


%files
%defattr(-,root,sys)
%dir %attr (0755, root, bin) %{_sbindir}
%attr(0555, root, bin) %{_sbindir}/pound
%attr(0555, root, bin) %{_sbindir}/poundctl

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man8
%attr(0444, root, bin) %{_mandir}/man8/pound.8
%attr(0444, root, bin) %{_mandir}/man8/poundctl.8

%dir %attr(755,root,sys) /etc
#%config(noreplace) %attr(644,root,root) /etc/*
/etc/*

%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) %{svcdir}
%class(manifest) %attr (0444, root, sys) %{svcdir}/*

%dir %attr(0755, root, sys) %{_datadir}


%changelog
* Tue Dec 17 2019 - Thomas Wagner
- add patch2 pound-02-BIO_read-cpu-load.diff - avoid indefinite loop with BIO_read if connections die, may cause high cpu load
- fix Makefile CC=
* Sun Aug  5 2018 - Thomas Wagner
- bump to 2.8 release, IPS_Component_Version: 2.8.0.1.0
* Tue Feb 14 2017 - Thomas Wagner
- bump to 2.8a, add IPS_Component_Version 2.8.0.0.1 (once released, this gets 2.8.0.1.0 for a moment)
- refresh (Build)Requires to use pnm_macros. Not finished for old SVR4-only build environments.
* Mon Aug 11 2014 - Thomas Wagner
- add IPS_Package_Name
* Fri Aug  1 2014 - Thomas Wagner
- bump version to 2.6
- change to (Build)Requires to %{pnm_buildrequires_SUNWopenssl} SUNWzlib SUNWbzip, %include packagenamacros.inc
* Thr Sep 16 2010 - Thomas Wagner
- bump version to 2.5
- re-enable IPS manifest informations, change maintainer
- name the example config file /etc/pound.cfg.example
- fix %files globbing for config file, pound.cfg.example is no longer editable
* Thu Nov 26 2009 - Thomas Wagner
- ported to SFE
* Wed Aug 12 2009 - Robert Milkowski
- spec changes after jucr update
* Thu May 05 2009 - Robert Milkowski
- initial version
