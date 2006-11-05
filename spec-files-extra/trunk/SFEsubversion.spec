#
# spec file for package SFEsubversion
#
# includes module(s): subversion
#
%include Solaris.inc

Name:			SFEsubversion
License:		Apache,LGPL,BSD
Group:			system/dscm
Version:		1.4.0
Release:		1
Summary:		Subversion SCM
Source:			http://subversion.tigris.org/downloads/subversion-%{version}.tar.bz2
Patch1:                 subversion-01-libneon.la.diff
URL:			http://subversion.tigris.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWcsl
Requires: SUNWcsr
Requires: SFEgdbm
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWpostrun
Requires: SUNWopenssl-libraries
Requires: SUNWlexpt
Requires: SFEneon
BuildRequires: SUNWopenssl-include
BuildRequires: SFEgdbm-devel
BuildRequires: SFEneon-devel
BuildConflicts: CBEsvn

%description
Subversion source code management system.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWbash

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n subversion-%{version}
%patch1 -p1 -b .patch01

%build
export CFLAGS="%optflags -I/usr/sfw/include -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export CPPFLAGS="-I/usr/sfw/include"
export LD=/usr/ccs/bin/ld
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib -L$RPM_BUILD_ROOT%{_libdir}"
export PATH=$PATH:/usr/apache2/bin
aclocal -I build/ac-macros
autoconf
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --disable-static \
    --with-apxs=/usr/apache2/bin/apxs \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --disable-mod-activation \
    --mandir=%{_mandir} \
    --with-ssl \
    --infodir=%{_infodir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

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
/usr/apache2

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
