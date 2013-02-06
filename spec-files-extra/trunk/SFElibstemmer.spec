#
# spec file for package SFElibstemmer
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

Name:                SFElibstemmer
IPS_Package_Name:    text/library/libstemmer
Summary:             libstemmer - snowball stemming algorithms
# below 520 is the apparent svn revision that the tgz matches
Version:             1.0.520
URL:                 http://snowball.tartarus.org
Source:              http://snowball.tartarus.org/dist/libstemmer_c.tgz
License:      	     BSD
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:       SFEgcc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n libstemmer_c

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC="gcc -fPIC"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp stemwords $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp libstemmer.o $RPM_BUILD_ROOT%{_libdir}/libstemmer.a
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp include/* $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libstemmer.a

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Feb 5 2013 - Logan Bruns <logan@gedanken.org>
- initial version
