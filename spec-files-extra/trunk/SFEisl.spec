#
# spec file for package SFEisl
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-gnu.inc

%define src_name   isl

Name:                SFEisl
IPS_Package_Name:    sfe/library/isl
Summary:             isl - An Integer Set Library for the Polyhedral Model
Version:             0.11.1
URL:                 http://freecode.com/projects/isl
Source:              ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{version}.tar.bz2
License:      	     MIT
SUNW_Copyright:      SFEisl.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgmp-devel
Requires: SFEgmp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description
isl is a thread-safe C library for manipulating sets and relations
of integer points bounded by affine constraints.  The descriptions of
the sets and relations may involve both parameters and existentially
quantified variables.  All computations are performed in exact integer
arithmetic using GMP.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}
            

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Feb 21 2013 - Logan Bruns <logan@gedanken.org>
- initial version
