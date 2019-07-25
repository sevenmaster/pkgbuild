##TODO## C++ bindings?

#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include usr-gnu.inc

%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

Name:		SFElibgpg-error-gnu
IPS_Package_Name: library/security/gnu/libgpg-error
Summary:	common error codes and error handling functions used by GnuPG (/usr/gnu)
Version:	1.36
Source:		ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-%{version}.tar.bz2
Patch1:         libgpg-error-01-10_gen-posix-lock-obj.patch
URL:		http://www.gnupg.org/
License:	GPLv3
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %{omnios}
%else
BuildRequires:	%{pnm_buildrequires_SUNWtexi}
Requires:	%{pnm_requires_SUNWtexi}
%endif

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}


%prep
%setup -q -n libgpg-error-%version

%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --enable-shared \
            --disable-static

#fix reserved variable namespace in gawk
#gawk: fatal: cannot use gawk builtin `namespace' as variable name
gsed -i.bak -e 's?namespace?Cnamespace?g' src/mkstrtable.awk src/Makefile

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/usr/share/info/dir
rm -rf $RPM_BUILD_ROOT/usr/gnu/share/info/dir

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%defattr (-, root, bin)
%dir %attr (-, root, bin) %{_datadir}/locale
%{_datadir}/locale/*
%dir %attr (-, root, other) %{_datadir}/common-lisp
%{_datadir}/common-lisp/*
%dir %attr (-, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr (-, root, bin) %{_datadir}/libgpg-error
%{_datadir}/libgpg-error/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*

#   1 package delivers 'dir group=bin mode=0755 owner=root path=usr/gnu/lib/pkgconfig':
     

%changelog
* Thu Jul 25 2019 - Thomas Wagner
- bump to version 1.36
- fix %files for pkgconfig
* Thu Apr 18 2019 - Thomas Wagner
- remove $RPM_BUILD_ROOT/usr/gnu/share/info/dir
* Wed Mar 13 2019 - Thomas Wagner
- use gcc for all platforms
- import patch libgpg-error-01-10_gen-posix-lock-obj.patch from solaris userland
* Sun Mar  3 2019 - Thomas Wagner
- bump to version 1.31
* Sun Aug 13 2017 - Thomas Wagner
- bump to version 1.27
- add IPS_Package_Name library/security/gnu/libgpg-error, change spec filename and SVR4 package name to -gnu
*               - Thomas Wagner
- Initial spec
- fix permissions for %{_datadir}/locale
