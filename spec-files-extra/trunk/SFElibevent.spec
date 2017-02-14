#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc
%define _pkg_docdir %_docdir/libevent

Name:                SFElibevent-gnu
IPS_Package_Name:    library/gnu/libevent
Summary:             libevent - An event notification library for event-driven network servers. (/usr/gnu)
Version:             1.4.15
Source:              %{sf_download}/levent/libevent/libevent-1.4/libevent-%{version}-stable.tar.gz
URL:                 http://monkey.org/~provos/libevent/
License:             BSD
Group:               System/Libraries
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n libevent-%version-stable

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/libevent*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc README ChangeLog
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/event_rpcgen.py
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 - Thomas Wagner
- bump to 1.4.15
- relocate with usr-gnu.inc, Solaris 11.2 has library/libevent@1.4.14
* Thr Mar 17 2011 - Thomas Wagner
- fix ownergroup for %{_docdir}
* Mon Mar 14 2011 - Alex Viskovatoff
- use %optflags
* Mon Jan 10 2011 - Thomas Wagner
- new download URL, original site currently down
* Wed May 13 2010 - Milan Jurik
- bump to 1.4.13
* Mon May 10 2010 - Milan Jurik
- update to 1.4.10
* Wed Feb 25 2009 - alfred.peng@sun.com
- Bump to 1.4.9 and build with Sun Studio.
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* DOW MMM DD 2006 - Eric Boutilier
- Initial spec
