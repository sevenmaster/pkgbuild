#
# spec file for package SFEphantomjs
#
# includes module(s): phantomjs
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define srcname phantomjs
%define major 12.7
%define minor 1

Name:                    SFEphantomjs
IPS_Package_Name:	 network/phantomjs
Summary:                 PhantomJS - Headless WebKit
Group:                   Utility
Version:                 1.8.1
URL:		         http://phantomjs.googlecode.com
# OI has an old version of unzip that improperly processes the zip version use the tar.gz version instead
Source:		         http://github.com/ariya/phantomjs/archive/%{version}.tar.gz
#Source:		         http://phantomjs.googlecode.com/files/phantomjs-%{version}-source.zip
Patch1:                  phantomjs-01-mkspecs.diff
Patch2:                  phantomjs-02-yield.diff
Patch3:                  phantomjs-03-isnan.diff
Patch4:                  phantomjs-04-pthread_getattr.diff
Patch5:                  phantomjs-05-no_explicit_xopen_source.diff
License: 		 BSD
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and
native support for various web standards: DOM handling, CSS selector,
JSON, Canvas, and SVG.

%prep
rm -rf %srcname-%version
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

cd src/qt
./preconfig.sh --jobs $CPUS --qt-config "-platform solaris-g++"
cd ../..
./src/qt/bin/qmake
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin/
cp bin/phantomjs $RPM_BUILD_ROOT%{_prefix}/bin/
strip -x $RPM_BUILD_ROOT%{_prefix}/bin/phantomjs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/phantomjs
cp ChangeLog LICENSE.BSD README.md third-party.txt $RPM_BUILD_ROOT%{_datadir}/phantomjs
cp -r examples $RPM_BUILD_ROOT%{_datadir}/phantomjs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/phantomjs
%{_datadir}/phantomjs/*

%changelog
* Tue Feb 19 2013 - Logan Bruns <logan@gedanken.org>
- Updated to 1.8.1
* Fri Dec 7 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
