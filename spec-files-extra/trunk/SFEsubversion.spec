#
# spec file for package SFEsubversion
#
# includes module(s): subversion
#
%include Solaris.inc
%include usr-gnu.inc

%define package_svn_apache %(/usr/bin/pkginfo -q SUNWsvn && echo 0 || echo 1)

Name:			SFEsubversion
IPS_package_name:	sfe/developer/versioning/subversion
License:		Apache,LGPL,BSD
Group:			Development/Source Code Management
Version:		1.7.13
#Release:		1
Summary:		The Subversion Source Control Management System
Source:			http://subversion.tigris.org/downloads/subversion-%{version}.tar.bz2

# Home-grown svn-config needed by kdesdk
Source1:                svn-config
#Patch1:                 subversion-01-libneon.la.diff
URL:			http://subversion.tigris.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWcsl
Requires: SUNWcsr
#Requires: SFEgdbm
Requires: library/database/gdbm
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWpostrun
Requires: SUNWopenssl-libraries
Requires: SUNWlexpt
#%if %(pkginfo -q SUNWneon && echo 1 || echo 0)
Requires: SUNWneon
# %else
# Requires: SFEneon
# %endif
Requires: library/apr-13
Requires: library/apr-util-13
BuildRequires: SUNWPython
BuildRequires: SUNWopenssl-include
#BuildRequires: SFEgdbm-devel
BuildRequires: library/database/gdbm
#BuildRequires: SUNWapch22u
BuildRequires: web/server/apache-22
BuildRequires: library/apr-13
BuildRequires: library/apr-util-13
BuildConflicts: CBEsvn

%description
Subversion source code management system.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWbash
Requires: SUNWopenssl-include
Requires: SFEgdbm-devel
Requires: SUNWPython
Requires: library/apr-13
Requires: library/apr-util-13
%if %package_svn_apache
Requires: web/server/apache-22
%endif

%if %package_svn_apache
%package usr
Summary:                 %{summary} - Apache2 modules
SUNW_BaseDir:            %_basedir
%include default-depend.inc
Requires:                %{name}
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %_prefix
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n subversion-%{version}
#%patch1 -p1 -b .patch01

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LDFLAGS="%_ldflags -L$RPM_BUILD_ROOT%{_libdir} -R/usr/apr/1.3/lib:/usr/apr-util/1.3/lib"

./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --disable-static \
    --with-pic \
    --disable-mod-activation \
    --mandir=%{_mandir} \
    --with-ssl \
    --infodir=%{_infodir} \
    --without-berkeley-db \
    --with-apr=%_basedir/apr/1.3/bin/apr-1-config \
    --with-apr-util=%_basedir/apr-util/1.3/bin/apu-1-config \
    --with-neon=%_basedir

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Patch svn-config with the correct version
cat $RPM_BUILD_ROOT%{_bindir}/svn-config | sed s/SVN_VERSION/%{version}/ > $RPM_BUILD_ROOT%{_bindir}/svn-config.new
mv $RPM_BUILD_ROOT%{_bindir}/svn-config.new $RPM_BUILD_ROOT%{_bindir}/svn-config
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/svn-config

%if %package_svn_apache
%else
rm -rf ${RPM_BUILD_ROOT}%_prefix/apache2
%endif

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
%{_libdir}/lib*.so*
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

%if %package_svn_apache
%files usr
%defattr (-, root, bin)
%_basedir/apache2
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
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
