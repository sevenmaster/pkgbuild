#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:		SFEimlib2
IPS_Package_Name:	image/library/imlib2
Summary:	General image loading and rendering library
Group:		System/Multimedia Libraries
Version:	1.4.5
License:	BSD
SUNW_Copyright:	imlib2.copyright
Source:		%{sf_download}/enlightenment/imlib2-%{version}.tar.gz
Patch1:		imlib2-01-std99.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWxwplt
BuildRequires:	SFElibid3tag-devel
Requires:	SFElibid3tag

%prep
%setup -q -n imlib2-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
autoconf
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm ${RPM_BUILD_ROOT}%{_libdir}/imlib2/filters/*.la
rm ${RPM_BUILD_ROOT}%{_libdir}/imlib2/loaders/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, other) %{_libdir}/imlib2
%{_libdir}/imlib2/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Sun Feb 05 2012 - Milan Jurik
- bump to 1.4.5
* Thu Aug 26 2010 - brian.cameron@oracle.com
- Bump to 1.4.4.
* Mon Jan 05 2008 - brian.cameron@sun.com
- Bump to 1.4.2.
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Add support for Indiana builds.
* Tue Nov 07 2006 - Eric Boutilier
- Initial spec
