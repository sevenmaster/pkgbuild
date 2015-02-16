#
# spec file for package SFElibapr
#
#

##TODO## make 32-/64-bit package

%include Solaris.inc

%define libapr_major_minor_version 1.5
%define libapr_version_package_string %( echo %{libapr_major_minor_version} | sed -e 's?\.??g' )

#%include usr-gnu.inc
%define  _prefix %{_basedir}/apr/%{libapr_major_minor_version}
%include base.inc

%include packagenamemacros.inc

Name:			SFElibapr
License:		Apache,LGPL,BSD
#IPS_Package_Name:	library/gnu/apr-15
IPS_Package_Name:	library/apr-15
Version:		1.5.1
Group:			Web Services/Application and Web Servers
#Summary:		Apache Portable Runtime (APR) %{libapr_major_minor_version} Shared Libraries (/usr/gnu)
Summary:		Apache Portable Runtime (APR) %{libapr_major_minor_version} Shared Libraries
Source:                 http://www.eu.apache.org/dist/apr/apr-%{version}.tar.bz2
Patch1:			apr-01-apr_common.m4.diff
Patch2:			apr-02-config.layout.diff
Patch3:			apr-03-doxygen.conf.diff
Patch4:			apr-04-extended_file.diff
Patch5:			apr-05-largefile.diff
Patch6:			apr-06-libtool.m4.diff
Patch7:			apr-07-makefile-out.diff
Patch8:			apr-08-parfait.diff
SUNW_Copyright:		%{name}.copyright

URL:			http://apr.apache.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_basedir}
#Requires: SFEgawk
BuildRequires:	%{pnm_buildrequires_SUNWsfwhea}

#Note: Installs into /usr/gnu directories.

%description
The shared libraries for any component using Apache Portable
Runtime (APR) Version %{libapr_major_minor_version}

Apache Portable Runtime (APR) provides software libraries
that provide a predictable and consistent interface to
underlying platform-specific implementations.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
Requires:	%{pnm_buildrequires_SUNWsfwhea}

%prep
%setup -q -n apr-%{version}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')  

export CFLAGS="%{optflags} -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="%{cxx_optflags} -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LDFLAGS="%{_ldflags}"

#https://hg.openindiana.org/upstream/oracle/userland-gate/file/ebe894a8833e/components/apr-1_5/Makefile

autoconf

./configure \
    --prefix=%{_prefix}    \
    --sysconfdir=%{_sysconfdir} \
    --enable-shared        \
    --disable-static       \
    --with-pic             \
    --mandir=%{_mandir}    \
    --infodir=%{_infodir}  \
    --enable-threads       \
    --enable-other-child   \
    --enable-nonportable-atomics \
    --enable-layout=Solaris      \
    --with-installbuilddir=%{_prefix}/build \
    CFLAGS="$(CFLAGS) -DSSL_EXPERIMENTAL -DSSL_ENGINE" \
    LTFLAGS="--tag=CC --silent"  \

#    --enable-debug \
#    --enable-layout=Solaris\
#    --enable-layout=Solaris-$(MACH64)
#raus    --with-installbuilddir=%{_datadir}/apr/build \


#  done CONFIGURE_OPTIONS +=	--enable-threads
#  done CONFIGURE_OPTIONS +=	--enable-other-child
#  done CONFIGURE_OPTIONS +=	--enable-nonportable-atomics
#  done CONFIGURE_OPTIONS +=	--enable-shared
#  done CONFIGURE_OPTIONS +=	CFLAGS="$(CFLAGS) -DSSL_EXPERIMENTAL -DSSL_ENGINE"
#  done CONFIGURE_OPTIONS +=	LTFLAGS="--tag=CC --silent"
#  done CONFIGURE_OPTIONS.32 +=	--enable-layout=OpenSolaris
#    52 CONFIGURE_OPTIONS.64 +=	--enable-layout=OpenSolaris-$(MACH64)
#  done CONFIGURE_OPTIONS.32 +=	--with-installbuilddir=$(CONFIGURE_PREFIX)/build
#    54 CONFIGURE_OPTIONS.64 +=	--with-installbuilddir=$(CONFIGURE_PREFIX)/build/$(MACH64)



gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';' -print
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';' -print
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.exp" -exec rm -f {} ';' -print

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_prefix}/build
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/apr/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Mon Feb 16 2015 - Thomas Wagner
- make CFLAGS work (fixes core dump of SFEsubversion.spec)
* Sun Feb 15 2015 - Thomas Wagner
- add autoconf to get patches for configure into effect
* Sun Jan 18 2015 - Thomas Wagner
- add copyright file
- fix paths for "build" dir, build with gmake -j$CPUS
* Sat Jan 17 2015 - Thomas Wagner
- bump to 1.5.1
- prepared for /usr/gnu but commented out. Only OmniOS need the package, so build it similar then S11/OI.
- add patches from userland-gate
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
