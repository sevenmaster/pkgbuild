#
# spec file for package SFEopenjdk7
#
# includes module(s): openjdk7
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define major 7
%define minor 80
%define buildnum 05
%define srcname openjdk%{major}
%define tag jdk%{major}u%{minor}-b%{buildnum}

Name:                    SFEopenjdk%{major}
IPS_Package_Name:	 developer/java/openjdk-%{major}
Summary:                 OpenJDK - open-source Java SE implementation
Group:                   Development/Java
Version:                 %{major}.0.%{minor}.%{buildnum}
URL:		         http://jdk%{major}.java.net
#from openjdk9 JDK-8071501 http://hg.openjdk.java.net/jdk9/jdk9/hotspot/raw-rev/c3f28a6822dd
Patch1:                  openjdk-n-01-JDK-8071501-dd_fd.diff
License: 		 GPLv2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_java_runtime_default}
BuildRequires: %{pnm_buildrequires_SUNWant}
BuildRequires: %{pnm_buildrequires_SUNWcups_devel}
Requires:      %{pnm_requires_SUNWcups}
BuildRequires: %{pnm_buildrequires_SUNWmercurial}
BuildRequires: %{pnm_buildrequires_SUNWfreetype2}
Requires:      %{pnm_requires_SUNWfreetype2}
# OpenJDK's AWT uses deja vu as the default font for latin character set languages
##TODO## use pnm_macros for dejavu package
BuildRequires: system/font/truetype/dejavu
Requires:      system/font/truetype/dejavu
BuildRequires: %{pnm_buildrequires_SUNWaudh}
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
hg clone -r %{tag} http://hg.openjdk.java.net/jdk%{major}u/jdk%{major}u-dev %{srcname}
cd %{srcname}
gsed -i -e 's/hg clone/hg clone -r %{tag}/g' make/scripts/hgforest.sh
bash ./make/scripts/hgforest.sh clone

cd hotspot
%patch -p1
cd ..


%build
cd %{srcname}
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ALT_COMPILER_PATH=`dirname \`which CC\``
export ALT_CUPS_HEADERS_PATH=/usr/include
export FULL_DEBUG_SYMBOLS=0
export ALT_PARALLEL_COMPILE_JOBS=$CPUS

export BUILD_NUMBER=b%{buildnum}
export MILESTONE=%{minor}

%ifarch amd64 sparcv9
export ARCH_DATA_MODEL=64
make sanity
make all
mv build/solaris-*/j2sdk-image .
make clean
%else
mkdir j2sdk-image
%endif

export ARCH_DATA_MODEL=32
make sanity
make all
(cd build/solaris-*/j2sdk-image ; tar cf - .) | (cd j2sdk-image ; tar xf -)

# build cacerts
for f in /etc/certs/CA/*.pem ; do 
  keytool -importcert -noprompt -trustcacerts -keystore j2sdk-image/jre/lib/security/cacerts -storepass changeit -alias $f -file $f 
done

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
* Wed May 27 2015 - Thomas Wagner
- Updated to JDK 7u80b05
- change (Build)Requires to:  pnm_buildrequires_SUNWant, SUNWcups_devel, SUNWfreetype2, SUNWaudh, SUNWmercurial
- add Patch1 openjdk-n-01-JDK-8071501-dd_fd.diff
* Mon July 15 2013 - Logan Bruns <logan@gedanken.org>
- Updated to JDK 7u40b32.
* Mon Mar  4 2013 - Logan Bruns <logan@gedanken.org>
- Updated to JDK 7u15b02.
* Wed Feb 27 2013 - Logan Bruns <logan@gedanken.org>
- Populate cacerts with /etc/certs/CA/*.pem at build time.
- Updated to JDK 7u14b13.
* Fri Feb  8 2013 - Logan Bruns <logan@gedanken.org>
- Added 64 bit build.
- Added dependency on dejavu font for AWT apps. 
  (Different default platform font for OpenJDK.)
- Updated to JDK 7u14b12.
- Enabled use of newer sun compiler.
* Sat Jan 26 2013 - Logan Bruns <logan@gedanken.org>
- Updated to JDK 7u14b11. 
- Changed install path to /usr/jdk/instances/openjdk1.7.0.
* Tue Dec 25 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
