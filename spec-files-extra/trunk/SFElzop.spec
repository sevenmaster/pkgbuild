#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElzop
IPS_Package_Name:    compress/lzop
Summary:             File compressor -- similar to, but faster than gzip
IPS_Component_version: 1.4
Version:             1.04
Source:              http://www.lzop.org/download/lzop-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFElzo

%prep
%setup -q -n lzop-%{version}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags -I%{_includedir}"
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1



%changelog
* Sun 24 2018 - Thomas Wagner
- bump to 1.04 (IPS 1.4)
* Mars 25 2010 - Gilles dauphin
- compat IPS versioning
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
