#
# spec file for package PostgreSQL 9.2
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%include packagenamemacros.inc
%include buildparameter.inc

%define _prefix /usr/postgres
%define _var_prefix /var/postgres
%define tarball_name     postgresql
%define tarball_version  9.6.12
%define major_version	 9.6
#e.g.                    96
%define major_version_no_dot	 %( echo %{major_version} | sed -e 's?\.??g' )
%define _basedir         %{_prefix}/%{major_version}

#perl -V:ccdlflags | gsed -e "s?.*-R *??" -e "s?';??"
#omnios: /usr/perl5/5.16.1/lib/i86pc-solaris-thread-multi-64/CORE
#s11.3:  /usr/perl5/5.12/lib/i86pc-solaris-64int/CORE
%define libperl_so  %( /usr/bin/perl -V:ccdlflags | gsed -e "s?.*-R *??" -e "s?';??" -e 's?$?/libperl.so?' )
%define perl_32_bit %( file %{libperl_so} | grep -- "32-bit" > /dev/null && echo 1 || echo 0 )
%define perl_64_bit %( file %{libperl_so} | grep -- "64-bit" > /dev/null && echo 1 || echo 0 )

#omnios has no tcl
%define with_tcl %( expr %{omnios} '=' 1 >/dev/null && echo 0 || echo 1 )

Name:                    SFEpostgres-96
%define prefix_name      %{name}
IPS_package_name:        database/postgres-96
Summary:	         PostgreSQL client tools
Version:                 %tarball_version
License:		 PostgreSQL
Group:			 System/Databases
Url:                     http://www.postgresql.org/
Source:                  http://ftp.postgresql.org/pub/source/v%tarball_version/%tarball_name-%tarball_version.tar.bz2
Source1:		 postgres-major_version-postgres
Source2:		 postgres-96-postgresql_96.xml
Source3:		 postgres-92-auth_attr
Source4:		 postgres-92-prof_attr
Source5:		 postgres-major_version-exec_attr
Source6:		 postgres-92-user_attr
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            /usr
SUNW_Copyright:          SFEpostgres-92.copyright

BuildRequires: %{pnm_buildrequires_library_libedit}
Requires:      %{pnm_requires_library_libedit}

BuildRequires: %{pnm_buildrequires_library_security_openssl}
Requires:      %{pnm_requires_library_security_openssl}

%if %{with_tcl}
BuildRequires: runtime/tcl-8
%endif
Requires: %{prefix_name}-libs

BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:       %{pnm_requires_perl_default}

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	PostgreSQL Global Development Group
Meta(info.maintainer):	 	pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.classification):	System Database

%description
PostgreSQL is a powerful, open source object-relational database system. It has
more than 15 years of active development and a proven architecture that has
earned it a strong reputation for reliability, data integrity, and
correctness. It runs on all major operating systems, including Linux, UNIX (AIX,
BSD, HP-UX, SGI IRIX, Mac OS X, Solaris, Tru64), and Windows. It is fully ACID
compliant, has full support for foreign keys, joins, views, triggers, and stored
procedures (in multiple languages). It includes most SQL:2008 data types,
including INTEGER, NUMERIC, BOOLEAN, CHAR, VARCHAR, DATE, INTERVAL, and
TIMESTAMP. It also supports storage of binary large objects, including pictures,
sounds, or video. It has native programming interfaces for C/C++, Java, .Net,
Perl, Python, Ruby, Tcl, ODBC, among others, and exceptional documentation.

%package -n %{prefix_name}-libs

IPS_package_name: database/postgres-96/library
Summary: PostgreSQL client libraries

%package -n %{prefix_name}-pl
IPS_package_name: database/postgres-96/language-bindings
Summary: PostgreSQL additional Perl, Python & TCL server procedural languages

Requires: %{name}
Requires: %{prefix_name}-libs

%package -n %{prefix_name}-devel
IPS_package_name: database/postgres-96/developer
Summary: PostgreSQL development tools and header files

Requires: %{name}
Requires: %{prefix_name}-libs

%package -n %{prefix_name}-docs
IPS_package_name: database/postgres-96/documentation
Summary: PostgreSQL documentation and man pages

%package -n %{prefix_name}-server
IPS_package_name: service/database/postgres-96
Summary: PostgreSQL database server

%define _basedir         /
SUNW_Basedir:            %{_basedir}

Requires: %{name}
Requires: %{prefix_name}-libs
BuildRequires: SFEpostgres-common
Requires: SFEpostgres-common

%package -n %{prefix_name}-contrib
IPS_package_name: database/postgres-96/contrib
Summary: PostgreSQL community contributed tools not part of core product

Requires: %{name}
Requires: %{prefix_name}-libs

%prep
%setup -c -n %{tarball_name}-%{tarball_version}
#%patch1 -p0

%ifarch amd64 sparcv9
rm -rf %{tarball_name}-%{tarball_version}-64
cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
%endif

%build

#get 2048MB mem per CPU
#get 768MB mem per CPU
#get 1536 mem per CPU to try lower /tmp/ usage by the compiler (trick)
#set TMPDIR to place large compiler tempfiles to /var/tmp/ instead of smallish /tmp
#and to not steal valuable memory from the compiler running in memory
export TMPDIR=%{_builddir}/compilertmpdir-%{name}
mkdir -p ${TMPDIR}
CPUS=%{_cpus_memory_2048}

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CCAS=cc
export CCASFLAGS=
export CC=cc
#export CFLAGS="-i -xO4 -xspace -xstrconst -Kpic -xregs=no%frameptr -xCC"
#getting hughe files form compiler, explodes /tmp residing in swap and being limited in size
#use local storage. Listing doesn't show the miximum size, only what has been catched during the compile
#could be the case that solaris studio 12.3 is a bit old. cc: Sun C 5.12 SunOS_i386 2011/11/16
#-rw-r--r--   1 sfe staff   9115153 Jul 11 17:01 acomp.1499784967.15585.02.sd
#-rw-r--r--   1 sfe staff 315490504 Jul 11 17:03 iropt.1499784967.15585.03.ir
#-rw-r--r--   1 sfe staff 742051468 Jul 11 17:01 acomp.1499784967.15585.01.ir
export CFLAGS="-i -xO3 -xspace -xstrconst -Kpic -xregs=no%frameptr -xCC -temp=${TMPDIR}"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -lncurses"
export LD_OPTIONS="-R/usr/gnu/lib -L/usr/gnu/lib"

%if %{perl_32_bit}
PERLCONFIG="--with-perl"
%else
PERLCONFIG=""
%endif

./configure --prefix=%{_prefix}/%{major_version} \
            --exec-prefix=%{_prefix}/%{major_version} \
            --bindir=%{_prefix}/%{major_version}/bin \
            --libexecdir=%{_prefix}/%{major_version}/bin \
            --sbindir=%{_prefix}/%{major_version}/bin \
            --datadir=%{_prefix}/%{major_version}/share \
            --sysconfdir=%{_prefix}/%{major_version}/etc \
            --mandir=%{_prefix}/%{major_version}/man \
            --libdir=%{_prefix}/%{major_version}/lib \
            --includedir=%{_prefix}/%{major_version}/include \
            --sharedstatedir=%{_var_prefix}/%{major_version} \
            --localstatedir=%{_var_prefix}/%{major_version} \
            --localedir=%{_prefix}/%{major_version}/share/locale/ \
            --enable-nls \
            --docdir=%{_prefix}/%{major_version}/doc \
            --with-system-tzdata=/usr/share/lib/zoneinfo \
            $PERLCONFIG \
            --with-python \
            --with-pam \
            --with-openssl \
            --with-libedit-preferred \
            --with-libxml \
            --with-libxslt \
            --with-gssapi \
            --enable-thread-safety \
            --enable-dtrace \
            --with-includes=/usr/gnu/include:/usr/include \
%if %{with_tcl}
            --with-tcl \
            --with-tclconfig=/usr/lib \
%endif
            --with-libs=/usr/gnu/lib:/usr/lib \


gmake -j$CPUS world || { echo "Probably out of memory. Re-try with CPUS=1."; gmake V=2 -j1; }

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64

#export CFLAGS="%optflags64"
##TODO## -xO5 testen
export CFLAGS="-m64 -i -xO3 -xspace -xstrconst -Kpic -xregs=no%frameptr -xCC -temp=${TMPDIR}"
export LDFLAGS="%_ldflags -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -lncurses"
#we aren't using the normal include schemas to get 32-/64-bit dual builds, so fix it here
export LDFLAGS=$( echo ${LDFLAGS}  | sed -e 's/-m32/-m64/g' )
#ld complaining: ld: warning: option '-R/usr/sfw/lib/%{_arch64}:/usr/gnu/lib/amd64' is incompatible with building a relocatable object, option ignored
export LD_OPTIONS="-R/usr/gnu/lib/%{_arch64} -L/usr/gnu/lib/%{_arch64}"

%if %{perl_64_bit}
PERLCONFIG="--with-perl"
%else
PERLCONFIG=""
%endif

./configure --prefix=%{_prefix}/%{major_version} \
            --exec-prefix=%{_prefix}/%{major_version} \
            --bindir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --libexecdir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --sbindir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --datadir=%{_prefix}/%{major_version}/share \
            --sysconfdir=%{_prefix}/%{major_version}/etc \
            --mandir=%{_prefix}/%{major_version}/man \
            --libdir=%{_prefix}/%{major_version}/lib/%{_arch64} \
            --includedir=%{_prefix}/%{major_version}/include \
            --sharedstatedir=%{_var_prefix}/%{major_version} \
            --localstatedir=%{_var_prefix}/%{major_version} \
            --localedir=%{_prefix}/%{major_version}/share/locale/ \
            --enable-nls \
            --docdir=%{_prefix}/%{major_version}/doc \
            --with-system-tzdata=/usr/share/lib/zoneinfo \
            $PERLCONFIG \
            --with-python \
            --with-pam \
            --with-openssl \
            --with-libedit-preferred \
            --with-libxml \
            --with-libxslt \
            --with-gssapi \
            --enable-thread-safety \
            --enable-dtrace \
            DTRACEFLAGS='-64' \
            --with-includes=/usr/gnu/include:/usr/include \
%if %{with_tcl}
            --with-tcl \
            --with-tclconfig=/usr/lib \
%endif
            --with-libs=/usr/gnu/lib/%{_arch64}:/usr/lib/%{_arch64} \


gmake -j$CPUS world || { echo "Probably out of memory. Re-try with CPUS=1."; gmake V=2 -j1; }

%endif

%install
rm -rf %buildroot

cd %{tarball_name}-%{tarball_version}
gmake install-world DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64
gmake install-world DESTDIR=$RPM_BUILD_ROOT
#link 64 -> %{_arch64} or 64 -> sparcv9   - makes SMF manifest / method file more easy
ln -fs %{_arch64} $RPM_BUILD_ROOT%{_prefix}/%{major_version}/bin/64
ln -fs %{_arch64} $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/64
%endif

mkdir -p $RPM_BUILD_ROOT/etc/security
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/backups
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/data
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/data_64

mkdir -p $RPM_BUILD_ROOT/lib/svc/method/
#cp %{SOURCE1} $RPM_BUILD_ROOT/lib/svc/method/postgres_96
gsed -e 's/@@MAJOR_DOT_MINOR@@/%{major_version}/g' < %{SOURCE1} > $RPM_BUILD_ROOT/lib/svc/method/postgres_%{major_version_no_dot}
chmod +x $RPM_BUILD_ROOT/lib/svc/method/postgres_%{major_version_no_dot}
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/application/database/
##TODO## replace cp with gsed -e 's/@@MAJOR_DOT_MINOR@@/%{major_version}/g' < %{SOURCE2} > $RPM_BUILD_ROOT/var/svc/manifest/application/database/postgresql_%{major_version_no_dot}.xml
#cp %{SOURCE2} $RPM_BUILD_ROOT/var/svc/manifest/application/database/postgresql_96.xml
gsed -e 's/@@MAJOR_DOT_MINOR@@/%{major_version}/g' < %{SOURCE2} > $RPM_BUILD_ROOT/var/svc/manifest/application/database/postgresql_%{major_version_no_dot}.xml

# attribute
mkdir -p $RPM_BUILD_ROOT/etc/security/auth_attr.d/
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/security/auth_attr.d/service\%2Fdatabase\%2Fpostgres-96
mkdir -p $RPM_BUILD_ROOT/etc/security/exec_attr.d/
cp %{SOURCE4} $RPM_BUILD_ROOT/etc/security/exec_attr.d/service\%2Fdatabase\%2Fpostgres-96
mkdir -p $RPM_BUILD_ROOT/etc/security/prof_attr.d/
##TODO## replace cp with 
#cp %{SOURCE5} $RPM_BUILD_ROOT/etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-96
gsed -e 's/@@MAJOR_MINOR_VERSION@@/%{major_version}/g' < %{SOURCE5} > $RPM_BUILD_ROOT/etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-%{major_version_no_dot}

mkdir -p $RPM_BUILD_ROOT/etc/user_attr.d/
cp %{SOURCE6} $RPM_BUILD_ROOT/etc/user_attr.d/service\%2Fdatabase\%2Fpostgres-96


mkdir -p $RPM_BUILD_ROOT/usr/share

# delete %{_arch64}
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/*.a


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# make symbolic link

mkdir -p $RPM_BUILD_ROOT/usr/bin/%{_arch64}
cd $RPM_BUILD_ROOT/usr/bin/
ln -fs ../postgres/%{major_version}/bin/clusterdb .
ln -fs ../postgres/%{major_version}/bin/createdb .
ln -fs ../postgres/%{major_version}/bin/createlang .
ln -fs ../postgres/%{major_version}/bin/createuser .
ln -fs ../postgres/%{major_version}/bin/dropdb .
ln -fs ../postgres/%{major_version}/bin/droplang .
ln -fs ../postgres/%{major_version}/bin/dropuser .
ln -fs ../postgres/%{major_version}/bin/ecpg .
ln -fs ../postgres/%{major_version}/bin/initdb .
ln -fs ../postgres/%{major_version}/bin/oid2name .
ln -fs ../postgres/%{major_version}/bin/pg_archivecleanup .
ln -fs ../postgres/%{major_version}/bin/pg_basebackup .
ln -fs ../postgres/%{major_version}/bin/pg_config .
ln -fs ../postgres/%{major_version}/bin/pg_controldata .
ln -fs ../postgres/%{major_version}/bin/pg_ctl .
ln -fs ../postgres/%{major_version}/bin/pg_dump .
ln -fs ../postgres/%{major_version}/bin/pg_dumpall .
ln -fs ../postgres/%{major_version}/bin/pg_resetxlog .
ln -fs ../postgres/%{major_version}/bin/pg_restore .
ln -fs ../postgres/%{major_version}/bin/pg_receivexlog .
ln -fs ../postgres/%{major_version}/bin/pg_standby .
ln -fs ../postgres/%{major_version}/bin/pg_test_fsync .
ln -fs ../postgres/%{major_version}/bin/pg_test_timing
ln -fs ../postgres/%{major_version}/bin/pg_upgrade .
ln -fs ../postgres/%{major_version}/bin/pgbench .
%if %{with_tcl}
ln -fs ../postgres/%{major_version}/bin/pltcl_delmod .
ln -fs ../postgres/%{major_version}/bin/pltcl_listmod .
ln -fs ../postgres/%{major_version}/bin/pltcl_loadmod .
%endif
ln -fs ../postgres/%{major_version}/bin/postgres .
ln -fs ../postgres/%{major_version}/bin/postmaster .
ln -fs ../postgres/%{major_version}/bin/psql .
ln -fs ../postgres/%{major_version}/bin/reindexdb .
ln -fs ../postgres/%{major_version}/bin/vacuumdb .
ln -fs ../postgres/%{major_version}/bin/vacuumlo .
ln -fs ../postgres/%{major_version}/bin/pg_xlogdump .
ln -fs ../postgres/%{major_version}/bin/pg_isready .
ln -fs ../postgres/%{major_version}/bin/pg_recvlogical .
ln -fs ../postgres/%{major_version}/bin/pg_rewind .


cd $RPM_BUILD_ROOT/usr/bin/%{_arch64}
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/clusterdb .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/createdb .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/createlang .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/createuser .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/dropdb .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/droplang .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/dropuser .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/ecpg .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/initdb .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/oid2name .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_archivecleanup .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_basebackup .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_config .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_controldata .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_ctl .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_dump .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_dumpall .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_resetxlog .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_restore .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_receivexlog .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_standby .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_test_fsync .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_test_timing
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_upgrade .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pgbench .
%if %{with_tcl}
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pltcl_delmod .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pltcl_listmod .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pltcl_loadmod .
%endif
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/postgres .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/postmaster .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/psql .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/reindexdb .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/vacuumdb .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/vacuumlo .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_xlogdump .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_isready .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_recvlogical .
ln -fs ../postgres/%{major_version}/bin/%{_arch64}/pg_rewind .

# plpython is out in postgresql 9.2
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plpython-%{major_version}.mo

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/clusterdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/createdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/createlang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/createuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/dropdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/droplang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/dropuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_basebackup
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_dump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_dumpall
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_restore
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_test_fsync
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_test_timing
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/vacuumdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/reindexdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/psql
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_xlogdump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_isready
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_recvlogical
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_rewind
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/psql
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/clusterdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createlang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/dropdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/droplang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/dropuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_basebackup
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_dump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_dumpall
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_restore
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_test_fsync
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_test_timing
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/reindexdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/vacuumdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_xlogdump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_isready
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_recvlogical
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_rewind
#%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/64

%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/clusterdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/createdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/createlang
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/createuser
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/dropdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/droplang
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/dropuser
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_basebackup
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_dump
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_dumpall
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_restore
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_test_fsync
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_test_timing
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/vacuumdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/reindexdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_xlogdump
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_isready
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_recvlogical
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/psql
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_rewind
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/psql
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/clusterdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/createdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/createlang
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/createuser
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/dropdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/droplang
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/dropuser
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_basebackup
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_dump
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_dumpall
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_restore
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_test_fsync
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_test_timing
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/reindexdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/vacuumdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_xlogdump
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_isready
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_recvlogical
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_rewind

%attr (0644, root, other) %{_prefix}/%{major_version}/share/psqlrc.sample
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_basebackup-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_rewind-%{major_version}.mo


%files -n %{prefix_name}-libs
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man/man5
#removed %attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgport.a
#removed %attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpq.a
#removed %attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg.a
#removed %attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.a
#removed %attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.a
#removed %attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgcommon.a
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/auth_delay.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/file_fdw.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/libecpg.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/libpq.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/libpgtypes.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/libecpg_compat.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pg_prewarm.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/postgres_fdw.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/test_decoding.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/auth_delay.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/file_fdw.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so*
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pg_prewarm.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/postgres_fdw.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/test_decoding.so


 
%files -n %{prefix_name}-pl
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/extension
%if %{with_tcl}
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_listmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_loadmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_delmod
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pltcl_listmod
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pltcl_loadmod
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pltcl_delmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pltcl_delmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pltcl_listmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pltcl_loadmod
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pltcl.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/pltcl.so
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/unknown.pltcl
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pltcl_delmod
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pltcl_listmod
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pltcl_loadmod
%endif
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plperl-%{major_version}.mo
#%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plpython-%{major_version}.mo
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/plpython.so
%if %{perl_32_bit}
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plperl.so
%endif
%if %{perl_64_bit}
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/plperl.so
%endif
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpython.so
%{_prefix}/%{major_version}/share/extension/plperl--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperl--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperl.control
%{_prefix}/%{major_version}/share/extension/plperlu--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperlu--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperlu.control
%{_prefix}/%{major_version}/share/extension/plpython2u--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpython2u--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpython2u.control
# %{_prefix}/%{major_version}/share/extension/plpython3u--1.0.sql
# %{_prefix}/%{major_version}/share/extension/plpython3u--unpackaged--1.0.sql
# %{_prefix}/%{major_version}/share/extension/plpython3u.control
%{_prefix}/%{major_version}/share/extension/plpythonu--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpythonu--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpythonu.control
%if %{with_tcl}
%{_prefix}/%{major_version}/share/extension/pltcl--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltcl--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltcl.control
%{_prefix}/%{major_version}/share/extension/pltclu--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltclu--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltclu.control
%endif


%files -n %{prefix_name}-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/internal
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/internal/libpq
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/informix
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/informix/esql
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/optimizer
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/regex
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/libpq
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/tsearch
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/dicts
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/catalog
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/executor
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/nodes
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/tcop
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/utils
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/portability
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/mb
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/sys
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/netinet
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/arpa
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/sys
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/postmaster
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/parser
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/replication
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/storage
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/bootstrap
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/commands
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/foreign
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/access
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/snowball
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/rewrite
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/datatype
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/common
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/common/*
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/libpq
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/config
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/makefiles
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/test
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/test/regress
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/makefiles
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test/regress
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config/install-sh
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config/missing
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.port
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.shlib
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/makefiles/pgxs.mk
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/nls-global.mk
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/ecpg
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_config
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/ecpg
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_config

%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/ecpg
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_config
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/ecpg
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_config

%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/config/install-sh
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/config/missing
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/Makefile.global
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/Makefile.port
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/Makefile.shlib
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/makefiles/pgxs.mk
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/nls-global.mk
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pgxs/src/test/regress/pg_regress
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.global
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test/regress/pg_regress
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/libpq/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/informix/esql/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/regex/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/dicts/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/portability/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/mb/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/sys/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/netinet/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/arpa/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/sys/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/replication/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/bootstrap/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/foreign/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/lib/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/datatype/timestamp.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/atomics/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/fe_utils/*.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/libpq/*.h

%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/pkgconfig
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pkgconfig

%files -n %{prefix_name}-docs
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc/html
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man
%{_prefix}/%{major_version}/doc/html/*
%{_prefix}/%{major_version}/man/*
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc/extension
%{_prefix}/%{major_version}/doc/extension/*

%files -n %{prefix_name}-server
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/extension
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/timezonesets
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/tsearch_data
%dir %attr (0755, postgres, postgres) %{_var_prefix}
%dir %attr (0755, postgres, postgres) %{_var_prefix}/%{major_version}
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/backups
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/data
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/data_64
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, sys) /etc/security
%dir %attr (0755, root, sys) /etc/security/auth_attr.d
%dir %attr (0755, root, sys) /etc/security/exec_attr.d
%dir %attr (0755, root, sys) /etc/security/prof_attr.d
%dir %attr (0755, root, sys) /etc/user_attr.d
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/application
%dir %attr (0755, root, sys) /var/svc/manifest/application/database
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hungarian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/ispell_sample.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/ispell_sample.dict
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample_long.dict
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample_long.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample_num.dict
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample_num.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/italian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/norwegian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/portuguese.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/russian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/spanish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/swedish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/synonym_sample.syn
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/thesaurus_sample.ths
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/turkish.stop
%attr (0555, root, bin) /lib/svc/method/postgres_96
%attr (0644, root, sys) /etc/security/auth_attr.d/service\%2Fdatabase\%2Fpostgres-96
%attr (0644, root, sys) /etc/security/exec_attr.d/service\%2Fdatabase\%2Fpostgres-96
%attr (0644, root, sys) /etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-96
%attr (0644, root, sys) /etc/user_attr.d/service\%2Fdatabase\%2Fpostgres-96
%class(manifest) %attr (0444, root, sys) /var/svc/manifest/application/database/postgresql_96.xml

%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/initdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_controldata
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_ctl
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_resetxlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/postgres
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/postmaster
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/%{_arch64}/pg_receivexlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/initdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_controldata
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_ctl
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_resetxlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/postgres
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/postmaster
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_receivexlog

%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/initdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_controldata
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_ctl
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_resetxlog
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/postgres
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/postmaster
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_receivexlog
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/initdb
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_controldata
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_ctl
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_resetxlog
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/postgres
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/postmaster
%attr (0555, root, bin) %ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_receivexlog

%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/ascii_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/cyrillic_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/dict_snowball.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/euc_cn_and_mic.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/euc_jis_2004_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/euc_jp_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/euc_kr_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/euc_tw_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/latin2_and_win1250.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/latin_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/plpgsql.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_ascii.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_cyrillic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_euc_cn.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_euc_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_euc_jp.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_euc_kr.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_euc_tw.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_gb18030.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_gbk.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_iso8859.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_iso8859_1.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_johab.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_uhc.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_win.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/ascii_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/cyrillic_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/dict_snowball.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_cn_and_mic.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_jis_2004_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_jp_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_kr_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_tw_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/latin2_and_win1250.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/latin_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpgsql.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_ascii.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_cyrillic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_cn.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_jp.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_kr.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_tw.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_gb18030.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_gbk.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_iso8859.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_iso8859_1.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_johab.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_uhc.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_win.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc2004_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpqwalreceiver.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpython2.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_euc2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/utf8_and_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/euc2004_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/plpython2.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}/libpqwalreceiver.so
##%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/initdb-%{major_version}.mo
##%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_controldata-%{major_version}.mo
##%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_ctl-%{major_version}.mo
##%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plpgsql-%{major_version}.mo
##%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/conversion_create.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/information_schema.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_hba.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_ident.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_service.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.bki
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.description
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.shdescription
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgresql.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/recovery.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/snowball_create.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/sql_features.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/system_views.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Africa.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/America.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Antarctica.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Asia.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Atlantic.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Australia
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Australia.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Default
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Etc.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Europe.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/India
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Indian.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Pacific.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/danish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/dutch.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/english.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/finnish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/french.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/german.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/extension/plpgsql--1.0.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/extension/plpgsql--unpackaged--1.0.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/extension/plpgsql.control

%files -n %{prefix_name}-contrib
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/%{_arch64}
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/extension
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/tsearch_data
%{_prefix}/%{major_version}/lib/adminpack.so
%{_prefix}/%{major_version}/lib/auto_explain.so
%{_prefix}/%{major_version}/lib/btree_gin.so
%{_prefix}/%{major_version}/lib/btree_gist.so
%{_prefix}/%{major_version}/lib/chkpass.so
%{_prefix}/%{major_version}/lib/citext.so
%{_prefix}/%{major_version}/lib/cube.so
%{_prefix}/%{major_version}/lib/dblink.so
%{_prefix}/%{major_version}/lib/dict_int.so
%{_prefix}/%{major_version}/lib/dict_xsyn.so
%{_prefix}/%{major_version}/lib/earthdistance.so
%{_prefix}/%{major_version}/lib/fuzzystrmatch.so
%{_prefix}/%{major_version}/lib/hstore.so
%{_prefix}/%{major_version}/lib/_int.so
%{_prefix}/%{major_version}/lib/isn.so
%{_prefix}/%{major_version}/lib/lo.so
%{_prefix}/%{major_version}/lib/ltree.so
%{_prefix}/%{major_version}/lib/pageinspect.so
%{_prefix}/%{major_version}/lib/passwordcheck.so
%{_prefix}/%{major_version}/lib/pg_buffercache.so
%{_prefix}/%{major_version}/lib/pg_freespacemap.so
%{_prefix}/%{major_version}/lib/pg_stat_statements.so
%{_prefix}/%{major_version}/lib/pg_trgm.so
#gone %{_prefix}/%{major_version}/lib/pg_upgrade_support.so
%{_prefix}/%{major_version}/lib/pgcrypto.so
%{_prefix}/%{major_version}/lib/pgrowlocks.so
%{_prefix}/%{major_version}/lib/pgstattuple.so
%{_prefix}/%{major_version}/lib/seg.so
%{_prefix}/%{major_version}/lib/autoinc.so
%{_prefix}/%{major_version}/lib/insert_username.so
%{_prefix}/%{major_version}/lib/moddatetime.so
%{_prefix}/%{major_version}/lib/refint.so
%{_prefix}/%{major_version}/lib/timetravel.so
%{_prefix}/%{major_version}/lib/tablefunc.so
#gone %{_prefix}/%{major_version}/lib/test_parser.so
%{_prefix}/%{major_version}/lib/tsearch2.so
%{_prefix}/%{major_version}/lib/unaccent.so
%{_prefix}/%{major_version}/lib/sslinfo.so
%{_prefix}/%{major_version}/lib/pgxml.so
%{_prefix}/%{major_version}/lib/tcn.so
%{_prefix}/%{major_version}/lib/tsm_system_time.so
%{_prefix}/%{major_version}/lib/tsm_system_rows.so
%{_prefix}/%{major_version}/lib/ltree_plpython2.so
%{_prefix}/%{major_version}/lib/pg_visibility.so
%{_prefix}/%{major_version}/lib/bloom.so
%{_prefix}/%{major_version}/lib/hstore_plpython2.so
%if %{perl_32_bit}
%{_prefix}/%{major_version}/lib/hstore_plperl.so
%endif
%if %{perl_64_bit}
%{_prefix}/%{major_version}/lib/%{_arch64}/hstore_plperl.so
%endif
%{_prefix}/%{major_version}/lib/%{_arch64}/autoinc.so
%{_prefix}/%{major_version}/lib/%{_arch64}/adminpack.so
%{_prefix}/%{major_version}/lib/%{_arch64}/auto_explain.so
%{_prefix}/%{major_version}/lib/%{_arch64}/btree_gin.so
%{_prefix}/%{major_version}/lib/%{_arch64}/btree_gist.so
%{_prefix}/%{major_version}/lib/%{_arch64}/chkpass.so
%{_prefix}/%{major_version}/lib/%{_arch64}/citext.so
%{_prefix}/%{major_version}/lib/%{_arch64}/cube.so
%{_prefix}/%{major_version}/lib/%{_arch64}/dblink.so
%{_prefix}/%{major_version}/lib/%{_arch64}/dict_int.so
%{_prefix}/%{major_version}/lib/%{_arch64}/dict_xsyn.so
%{_prefix}/%{major_version}/lib/%{_arch64}/earthdistance.so
%{_prefix}/%{major_version}/lib/%{_arch64}/fuzzystrmatch.so
%{_prefix}/%{major_version}/lib/%{_arch64}/hstore.so
%{_prefix}/%{major_version}/lib/%{_arch64}/_int.so
%{_prefix}/%{major_version}/lib/%{_arch64}/insert_username.so
%{_prefix}/%{major_version}/lib/%{_arch64}/isn.so
%{_prefix}/%{major_version}/lib/%{_arch64}/lo.so
%{_prefix}/%{major_version}/lib/%{_arch64}/ltree.so
%{_prefix}/%{major_version}/lib/%{_arch64}/moddatetime.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pageinspect.so
%{_prefix}/%{major_version}/lib/%{_arch64}/passwordcheck.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pg_buffercache.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pg_freespacemap.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pg_stat_statements.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pg_trgm.so
#gone %{_prefix}/%{major_version}/lib/%{_arch64}/pg_upgrade_support.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pgcrypto.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pgrowlocks.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pgstattuple.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pgxml.so
%{_prefix}/%{major_version}/lib/%{_arch64}/refint.so
%{_prefix}/%{major_version}/lib/%{_arch64}/seg.so
%{_prefix}/%{major_version}/lib/%{_arch64}/sslinfo.so
%{_prefix}/%{major_version}/lib/%{_arch64}/tablefunc.so
#gone %{_prefix}/%{major_version}/lib/%{_arch64}/test_parser.so
%{_prefix}/%{major_version}/lib/%{_arch64}/timetravel.so
%{_prefix}/%{major_version}/lib/%{_arch64}/tsearch2.so
%{_prefix}/%{major_version}/lib/%{_arch64}/unaccent.so
%{_prefix}/%{major_version}/lib/%{_arch64}/tcn.so
%{_prefix}/%{major_version}/lib/%{_arch64}/tsm_system_rows.so
%{_prefix}/%{major_version}/lib/%{_arch64}/tsm_system_time.so
%{_prefix}/%{major_version}/lib/%{_arch64}/ltree_plpython2.so
%{_prefix}/%{major_version}/lib/%{_arch64}/pg_visibility.so
%{_prefix}/%{major_version}/lib/%{_arch64}/bloom.so
%{_prefix}/%{major_version}/lib/%{_arch64}/hstore_plpython2.so
%{_prefix}/%{major_version}/share/extension/adminpack--1.0.sql
%{_prefix}/%{major_version}/share/extension/adminpack.control
%{_prefix}/%{major_version}/share/extension/adminpack--1.1.sql
%{_prefix}/%{major_version}/share/extension/adminpack--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/autoinc--1.0.sql
%{_prefix}/%{major_version}/share/extension/autoinc--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/autoinc.control
%{_prefix}/%{major_version}/share/extension/btree_gin--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gin--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gin.control
#gone %{_prefix}/%{major_version}/share/extension/btree_gist--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gist--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gist.control
%{_prefix}/%{major_version}/share/extension/chkpass--1.0.sql
%{_prefix}/%{major_version}/share/extension/chkpass--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/chkpass.control
#gone %{_prefix}/%{major_version}/share/extension/citext--1.0.sql
#gone %{_prefix}/%{major_version}/share/extension/citext--1.0--1.1.sql
#gone %{_prefix}/%{major_version}/share/extension/citext--1.1--1.0.sql
#gone %{_prefix}/%{major_version}/share/extension/citext--1.1.sql
%{_prefix}/%{major_version}/share/extension/citext--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/citext.control
#gone %{_prefix}/%{major_version}/share/extension/cube--1.0.sql
%{_prefix}/%{major_version}/share/extension/cube--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/cube.control
%{_prefix}/%{major_version}/share/extension/dblink--*.sql
%{_prefix}/%{major_version}/share/extension/dblink.control
%{_prefix}/%{major_version}/share/extension/dict_int--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_int--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_int.control
%{_prefix}/%{major_version}/share/extension/dict_xsyn--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_xsyn--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_xsyn.control
#gone %{_prefix}/%{major_version}/share/extension/earthdistance--1.0.sql
%{_prefix}/%{major_version}/share/extension/earthdistance--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/earthdistance.control
%{_prefix}/%{major_version}/share/extension/file_fdw--1.0.sql
%{_prefix}/%{major_version}/share/extension/file_fdw.control
#gone %{_prefix}/%{major_version}/share/extension/fuzzystrmatch--1.0.sql
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch.control
%{_prefix}/%{major_version}/share/extension/hstore--*.sql
%{_prefix}/%{major_version}/share/extension/hstore.control
%{_prefix}/%{major_version}/share/extension/insert_username--1.0.sql
%{_prefix}/%{major_version}/share/extension/insert_username--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/insert_username.control
#gone %{_prefix}/%{major_version}/share/extension/intagg--1.0.sql
%{_prefix}/%{major_version}/share/extension/intagg--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/intagg.control
#gone %{_prefix}/%{major_version}/share/extension/intarray--1.0.sql
%{_prefix}/%{major_version}/share/extension/intarray--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/intarray.control
#gone %{_prefix}/%{major_version}/share/extension/isn--1.0.sql
%{_prefix}/%{major_version}/share/extension/isn--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/isn.control
#gone %{_prefix}/%{major_version}/share/extension/lo--1.0.sql
%{_prefix}/%{major_version}/share/extension/lo--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/lo.control
#gone %{_prefix}/%{major_version}/share/extension/ltree--1.0.sql
%{_prefix}/%{major_version}/share/extension/ltree--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/ltree.control
%{_prefix}/%{major_version}/share/extension/moddatetime--1.0.sql
%{_prefix}/%{major_version}/share/extension/moddatetime--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/moddatetime.control
%{_prefix}/%{major_version}/share/extension/pageinspect--*.sql
%{_prefix}/%{major_version}/share/extension/pageinspect.control
#gone %{_prefix}/%{major_version}/share/extension/pg_buffercache--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_buffercache--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_buffercache.control
#gone %{_prefix}/%{major_version}/share/extension/pg_freespacemap--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_freespacemap--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_freespacemap.control
%{_prefix}/%{major_version}/share/extension/pg_stat_statements--*.sql
%{_prefix}/%{major_version}/share/extension/pg_stat_statements.control
%{_prefix}/%{major_version}/share/extension/pg_trgm--*.sql
%{_prefix}/%{major_version}/share/extension/pg_trgm.control
%{_prefix}/%{major_version}/share/extension/pgcrypto--*.sql
%{_prefix}/%{major_version}/share/extension/pgcrypto.control
%{_prefix}/%{major_version}/share/extension/pgrowlocks--*.sql
%{_prefix}/%{major_version}/share/extension/pgrowlocks.control
%{_prefix}/%{major_version}/share/extension/pgstattuple--*.sql
%{_prefix}/%{major_version}/share/extension/pgstattuple.control
%{_prefix}/%{major_version}/share/extension/refint--1.0.sql
%{_prefix}/%{major_version}/share/extension/refint--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/refint.control
#gone %{_prefix}/%{major_version}/share/extension/seg--1.0.sql
%{_prefix}/%{major_version}/share/extension/seg--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/seg.control
#gone %{_prefix}/%{major_version}/share/extension/sslinfo--1.0.sql
%{_prefix}/%{major_version}/share/extension/sslinfo--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/sslinfo.control
%{_prefix}/%{major_version}/share/extension/tablefunc--1.0.sql
%{_prefix}/%{major_version}/share/extension/tablefunc--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/tablefunc.control
#gone %{_prefix}/%{major_version}/share/extension/test_parser--1.0.sql
#gone %{_prefix}/%{major_version}/share/extension/test_parser--unpackaged--1.0.sql
#gone %{_prefix}/%{major_version}/share/extension/test_parser.control
%{_prefix}/%{major_version}/share/extension/timetravel--1.0.sql
%{_prefix}/%{major_version}/share/extension/timetravel--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/timetravel.control
%{_prefix}/%{major_version}/share/extension/tsearch2--1.0.sql
%{_prefix}/%{major_version}/share/extension/tsearch2--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/tsearch2.control
#gone %{_prefix}/%{major_version}/share/extension/unaccent--1.0.sql
%{_prefix}/%{major_version}/share/extension/unaccent--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/unaccent.control
#gone %{_prefix}/%{major_version}/share/extension/xml2--1.0.sql
%{_prefix}/%{major_version}/share/extension/xml2--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/xml2.control
%{_prefix}/%{major_version}/share/extension/tcn--1.0.sql
%{_prefix}/%{major_version}/share/extension/tcn.control
#gone %{_prefix}/%{major_version}/share/extension/worker_spi--1.0.sql
#gone %{_prefix}/%{major_version}/share/extension/test_shm_mq--1.0.sql
%{_prefix}/%{major_version}/share/extension/postgres_fdw.control
#gone %{_prefix}/%{major_version}/share/extension/test_shm_mq.control
%{_prefix}/%{major_version}/share/extension/postgres_fdw--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_prewarm.control
#gone %{_prefix}/%{major_version}/share/extension/pg_prewarm--1.0.sql
#gone %{_prefix}/%{major_version}/share/extension/worker_spi.control
%{_prefix}/%{major_version}/share/extension/tsm_system_time.control
%{_prefix}/%{major_version}/share/extension/tsm_system_rows--1.0.sql
%{_prefix}/%{major_version}/share/extension/tsm_system_time--1.0.sql
%{_prefix}/%{major_version}/share/extension/tsm_system_rows.control
%{_prefix}/%{major_version}/share/extension/pg_prewarm--1.1.sql
%{_prefix}/%{major_version}/share/extension/seg--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_visibility.control
%{_prefix}/%{major_version}/share/extension/citext--1.2--1.3.sql
%{_prefix}/%{major_version}/share/extension/intarray--1.1--1.2.sql
%{_prefix}/%{major_version}/share/extension/bloom.control
%{_prefix}/%{major_version}/share/extension/cube--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/sslinfo--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/citext--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_freespacemap--1.1.sql
%{_prefix}/%{major_version}/share/extension/hstore_plpython3u.control
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch--1.1.sql
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/hstore_plpython2u--1.0.sql
%{_prefix}/%{major_version}/share/extension/lo--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_visibility--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/hstore_plpython3u--1.0.sql
%{_prefix}/%{major_version}/share/extension/hstore_plperlu.control
%{_prefix}/%{major_version}/share/extension/ltree_plpython2u--1.0.sql
%{_prefix}/%{major_version}/share/extension/earthdistance--1.1.sql
%{_prefix}/%{major_version}/share/extension/ltree_plpython3u--1.0.sql
%{_prefix}/%{major_version}/share/extension/ltree_plpython3u.control
%{_prefix}/%{major_version}/share/extension/pg_buffercache--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/unaccent--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/lo--1.1.sql
%{_prefix}/%{major_version}/share/extension/ltree--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_visibility--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_buffercache--1.2.sql
%{_prefix}/%{major_version}/share/extension/ltree--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/hstore_plperlu--1.0.sql
%{_prefix}/%{major_version}/share/extension/seg--1.1.sql
%{_prefix}/%{major_version}/share/extension/ltree_plpython2u.control
%{_prefix}/%{major_version}/share/extension/hstore_plpython2u.control
%{_prefix}/%{major_version}/share/extension/bloom--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gist--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_freespacemap--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_buffercache--1.1--1.2.sql
%{_prefix}/%{major_version}/share/extension/ltree_plpythonu.control
%{_prefix}/%{major_version}/share/extension/btree_gist--1.2.sql
%{_prefix}/%{major_version}/share/extension/isn--1.1.sql
%{_prefix}/%{major_version}/share/extension/xml2--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/intarray--1.2.sql
%{_prefix}/%{major_version}/share/extension/citext--1.1--1.2.sql
%{_prefix}/%{major_version}/share/extension/isn--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/citext--1.3.sql
%{_prefix}/%{major_version}/share/extension/sslinfo--1.1--1.2.sql
%{_prefix}/%{major_version}/share/extension/cube--1.1--1.2.sql
%{_prefix}/%{major_version}/share/extension/intarray--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/xml2--1.1.sql
%{_prefix}/%{major_version}/share/extension/hstore_plperl.control
%{_prefix}/%{major_version}/share/extension/btree_gist--1.1--1.2.sql
%{_prefix}/%{major_version}/share/extension/intagg--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/pg_prewarm--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/earthdistance--1.0--1.1.sql
%{_prefix}/%{major_version}/share/extension/unaccent--1.1.sql
%{_prefix}/%{major_version}/share/extension/intagg--1.1.sql
%{_prefix}/%{major_version}/share/extension/hstore_plpythonu.control
%{_prefix}/%{major_version}/share/extension/hstore_plpythonu--1.0.sql
%{_prefix}/%{major_version}/share/extension/ltree_plpythonu--1.0.sql
%{_prefix}/%{major_version}/share/extension/hstore_plperl--1.0.sql
%{_prefix}/%{major_version}/share/extension/sslinfo--1.2.sql
%{_prefix}/%{major_version}/share/extension/cube--1.2.sql
%{_prefix}/%{major_version}/share/tsearch_data/xsyn_sample.rules
%{_prefix}/%{major_version}/share/tsearch_data/unaccent.rules
%{_prefix}/%{major_version}/bin/oid2name
%{_prefix}/%{major_version}/bin/pg_archivecleanup
%{_prefix}/%{major_version}/bin/pg_standby
%{_prefix}/%{major_version}/bin/pg_upgrade
%{_prefix}/%{major_version}/bin/pgbench
%{_prefix}/%{major_version}/bin/vacuumlo
%{_prefix}/%{major_version}/bin/%{_arch64}/oid2name
%{_prefix}/%{major_version}/bin/%{_arch64}/pg_archivecleanup
%{_prefix}/%{major_version}/bin/%{_arch64}/pg_standby
%{_prefix}/%{major_version}/bin/%{_arch64}/pg_upgrade
%{_prefix}/%{major_version}/bin/%{_arch64}/pgbench
%{_prefix}/%{major_version}/bin/%{_arch64}/vacuumlo

%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/oid2name
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_archivecleanup
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_standby
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pg_upgrade
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/pgbench
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/vacuumlo
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/oid2name
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_archivecleanup
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_standby
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pg_upgrade
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/pgbench
%ips_tag (mediator=postgres mediator-version=%{major_version}) /usr/bin/%{_arch64}/vacuumlo

%changelog
* Mon Mar 11 2019 - Thomas Wagner
- set TMPDIR to %{_builddir} assuming this is a fast (local) filesystem and use this as CFLAGS -temp=${TMPDIR}
- make one re-try with gmake -j1 if first compile attempt fails.
- fix packaging again for extension/adminpack--*
* Sun Mar 10 2019 - Thomas Wagner
- fix packaging for extension/adminpack--1.1*
- set TMPDIR to avoid filling up /tmp/ and steal memory
* Sun Mar  3 2019 - Thomas Wagner
- bump to version 9.6.12
* Tue Mar  6 2018 - Thomas Wagner
- bump to version 9.6.8
* Fri Jan  5 2018 - Thomas Wagner
- bump to version 9.6.6
- use CPUS=%{_cpus_memory_2048} - got OOM in S11.3 with 4GB RAM (example:   1950M 1607M sleep    60    1   0:00:09 0,2% iropt/1)
* Mon Jul 10 2017 - Thomas Wagner
- add missing Requires: libedit openssl
- add -temp=%{_builddir} to CFLAGS to have compiler interim files of size 1GB not live in size-limited /tmp on swap (seen with Sun CC 5.12 aka 12.3)
* Sun Jun  4 2017 - Thomas Wagner
- bump to version 9.6.3
- create symlink bin/64 bin/%{_arch64} or bin/sparcv9 to match path to bin in SMF xml (shows bin/64/ )
- start replacing major_version like 9.6 in ext-sources/ postgres-96-postgres_96 postgres-96-exec_attr postgres-96-postgresql_96.xml with @@macro@@
- remove tcl from omnios build (OM)
- allow 32-bit or 64-bit perl (OM and potentially other distro)
* Sun Dec  7 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec, adapted from SFEpostgres-92.spec
* Fri Nov 27 EST 2015 Alex Viskovatoff <herzen@imap.cc>
- update to 9.2.14
* Thu Feb  7 JST 2013 TAKI, Yasushi <taki@justplayer.com>
- bump to 9.2.3
* Thu Jan 17 PST 2013 TAKI, Yasushi <taki@justplayer.com>
- support mediator.
* Sun Jan  6 JST 2013 TAKI, Yasushi <taki@justplayer.com>
- fix comment
* Sat Dec 15 JST 2012 Fumihisa TONAKA <fumi.ftnk@gmail.com>
- initial commit
