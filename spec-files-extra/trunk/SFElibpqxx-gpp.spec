#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                SFElibpqxx
IPS_Package_Name:    database/postgres/library/g++/libpqxx
Summary:             Official C++ client API for PostgreSQL.
Version:             4.0
URL:                 http://pqxx.org/development/libpqxx/
Source:              ftp://pqxx.org/software/libpqxx/libpqxx-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %(/usr/bin/pkginfo -q SFEpostgres-91-devel 2>/dev/null  && echo 1 || echo 0)
Requires:            SFEpostgres-91
BuildRequires:       SFEpostgres-91-devel
%else
Requires:            SUNWpostgr
BuildRequires:       SUNWpostgr-devel
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%if %(/usr/bin/pkginfo -q SFEpostgres-91-devel 2>/dev/null  && echo 1 || echo 0)
Requires:       SFEpostgres-91-devel
%else
Requires:       SUNWpostgr-devel
%endif

%prep
%setup -q -n libpqxx-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++ 
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

%if %(/usr/bin/pkginfo -q SFEpostgres-91-devel 2>/dev/null  && echo 1 || echo 0)
export PATH=$PATH:/usr/postgres/9.1/bin
%endif

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --enable-shared=yes \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Dec 23 2012 - Logan Bruns <logan@gedanken.org>
- Forked from sunstudio version
- Updated to 4.0
- Allow SFEpostgres-91(-devel) instead of just SUNWpostgr(-devel)
- Added IPS name
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Initial spec.
