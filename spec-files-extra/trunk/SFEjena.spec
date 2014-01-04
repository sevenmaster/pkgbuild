#
# spec file for package SFEjena
#
# includes module(s): jena
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define srcname apache-jena

Name:                    SFEjena
IPS_Package_Name:	 database/jena
Summary:                 Jena - A free and open source Java framework for building Semantic Web and Linked Data applications
Group:                   System/Databases
Version:                 2.11.0
URL:		         http://jena.apache.org
Source:		         http://www.apache.org/dist/jena/binaries/apache-jena-%{version}.tar.gz
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


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
Apache Jena (or Jena in short) is a free and open source Java framework for building semantic web and Linked Data applications. The framework is composed of different APIs interacting together to process RDF data.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/jena
rm -rf bat lib-src javadoc-* src-examples
mv * $RPM_BUILD_ROOT%{_datadir}/jena
mkdir -p $RPM_BUILD_ROOT/usr/bin
for f in $RPM_BUILD_ROOT%{_datadir}/jena/bin/* ; do 
  ln -s %{_datadir}/jena/bin/`basename $f` $RPM_BUILD_ROOT/usr/bin/`basename $f`
done
gsed -i -e 's|^java|%java_home/bin/java|g' $RPM_BUILD_ROOT%{_datadir}/jena/bin/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/jena
%{_datadir}/jena/*

%changelog
* Fri Jan 3 2013 - Logan Bruns <logan@gedanken.org>
- Initial spec.
