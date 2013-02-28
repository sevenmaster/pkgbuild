
#1 use, 0 don't
%define use_stdcxx 0

# oh well, this is in a _very_ early state. it compiles. no fine tuning. 32-bit only.

%include Solaris.inc
%include base.inc
%if %{use_stdcxx}
%include stdcxx.inc
%endif
%include packagenamemacros.inc

%define src_name mysql

Name: SFEmysql56
Summary: MySQL Server Community Edition
Version:	5.6.10
#%define major_minor $( echo $version | awk -F'.' '{print $1 "." $2}' )
%define major_minor 5.6



Source: http://cdn.mysql.com/Downloads/MySQL-5.6/mysql-%{version}.tar.gz

#evtl. neu machen Patch1: mysql56-01-0003-I-HATE-CMAKE.patch.diff
Patch2: mysql56-02-0005-Do-not-strip-RPATH-from-binaries.patch.diff

SUNW_BaseDir:   /usr


BuildRequires: SFEcmake


###%package lib
###IPS_package_name: database/mysql-%{major_minor}/library
###Summary: mysql client libraries
####Requires:
###%package r
####Requires:
###%package u
####Requires:
###%package test
####Requires:


%prep
%setup -q -n %{src_name}-%{version}

#evtl. neu machen %patch1 -p1
%patch2 -p1

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')


#unbenutzt export MYSQL_VERSION="%{version}"
#unbenutzt export MYSQL_DIR=mysql-${MYSQL_VERSION}
#unbenutzt export MYSQL_DIR_64=mysql-${MYSQL_VERSION}_64
export PREFIX="/usr/mysql/%{major_minor}"
#unbenutzt export CONFDIR="/etc/mysql/%{major_minor}"
export DATA_PREFIX="/var/mysql/%{major_minor}"

#cmake/build_configurations/compiler_options.cmake
#da ist schon viel drin, eher weniger setzen hier
#Beispiel:
#   SET(COMMON_C_FLAGS                   "-g -mt -fsimple=1 -ftrap=%none -nofstore -xbuiltin=%all -xlibmil -xlibmopt -xtarget=generic")
#   SET(COMMON_CXX_FLAGS                 "-g0 -mt -fsimple=1 -ftrap=%none -nofstore -xbuiltin=%all -xlibmil -xlibmopt -xtarget=generic -library=stlport4")
 


# C++ common flags

#export CXXCOMMONFLAGS=" -DDBUG_OFF -DBIG_TABLES -DHAVE_RWLOCK_T -KPIC -DPIC -xO4 -xmaxopt=4 -xprefetch=auto -xprefetch_level=3 -mt -fns=no -fsimple=1 -xbuiltin=%%all -xlibmil -xlibmopt -norunpath"

# C++ 32 bit flags
#export CXX32FLAGS="${CXXCOMMONFLAGS}"

# C common compiler flags
#export COMMONCFLAGS="-xO4 -xstrconst -xprefetch=auto -xprefetch_level=3 -mt -fns=no -fsimple=1 -xbuiltin=%%all -xlibmil -xlibmopt -xnorunpath"



#test with -lthread
export LDFLAGS="%{_ldflags} -lrt -lm -lthread "
#export CFLAGS="%{optflags}"
#export CFLAGS=""  or get #bool Rpl_info_factory::change_mi_repository(Master_info*,const unsigned,const char**) ../../../sql/libsql.a(sys_vars.cc.o)
export CFLAGS=""
export CXXFLAGS="%{cxx_optflags}"

%if %{use_stdcxx}
export CC=${CC}
export CXX="${CXX} -library=no%Cstd"
export CFLAGS="%{optflags}"
%endif

#aus compile-lauf:
# -norunpath  -i -xO3 -xspace -xarch=pentium_pro -mr -norunpath -xregs=no%frameptr    -KPIC -library=stlport4  -R'$ORIGIN/../lib' -R/usr/mysql/5.6/lib   -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect  -lrt -lm  -lmtmalloc CMakeFiles

echo "DEBUG: CC      " $CC
echo "DEBUG: CXX     " $CXX
echo "DEBUG: CFLAGS  " $CFLAGS
echo "DEBUG: CXXFLAGS" $CXXFLAGS
echo "DEBUG: LDFLAGS " $LDFLAGS

#bash

#cd $(MYSQL_DIR); env - $(ENVLINE32)  /bin/ksh ./configure \
#/usr/bin/bash ./configure \
#	${COMMON_CONFIG_OPTIONS} \
#	--libexecdir=${PREFIX}/bin \
#	--bindir=${PREFIX}/bin	\
#	--libdir=${PREFIX}/lib \
#	--enable-dtrace DTRACEFLAGS='-32'

# -DINSTALL_LAYOUT=SVR4


#CMAKE_SYSTEM_NAME MATCHES "SunOS"

mkdir %{bld_arch}
cd %{bld_arch}
           #-DFEATURE_SET="%{feature_set}" \
           #%{ssl_option} \
           #-DCOMPILATION_COMMENT="%{compilation_comment_debug}" \
           #-DMYSQL_SERVER_SUFFIX="%{server_suffix}"
# CSW # CMAKE_ARGS += -DINSTALL_PLUGINDIR=$(subst $(prefix)/,,$(libdir))/$(NAME)/$(MM_LIBDIR)/plugin
# CSW # CMAKE_ARGS += -DWITH_READLINE=1
# CSW # CMAKE_ARGS += -DWITH_SSL=system
# CSW # CMAKE_ARGS += -DWITH_ZLIB=system
# CSW # CMAKE_ARGS += -DDEFAULT_CHARSET=utf8
# CSW # CMAKE_ARGS += -DDEFAULT_COLLATION=utf8_general_ci
# CSW # CMAKE_ARGS += -DWITH_COMMENT='OpenCSW'
# CSW # CMAKE_ARGS += -DCMAKE_C_FLAGS="$(CFLAGS)" -DCMAKE_CXX_FLAGS="$(CXXFLAGS)"
# CSW # CMAKE_ARGS += -DBUILD_CONFIG=mysql_release
# CSW # # CMAKE_ARGS += -DOPENSSL_INCLUDE_DIR="$(includedir)"
# CSW # # CMAKE_ARGS += -DCMAKE_LIBRARY_PATH="$(libdir)"
# CSW # # CMAKE_ARGS += -DCMAKE_PREFIX_PATH="$(prefix)"
# CSW # CMAKE_ARGS += -DOPENSSL_ROOT_DIR=$(prefix)
# CSW # # CMAKE_ARGS += -DOPENSSL_SSL_LIBRARIES=$(libdir)/$(MM_LIBDIR)/libssl.so
# CSW # # CMAKE_ARGS += -DOPENSSL_CRYPTO_LIBRARIES=$(libdir)/$(MM_LIBDIR)/libcrypto.so
# CSW # CMAKE_ARGS += -DCMAKE_INCLUDE_PATH="$(includedir)"
# CSW # CMAKE_ARGS += -DCMAKE_LIBRARY_PATH="$(libdir)"

CMAKE=cmake
  ${CMAKE} .. -DBUILD_CONFIG=mysql_release -DINSTALL_LAYOUT=SVR4 \
              -DCMAKE_INSTALL_PREFIX=${PREFIX} \
              -DMYSQL_DATADIR=${DATA_PREFIX}/data \
                 -DSYSCONFDIR=/etc/mysql \
           -DMYSQL_DATADIR=/var/mysql/data \
           -DMYSQL_UNIX_ADDR="/tmp/mysql.sock" \
                 -DCMAKE_VERBOSE_MAKEFILE=TRUE \
             -DINSTALL_PLUGINDIR=${PREFIX}/lib/mysql/plugin \
                       -DWITH_READLINE=1 \
                       -DBUILD_CONFIG=mysql_release \
                       -DWITH_COMMENT='SFE' \
                       -DCMAKE_C_FLAGS="${CFLAGS}" -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
%if %{use_stdcxx}
%else
                       -DLIBS="-lstlport" \
%endif

#geht nicht                       -DWITH_ZLIB=system \
#geht nicht                       -DWITH_SSL=system \

  echo BEGIN_DEBUG_CONFIG ; egrep '^#define' include/config.h ; echo END_DEBUG_CONFIG

  gmake -j$CPUS VERBOSE=1

%install
cd %{bld_arch}
make install DESTDIR=$RPM_BUILD_ROOT

%if %{use_stdcxx}
%else
gsed -i -e 's?\(-lmysqlclient\|-lmysqlclient_r\)?\1 -lstlport?' $RPM_BUILD_ROOT%{_prefix}/mysql/%{major_minor}/bin/mysql_config
#embedded_libs="$embedded_libs  -R'\$ORIGIN/../lib' -R/swapnomirror/solstudio12.3/SolarisStudio12.3-solaris-x86-bin/solarisstudio12.3/lib/stlport4 -lstlport "
#add -stlport to the end, unconditionally
gsed -i -e '/^embedded_libs/ s?\"$? -lstlport "?' $RPM_BUILD_ROOT%{_prefix}/mysql/%{major_minor}/bin/mysql_config
%endif

rm $RPM_BUILD_ROOT%{_prefix}/mysql/%{major_minor}/lib/libmysqld.a
rm $RPM_BUILD_ROOT%{_prefix}/mysql/%{major_minor}/lib/libmysqlclient.a
rm $RPM_BUILD_ROOT%{_prefix}/mysql/%{major_minor}/lib/libmysqlservices.a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
#%dir %attr (0755,root,bin) %{_prefix}
%dir %attr (0755,root,bin) %{_prefix}/mysql
%dir %attr (0755,root,bin) %{_prefix}/mysql/%{major_minor}
%{_prefix}/mysql/%{major_minor}/*


%changelog
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6
##%files lib
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/lib

##%files r
%defattr(-, root, sys)
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none etc 0755 root sys
%defattr(-, root, bin)
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none etc/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none lib 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none lib/svc 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none lib/svc/method 0755 root bin

%defattr(-, root, sys)
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var 0755 root sys
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/svc 0755 root sys
%defattr(-, mysql, mysql)
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/mysql 0700 mysql mysql

##%files u
%defattr(-, root, sys)
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr 0755 root sys
%defattr(-, root, bin)
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/bin 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql 0755 root bin
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/bin
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/scripts
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/docs
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/man
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/man/man8
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/man/man1
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/support-files
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/include
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/share

##%files test
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/sql-bench
/var/tmp/pkgbuild-tom/SFEmysql56-5.6.10-build/usr/mysql/5.6/mysql-test


##%changelog
* Sat Feb  9 2013 - Thomas Wagner
- initial spec, only compiles, no fine tuning, 32-bit only


=====================dumping space
visit later!
#These COMMON_CONFIG_OPTIONS are common for both 32 and 64-bit
export COMMON_CONFIG_OPTIONS="\
                ac_cv_func_stpcpy=no \
                --datadir=${PREFIX}/share  \
                --sbindir=${PREFIX}sbin  \
                --sharedstatedir=${PREFIX}/com  \
                --includedir=${PREFIX}/include \
                --oldincludedir=${PREFIX}/include \
                --infodir=${PREFIX}/docs \
                --mandir=${PREFIX}/man  \
                --sysconfdir=${CONFDIR}  \
                --enable-thread-safe-client     \
                --with-mysqld-libs=-lmtmalloc   \
                --with-named-curses=-lcurses    \
                --with-client-ldflags=-static   \
                --with-mysql-ldflags=-static    \
                --with-pic \
                --with-big-tables \
                --with-ssl \
                --with-readline \
                --with-extra-charsets=complex   \
                --with-plugins=archive,blackhole,csv,myisam,example,federated,innobase,myisammrg \
                --enable-local-infile
"


=====================dumping space




MYSQL_VERSION=5.1.37
MYSQL_DIR=mysql-$(MYSQL_VERSION)
MYSQL_DIR_64=mysql-$(MYSQL_VERSION)_64
PREFIX=/usr/mysql/5.1
CONFDIR=/etc/mysql/5.1
DATA_PREFIX=/var/mysql/5.1



all : build32 build64

install : install32 install64

test: test32 test64

include ../Makefile.cmd



# C++ common flags

CXXCOMMONFLAGS= -DDBUG_OFF -DBIG_TABLES -DHAVE_RWLOCK_T -KPIC -DPIC -xO4 -xmaxopt=4 \
-xprefetch=auto -xprefetch_level=3 -mt -fns=no -fsimple=1 -xbuiltin=%all \
-xlibmil -xlibmopt -norunpath

# C++ 64 bit flags
CXX64FLAGS= $(CXXCOMMONFLAGS) -features=no%except -m64

# C++ 32 bit flags
CXX32FLAGS= $(CXXCOMMONFLAGS)

# C common compiler flags
COMMONCFLAGS= -xO4 -xstrconst -xprefetch=auto -xprefetch_level=3 -mt\
-fns=no -fsimple=1 -xbuiltin=%all -xlibmil -xlibmopt -xnorunpath

# common ENV for both 32 & 64bit compilation 
ENVCOMMONLINE=MAKE=$(GMAKE) \
	PATH=$(SFW_PATH) \
	DESTDIR=$(ROOT) \
	INSTALL_ROOT=$(ROOT) \
	INSTALL=/usr/ucb/install \
	CC=$(CC) \
	CXX="$(CCC) -norunpath" 

#ENV for 32 bit compilation only
ENVLINE32 = $(ENVCOMMONLINE) \
	LDFLAGS="-L$(SPRO_VROOT)/lib -lCrun -lrt"\
	CFLAGS="$(COMMONCFLAGS)"\
	CXXFLAGS="$(CXX32FLAGS)" 

#ENV for 64 bit compilation only 
ENVLINE64= $(ENVCOMMONLINE) \
	LD="$(LD) -64" \
	LDFLAGS="-lrt" \
	CFLAGS="$(COMMONCFLAGS) -m64" \
	CXXFLAGS="$(CXX64FLAGS) -m64"

#These COMMON_CONFIG_OPTIONS are common for both 32 and 64-bit
COMMON_CONFIG_OPTIONS= \
		ac_cv_func_stpcpy=no \
		--prefix=$(PREFIX) \
		--localstatedir=$(DATA_PREFIX)/data \
		--datadir=$(PREFIX)/share  \
		--sbindir=$(PREFIX)sbin  \
		--sharedstatedir=$(PREFIX)/com  \
		--includedir=$(PREFIX)/include \
		--oldincludedir=$(PREFIX)/include \
		--infodir=$(PREFIX)/docs \
		--mandir=$(PREFIX)/man  \
		--sysconfdir=$(CONFDIR)  \
		--enable-thread-safe-client     \
		--with-mysqld-libs=-lmtmalloc   \
		--with-named-curses=-lcurses    \
		--with-client-ldflags=-static   \
		--with-mysql-ldflags=-static    \
		--with-pic \
		--with-big-tables \
		--with-ssl \
		--with-readline \
		--with-extra-charsets=complex   \
		--with-plugins=archive,blackhole,csv,myisam,example,federated,innobase,myisammrg \
		--enable-local-infile 


#----Main MySQL Targets -----

build32:$(MYSQL_DIR)/config.status
	( cd $(MYSQL_DIR); env - $(ENVLINE32) $(GMAKE) all )

build64:$(MYSQL_DIR_64)/config.status
	( cd $(MYSQL_DIR_64); env - $(ENVLINE64) $(GMAKE) all )

test32:build32
	(cd $(MYSQL_DIR); env - $(ENVLINE32) $(GMAKE) test)

test64:build64
	(cd $(MYSQL_DIR_64); env - $(ENVLINE64) $(GMAKE) test)


install32:build32 
	(cd $(MYSQL_DIR);  \
	env - $(ENVLINE32) $(GMAKE) install)
	ksh93 ./install-mysql 


install64:build64
	(cd $(MYSQL_DIR_64);  \
	env - $(ENVLINE64) $(GMAKE) install)
	MACH64=$(MACH64) ksh93 ./install-mysql-64


$(MYSQL_DIR)/config.status: $(MYSQL_DIR)/configure
	(cd $(MYSQL_DIR); env - $(ENVLINE32)  /bin/ksh ./configure \
	$(COMMON_CONFIG_OPTIONS) \
	--libexecdir=$(PREFIX)/bin \
	--bindir=$(PREFIX)/bin	\
	--libdir=$(PREFIX)/lib \
	--enable-dtrace DTRACEFLAGS='-32')



$(MYSQL_DIR_64)/config.status: $(MYSQL_DIR_64)/configure
	(cd $(MYSQL_DIR_64); env - $(ENVLINE64)  /bin/ksh ./configure \
	$(COMMON_CONFIG_OPTIONS) \
	--libexecdir=$(PREFIX)/bin/$(MACH64) \
	--bindir=$(PREFIX)/bin/$(MACH64)  \
	--libdir=$(PREFIX)/lib/$(MACH64) \
	--enable-dtrace DTRACEFLAGS='-64')



$(MYSQL_DIR)/configure: $(MYSQL_DIR).tar.gz
	/usr/bin/gzip -dc $(MYSQL_DIR).tar.gz | \
        $(GTAR) xpf - --no-same-owner
	(cd $(MYSQL_DIR); gpatch -p1 < ../patches/mysql-5.1.37-dtrace.sunpatch)
	(cd $(MYSQL_DIR); gpatch -p1 < ../patches/yassl.patch)
	gpatch $(MYSQL_DIR)/storage/innobase/include/univ.i -i patches/inline.patch
	gpatch $(MYSQL_DIR)/scripts/mysql_config.sh -i patches/mysql_config.patch
	gpatch $(MYSQL_DIR)/mysql-test/Makefile.in -i patches/ksh-hang.patch
	gpatch $(MYSQL_DIR)/configure -i patches/configure.patch
	gpatch $(MYSQL_DIR)/sql/sql_select.cc -i patches/xO4_optimization.patch
	(cd $(MYSQL_DIR); touch configure.in config/ac-macros/*; sleep 5; touch aclocal.m4 config.h.in; sleep 5;\
	touch configure ; find . -name Makefile.in | xargs touch)
	find $(MYSQL_DIR) -type d -exec /usr/bin/chmod 755 "{}" \;
	find $(MYSQL_DIR) -type f -exec /usr/bin/chmod ugo+r "{}" \;
	find $(MYSQL_DIR) -name "dtrace_providers" -exec rm {} \;



$(MYSQL_DIR_64)/configure: $(MYSQL_DIR).tar.gz
	 mkdir -p tmp; cp $(MYSQL_DIR).tar.gz tmp
	cd tmp; /usr/bin/gzip -dc $(MYSQL_DIR).tar.gz | tar xopf -
	mv tmp/$(MYSQL_DIR) $(MYSQL_DIR_64); rm -rf tmp
	(cd $(MYSQL_DIR_64); gpatch -p1 < ../patches/mysql-5.1.37-dtrace.sunpatch)
	(cd $(MYSQL_DIR_64); gpatch -p1 < ../patches/yassl.patch)
	gpatch $(MYSQL_DIR_64)/storage/innobase/include/univ.i -i patches/inline.patch
	gpatch $(MYSQL_DIR_64)/scripts/mysql_config.sh -i patches/mysql_config.patch
	gpatch $(MYSQL_DIR_64)/mysql-test/Makefile.in -i patches/ksh-hang.patch
	gpatch $(MYSQL_DIR_64)/configure -i patches/configure.patch
	gpatch $(MYSQL_DIR_64)/sql/sql_select.cc -i patches/xO4_optimization.patch
	(cd $(MYSQL_DIR_64); touch configure.in config/ac-macros/*; sleep 5; touch aclocal.m4 config.h.in; sleep 5;\
	touch configure ; find . -name Makefile.in | xargs touch)
	find $(MYSQL_DIR_64) -type d -exec /usr/bin/chmod 755 "{}" \;
	find $(MYSQL_DIR_64) -type f -exec /usr/bin/chmod ugo+r "{}" \;
	find $(MYSQL_DIR_64) -name "dtrace_providers" -exec rm {} \;




clean: clean32 clean64

clean32:
	-rm -rf $(MYSQL_DIR)

clean64:
	-rm -rf $(MYSQL_DIR_64)
#---------------------------------------------end of MySQL Targets




aus: ../packages/BUILD/mysql-5.6.10/INSTALL-SOURCE


   The MySQL files are installed into /usr/mysql which symbolic links
   for the sub directories (bin, lib, etc.) to a version specific
   directory. For MySQL 5.6, the full installation is located in
   /usr/mysql/5.6. The default data directory is /var/mysql/5.6/data.
   The configuration file is installed in /etc/mysql/5.6/my.cnf. This
   layout permits multiple versions of MySQL to be installed, without
   overwriting the data and binaries from other versions.

   Once installed, you must run mysql_install_db to initialize the
   database, and use the mysql_secure_installation to secure your
   installation.

Using SMF to manage your MySQL installation

   Once installed, you can start and stop your MySQL server using the
   installed SMF configuration. The service name is mysql, or if you
   have multiple versions installed, you should use the full version
   name, for example mysql:version_56. To start and enable MySQL to
   be started at boot time:
shell> svcadm enable mysql

   To disable MySQL from starting during boot time, and shut the
   MySQL server down if it is running, use:
shell> svcadm disable mysql

   To restart MySQL, for example after a configuration file changes,
   use the restart option:
shell> svcadm restart mysql

   You can also use SMF to configure the data directory and enable
   full 64-bit mode. For example, to set the data directory used by
   MySQL:
shell> svccfg
svc:> select mysql:version_56
svc:/application/database/mysql:version_56> setprop mysql/data=/data0
/mysql


   By default, the 32-bit binaries are used. To enable the 64-bit
   server on 64-bit platforms, set the enable_64bit parameter. For
   example:
svc:/application/database/mysql:version_56> setprop mysql/enable_64bi
t=1

   name, for example mysql:version_56. To start and enable MySQL to
   be started at boot time:
shell> svcadm enable mysql

   To disable MySQL from starting during boot time, and shut the
   MySQL server down if it is running, use:
shell> svcadm disable mysql

   To restart MySQL, for example after a configuration file changes,
   use the restart option:
shell> svcadm restart mysql

   You can also use SMF to configure the data directory and enable
   full 64-bit mode. For example, to set the data directory used by
   MySQL:
shell> svccfg
svc:> select mysql:version_56
svc:/application/database/mysql:version_56> setprop mysql/data=/data0
/mysql


   By default, the 32-bit binaries are used. To enable the 64-bit
   server on 64-bit platforms, set the enable_64bit parameter. For
   example:
svc:/application/database/mysql:version_56> setprop mysql/enable_64bi
t=1

   You need to refresh the SMF after settings these options:
shell> svcadm refresh mysql


INSTALL-SOURCE:     * -DCMAKE_INSTALL_PREFIX=dir_name: Configure the distribution
INSTALL-SOURCE:   values for the CMAKE_INSTALL_PREFIX, MYSQL_TCP_PORT, and
INSTALL-SOURCE:   CMAKE_INSTALL_PREFIX option, which specifies the installation base
INSTALL-SOURCE:   CMAKE_INSTALL_PREFIX Installation base directory /usr/local/mysql
INSTALL-SOURCE:   INSTALL_BINDIR User executables directory PREFIX/bin
INSTALL-SOURCE:   INSTALL_DOCDIR Documentation directory PREFIX/docs
INSTALL-SOURCE:   INSTALL_DOCREADMEDIR README file directory PREFIX
INSTALL-SOURCE:   INSTALL_INCLUDEDIR Header file directory PREFIX/include
INSTALL-SOURCE:   INSTALL_INFODIR Info file directory PREFIX/docs
INSTALL-SOURCE:   INSTALL_LAYOUT Select predefined installation layout STANDALONE
INSTALL-SOURCE:   INSTALL_LIBDIR Library file directory PREFIX/lib
INSTALL-SOURCE:   INSTALL_MANDIR Manual page directory PREFIX/man
INSTALL-SOURCE:   INSTALL_MYSQLSHAREDIR Shared data directory PREFIX/share
INSTALL-SOURCE:   INSTALL_MYSQLTESTDIR mysql-test directory PREFIX/mysql-test
INSTALL-SOURCE:   INSTALL_PLUGINDIR Plugin directory PREFIX/lib/plugin
INSTALL-SOURCE:   INSTALL_SBINDIR Server executable directory PREFIX/bin
INSTALL-SOURCE:   INSTALL_SCRIPTDIR Scripts directory PREFIX/scripts
INSTALL-SOURCE:   INSTALL_SHAREDIR aclocal/mysql.m4 installation directory
INSTALL-SOURCE:   INSTALL_SQLBENCHDIR sql-bench directory PREFIX
INSTALL-SOURCE:   INSTALL_SUPPORTFILESDIR Extra support files directory
INSTALL-SOURCE:   CMAKE_INSTALL_PREFIX, MYSQL_TCP_PORT, and MYSQL_UNIX_ADDR options
INSTALL-SOURCE:   The CMAKE_INSTALL_PREFIX option indicates the base installation
INSTALL-SOURCE:   directory. Other options with names of the form INSTALL_xxx that
INSTALL-SOURCE:     * -DCMAKE_INSTALL_PREFIX=dir_name
INSTALL-SOURCE:     * -DINSTALL_BINDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_DOCDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_DOCREADMEDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_INCLUDEDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_INFODIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_LAYOUT=name
INSTALL-SOURCE:shell> cmake . -DINSTALL_LAYOUT=SVR4 -DMYSQL_DATADIR=/var/mysql/data
INSTALL-SOURCE:     * -DINSTALL_LIBDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_MANDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_MYSQLSHAREDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_MYSQLTESTDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_PLUGINDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_SBINDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_SCRIPTDIR=dir_name
INSTALL-SOURCE:       Where to install mysql_install_db.
INSTALL-SOURCE:     * -DINSTALL_SHAREDIR=dir_name
INSTALL-SOURCE:     * -DINSTALL_SQLBENCHDIR=dir_name
INSTALL-SOURCE:       directory, use an empty value (-DINSTALL_SQLBENCHDIR=).
INSTALL-SOURCE:     * -DINSTALL_SUPPORTFILESDIR=dir_name
I



