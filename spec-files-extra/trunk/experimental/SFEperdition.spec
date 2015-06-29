
# spec file for package SFEperdition

# NOTE version bumpers:  if SFEperdition does not compile well, you *might* have missed updates
#                        to the necessary SFElibvanessa-* tools !!!
#                        go uninstall the old ones first: pkgtool uninstall-pkgs SFElibvanessa-*

# NOTE version bumpers:  change the base version number in the *include* file here:
#                           include/perditionparentversion.inc

# help needed:
##TODO## add database modules, unisodbc, postgres, mysql, gdbm, others ...

##TODO## migrate the pam settings from the file /etc/perdition/pam.d/perdition over to /etc/pam.conf to the format used in Solaris - is this correct?

##TODO## might love a refresh of the patch1 for the more recent Makefile.am/Makefile.in

##TODO## check (Build)Requirements

%define src_name perdition

#set the base version number (->download dir libvanessa-* and ->perdition version)
%include perditionparentversion.inc

%define src_version %{perditionparentversion}

#be carefull with setting IPS_component_version to a valid numeric setting!!!
#make the string 1.19-rc1 reading 1.19.0.1 or forget about it and change nothing
IPS_component_version: $( echo %{perditionparentversion} | sed -e '/-rc[0-9][0-9]*/ s/-rc/.0./' )


%include Solaris.inc
%include packagenamemacros.inc
## mysql version
##TODO## enhance packagenamemacros.inc to know the variables below,
#then use the variables from packagenamemacros.inc instead defining locally
#defines by packagenamemacros.inc ... %define mysql_version 5.1
##TODO## below: move those handy _path variabled to packagenamemacros.inc
%define mysql_lib      %{_prefix}/%{mysql_default_libdir}
%define mysql_lib_path -L%{mysql_lib} -R%{mysql_lib}
%define mysql_include  %{_prefix}/%{mysql_default_includedir}
%define mysql_include_path -I%{mysql_include}



#%define cc_is_gcc 1
#%define _gpp /usr/sfw/bin/g++
#%include base.inc


Name:                    SFEperdition
IPS_Package_Name:	service/network/imap/perdition
Summary:                 perdition - POP3/IMAP proxy to route requests based on tables (migrations, server grouping, load balancing)
URL:                     http://www.vergenet.net/linux/perdition/
#remember: version is set for all required specs in the include file 
#include/perditionparentversion.inc
Version:                 %{src_version}
Source:                  http://www.vergenet.net/linux/perdition/download/%{src_version}/perdition-%{version}.tar.gz
Source2:                 perdition.xml
Patch1:			perdition-01-Makefile_in_am-LDFLAGS.diff
Patch3:			perdition-03-remove-strcasestr.diff
Patch4:			perdition-04-cont-char-gdbm_version.h.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SFElibvanessa-logger
Requires:      SFElibvanessa-logger
BuildRequires: SFElibvanessa-adt
Requires:      SFElibvanessa-adt
BuildRequires: SFElibvanessa-socket
Requires:      SFElibvanessa-socket
##TODO## Add buildrequires to mysql (optional Requires mysql)
##TODO## parametrize path to mysql/version.version
BuildRequires: SFEopenldap-gnu
Requires:      SFEopenldap-gnu

BuildRequires: %{pnm_buildrequires_SUNWgnu_dbm}
Requires:      %{pnm_requires_SUNWgnu_dbm}

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch3 -p1
if grep "extern int const gdbm_version" /usr/include/gdbm.h
 then
 %patch4 -p1
fi
cp -p %{SOURCE2} perdition.xml


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%{optflags} -I%{gnu_inc}"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc}"

export LDFLAGS="%{_ldflags} -lsocket -lxnet %{mysql_lib_path} %{gnu_lib_path}"

#spyed on perdition.spec (from source tarball)
aclocal
libtoolize --force --copy
autoheader
automake
autoconf

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir} \
            --disable-static     \
            --disable-odbc       \
            --with-mysql-includes=%{mysql_include} \
            --with-mysql-libraries=%{mysql_lib} \
            --with-ldap-includes=/usr/gnu/include \
            --with-ldap-libraries=/usr/gnu/lib  \
            --with-ldap-schema-directory=/etc/gnu/openldap/schema 


gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT 

make install DESTDIR=$RPM_BUILD_ROOT

#temporarily remove the supplied pam configuration
rm -r $RPM_BUILD_ROOT/etc/pam.d/perdition
rmdir $RPM_BUILD_ROOT/etc/pam.d

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp perdition.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

##TODO## below: /etc/perdition/pam.d/perdition not in Solaris format and location
%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
#%attr (0755, root, bin) %dir %{_sysconfdir}/openldap
#%{_sysconfdir}/openldap/*
%attr (0755, root, bin) %dir %{_sysconfdir}/gnu/openldap
%{_sysconfdir}/gnu/openldap/*
%attr (0755, root, bin) %dir %{_sysconfdir}/perdition
%class(renamenew) %{_sysconfdir}/perdition/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%config %attr(0444, root, sys)/var/svc/manifest/site/perdition.xml


%changelog
* Mon Jun 29 2015 - Thomas Wagner
- add patch4 to handle int const gdbm_version (1.11.x SFEgdbm on OM / int gdbm_version (older gdbm)
* Thu Jun 25 2015 - Thomas Wagner
- add (Build)Requires: SFEopenldap-gnu, pnm_buildrequires_SUNWgnu_dbm
- fix %files for etc/gnu/openldap
* Fri May 21 2015 - Thomas Wagner
- move SMF manifest in place for auto-import
* Thu May 21 2015 - Thomas Wagner
- bump to version 2.1 (include/perditionparentversion.inc)
- add SMF manifest, add IPS_Package_Name
- use mysql defaults for the platform from packagenamenmacros.inc
- iadd patch3 to remove strcasestr
* Sun Feb  2 2012 - Thomas Wagner
- bump to 1.19-rc4 (in file include/perditionparentversion.inc)
* Mon Aug 02 2010 - Thomas Wagner
- change %files _sbindir to catch all files *
- export Version to include/perditionparentversion.inc and detect automaticly 
  libraries version
- bump to 1.19-rc3 (in file include/perditionparentversion.inc)
* Fri Jul  9 2010 - Thomas Wagner
- missing symbol inet_*, add to LDFLAGS (-lsocket) -lxnet 
- automate IPS version numbers if you insist on using release candidates
  like 1.19-rc1 -> 1.19.0.1 is then the automatic IPS version number
- experimental add mysql (does this work at the moment, I think not)
* Fri Jul  9 2010 - Thomas Wagner
- bump to 1.18
* Sat Jul 18 2009 - Thomas Wagner
- Initial spec
