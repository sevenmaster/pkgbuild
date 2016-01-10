#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Avoid conflict with system libtool
%include usr-gnu.inc

Name:                SFElibtool
IPS_package_name:    sfe/developer/build/libtool
Summary:             GNU libtool - library support utility
Group:		     Development/GNU
Version:             2.4.6
Source:              http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      SFExdialog.copyright
%include default-depend.inc

Requires: SUNWbash
Requires: SUNWpostrun

%prep
%setup -q -n libtool-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure \
    --prefix=%_prefix \
    --infodir=%_datadir/info \
    --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libltdl.la
# Updating info listings still seems to require user intervention
rm $RPM_BUILD_ROOT%_datadir/info/dir

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_includedir}/libltdl
%{_includedir}/libltdl/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %_mandir
%dir %attr (0755, root, bin) %_mandir/man1
%_mandir/man1/libtool.1
%_mandir/man1/libtoolize.1
%dir %attr (0755, root, bin) %{_datadir}/info
%{_datadir}/info/libtool.info
%{_datadir}/info/libtool.info-1
%{_datadir}/info/libtool.info-2
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/libtool
%{_datadir}/libtool/*

%changelog
* Sat Jan  9 2015 - Alex Viskovatoff
- Bump to 2.4.6
* Fri Sep 13 2013 - Alex Viskovatoff
- Update to 2.4.2
- Install in /usr/gnu so as not to coflict with system libtool
* Wed May 26 2010 - brian.cameron@oracle.com
- Bump to 2.2.6b.
* Sat May 24 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 2.2.4.  Add patch1 to use bash.
* Sun Mar 2 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 1.5.26.
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 1.5.24
- Use http url in Source.
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency.
* Sun Jan  7 2007 - laca@sun.com
- fix infodir permissions, update info dir file using postrun scripts
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
