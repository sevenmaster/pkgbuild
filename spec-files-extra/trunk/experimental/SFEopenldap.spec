
#
# spec file for package SFEopenldap.spec
#

# NOTE: some distributions provide theyr own openldap package,
#       you only want his package here in case you need special
#       options set/compiled in

# for now:  32-bit *only*, 32/64-bit can be added on request

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

#avoid ovelapping with SUNWhea and SUNWman
%include usr-gnu.inc


%define src_name openldap


Name:                    SFEopenldap
##TODO##
#IPS_package_name:   
#Group:
Summary:                 OpenLDAP - LDAP Server, Tools and Libraries
URL:                     http://www.openldap.org
Version:                 2.4.38
Source:                  http://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source2:		ldap-olslapd.xml
Source3:		openldap-exec_attr
Source4:		openldap-prof_attr
SUNW_Copyright:		 %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

##TODOä## make (Build)Requires complete
BuildRequires:   SFEbdb
Requires:        SFEbdb
#BuildRequires:   SFEgcc
#Requires:        SFEgcc-runtime

#if not using usr-gnu.inc, then
#Conflicts: SUNWopenldap,SUNWopenldapu,SUNWopenldapr

Requires: %name-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /

%description
OpenLDAP Server, Tools and Libraries
Replaces distro provided LDAP Server package


%prep
%setup -q -n %{src_name}-%version

cp -p %{SOURCE2}  ldap-olslapd.xml
cp -p %{SOURCE3}  openldap-exec_attr
cp -p %{SOURCE4}  openldap-prof_attr

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#we use SFEbdb

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export CPPFLAGS=${CXXFLAGS}
export LDFLAGS="%_ldflags %{gnu_lib_path}"

export RUNDIR="%{_std_localstatedir}/run/%{src_name}"

#note: at the moment %install section moves binaries from %{_bindir} over to %{gnu_bin}
#note: at the moment %install section moves one library from %{_libdir} over to %{gnu_lib}
./configure --prefix=%{_prefix}				\
            --libexecdir=%{_libexecdir}			\
            --sysconfdir=%{_sysconfdir}			\
            --localstatedir=%{_localstatedir}/%{src_name}\
            --enable-wrappers		\
            --disable-static

##TODO## choose options, add (Build)Requires and then remove the comments below
#    --enable-dynacl	  enable run-time loadable ACL support (experimental) [no]
#    --enable-aci	  enable per-object ACIs (experimental) no|yes|mod [no]
#    --enable-cleartext	  enable cleartext passwords [yes]
#    --enable-crypt	  enable crypt(3) passwords [no]
#    --enable-lmpasswd	  enable LAN Manager passwords [no]
#    --enable-spasswd	  enable (Cyrus) SASL password verification [no]
#    --enable-modules	  enable dynamic module support [no]
#    --enable-rewrite	  enable DN rewriting in back-ldap and rwm overlay [auto]
#    --enable-rlookups	  enable reverse lookups of client hostnames [no]
#    --enable-slapi        enable SLAPI support (experimental) [no]
#    --enable-slp          enable SLPv2 support [no]
#    --enable-wrappers	  enable tcp wrapper support [no]

#SLAPD Backend Options:
#    --enable-backends	  enable all available backends no|yes|mod
#    --enable-bdb	  enable Berkeley DB backend no|yes|mod [yes]
#    --enable-dnssrv	  enable dnssrv backend no|yes|mod [no]
#    --enable-hdb	  enable Hierarchical DB backend no|yes|mod [yes]
#    --enable-ldap	  enable ldap backend no|yes|mod [no]
#    --enable-meta	  enable metadirectory backend no|yes|mod [no]
#    --enable-monitor	  enable monitor backend no|yes|mod [yes]
#    --enable-ndb	  enable MySQL NDB Cluster backend no|yes|mod [no]
#    --enable-null	  enable null backend no|yes|mod [no]
#    --enable-passwd	  enable passwd backend no|yes|mod [no]
#    --enable-perl	  enable perl backend no|yes|mod [no]
#    --enable-relay  	  enable relay backend no|yes|mod [yes]
#    --enable-shell	  enable shell backend no|yes|mod [no]
#    --enable-sock	  enable sock backend no|yes|mod [no]
#    --enable-sql	  enable sql backend no|yes|mod [no]

#SLAPD Overlay Options:
#    --enable-overlays	  enable all available overlays no|yes|mod
#    --enable-accesslog	  In-Directory Access Logging overlay no|yes|mod [no]
#    --enable-auditlog	  Audit Logging overlay no|yes|mod [no]
#    --enable-collect	  Collect overlay no|yes|mod [no]
#    --enable-constraint	  Attribute Constraint overlay no|yes|mod [no]
#    --enable-dds  	  Dynamic Directory Services overlay no|yes|mod [no]
#    --enable-deref	  Dereference overlay no|yes|mod [no]
#    --enable-dyngroup	  Dynamic Group overlay no|yes|mod [no]
#    --enable-dynlist	  Dynamic List overlay no|yes|mod [no]
#    --enable-memberof	  Reverse Group Membership overlay no|yes|mod [no]
#    --enable-ppolicy	  Password Policy overlay no|yes|mod [no]
#    --enable-proxycache	  Proxy Cache overlay no|yes|mod [no]
#    --enable-refint	  Referential Integrity overlay no|yes|mod [no]
#    --enable-retcode	  Return Code testing overlay no|yes|mod [no]
#    --enable-rwm       	  Rewrite/Remap overlay no|yes|mod [no]
#    --enable-seqmod	  Sequential Modify overlay no|yes|mod [no]
#    --enable-sssvlv	  ServerSideSort/VLV overlay no|yes|mod [no]
#    --enable-syncprov	  Syncrepl Provider overlay no|yes|mod [yes]
#    --enable-translucent  Translucent Proxy overlay no|yes|mod [no]
#    --enable-unique       Attribute Uniqueness overlay no|yes|mod [no]
#    --enable-valsort      Value Sorting overlay no|yes|mod [no]


#Optional Packages:
#  --with-PACKAGE[=ARG]    use PACKAGE [ARG=yes]
#  --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
#  --with-subdir=DIR       change default subdirectory used for installs
#  --with-cyrus-sasl	  with Cyrus SASL support [auto]
#  --with-fetch		  with fetch(3) URL support [auto]
#  --with-threads	  with threads [auto]
#  --with-tls		  with TLS/SSL support auto|openssl|gnutls|moznss [auto]
#  --with-yielding-select  with implicitly yielding select [auto]
#  --with-mp               with multiple precision statistics auto|longlong|long|bignum|gmp [auto]
#  --with-odbc             with specific ODBC support iodbc|unixodbc|odbc32|auto [auto]
#  --with-gnu-ld           assume the C compiler uses GNU ld [default=no]
#  --with-pic              try to use only PIC/non-PIC objects [default=use
#                          both]
#  --with-tags[=TAGS]      include additional configurations [automatic]


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

[ -d $RPM_BUILD_ROOT%{_datadir}/doc/%{src_name} ] || mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{src_name}
cp [A-Z][A-Z]* $RPM_BUILD_ROOT%{_datadir}/doc/%{src_name}

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network/ldap/
cp ldap-olslapd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/network/ldap/

mkdir -p $RPM_BUILD_ROOT%{_std_sysconfdir}/security/exec_attr.d
mkdir -p $RPM_BUILD_ROOT%{_std_sysconfdir}/security/prof_attr.d
cp  openldap-exec_attr $RPM_BUILD_ROOT%{_std_sysconfdir}/security/exec_attr.d/%{name}
cp  openldap-prof_attr $RPM_BUILD_ROOT%{_std_sysconfdir}/security/prof_attr.d/%{name}

#clean from static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

#relocate a few binaries, relocate one basic client library to usr_gnu
#mkdir -p $RPM_BUILD_ROOT%{gnu_bin}/
#mv $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT/%{gnu_bin}/
#rmdir $RPM_BUILD_ROOT%{_bindir}
#mkdir -p $RPM_BUILD_ROOT%{gnu_lib}/
#mv $RPM_BUILD_ROOT%{_libdir}/libldap.so* $RPM_BUILD_ROOT/%{gnu_lib}/
#not moving, instead remove the symlink (let OS ldap package's symlink in place)
#rm $RPM_BUILD_ROOT%{_libdir}/libldap.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
#moved to /usr/gnu/bin
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%dir %attr (0755, root, bin) %{gnu_bin}
#%{gnu_bin}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
#see %install, paused - symlink removed
#%dir %attr (0755, root, bin) %{gnu_lib}
#%{gnu_lib}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files root
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_std_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{src_name}
%attr (-, openldap, openldap) %{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_std_sysconfdir}/security
%{_std_sysconfdir}/security/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%defattr (-, openldap, openldap)
%dir %attr (0700, openldap, openldap) %{_localstatedir}/%{src_name}
%{_localstatedir}/%{src_name}/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_std_localstatedir}
%dir %attr (0755, root, sys) %{_std_localstatedir}/svc
%dir %attr (0755, root, sys) %{_std_localstatedir}/svc/manifest
%class(manifest) %attr(0444, root, sys)%{_std_localstatedir}/svc/manifest/network/ldap/ldap-olslapd.xml

%changelog
* Tue Jan 21 2014 - Thomas Wagner
- bump to 2.4.38
- remove typo in CXXLAGS -> CXXFLAGS (no finds right BDB db.h in %{gnu_inc}, export CPPFLAGS=${CXXFLAGS}
- remove depenency on %name in package %name-root
* Sat Oct  8 2011 - Thomas Wagner
- add SMF manifest (copied from distro, modified), add security/ RBAC info (copied from distro, modified)
* Fri Oct  7 2011 - Thomas Wagner
- Initial spec
