#
# spec file for package PostgreSQL common
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc

%define _prefix /usr/postgres
%define _var_prefix /var/postgres
%define _basedir         %{_prefix}

Name:                    SFEpostgres-common
IPS_package_name:        database/postgres
Summary:	         PostgreSQL common packages
Version:                 1.0.0
License:		 PostgreSQL
#Url:                     http://www.postgresql.org/
#Source:			 http://wwwmaster.postgresql.org/redir/311/h/source/v%{tarball_version}/%{tarball_name}-%{tarball_version}.tar.bz2
#Source:                  http://ftp.postgresql.org/pub/source/v%{tarball_version}/%{tarball_name}-%{tarball_version}.tar.bz2
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            /
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	PostgreSQL Global Development Group
Meta(info.maintainer):	 	pkglabo.justplayer.com <taki@justplayer.com>

# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Database

%description
PostgreSQL package needs to add user and group.
This package make for common packages.

%prep
%build
%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/
%clean
rm -rf $RPM_BUILD_ROOT
%actions
group groupname="postgres"
user ftpuser=false gcos-field="PostgreSQL Reserved UID" username="postgres" password=NP group="postgres"

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) /var
%dir %attr (0755, postgres, postgres) %{_var_prefix}


%changelog
* Wed Jan 23 JST 2012 Fumihisa TONAKA <fumi.ftnk@gmail.com>
- fix %files to avoid conflict
* Tue Jan 25 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
