#
# spec file for package SFEopenjdk7
#
# includes module(s): openjdk7
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define srcname openjdk7
%define major 7
%define minor 6
%define buildnum 24

Name:                    SFEopenjdk7
IPS_Package_Name:	 developer/java/openjdk-7
Summary:                 OpenJDK - open-source Java SE implementation
Group:                   Development/Java
Version:                 %{major}.0.%{minor}
URL:		         http://jdk7.java.net
Source:		         http://www.java.net/download/openjdk/jdk7u6/promoted/b24/openjdk-%{major}u%{minor}-fcs-src-b%{buildnum}-28_aug_2012.zip
License: 		 GPLv2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %pnm_buildrequires_java_runtime_default
BuildRequires: SUNWant 
BuildRequires:	SUNWcupsu
Requires:	SUNWcupsu
BuildRequires: SUNWfreetype2
Requires: SUNWfreetype2

%define jdkroot %{_prefix}/jdk/instances/jdk1.%{major}.0

%description
Java Platform, Standard Edition (Java SE) lets you develop and deploy
Java applications on desktops and servers, as well as in today's
demanding embedded environments. Java offers the rich user interface,
performance, versatility, portability, and security that today’s
applications require.

%prep
rm -rf openjdk
%setup -q -n openjdk

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ALT_COMPILER_PATH=/opt/sunstudio12.1/bin
export ALT_CUPS_HEADERS_PATH=/usr/include
export FULL_DEBUG_SYMBOLS=0
export BUILD_NUMBER=b%{buildnum}
export MILESTONE=%{minor}

make sanity
make all

%install
rm -rf $RPM_BUILD_ROOT
cd build/solaris-*/j2sdk-image
mkdir -p $RPM_BUILD_ROOT%{jdkroot}
cp -r * $RPM_BUILD_ROOT%{jdkroot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{jdkroot}
%{jdkroot}/*

%changelog
* Tue Dec 25 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
