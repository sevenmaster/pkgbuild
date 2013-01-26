#
# spec file for package SFEscala
#
# includes module(s): scala
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define srcname scala

Name:                    SFEscala
IPS_Package_Name:	 runtime/java/scala
Summary:                 Scala - The Scala Programming Language
Group:                   Development/Scala
Version:                 2.10.0
URL:		         http://www.scala-lang.org/
Source:		         http://www.scala-lang.org/downloads/distrib/files/scala-%{version}.tgz
License: 		 BSD License
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %pnm_requires_java_runtime_default

%description
Scala is a general purpose programming language designed to express
common programming patterns in a concise, elegant, and type-safe
way. It smoothly integrates features of object-oriented and functional
languages, enabling Java and other programmers to be more
productive. Code sizes are typically reduced by a factor of two to
three when compared to an equivalent Java application.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/scala
mv man $RPM_BUILD_ROOT%{_datadir}
rm bin/*.bat
mv * $RPM_BUILD_ROOT%{_datadir}/scala
ln -s /usr/java/lib/tools.jar $RPM_BUILD_ROOT%{_datadir}/scala/lib/tools.jar
mkdir -p $RPM_BUILD_ROOT/usr/bin
for f in $RPM_BUILD_ROOT%{_datadir}/scala/bin/* ; do 
  ln -s %{_datadir}/scala/bin/`basename $f` $RPM_BUILD_ROOT/usr/bin/`basename $f`
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/scala
%{_datadir}/scala/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sat Jan 26 2013 - Logan Bruns <logan@gedanken.org>
- Updated to 2.10.0
* Sun Dec 16 2012 - Logan Bruns <logan@gedanken.org>
- Changed IPS package name from runtime/scala to runtime/java/scala.
* Sat Dec 15 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
