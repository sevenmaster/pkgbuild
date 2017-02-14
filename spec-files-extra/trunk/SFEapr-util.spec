#No matching version of library/apr-15 can be installed:
#  Reject:  pkg://localhosts12/library/apr-15@1.5.1-0.5.12.0.0.0.79.1
#  Grund:  Diese Version wird durch die installierte Inkorporation consolidation/userland/userland-incorporation@5.12-5.12.0.0.0.95.0 ausgeschlossen

#
# spec file for package SFElibapr
#
#

##TODO## make 32-/64-bit package

%include Solaris.inc

%define local_apr_util_major_minor_version 1.5
%define libapr_major_minor_version 1.5
%define aprutil_version_package_string %( echo %{local_apr_util_major_minor_version} | sed -e 's?\.??g' )

#%include usr-gnu.inc
%define  _prefix %{_basedir}/apr-util/%{local_apr_util_major_minor_version}
%include base.inc

%include packagenamemacros.inc

%if %{solaris12}
exit 1
%endif
%if %{solaris11}
exit 1
%endif


Name:			SFEapr-util
License:		Apache,LGPL,BSD
#IPS_Package_Name:	library/gnu/apr-util-15
IPS_Package_Name:	library/apr-util-15
Group:                 Web Services/Application and Web Servers
Version:		1.5.4
#Summary:		Apache Portable Runtime Utility (APR-util) %{local_apr_util_major_minor_version} development header files and libraries (/usr/gnu)
Summary:		Apache Portable Runtime Utility (APR-util) %{local_apr_util_major_minor_version} development header files and libraries
Source:                 http://www.eu.apache.org/dist/apr/apr-util-%{version}.tar.bz2
Patch1:			apr-util-01-apr_common.m4.diff
Patch2:			apr-util-02-config.layout.diff
Patch3:			apr-util-03-doxygen.conf.diff
Patch4:			apr-util-04-makefile-out.diff
SUNW_Copyright:		%{name}.copyright

URL:			http://apr.apache.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
%include		default-depend.inc
#Requires: SFEgawk
BuildRequires:	SFElibapr-devel
Requires:	SFElibapr
BuildRequires:	%{pnm_buildrequires_SUNWsqlite3}
Requires:	%{pnm_requires_SUNWsqlite3}
BuildRequires:	%{pnm_buildrequires_SUNWsfwhea}
BuildRequires:  %{pnm_buildrequires_SUNWlexpt_devel}


#Note: Installs into /usr/gnu directories.

%description

Apache Portable Runtime (APR) provides software libraries
that provide a predictable and consistent interface to
underlying platform-specific implementations.

APR-util provides a number of helpful abstractions on top of APR.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
Requires:	%{pnm_buildrequires_SUNWsfwhea}
Requires:	SFElibapr-devel
Requires:	%{pnm_requires_SUNWsqlite3}    

%prep
%setup -q -n apr-util-%{version}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')  

export CFLAGS="%{optflags} -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="%{cxx_optflags} -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LDFLAGS="%{_ldflags}"

autoconf
./configure \
    --prefix=%{_prefix}    \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir}         \
    --infodir=%{_infodir}       \
    --with-apr=%{_basedir}/apr/%{libapr_major_minor_version}/bin/apr-1-config \
    --with-expat=/usr           \
    --with-sqlite3=/usr         \
    --without-odbc              \
    --enable-layout=Solaris	\
    CFLAGS="$(CFLAGS)"     \

#    --enable-debug \
#    CFLAGS="${CFLAGS}"     \
#    --with-dbm=gdbm \
#    --with-gdbm=/usr \
#    --with-pgsql=/usr \

#  done CONFIGURE_PREFIX=/usr/apr-util/1.5
#    51 CONFIGURE_OPTIONS +=	--with-mysql=/usr/mysql/5.5
#  done CONFIGURE_OPTIONS +=	--with-expat=/usr
#  done CONFIGURE_OPTIONS +=	--with-sqlite3=/usr
#    54 CONFIGURE_OPTIONS +=	--with-ldap=ldap_r-2.4
#    55 CONFIGURE_OPTIONS +=	--with-ldap-include=/usr/include/openldap
#  done CONFIGURE_OPTIONS +=	--without-odbc
#  done CONFIGURE_OPTIONS +=	CFLAGS="$(CFLAGS)"
#  done CONFIGURE_OPTIONS.32 +=	--enable-layout=Solaris
#    59 CONFIGURE_OPTIONS.64 +=	--enable-layout=Solaris-$(MACH64)
#  done CONFIGURE_OPTIONS.32 +=	--with-apr=/usr/apr/1.5/bin/apr-1-config
#    61 CONFIGURE_OPTIONS.64 +=	--with-apr=/usr/apr/1.5/bin/$(MACH64)/apr-1-config
#    62 CONFIGURE_OPTIONS.32 +=	MYSQL_CONFIG=/usr/mysql/5.5/bin/$(MACH32)/mysql_config
#    64 PATH=$(SPRO_VROOT)/bin:/usr/bin:/usr/gnu/bin
#    65 ifeq   ($(strip $(PARFAIT_BUILD)),yes)
#    66 PATH=$(PARFAIT_TOOLS):$(SPRO_VROOT)/bin:/usr/bin:/usr/gnu/bin
#    67 endif
#    69 COMPONENT_TEST_TARGETS= test
#    71 $(INSTALL_64): COMPONENT_POST_INSTALL_ACTION += \
#    72         cd $(SOURCE_DIR); \
#    73         sed 's;OUTPUT_DIRECTORY=.*;OUTPUT_DIRECTORY=$(PROTO_DIR)$(CONFIGURE_PREFIX);' \
#    74           docs/doxygen.conf | doxygen - ;
#
#    76 # Some patches need configure script recreation.
#    77 COMPONENT_PREP_ACTION += (cd $(@D); autoconf);
#    79 ASLR_MODE = $(ASLR_NOT_APPLICABLE)
#    81 configure:	$(CONFIGURE_32_and_64)



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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/apr-util-1/apr*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Apr 29 2016 - Thomas Wagner
- make spec file exit 1 on Solaris 11 and 12
* Mon Feb 16 2015 - Thomas Wagner
- make CFLAGS work
* Sun Jan 18 2015 - Thomas Wagner
- add copyright file
- build with gmake -j$CPUS
* Sat Jan 17 2015 - Thomas Wagner
- bump to 1.5.4
- prepared for /usr/gnu but commented out. Only OmniOS need the package, so build it similar then S11/OI.
- add patches from userland-gate
- add BuildRequires: %{pnm_buildrequires_SUNWlexpt_devel}
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
