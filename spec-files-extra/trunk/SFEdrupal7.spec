#
# spec file for package: drupal6
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include packagenamemacros.inc

%define     src_name drupal
%define     targetdirname drupal
#set to blank if not text part like ".RC2" is in the version string. IPS can't handle non-numeric version strings
#mind to include a "dot" if non empty
#%define     src_name_minor_extra 
%define     src_name_minor_extra 
%define     apache2_majorversion 2
%define     apache2_version 2.2
#IPS_component_version: <numeric-only>

Name:                SFEdrupal7
IPS_Package_Name:	 web/service/drupal 
Summary:             Drupal - open-source content-management platform
Version:             7.63
License: 	     GPLv2
Source:              http://ftp.drupal.org/files/projects/drupal-%{version}%{src_name_minor_extra}.tar.gz
#Source2:             %{src_name}-htaccess-protect-backend
Source3:             %{name}.conf.example
URL:	             http://www.drupal.org
Group:		Web Services/Portals
SUNW_BaseDir:        /
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}%{src_name_minor_extra}-build
%include default-depend.inc

Requires:            %{pnm_requires_SUNWapch22}
Requires:            %{pnm_requires_SUNWapch22m_php52}
Requires:            %{pnm_requires_SUNWphp52_mysql}
Requires:            %{pnm_requires_SUNWphp52}
Meta(info.upstream):            http://www.drupal.org/
Meta(info.maintainer):          Thomas Wagner <tom68@users.sourceforge.net>
Meta(info.classification):      org.opensolaris.category.2008:Social Applications

##TEMP## enhance description, drupal basics
%description
Drupal CMS System
see http://pkgbuild.wiki.sourcefore.net/SFEdrupal7.spec for initial setup 
instructions regarding Solaris (TM) and see www.drupal.org for
drupal platform independent instructions.
Note: Only english language files included. Please install more languages yourself.


%prep
%setup -q -n drupal-%version
#%setup -q -c -T -a0 -n %{src_name}-%{version}%{src_name_minor_extra}
#cp -p %{SOURCE2} .

#copy example apache config
cp -p %{SOURCE3} .

##[ -f .htaccess.default ] && mv .htaccess.default .htaccess
##[ -f ._htaccess ] && mv ._htaccess .htaccess

#%build

#dummy - nothing to make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/
cp -p %{name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
cp -pr * $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#just in case we places an .htaccess or .htpasswd file here:
cp -pr .ht* $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#mv %{src_name}-htaccess-protect-backend $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/.htaccess
ln -s %{src_name}-%{version}%{src_name_minor_extra} $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (0640, webservd, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
     %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/*
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/.htaccess
#don't let drupal modify it's files - for security owned by root and not writable by the webservd userid
#places explicitly needed writable are system/logs, system/html, system/tmp
%defattr (0644, root, bin)
#example %dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/writable_file_this_is

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%class(renamenew) %{_sysconfdir}/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{name}.conf


%changelog
* Mon Feb  4 2019 - Thomas Wagner
- bump to 7.63 - Hotfix necessary after SA-CORE-2019-002
* Tue Dec 18 2018 - Thomas Wagner
- bump to 7.61 - Full compatibility with PHP 7.2
* Sat Oct 20 2018 - Thomas Wagner
- bump to 7.60 - Drupal core - Multiple vulnerabilities - SA-CORE-2018-006
* Thu Apr 26 2018 - Thomas Wagner
- bump to 7.59 - Drupal core - Drupal core - Highly critical - Remote Code Execution - SA-CORE-2018-002 CVE-2018-7602
* Sun Apr  1 2018 - Thomas Wagner
- bump to 7.58 - Drupal core - Highly Critical - Remote Code Execution - SA-CORE-2018-002
* Mon Mar 12 2018 - Thomas Wagner
- bump to 7.57 - Drupal Core - Critical - Multiple Vulnerabilities - SA-CORE-2018-001
* Thu Feb  2 2017 - Thomas Wagner
- bump to 7.56 - Drupal Core - Multiple Vulnerabilities - https://www.drupal.org/SA-CORE-2017-003
* Sun Dec 11 2016 - Thomas Wagner
- bump to 7.53 - Drupal Core - Issue #2821441 by davic, droplet, David_Rothstein, Joe Keene, Fabianx, tory-w: Fixed that newer Chrome versions cannot drag and drop anymore on desktop after 7.51 update when jQuery is updated to 1.7-1.11.0
* Fri Nov 18 2016 - Thomas Wagner
- bump to 7.52 - Drupal Core - Moderately Critical - Multiple Vulnerabilities - SA-CORE-2016-005 https://www.drupal.org/SA-CORE-2016-005
* Fri Oct  7 2016 - Thomas Wagner
- bump to 7.51 - small changes, read the changelog https://www.drupal.org/project/drupal/releases/7.51
* Wed Jul 13 2016 - Thomas Wagner
- bump to 7.50 - several changes, improved PHP7 support, read the changelog https://www.drupal.org/blog/drupal-7-50
* Thu Jun 15 2016 - Thomas Wagner
- bump to 7.44 - Drupal Core - Moderately Critical - Multiple Vulnerabilities - SA-CORE-2016-002
* Mon Feb 29 2016 - Thomas Wagner
- bump to 7.43 - Drupal Core - Critical - Multiple Vulnerabilities - SA-CORE-2016-001
* Thu Feb  4 2016 - Thomas Wagner
- bump to 7.42 - Maintenance release
* Thu Okt 22 2015 - Thomas Wagner
- bump to 7.41 - Drupal Core - Overlay - Less Critical - Open Redirect - SA-CORE-2015-004 https://www.drupal.org/SA-CORE-2015-004
* Fri Aug 21 2015 - Thomas Wagner
- bump to 7.40 - Maintenance release
* Wed Jun 17 2015 - Thomas Wagner
- bump to 7.38 - Drupal Core - Moderately Critical - Multiple Vulnerabilities - SA-CORE-2015-002 https://www.drupal.org/SA-CORE-2015-002 fixing CVE-2015-3234 CVE-2015-3232 CVE-2015-3233 CVE-2015-3231
* Sun May 10 2015 - Thomas Wagner
- bump to 7.37 - Maintenance release
* Fri Apr  3 2015 - Thomas Wagner
- bump to 7.36 - Maintenance release
* Fri Mar 20 2015 - Thomas Wagner
- bump to 7.35 - Drupal Core - Moderately Critical - Multiple Vulnerabilities - SA-CORE-2015-001 https://www.drupal.org/SA-CORE-2015-001
* Tue Dec  8 2014 - Thomas Wagner
- bump to 7.34 - Maintenance release
* Mon Nov 17 2014 - Thomas Wagner
- bump to 7.33 - Maintenance release
* Wed Okt 15 2014 - Thomas Wagner
- bump to 7.32 - SA-CORE-2014-005 - Drupal core - SQL injection (fix is also avail. as a patch) https://www.drupal.org/SA-CORE-2014-005
* Sun Aug 10 2014 - Thomas Wagner
- bump to 7.31 - SA-CORE-2014-004 - Drupal core - Denial of service XML-RPC https://www.drupal.org/SA-CORE-2014-004
* Wed Jul 16 2014 - Thomas Wagner
- bump to 7.29 SA-CORE-2014-003 - Drupal core - Multiple vulnerabilities Denial of service, Access bypass, Cross-site scripting https://www.drupal.org/SA-CORE-2014-003
- bump to 7.28 - bug fixes, 7.27: SA-CORE-2014-002 - Drupal core - Information Disclosure  https://drupal.org/SA-CORE-2014-002
* Wed Jan 22 2014 - Thomas Wagner
- bump to 7.26 - SA-CORE-2014-001 - Drupal core - Multiple vulnerabilities https://drupal.org/SA-CORE-2014-001
  Updrade strongly recommended
* Sat Nov 30 2013 - Thomas Wagner
- bump to 7.24 - SA-CORE-2013-003 - Drupal core - Multiple vulnerabilities https://drupal.org/SA-CORE-2013-003
* Wed Apr 10 2013 - Thomas Wagner
- bump to 7.22 - Maintenance release of the Drupal 7 series. Includes bugfixes and small API/feature improvements only (no major new functionality)
* Sun Mar 17 2013 - Thomas Wagner
- use cp instead of mv for the example apache config file (%install)
* Tue Mar 12 2013 - Thomas Wagner
- bump to 7.21 - Maintenance release of the Drupal 7 series. Includes fixes for incompatibilities introduced in the Drupal 7.20 security release only. Read the release notes for instructions!
* Thu Feb 21 2013 - Thomas Wagner
- bump to 7.20 - DRUPAL-SA-CORE-2013-002 - Drupal core - Denial of service (from remote, Image module)
* Thu Jan 17 2013 - Thomas Wagner
- bump to 7.19 - DRUPAL-SA-CORE-2013-001 - Drupal core - Multiple vulnerabilities:
  Cross-site scripting, Access bypass Book module, Access bypass Image module
  Security risk: Highly critical
* Wed Dec 19 2012 - Thomas Wagner
- bump to 7.18 - DRUPAL-SA-CORE-2012-004 - Drupal core - Multiple vulnerabilities:
  Access bypass (User module search - Drupal 6 and 7)
  Arbitrary PHP code execution (File upload modules - Drupal 6 and 7)
* Thu Nov  8 2012 - Thomas Wagner
- bump to 7.17 - bug fixes only
* Thu Oct 18 2012 - Thomas Wagner
- bump to 7.16 - DRUPAL-SA-CORE-2012-003 Security risk: Highly critical Exploitable from: Remote Vulnerability: Information Disclosure, Arbitrary PHP code execution
* Tue Sep 18 2012 - Thomas Wagner
- bump to 7.15 - bug fixes (no security fixes since 7.14)
* Sun May 06 2012 - Thomas Wagner
- bump to 7.14 - bug fixes + security fixes
* Thu Feb 23 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 7.12
* Fri Dec 30 2011 - Thomas Wagner
- bump to 7.10 - various fixes
* Fri Oct 31 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 7.9
* Fri Oct 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 7.8
* Sat Jul 30 2011 - Thomas Wagner
- bump to 7.7
* Sat Jul 16 2011 - Thomas Wagner
- bump to 7.4
* Sat Feb 12 2011 - Thomas Wagner
- initial version 7.0, derived form spec-files-jucr/specs/drupal6.spec
