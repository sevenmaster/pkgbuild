#
# spec file for package SFEirker
#
# includes module(s): irker
#
#
#

##TODO## make SMF manifest for irkerd

%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEirker
IPS_Package_Name:	 network/irker
Summary:		 An IRC client that runs as a daemon accepting notification requests as JSON objects presented to a listening socket
Version:                 2.18
Source:                  http://www.catb.org/~esr/irker/irker-%{version}.tar.gz
Source2:                 irker.xml
##TODO## temporary patch
#Patch1:			 irker-1.12-urlparse.diff
Patch2:                  irker-02-2.18-use-syslog-stream-not-dev.diff
URL:                     http://www.catb.org/esr/irker
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
License:		BSD

%include default-depend.inc
Requires:                  %{pnm_requires_python_default}
BuildRequires:             %{pnm_buildrequires_python_default}
##TODO## need version independent package names
##TODO## alternatively a switch determining the platform default python version for these packages
#Requires:                  SFEpython%{python_major_minor}-argparse
#BuildRequires:             SFEpython%{python_major_minor}-argparse
#included in python2.7++ Requires:                  SFEpython26-argparse
#included in python2.7++ BuildRequires:             SFEpython26-argparse

#irclib in perl

%description
IRC relay daemon with server and client.
Mind setting start parameters to the irkerd daemon to get it listen to other then 127.0.0.1 in case you need to send remotely to irkerd. Change start/exec to have e.g. -h hostname 


%prep
%setup -q -n irker-%{version}
cp %{SOURCE2} irker.xml

#replace with explicit python version from %{python_major_minor_version}
perl -pi -e 's:^#! */usr/bin/python.*:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`
perl -pi -e 's:^#! */usr/bin/env *python:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`

#%patch1 -p1
%patch2 -p1

%build


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755              $RPM_BUILD_ROOT/%{_sbindir}
install -m    0755 irkerd       $RPM_BUILD_ROOT/%{_sbindir}/irkerd
install -d -m 0755              $RPM_BUILD_ROOT/%{_bindir}
install -m    0755 irk          $RPM_BUILD_ROOT/%{_bindir}/irk
install -m    0755 irkerhook.py $RPM_BUILD_ROOT/%{_bindir}/irkerhook.py

install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}/irker

for file in COPYING Makefile NEWS README filter-example.py filter-test.py hacking.txt install.txt irker-logo.png irkerd.service irkerd.xml irkerhook.xml org.catb.irkerd.plist security.txt
 do
##TODO## be next time more nice to executable scripts, okay?
 install            $file $RPM_BUILD_ROOT/%{_docdir}/irker/$file
 done

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network
cp irker.xml ${RPM_BUILD_ROOT}/var/svc/manifest/network/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/irker
%{_docdir}/irker/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/network
%class(manifest) %attr(0444, root, sys) /var/svc/manifest/network/irker.xml




%changelog
* Sun Dec 23 2018 - Thomas Wagner
- add patch2 irker-02-2.18-use-syslog-stream-not-dev.diff to always use on SunOS the StreamHandler for syslog
* Mon Feb 27 2018 - Thomas Wagner
- bump to 2.18
- remove support for python26 (remove (Build)Requires SFEpython26-argparse)
- only start irker once milestone multi-user-server is reached
* Sat Aug 15 2015 - Thomas Wagner
- bump to 2.15
- add (Build)Requires SFEpython26-argparse
* Thu Jan 23 2014 - Thomas Wagner
- bump to 2.5 (pyirclib is no longer a dependeny)
- add IPS_Package_Name
* Sat Mar 23 2013 - Thomas Wagner
- bump to 1.17
- remove patch1 irker-1.12-urlparse.diff
* Sat Oct 27 2012 - Thomas Wagner
- relocate irkerd to /usr/sbin/
- add SMF manifest (run irkerd as user nobody:nogroup)
* Thu Oct 25 2012 - Thomas Wagner
- initial spec
- use patch1 until code base includes fix for lazy urlparse
  which can't decode irc://
