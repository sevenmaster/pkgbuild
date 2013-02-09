#
# spec file for package SFEopenjdk8
#
# includes module(s): openjdk8
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define major 8
%define minor 0
%define buildnum 76
%define srcname openjdk%{major}
%define tag jdk%{major}-b%{buildnum}

Name:                    SFEopenjdk%{major}
IPS_Package_Name:	 developer/java/openjdk-%{major}
Summary:                 OpenJDK - open-source Java SE implementation
Group:                   Development/Java
Version:                 %{major}.0.%{minor}.%{buildnum}
URL:		         http://jdk%{major}.java.net
License: 		 GPLv2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEopenjdk7
BuildRequires: SUNWant 
BuildRequires:	SUNWcupsu
BuildRequires: SUNWmercurial
Requires:	SUNWcupsu
BuildRequires: SUNWfreetype2
Requires: SUNWfreetype2
# OpenJDK's AWT uses deja vu as the default font for latin character set languages
BuildRequires: system/font/truetype/dejavu
Requires: system/font/truetype/dejavu
BuildRequires: SUNWaudh
BuildRequires: SUNWxorg-headers

%define jdkroot %{_prefix}/jdk/instances/openjdk1.%{major}.0

%description
Java Platform, Standard Edition (Java SE) lets you develop and deploy
Java applications on desktops and servers, as well as in today's
demanding embedded environments. Java offers the rich user interface,
performance, versatility, portability, and security that today’s
applications require.

%prep
rm -rf %{srcname}
hg clone -r %{tag} http://hg.openjdk.java.net/jdk%{major}/jdk%{major} %{srcname}
cd %{srcname}
gsed -i -e 's/{hg} clone/{hg} clone -r jdk%{major}-b%{buildnum}/g' common/bin/hgforest.sh
bash ./common/bin/hgforest.sh clone

gsed -i -e 's/ -z defs//g' common/autoconf/generated-configure.sh

%build
cd %{srcname}
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export BUILD_NUMBER=b%{buildnum}
export MILESTONE=%{minor}

bash ./configure --prefix=%{jdkroot} \
                 --with-build-number=b%{buildnum} \
                 --with-boot-jdk=/usr/jdk/instances/openjdk1.7.0 \
                 --with-target-bits=32

make images JOBS=$CPUS ENABLE_FULL_DEBUG_SYMBOLS=0

mv build/solaris-*/images/j2sdk-image .

%ifarch amd64 sparcv9

make clean
rm -rf build

bash ./configure --prefix=%{jdkroot} \
                 --with-build-number=b%{buildnum} \
                 --with-boot-jdk=/usr/jdk/instances/openjdk1.7.0

make overlay-images JOBS=$CPUS ENABLE_FULL_DEBUG_SYMBOLS=0

(cd build/solaris-*/images/j2sdk-overlay-image ; tar cf - *) | (cd j2sdk-image ; tar xf -)

%endif

%install
cd %{srcname}
rm -rf $RPM_BUILD_ROOT
cd j2sdk-image
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
* Sat Feb  9 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
