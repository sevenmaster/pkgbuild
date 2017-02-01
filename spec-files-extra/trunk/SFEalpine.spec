# 
# spec file for package SFEalpine
# 
%include Solaris.inc
%include packagenamemacros.inc
%include arch64.inc

#%define tcl_version 8.4
#%define tcl_8_3 %(pkgchk -l SUNWTcl 2>/dev/null | grep /usr/sfw/bin/tclsh8.3 >/dev/null && echo 1 || echo 0)

# Don't use the default paths from arch64.inc so the 32-bit part is tidier
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%define src_name alpine

Name:                SFEalpine
IPS_Package_Name:	mail/alpine
License:             Apache
Summary:             Apache licensed PINE mail user agent
Version:             2.20
Source:              http://patches.freeiz.com/%{src_name}/release/src/%{src_name}-%{version}.tar.xz
#Patch2:             alpine-02-CC.diff
#Patch3:		   	 alpine-03-dirfd.diff
Patch2:				 alpine-2.20-02-Sun-CC.diff
Patch3:				 alpine-2.20-03-solaris-dirfd.diff
Patch4:				 alpine-2.20-04-freeiz-all.diff
URL:                 http://patches.freeiz.com/alpine/
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
Group:		      	 Office/Email
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_openssl}
Requires: %{pnm_requires_openssl}
BuildRequires: SUNWhea
Requires: SUNWcsl
#BuildRequires: SUNWTcl
BuildRequires: %{pnm_buildrequires_SUNWgawk}

%prep
%setup -q -n alpine-%{version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%ifarch amd64 sparcv9
cd ..
if [ -d %{src_name}-%{version}-64]; then
	rm -rf %{src_name}-%{version}-64
fi
cp -pr %{src_name}-%{version} %{src_name}-%{version}-64
cd %{src_name}-%{version}
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags"

#%if %tcl_8_3
#TCL_OPTS="--with-tcl-lib=tcl8.3"
#%else
#TCL_OPTS="--with-tcl-lib=tcl%{tcl_version}"
#%endif
# Disable Tcl until we figure out what to do with Web Alpine
TCL_OPTS=--without-tcl
SSL_CERTS_DIR=%{_sysconfdir}/openssl/certs
SSL_INCLUDE_DIR=%{_includedir}
SSL_LIB_DIR=%{_libdir}

export CC=${CC32:-$CC}
export CFLAGS="$CFLAGS32"
export LDFLAGS="$LDFLAGS32"

# Make 32-bit

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --with-system-pinerc=%{_sysconfdir}/pine.conf \
            --with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed \
            --with-passfile=.pine-passfile \
            --disable-debug \
            --with-debug-level=0 \
            --with-ssl-certs-dir=$SSL_CERTS_DIR \
            --with-ssl-include-dir=$SSL_INCLUDE_DIR \
            --with-ssl-lib-dir=$SSL_LIB_DIR \
            $TCL_OPTS

make -j$CPUS

# Make 64-bit

%ifarch amd64 sparcv9
export CC=${CC64:-$CC}
export CFLAGS="$CFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd ../%{src_name}-%{version}-64

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
			--mandir=%{_mandir} \
            --libdir=%{_libdir}/%{_arch64} \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
			--with-system-pinerc=%{_sysconfdir}/pine.conf \
			--with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed \
            --with-passfile=.pine-passfile \
            --disable-debug \
            --with-debug-level=0 \
			--with-ssl-certs-dir=$SSL_CERTS_DIR \
			--with-ssl-include-dir=$SSL_INCLUDE_DIR \
			--with-ssl-lib-dir=$SSL_LIB_DIR \
            $TCL_OPTS

make -j$CPUS
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%ifarch amd64 sparcv9
cd ../%{src_name}-%{version}-64
make DESTDIR=$RPM_BUILD_ROOT install
%endif

# 2017-02-01 - Renaming these binaries is probably not necessary.
 
#for prog in pico pilot rpdump rpload; do
#	mv $RPM_BUILD_ROOT%{_bindir}/$prog $RPM_BUILD_ROOT%{_bindir}/alpine-$prog
#	mv $RPM_BUILD_ROOT%{_mandir}/man1/$prog.1 $RPM_BUILD_ROOT%{_mandir}/man1/alpine-$prog.1
#done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/alpine
%{_bindir}/p*
%{_bindir}/r*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%endif

%changelog
* Wed Feb 01 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- 32/64-bit dual build for easy large file support
* Thu Jan 12 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 2.20
- change source
- add popular patches (based on Arch Linux AUR alpine package)
- 64-bit only build
* Mon Mar 24 2014 - ianj@tsundoku.ne.jp
- add patch3 to fix dirfd issue
- %include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_openssl}
- change BuildRequires to %{pnm_buildrequires_SUNWgawk}
- remove obsolete SUNWgawk define that depended on SVR4 packages
- change SSL_*_DIR variables to use system paths instead of SFW paths
* Mon Aug 10 2009 - matt@greenviolet.net
- Allow BuildRequires to accept SUNWgawk
- Remove autoconf, as source is unfriendly to newer versions and aclocal doesn't help.
* Mon Mar 02 2009 - Albert Lee
- Fix SSL support
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Fix link
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add license and grouping
* Mon May 12 2008 - trisk@acm.jhu.edu
- Bump to 1.10
* Sat Jan 05 2007 - Thomas Wagner
- bump to 1.00 - old dwnl file removed, no other changes to spec/patches
* Fri Dec 07 2007 - trisk@acm.jhu.edu
- Bump to 0.999999 (Six Nines), drop patch1
* Fri Nov 09 2007 - trisk@acm.jhu.edu
- Bump to 0.99999, replace patch1
* Sat Oct 13 2007 - laca@sun.com
- add patch for using $CC instead of /opt/SUNWspro/bin/cc
* Mon Oct 08 2007 - trisk@acm.jhu.edu
- Initial spec, should be friendly with SFEpine
