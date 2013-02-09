
# oh well, this is in a _very_ early state. it compiles. no fine tuning. 32-bit only.

%include Solaris.inc
%include packagenamemacros.inc

%define src_name mysql

Name: SFEmysql56
Summary: MySQL Server Community Edition
Version:	5.6.10
#%define major_minor $( echo $version | awk -F'.' '{print $1 "." $2}' )
%define major_minor 5.6



Source: http://cdn.mysql.com/Downloads/MySQL-5.6/mysql-%{version}.tar.gz



%prep
%setup -q -n %{src_name}-%{version}


%build


MYSQL_VERSION="%{version}"
MYSQL_DIR=mysql-${MYSQL_VERSION}
MYSQL_DIR_64=mysql-${MYSQL_VERSION}_64
PREFIX="/usr/mysql/%{major_minor}"
CONFDIR="/etc/mysql/%{major_minor}"
DATA_PREFIX="/var/mysql/%{major_minor}"


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

#cd $(MYSQL_DIR); env - $(ENVLINE32)  /bin/ksh ./configure \
#/usr/bin/bash ./configure \
#	${COMMON_CONFIG_OPTIONS} \
#	--libexecdir=${PREFIX}/bin \
#	--bindir=${PREFIX}/bin	\
#	--libdir=${PREFIX}/lib \
#	--enable-dtrace DTRACEFLAGS='-32'

# -DINSTALL_LAYOUT=SVR4

mkdir %{bld_arch}
cd %{bld_arch}
           #-DFEATURE_SET="%{feature_set}" \
           #%{ssl_option} \
           #-DCOMPILATION_COMMENT="%{compilation_comment_debug}" \
           #-DMYSQL_SERVER_SUFFIX="%{server_suffix}"
CMAKE=cmake
  ${CMAKE} .. -DBUILD_CONFIG=mysql_release -DINSTALL_LAYOUT=SVR4 \
              -DCMAKE_INSTALL_PREFIX=${PREFIX} \
              -DMYSQL_DATADIR=${DATA_PREFIX}/data \
           -DMYSQL_DATADIR=/var/mysql/data \
           -DMYSQL_UNIX_ADDR="/tmp/mysql.sock" \
              -DINSTALL_PLUGINDIR${PREFIX}/lib/mysql/plugin \

  echo BEGIN_DEBUG_CONFIG ; egrep '^#define' include/config.h ; echo END_DEBUG_CONFIG

  gmake -j3 VERBOSE=1

%changelog
* Sat Feb  9 2013 - Thomas Wagner
- initial spec, only compiles, no fine tuning, 32-bit only


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



====erter Lauf:
BEGIN_DEBUG_CONFIG
+ egrep '^#define' include/config.h
#define MY_CONFIG_H
#define DOT_FRM_VERSION 6
#define STDC_HEADERS 1
#define HAVE_ALLOCA_H 1
#define HAVE_AIO_H 1
#define HAVE_ARPA_INET_H 1
#define HAVE_BSEARCH 1
#define HAVE_CRYPT_H 1
#define HAVE_CURSES_H 1
#define HAVE_DIRENT_H 1
#define HAVE_DLFCN_H 1
#define HAVE_EXECINFO_H 1
#define HAVE_FCNTL_H 1
#define HAVE_FENV_H 1
#define HAVE_FLOAT_H 1
#define HAVE_FLOATINGPOINT_H 1
#define HAVE_FNMATCH_H 1
#define HAVE_GRP_H 1
#define HAVE_IEEEFP_H 1
#define HAVE_INTTYPES_H 1
#define HAVE_LIMITS_H 1
#define HAVE_LOCALE_H 1
#define HAVE_MALLOC_H 1
#define HAVE_MEMORY_H 1
#define HAVE_NETINET_IN_H 1
#define HAVE_POLL_H 1
#define HAVE_PORT_H 1
#define HAVE_PWD_H 1
#define HAVE_SCHED_H 1
#define HAVE_SOLARIS_LARGE_PAGES 1
#define HAVE_STDDEF_H 1
#define HAVE_STDLIB_H 1
#define HAVE_STDARG_H 1
#define HAVE_STRINGS_H 1
#define HAVE_STRING_H 1
#define HAVE_STDINT_H 1
#define HAVE_SEMAPHORE_H 1
#define HAVE_SYNCH_H 1
#define HAVE_SYS_FILE_H 1
#define HAVE_SYS_IOCTL_H 1
#define HAVE_SYS_IPC_H 1
#define HAVE_SYS_MMAN_H 1
#define HAVE_SYS_PTE_H 1
#define HAVE_SYS_PTEM_H 1
#define HAVE_SYS_RESOURCE_H 1
#define HAVE_SYS_SELECT_H 1
#define HAVE_SYS_SHM_H 1
#define HAVE_SYS_SOCKET_H 1
#define HAVE_SYS_STAT_H 1
#define HAVE_SYS_STREAM_H 1
#define HAVE_SYS_TIMEB_H 1
#define HAVE_SYS_TIMES_H 1
#define HAVE_SYS_TIME_H 1
#define HAVE_SYS_TYPES_H 1
#define HAVE_SYS_UN_H 1
#define HAVE_TERM_H 1
#define HAVE_TERMIOS_H 1
#define HAVE_TERMIO_H 1
#define HAVE_TIME_H 1
#define HAVE_UNISTD_H 1
#define HAVE_UTIME_H 1
#define HAVE_VARARGS_H 1
#define HAVE_SYS_UTIME_H 1
#define HAVE_SYS_WAIT_H 1
#define HAVE_SYS_PARAM_H 1
#define HAVE_LIBM 1
#define HAVE_LIBSOCKET 1
#define HAVE_LIBNSL 1
#define HAVE_HIST_ENTRY 1
#define USE_LIBEDIT_INTERFACE 1
#define FIONREAD_IN_SYS_FILIO 1
#define HAVE_ALARM 1
#define HAVE_ALLOCA 1
#define HAVE_INDEX 1
#define HAVE_CHOWN 1
#define HAVE_CLOCK_GETTIME 1
#define HAVE_CRYPT 1
#define HAVE_CUSERID 1
#define HAVE_DIRECTIO 1
#define HAVE_DLERROR 1
#define HAVE_DLOPEN 1
#define HAVE_DOPRNT 1
#define HAVE_FCHMOD 1
#define HAVE_FCNTL 1
#define HAVE_FCONVERT 1
#define HAVE_FDATASYNC 1
#define HAVE_FESETROUND 1
#define HAVE_FINITE 1
#define HAVE_FP_EXCEPT 1
#define HAVE_FPSETMASK 1
#define HAVE_FSEEKO 1
#define HAVE_FSYNC 1
#define HAVE_FTIME 1
#define HAVE_GETADDRINFO 1
#define HAVE_GETCWD 1
#define HAVE_GETHOSTBYADDR_R 1
#define HAVE_GETHRTIME 1
#define HAVE_GETNAMEINFO 1
#define HAVE_GETPAGESIZE 1
#define HAVE_GETPASS 1
#define HAVE_GETPASSPHRASE 1
#define HAVE_GETPWNAM 1
#define HAVE_GETPWUID 1
#define HAVE_GETRLIMIT 1
#define HAVE_GETRUSAGE 1
#define HAVE_GETTIMEOFDAY 1
#define HAVE_GETWD 1
#define HAVE_GMTIME_R 1
#define HAVE_INITGROUPS 1
#define HAVE_ISSETUGID 1
#define HAVE_GETUID 1
#define HAVE_GETEUID 1
#define HAVE_GETGID 1
#define HAVE_GETEGID 1
#define HAVE_ISNAN 1
#define HAVE_LARGE_PAGE_OPTION 1
#define HAVE_LDIV 1
#define HAVE_LRAND48 1
#define HAVE_LOCALTIME_R 1
#define HAVE_LOG2 1
#define HAVE_LONGJMP 1
#define HAVE_LSTAT 1
#define HAVE_MEMALIGN 1
#define HAVE_NL_LANGINFO 1
#define HAVE_MADVISE 1
#define HAVE_DECL_MADVISE 1
#define HAVE_DECL_MHA_MAPSIZE_VA
#define HAVE_MEMCPY 1
#define HAVE_MEMMOVE 1
#define HAVE_MKSTEMP 1
#define HAVE_MLOCKALL 1
#define HAVE_MMAP 1
#define HAVE_MMAP64 1
#define HAVE_PERROR 1
#define HAVE_POLL 1
#define HAVE_PORT_CREATE 1
#define HAVE_POSIX_FALLOCATE 1
#define HAVE_POSIX_MEMALIGN 1
#define HAVE_PREAD 1
#define HAVE_PAUSE_INSTRUCTION 1
#define HAVE_PTHREAD_ATTR_GETSTACKSIZE 1
#define HAVE_PTHREAD_ATTR_SETSCOPE 1
#define HAVE_PTHREAD_ATTR_SETSTACKSIZE 1
#define HAVE_PTHREAD_CONDATTR_SETCLOCK 1
#define HAVE_PTHREAD_KEY_DELETE 1
#define HAVE_PTHREAD_KEY_DELETE 1
#define HAVE_PTHREAD_RWLOCK_RDLOCK 1
#define HAVE_PTHREAD_SIGMASK 1
#define PTHREAD_ONCE_INITIALIZER PTHREAD_ONCE_INIT
#define HAVE_PUTENV 1
#define HAVE_RE_COMP 1
#define HAVE_REGCOMP 1
#define HAVE_READDIR_R 1
#define HAVE_READLINK 1
#define HAVE_REALPATH 1
#define HAVE_RENAME 1
#define HAVE_RINT 1
#define HAVE_RWLOCK_INIT 1
#define HAVE_SCHED_YIELD 1
#define HAVE_SELECT 1
#define HAVE_SETENV 1
#define HAVE_SETLOCALE 1
#define HAVE_SIGADDSET 1
#define HAVE_SIGEMPTYSET 1
#define HAVE_SIGHOLD 1
#define HAVE_SIGSET 1
#define HAVE_SIGSET_T 1
#define HAVE_SIGACTION 1
#define HAVE_SIGWAIT 1
#define HAVE_SLEEP 1
#define HAVE_SNPRINTF 1
#define HAVE_STRERROR 1
#define HAVE_STRCOLL 1
#define HAVE_STRSIGNAL 1
#define HAVE_STRLCPY 1
#define HAVE_STRLCAT 1
#define HAVE_STRNLEN 1
#define HAVE_STRPBRK 1
#define HAVE_STRSEP 1
#define HAVE_STRSTR 1
#define HAVE_STRTOK_R 1
#define HAVE_STRTOL 1
#define HAVE_STRTOLL 1
#define HAVE_STRTOUL 1
#define HAVE_STRTOULL 1
#define HAVE_SHMAT 1
#define HAVE_SHMCTL 1
#define HAVE_SHMDT 1
#define HAVE_SHMGET 1
#define HAVE_TELL 1
#define HAVE_TEMPNAM 1
#define HAVE_THR_SETCONCURRENCY 1
#define HAVE_THR_YIELD 1
#define HAVE_TIME 1
#define HAVE_TIMES 1
#define HAVE_VALLOC 1
#define HAVE_VIO_READ_BUFF 1
#define HAVE_VASPRINTF 1
#define HAVE_VPRINTF 1
#define HAVE_VSNPRINTF 1
#define HAVE_FTRUNCATE 1
#define HAVE_TZNAME 1
#define HAVE_AIO_READ 1
#define HAVE_BACKTRACE 1
#define HAVE_BACKTRACE_SYMBOLS 1
#define HAVE_BACKTRACE_SYMBOLS_FD 1
#define HAVE_PRINTSTACK 1
#define HAVE_STRUCT_SOCKADDR_IN6 1
#define HAVE_STRUCT_IN6_ADDR 1
#define HAVE_IPV6 1
#define STRUCT_DIRENT_HAS_D_INO 1
#define SPRINTF_RETURNS_INT 1
#define DNS_USE_CPU_CLOCK_FOR_ID 1
#define HAVE_INET_NTOP 1
#define HAVE_SIGNAL 1
#define HAVE_TIMERADD 1
#define HAVE_TIMERCLEAR 1
#define HAVE_TIMERCMP 1
#define HAVE_TIMERISSET 1
#define HAVE_DEVPOLL 1
#define HAVE_SIGNAL_H 1
#define HAVE_SYS_DEVPOLL_H 1
#define HAVE_SYS_QUEUE_H 1
#define HAVE_TAILQFOREACH 1
#define USE_MB 1
#define USE_MB_IDENT 1
#define SIZEOF_LONG   4
#define SIZEOF_VOIDP  4
#define SIZEOF_CHARP  4
#define SIZEOF_SIZE_T 4
#define SIZEOF_CHAR 1
#define HAVE_CHAR 1
#define HAVE_LONG 1
#define HAVE_CHARP 1
#define SIZEOF_SHORT 2
#define HAVE_SHORT 1
#define SIZEOF_INT 4
#define HAVE_INT 1
#define SIZEOF_LONG_LONG 8
#define HAVE_LONG_LONG 1
#define SIZEOF_OFF_T 8
#define HAVE_OFF_T 1
#define SIZEOF_SIGSET_T 16
#define HAVE_SIGSET_T 1
#define HAVE_SIZE_T 1
#define SIZEOF_UINT 4
#define HAVE_UINT 1
#define SIZEOF_ULONG 4
#define HAVE_ULONG 1
#define SOCKET_SIZE_TYPE socklen_t
#define HAVE_MBSTATE_T
#define MAX_INDEXES 64U
#define QSORT_TYPE_IS_VOID 1
#define RETQSORTTYPE void
#define SIGNAL_RETURN_TYPE_IS_VOID 1
#define RETSIGTYPE void
#define VOID_SIGHANDLER 1
#define STRUCT_RLIMIT struct rlimit
#define C_HAS_inline 1
#define HAVE_WCTYPE_H 1
#define HAVE_WCHAR_H 1
#define HAVE_LANGINFO_H 1
#define HAVE_MBRLEN
#define HAVE_MBSRTOWCS
#define HAVE_WCRTOMB
#define HAVE_MBRTOWC
#define HAVE_WCSCOLL
#define HAVE_WCWIDTH
#define HAVE_WCTYPE
#define HAVE_ISWLOWER 1
#define HAVE_ISWUPPER 1
#define HAVE_TOWLOWER 1
#define HAVE_TOWUPPER 1
#define HAVE_ISWCTYPE 1
#define HAVE_WCHAR_T 1
#define HAVE_WCTYPE_T 1
#define HAVE_WINT_T 1
#define HAVE_STRCASECMP 1
#define HAVE_STRNCASECMP 1
#define HAVE_STRDUP 1
#define HAVE_LANGINFO_CODESET
#define HAVE_TCGETATTR 1
#define HAVE_FLOCKFILE 1
#define HAVE_WEAK_SYMBOL 1
#define HAVE_POSIX_SIGNALS 1
#define HAVE_SOLARIS_STYLE_GETHOST 1
#define HAVE_SOLARIS_ATOMIC 1
#define _LARGEFILE_SOURCE 1
#define _FILE_OFFSET_BITS 64
#define TIME_WITH_SYS_TIME 1
#define STACK_DIRECTION -1
#define SYSTEM_TYPE "solaris11"
#define MACHINE_TYPE "i386"
#define HAVE_DTRACE 1
#define SIGNAL_WITH_VIO_CLOSE 1
#define setenv(a,b,c) _putenv_s(a,b)
#define NOMINMAX
#define HAVE_SASL_SASL_H 1
#define HAVE_HTONLL 1
#define ENABLED_LOCAL_INFILE 1
#define ENABLED_PROFILING 1
#define OPTIMIZER_TRACE 1
#define INNODB_COMPILER_HINTS
#define MYSQL_DEFAULT_CHARSET_NAME "latin1"
#define MYSQL_DEFAULT_COLLATION_NAME "latin1_swedish_ci"
#define USE_MB 1
#define USE_MB_IDENT 1
#define HAVE_CHARSET_armscii8 1
#define HAVE_CHARSET_ascii 1
#define HAVE_CHARSET_big5 1
#define HAVE_CHARSET_cp1250 1
#define HAVE_CHARSET_cp1251 1
#define HAVE_CHARSET_cp1256 1
#define HAVE_CHARSET_cp1257 1
#define HAVE_CHARSET_cp850 1
#define HAVE_CHARSET_cp852 1
#define HAVE_CHARSET_cp866 1
#define HAVE_CHARSET_cp932 1
#define HAVE_CHARSET_dec8 1
#define HAVE_CHARSET_eucjpms 1
#define HAVE_CHARSET_euckr 1
#define HAVE_CHARSET_gb2312 1
#define HAVE_CHARSET_gbk 1
#define HAVE_CHARSET_geostd8 1
#define HAVE_CHARSET_greek 1
#define HAVE_CHARSET_hebrew 1
#define HAVE_CHARSET_hp8 1
#define HAVE_CHARSET_keybcs2 1
#define HAVE_CHARSET_koi8r 1
#define HAVE_CHARSET_koi8u 1
#define HAVE_CHARSET_latin1 1
#define HAVE_CHARSET_latin2 1
#define HAVE_CHARSET_latin5 1
#define HAVE_CHARSET_latin7 1
#define HAVE_CHARSET_macce 1
#define HAVE_CHARSET_macroman 1
#define HAVE_CHARSET_sjis 1
#define HAVE_CHARSET_swe7 1
#define HAVE_CHARSET_tis620 1
#define HAVE_CHARSET_ucs2 1
#define HAVE_CHARSET_ujis 1
#define HAVE_CHARSET_utf8mb4 1
#define HAVE_CHARSET_utf8 1
#define HAVE_CHARSET_utf16 1
#define HAVE_CHARSET_utf32 1
#define HAVE_UCA_COLLATIONS 1
#define HAVE_COMPRESS 1
#define HAVE_SPATIAL 1
#define HAVE_RTREE_KEYS 1
#define HAVE_QUERY_CACHE 1
#define BIG_TABLES 1
#define WITH_MYISAM_STORAGE_ENGINE 1
#define WITH_MYISAMMRG_STORAGE_ENGINE 1
#define WITH_HEAP_STORAGE_ENGINE 1
#define WITH_CSV_STORAGE_ENGINE 1
#define WITH_PARTITION_STORAGE_ENGINE 1
#define WITH_PERFSCHEMA_STORAGE_ENGINE 1
#define DEFAULT_MYSQL_HOME "/usr/mysql/5.6"
#define SHAREDIR "/usr/mysql/5.6/share"
#define DEFAULT_BASEDIR "/usr/mysql/5.6"
#define MYSQL_DATADIR "/var/mysql/data"
#define DEFAULT_CHARSET_HOME "/usr/mysql/5.6"
#define PLUGINDIR "/usr/mysql/5.6/lib/plugin"
INSTALL-SOURCE:   INSTALL_PLUGINDIR Plugin directory PREFIX/lib/plugin
#define DEFAULT_SYSCONFDIR "/usr/mysql/5.6/etc"
#define MYSQL_VERSION_MAJOR 5
#define MYSQL_VERSION_MINOR 6
#define MYSQL_VERSION_PATCH 10
#define MYSQL_VERSION_EXTRA ""
#define PACKAGE "mysql"
#define PACKAGE_BUGREPORT ""
#define PACKAGE_NAME "MySQL Server"
#define PACKAGE_STRING "MySQL Server 5.6.10"
#define PACKAGE_TARNAME "mysql"
#define PACKAGE_VERSION "5.6.10"
#define VERSION "5.6.10"
#define PROTOCOL_VERSION 10
#define SIZEOF_TIME_T 4
#define CPU_LEVEL1_DCACHE_LINESIZE 64
+ echo END_DEBUG_CONFIG
END_DEBUG_CONFIG
+
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr 0755 root sys
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1/lib 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1/lib/amd64 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1/lib/amd64/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1/lib/amd64/mysql/plugin 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1/lib/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51lib/save/pspool/SUNWmysql51lib/pkgmap:1 d none usr/mysql/5.1/lib/mysql/plugin 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none etc 0755 root sys
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none etc/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none etc/mysql/5.1 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none lib 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none lib/svc 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none lib/svc/method 0755 root bin
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var 0755 root sys
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/mysql 0700 mysql mysql
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/mysql/5.1 0700 mysql mysql
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/mysql/5.1/data 0700 mysql mysql
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/svc 0755 root sys
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/svc/manifest 0755 root sys
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/svc/manifest/application 0755 root sys
/var/sadm/pkg/SUNWmysql51r/save/pspool/SUNWmysql51r/pkgmap:1 d none var/svc/manifest/application/database 0755 root sys
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr 0755 root sys
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/mysql-test 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/sql-bench 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/sql-bench/Comments 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/sql-bench/Data 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/sql-bench/Data/ATIS 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/sql-bench/Data/Wisconsin 0755 root bin
/var/sadm/pkg/SUNWmysql51test/save/pspool/SUNWmysql51test/pkgmap:1 d none usr/mysql/5.1/sql-bench/limits 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr 0755 root sys
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/bin 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/bin 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/bin/amd64 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/docs 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/include 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/include/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/include/mysql/storage 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/man 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/man/man1 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/man/man8 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/share 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/share/aclocal 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/mysql/5.1/share/mysql 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/share 0755 root sys
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/share/man 0755 root bin
/var/sadm/pkg/SUNWmysql51u/save/pspool/SUNWmysql51u/pkgmap:1 d none usr/share/man/man1 0755 root bin
