# 
# nachsehen mit welchem Compiler das Python gebaut wurde, dann NUR diesen CC und leere CFLAGS angeben
# das python das mit dem fremden Compiler gebaut wurde das braucht die extra Behandlung
# cd lang/python
#   660  gmake V=2 -j1 PYTHONS=/usr/bin/python2 GPG=gpg2
# echo $?
# #compiler flags coming form actual python config for modules should be enough for now
#   663  gmake V=2 -j1 PYTHONS=/usr/bin/python3 GPG=gpg2 CC=cc CFLAGS=""
# echo $?
# cd ../..
# 
# 
# /usr/lib/python3.5/config-3.5m/Makefile:CCSHARED=       -Kpic
# /usr/lib/python3.5/_sysconfigdata.py: 'CCSHARED': '-Kpic',
# /usr/lib/python3.5/_sysconfigdata.py: 'CFLAGSFORSHARED': '-Kpic',
# /usr/lib/python3.5/_sysconfigdata.py:                   '-i -mr -xregs=no%frameptr  -I. -IInclude -I./Include -Kpic '
# vim /usr/lib/python3.5/config-3.5m/Makefile /usr/lib/python3.5/_sysconfigdata.py
# pwd
# vim Makefile
# vim /usr/lib/python2.7/config/Makefile /usr/lib/python2.7/_sysconfigdata.py


#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%if %( expr %{omnios} '|' %{oihipster} )
%define cc_is_gcc 1
%include base.inc
%endif

Name:                SFEgpgme
IPS_Package_Name:    library/security/gpgme
Summary:             A C wrapper library for GnuPG
Version:             1.11.1
Source:              ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2
Patch1:              gpgme-01-GNUPGHOME.patch

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWlibgpg_error}
Requires:      %{pnm_requires_SUNWlibgpg_error}
BuildRequires: SFEgnupg2
Requires:      SFEgnupg2
BuildRequires: SFElibassuan
Requires:      SFElibassuan


%prep
%setup -q -n gpgme-%version

%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
%endif

export CFLAGS="%optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags -lsocket -lnsl %{gnu_lib_path}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --disable-silent-rules \
            --enable-largefile \
            --enable-gpg-test \
            --enable-gpgsm-test \
            --enable-gpgconf-test \


gmake V=2 -j$CPUS GPG=gpg2

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libgpgme-pthread.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libgpgme-pth.la
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/info/dir

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
%{_libdir}/python*
%{_libdir}/cmake*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%{_includedir}/gpgme++/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%{_datadir}/common-lisp

%changelog
* Wed Mar 13 2019 - Thomas Wagner
- bump to 1.11.1
- import patch1 gpgme-01-GNUPGHOME.patch from solaris userland
- change (Build)Requires to pnm_macros, remove texi, add SFElibassuan
* Thu Oct 2 2008 - markwright@internode.on.net
- Remove lib/libgpgme-pth.la, if it is built.
* Tue Feb 26 2008 - jijun.yu@sun.com
- Remove a file.
* Wed Jan 02 2008 - jijun.yu@sun.com
- Remove the unused file. 
* Mon Dec 17 2007 - jijun.yu@sun.com
- Bump to 1.1.5 and add some files to the package.
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Add '-lsocket -lnsl' to LDFLAGS for the accept/recvmsg/connect functions.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
