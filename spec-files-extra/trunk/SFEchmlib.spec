#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEchmlib
IPS_Package_Name:	library/desktop/chmlib
Summary:             A library for reading Microsoft .CHM files.
Version:             0.40
Group:		Desktop (GNOME)/Libraries
License:             LGPLv2.1+ and GPLv2+
SUNW_Copyright:      chmlib.copyright
Source:              http://www.jedrea.com/chmlib/chmlib-%{version}.tar.gz
URL:		     http://www.jedrea.com/chmlib/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n chmlib-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libchm.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libchm.a
rmdir ${RPM_BUILD_ROOT}%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/*.h

%changelog
* Wed Sep 25 2013 - Alex Viskovatoff
- place headers in seperate SVr4 package
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Fri Mar 05 2010 - Milan Jurik
- update to 0.40 
* Wed Dec 13 2006 - Eric Boutilier
- Initial spec
