#
# spec file for package SFEgeoip
#
#
%include Solaris.inc
%include osdistro.inc

Name:		SFEgeoip
IPS_Package_Name:	library/geoip
Summary:	The GeoIP library and cli tools
Version:	1.4.8
Group:		System/Libraries
License:	LGPLv2.1+
SUNW_Copyright:	geoip.copyright
Source:		http://www.maxmind.com/download/geoip/api/c/GeoIP-%{version}.tar.gz
Patch1:		geoip-01-solaris.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n GeoIP-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %{SXCE}
libtoolize --copy --force
aclocal
automake -a -f
autoconf -f
%endif

./configure --prefix=%{_prefix}           \
            --bindir=%{_bindir}           \
            --sysconfdir=%{_sysconfdir}    \
            --libdir=%{_libdir}           \
            --includedir=%{_includedir}   \
            --mandir=%{_mandir}           \
            --infodir=%{_infodir}         \
            --disable-static              

%if %{SXCE}
sed -i -e 's?LIBTOOL =.*?LIBTOOL = /usr/bin/libtool?' `find . -type f -name Makefile`
%endif

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/GeoIP/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*

%files root
%defattr(-, root, sys)
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/*


%changelog
* Thu Apr 11 2013 - Thomas Wagner
- make use libtoolize/* conditional (S10/SXCE)
* Sun Dec 11 2011 - Milan Jurik
- bump to 1.4.8
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sat May 30 2009 - Andras Barna (andras.barna@gmail.com)
- bump to 1.4.6
* Tue Oct 28 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec.


