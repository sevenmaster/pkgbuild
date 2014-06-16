#

#owner: Thomas Wagner
##TODO## modify to have daloradius.conf.php protected my something like renamenew for upgrading w/o erasing the old configuration settings. carefull to not let the .new file be read by simple http GET requests

%include Solaris.inc

%define     src_name daloradius
#%define     targetdirname daloradius
#set to blank if not text part like ".RC2" is in the version string. IPS can't handle non-numeric version strings
#mind to include a "dot" if non empty
#%define     src_name_minor_extra 
%define     src_name_minor_extra 
%define     apache2_majorversion 2
%define     apache2_version 2.2

Name:                SFEdaloradius
Summary:             Authentication, Authorization and Accounting based on FreeRadius with MySQL backend
Version:             0.9-9
IPS_component_version: $(echo %{version} | sed -e 's/-/./')
Source:              %{sf_download}/project/%{src_name}/%{src_name}/%{src_name}-%{version}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        /
URL:	             http://www.daloradius.com/
Source3:             %{src_name}.conf.example
BuildRoot:           %{_tmppath}/%{name}-%{version}%{src_name_minor_extra}-build
%include default-depend.inc

#Requires: SFEfreeradius
#Requires: *mysql*

#Requires: Apache2 and php

%description
Frontent to database for FreeRadius authentication and accounting.
Read the pkgbuild.wiki.sourceforge.net/SFEdaloradius.spec for setup
instructions on Solaris.

%prep
%setup -q -n %{src_name}-%{version}%{src_name_minor_extra}

#copy example apache config
cp -p %{SOURCE3} .


#$configValues['CONFIG_DB_TBL_RADUSERGROUP'] = 'radusergroup';
perl -pi -e 's:usergroup:radusergroup:' library/daloradius.conf.php*
#$configValues['CONFIG_FILE_RADIUS_PROXY'] = '/etc/freeradius/proxy.conf';
perl -pi -e 's:/etc/freeradius/proxy.conf:/etc/raddb/proxy.conf:' library/daloradius.conf.php*

#remove the config file (or change spec file to flag as %class(renamenew) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/library/daloradius.conf.php
#problem with that: file with extention .new would be created -> all variabes not protected by php interpreter from being displayed by simple http GET
rm library/daloradius.conf.php


#%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/
mv %{src_name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
cp -pr * $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#just in case we places an .htaccess or .htpasswd file here:
#cp -pr .ht* $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
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
#don't let daloradius modify it's files - for security owned by root and not writable by the webservd userid
#places explicitly needed writable are system/logs, system/html, system/tmp
%defattr (0644, root, bin)
#example %dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/writable_file_this_is

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%class(renamenew) %{_sysconfdir}/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf


%changelog
* Mon Jun 16 2014 - Thomas Wagner
- bump to 0.9-9 (0.9.9 on IPS)
* Sat Jan 14 2011 - Thomas Wagner
- initial version
