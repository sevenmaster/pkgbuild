# spec file for package SFEgroovy
#

%include Solaris.inc
%define groovy_version 2.1.1


Name:                    SFEgroovy
IPS_Package_Name:	 runtime/java/groovy
Version:                 %{groovy_version}
Release:                 2
License:                 See: http://groovy.codehaus.org/license.html
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
Group:                   Development
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Summary:                 Contains the base system for executing groovy scripts.
Source:                  http://dist.codehaus.org/groovy/distributions/groovy-binary-%{groovy_version}.zip
BuildArch:               noarch
BuildRequires:           SUNWunzip

%define SFEopenjdk7     %(/usr/bin/pkginfo -q SFEopenjdk7  2>/dev/null && echo 1 || echo 0)

# Use openjdk7 if present instead of OI's older version of java
%if %SFEopenjdk7
Requires: SFEopenjdk7
%define java_home /usr/jdk/instances/openjdk1.7.0
%else
Requires:           %pnm_requires_java_runtime_default
%define java_home /usr/java
%endif

%description
Groovy is an object-oriented programming language for the Java Platform as an 
alternative to the Java programming language. It can be viewed as a scripting 
language for the Java Platform, as it has features similar to those of Python, 
Ruby, Perl, and Smalltalk. In some contexts, the name JSR 241 is used as an 
alternate identifier for the Groovy language.

%prep
%setup -n groovy-%{version}
rm bin/*.bat

%build

%install
install -d $RPM_BUILD_ROOT/usr/share/groovy/bin
install -p bin/* $RPM_BUILD_ROOT/usr/share/groovy/bin

install -d $RPM_BUILD_ROOT/usr/share/groovy/lib
install -p lib/* $RPM_BUILD_ROOT/usr/share/groovy/lib

install -d $RPM_BUILD_ROOT/usr/share/groovy/conf
install -p conf/* $RPM_BUILD_ROOT/usr/share/groovy/conf

install -d $RPM_BUILD_ROOT/usr/share/groovy/embeddable
install -p embeddable/* $RPM_BUILD_ROOT/usr/share/groovy/embeddable

install -d $RPM_BUILD_ROOT/usr/share/groovy/lib
install -p lib/* $RPM_BUILD_ROOT/usr/share/groovy/lib

gsed -i -e 's|earlyInit ( ) {|earlyInit ( ) {\n    GROOVY_HOME=/usr/share/groovy\nJAVA_HOME=%java_home\n|g' \
    $RPM_BUILD_ROOT/usr/share/groovy/bin/startGroovy

install -d $RPM_BUILD_ROOT/usr/bin
cd bin
for f in * ; do 
  ln -s /usr/share/groovy/bin/$f $RPM_BUILD_ROOT/usr/bin/$f
done

%clean
rm -rf "$RPM_BUILD_ROOT"

%post

%postun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/groovy
%{_datadir}/groovy/*

%changelog
* Sat Mar  1 2013 - Logan Bruns <logan@gedanken.org>
- Updated to 2.1.1.
- Added IPS name.
- Fixed permissions and updated dependencies.
* Sat Aug 17 2008 - rafael.alfaro@gmail.com
- Add license and group
* Mon Jun 25 2008 - rafael.alfaro@gmail.com
- Initial Spec File 
