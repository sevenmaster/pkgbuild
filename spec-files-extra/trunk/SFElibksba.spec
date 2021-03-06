#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc

Name:                SFElibksba
IPS_Package_Name:	system/library/security/libksba
Summary:             A library to make X.509 certificates as well as the CMS (/usr/gnu)
License:             GPLv3
Group:		System/Libraries
SUNW_Copyright:	     libksba.copyright
URL:                 http://www.gnupg.org/related_software/libksba/index.en.html
Version:             1.3.4
Source:              ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %{omnios}
BuildRequires: %{pnm_buildrequires_SUNWlibgpg_error_devel}
Requires:      %{pnm_requires_SUNWlibgpg_error}
%else
BuildRequires: %{pnm_buildrequires_SUNWlibgpg_error_devel}
Requires:      %{pnm_requires_SUNWlibgpg_error}
Requires:      %{pnm_requires_SUNWtexi}
%endif

%prep
%setup -q -n libksba-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/libksba.*a
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/info/dir

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%changelog
* Sun Aug 13 2017 - Thomas Wagner
- change (Build)Requires to pnm_macros, %include packagenamemacros.inc
* Sun Oct 30 2016 - Thomas Wagner
- bump to 1.3.4
* Wed Oct  2 2013 - Thomas Wagner
- bump to 1.3.0
- fix %files
* Wed May 16 2012 - Thomas Wagner
- move to usr-gnu
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sat Apr 16 2011 - Alex Viskovatoff
- bump to 1.2.0
* Mars 24 2010 - rm in _prefix
* Sat Jul 11 2009 - Thomas Wagner
- bump to 1.0.7
* Sat Dec 29 2007 - jijun.yu@sun.com
- Initial spec
