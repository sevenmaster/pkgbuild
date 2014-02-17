# 
# 
# 
%include Solaris.inc
%include base.inc
%include packagenamemacros.inc

Name:                SFEmod-authnz-external
IPS_Package_Name:	 web/server/apache-22/module/apache-authnz_external
License:             Apache
Summary:             Apache External Authentication Modules
Version:             3.2.6
Source:				 http://mod-auth-external.googlecode.com/files/mod_authnz_external-%{version}.tar.gz
URL:                 http://code.google.com/p/mod-auth-external/
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{license}.copyright
Group:		     Applications/Internet
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		 %{pnm_buildrequires_apache2_default}
Requires:			 %{pnm_requires_apache2_default}

%description
Flexible tools for building custom basic authentication systems for the Apache HTTP Daemon.

%prep
%setup -q -n mod_authnz_external-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

make -j $CPUS build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/usr/apache2/2.2/libexec
install -c -m 0444 .libs/mod_authnz_external.so %{buildroot}/usr/apache2/2.2/libexec/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /usr/apache2/2.2/libexec
/usr/apache2/2.2/libexec/*

%changelog
* Mon Feb 17 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec version 3.2.6
