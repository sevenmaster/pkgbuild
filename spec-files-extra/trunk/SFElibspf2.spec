#
# spec file for package SFElibspf2
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

Name:                SFElibspf2
IPS_Package_Name:    mail/library/libspf2
Summary:             libspf2 - implements the Sender Policy Framework
Version:             1.2.9
URL:                 http://www.spf2.org
Source:              http://www.libspf2.org/spf/libspf2-%{version}.tar.gz
License:      	     GPLv2 or BSD
SUNW_Copyright:      SFElibspf2.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n libspf2-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_bindir}/*_static

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
%{_libdir}/*

%changelog
* Thu Jan 31 2012 - Logan Bruns <logan@gedanken.org>
- initial version
