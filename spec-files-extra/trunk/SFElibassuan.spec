#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc
%include base.inc

%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

Name:		SFElibassuan
IPS_Package_Name:	system/library/security/gnu/libassuan
Summary:	An IPC libbray used by GnuPG 2, GPGME etc. (/usr/gnu)
Version:	2.0.3
URL:		http://www.gnupg.org/related_software/libassuan/
Source:		ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-%{version}.tar.bz2
URL:		http://www.gnupg.org/
License:	GPLv3+
SUNW_Copyright:	libassuan.copyright
Group:		System/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %{omnios}
BuildRequires: %{pnm_buildrequires_SUNWpth}
Requires: %{pnm_requires_SUNWpth}
BuildRequires: %{pnm_buildrequires_SUNWlibgpg_error}
Requires: %{pnm_requires_SUNWlibgpg_error}
%else
BuildRequires: %{pnm_buildrequires_SUNWpth}
Requires: %{pnm_requires_SUNWpth}
BuildRequires: %{pnm_buildrequires_SUNWlibgpg_error}
Requires: %{pnm_requires_SUNWlibgpg_error}
Requires: %{pnm_requires_SUNWtexi}
%endif

%description
Libassuan is a small library implementing the so-called Assuan protocol. This
protocol is used for IPC between most newer GnuPG components. Both server and
client side functions are provided. Assuan's primary use is to allow a client
to interact with a non-persistent server.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}


%prep
%setup -q -n libassuan-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --enable-shared \
            --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
[ -e $RPM_BUILD_ROOT%{_datadir}/info/dir ] && rm $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
#%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%changelog
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Wed Oct  2 2013 - Thomas Wagner
- %include usr-gnu.inc (S11 implements ver 2.0.1)
- change IPS_Package_Name, add /gnu/
- remove info/dir as it can't me merged with other existing content
- add (Build)Requires SUNWpth (2.0.7)
* Tue Feb 07 2012 - Milan Jurik
- bump to 2.0.3
* Wed Dec 01 2010 - Milan Jurik
- bump to 2.0.1
* Sat Jun 12 2010 - Milan Jurik
- bump to 2.0.0, make it shared only
* Mars 25 2010 - Gilles Dauphin
- build with pth, add --with-pth-prefix
* Sat Jul 11 2009 - Thomas Wagner
- bump to 1.0.5
* Sat Dec 29 2007 - jijun.yu@sun.com
- Initial spec
