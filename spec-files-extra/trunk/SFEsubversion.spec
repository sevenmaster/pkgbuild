#
# spec file for package SFEsubversion
#
# includes module(s): subversion
#
%include Solaris.inc
%include usr-gnu.inc

%include packagenamemacros.inc

#get multiple dependencies (wrong), so disable it and do it manually
%define _use_internal_dependency_generator 0

Name:			SFEsubversion
IPS_package_name:	developer/versioning/gnu/subversion
License:		Apache,LGPL,BSD
Group:			Development/Source Code Management
Version:		1.8.11
Summary:		The Subversion Source Control Management System (/usr/gnu)
Source:			http://mirror.serversupportforum.de/apache/subversion/subversion-%{version}.tar.bz2

# Home-grown svn-config needed by kdesdk
Source1:                svn-config
#Patch1:                 subversion-01-libneon.la.diff
URL:			http://subversion.tigris.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_basedir}

# missing package
#BuildRequires: SFEserf
#Requires:      SFEserf

# 10 system/library/security/gss
BuildRequires:  %{pnm_buildrequires_SUNWgss_devel}
Requires:	%{pnm_buildrequires_SUNWgss}

#  1 database/sqlite-3
BuildRequires:     %{pnm_buildrequires_SUNWsqlite3}
Requires:          %{pnm_requires_SUNWsqlite3}

BuildRequires: %{pnm_buildrequires_SUNWgnu_dbm}
Requires:      %{pnm_requires_SUNWgnu_dbm}
BuildRequires: %{pnm_buildrequires_SUNWlibms}
Requires:      %{pnm_requires_SUNWlibms}
#  7 library/zlib
BuildRequires: %{pnm_buildrequires_SUNWzlib}
Requires:      %{pnm_requires_SUNWzlib}
#paused# S10 SXCE Requires: SUNWpostrun
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
Requires:      %{pnm_requires_SUNWopenssl}
#  5 library/expat
BuildRequires: %{pnm_buildrequires_SUNWlexpt}
Requires:      %{pnm_requires_SUNWlexpt}
BuildRequires: %{pnm_buildrequires_python_default}
Requires:      %{pnm_requires_python_default}
BuildRequires: %{pnm_buildrequires_SUNWgnu_dbm}
Requires:      %{pnm_requires_SUNWgnu_dbm}
#  3 library/apr-15
#  4 library/apr-util-15
##TODO## change to something like apr_default apr_util_default once this appears in osbuilds
BuildRequires: %{pnm_buildrequires_apr_default}
Requires:      %{pnm_requires_apr_default}
BuildRequires: %{pnm_buildrequires_apr_util_default}
Requires:      %{pnm_requires_apr_util_default}
%if %{omnios}
#no apache here, except you build your own or SFE adds one
%else
BuildRequires: %{pnm_buildrequires_apache2_default}
Requires: %{pnm_requires_apache2_default}
%endif
BuildRequires:  %{pnm_buildrequires_SUNWbash}

%description
Subversion source code management system.
Installs into /usr/gnu directories, please set your
$PATH=/usr/gnu/bin:$PATH or use full path names.

%if %{omnios}
Currently there are no apache modules on OmniOS.
Maybe they can be added to SFE one day.
%else
If you want the apache modules, use the libexec directory
/usr/gnu/apache2/2.2/libexec/ when configuring Apache to
find the modules mod_authz_svn.so and mod_dav_svn.so
(note the /usr/gnu/ prefix!)
%endif


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n subversion-%{version}
#%patch1 -p1 -b .patch01

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%{optflags} -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
#from userland-gate components/subversion/Makefile
#https://hg.openindiana.org/upstream/oracle/userland-gate/file/ebe894a8833e/components/subversion/Makefile
export CFLAGS="${CFLAGS} -features=extensions"
export CFLAGS="${CFLAGS} -xustr=ascii_utf16_ushort -xcsi"
export CXXFLAGS="%{cxx_optflags} -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="${CXXFLAGS} -features=nestedaccess,tmplife,tmplrefstatic"
export CXXFLAGS="${CXXFLAGS} -template=geninlinefuncs"
export CXXFLAGS="${CXXFLAGS} -verbose=template"
export CXXFLAGS="${CXXFLAGS} -xustr=ascii_utf16_ushort"
export CXXFLAGS="${CXXFLAGS} -mt -D_REENTRANT -DNDEBUG -DSOLARIS"
export LDFLAGS="%{_ldflags} -L%{_basedir}/%{apr_default_libdir}:%{_basedir}/%{apr_util_default_libdir} -R%{_basedir}/%{apr_default_libdir}:%{_basedir}/%{apr_util_default_libdir}"


#from userland-gate components/subversion/Makefile
##TODO## read the Makefile again and see if more tweaks do make sense / are necessary

./configure                        \
    --prefix=%{_prefix}            \
    --exec-prefix=%{_prefix}       \
    --mandir=%{_mandir}            \
    --infodir=%{_infodir}          \
    --libdir=%{_libdir}/svn        \
    --localstatedir=%{_std_localstatedir} \
    --enable-shared                \
    --disable-static               \
    --with-pic                     \
    --disable-mod-activation       \
    --with-openssl                 \
    --with-apr=%{_basedir}/%{apr_default_basedir}   \
    --with-apr-util=%{_basedir}/%{apr_util_default_basedir} \
%if %{omnios}
%else
    --with-apxs=%{_basedir}/%{apache2_default_apxs} \
    --with-apache-libexecdir=%{_prefix}/%{apache2_default_libexecdir} \
%endif
    --disable-libtool-lock         \
    --disable-experimental-libtool \
    --enable-nls                   \
    --with-gssapi=%{_basedir}      \

  # optional: --with-libmagic=PREFIX  libmagic filetype detection library
  # why should we disable?
  #  --without-berkeley-db          \

  #  --with-apr=%{_basedir}/apr/1.3                  \
  #  --with-apr-util=%{_basedir}/apr-util/1.3        \

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
LD_LIBRARY_PATH=/usr/gnu/lib/svn gmake install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Patch svn-config with the correct version
cat $RPM_BUILD_ROOT%{_bindir}/svn-config | sed s/SVN_VERSION/%{version}/ > $RPM_BUILD_ROOT%{_bindir}/svn-config.new
mv $RPM_BUILD_ROOT%{_bindir}/svn-config.new $RPM_BUILD_ROOT%{_bindir}/svn-config
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/svn-config

find  $RPM_BUILD_ROOT%{_libdir}/svn -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/svn*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/svn/lib*.so*
%if %{omnios}
#no apache here, except you build your own
%else
%{_prefix}/apache2
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jan 17 2015 - Thomas Wagner
- change (Build)Requires to  %{pnm_buildrequires_apr_default} %{pnm_buildrequires_apr_util_default}
  use pnm_macros to point to the apr and apr-util install directories
* Fri Jan 16 2015 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWopenssl} SUNWzlib SUNWbzip, %include packagenamacros.inc
  SUNWsqlite3
- relocate apache2 modules to /usr/gnu/apache2/2.2/libexec and exclude apache / apxs / apr on OmniOS
- bump to 1.8.11
* Fri Sep 13 2013 - Alex Viskovatoff
- Update to 1.7.13
- Use usr-gnu.inc
* Mon Feb 25 2008 - laca@sun.com
- build against either SUNWneon or SFEneon
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Major rework to install in /usr/gnu and avoid conflict with SUNWsvn
- Depends on two new package SFElibapr and SFEaprutil. Having svn to depend on whole
- of Apache seems a bit of an overkill. These are also needed by kdesdk.
- Bumped version to 1.4.6
- Package a home-grown svn-config to satisfy a few software like kdesdk.
* Thu Jan  3 2008 - laca@sun.com
- update apache2 location for newer nevada builds
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 1.4.3.
- Remove "-I/usr/sfw/include" from CFLAGS and 
  "-L/usr/sfw/lib -R/usr/sfw/lib" from LDFLAGS to build pass
- Nevada bundle neon, Change require from SFEneon to SUNWneon
* Sat Oct 14 2006 - laca@sun.com
- disable parallel build as it breaks on multicpu systems
- bump to 1.4.0
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Fri Jul  7 2006 - laca@sun.com
- rename to SFEsubversion
- add info stuff
- add some configure options to enable ssl, apache, https support
- add devel and l10n pkgs
* Sat Jan  7 2006  <glynn.foster@sun.com>
- initial version
