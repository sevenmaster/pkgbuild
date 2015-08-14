#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_version  2.09

Name:                SFElzo
IPS_Package_Name:	library/lzo
Summary:             Lossless data compression library
License:             GPLv2
SUNW_Copyright:	     lzo.copyright
URL:                 http://www.oberhumer.com/opensource/lzo/
Meta(info.upstream): Markus F.X.J. Oberhumer <markus@oberhumer.com>
Version:             2.9
Group:               System/Libraries
Source:              http://www.oberhumer.com/opensource/lzo/download/lzo-%{src_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{src_version}-build
%include default-depend.inc

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

%prep
%setup -q -n lzo-%src_version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no \
            --enable-shared=yes

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/liblzo2.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_docdir
%_docdir/lzo

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/lzo

%changelog
* Fri Aug 14 2015 - Thomas Wagner
- bump to version 2.09 (2.9 on IPS)
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
- bump to 2.06
* Tue Aug  8 2011 - Alex Viskovatoff
- Package development files separately
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sat Jun 25 2011 - Alex Viskovatoff
- bump to 2.05
* Mon 29 2010 - Milan Jurik
- update to 2.03
*  Mars 25 2010 - Gilles Dauphin
- IPS compat versioning
* Wed Wep 27 2006 - Eric Boutilier
- Initial spec
