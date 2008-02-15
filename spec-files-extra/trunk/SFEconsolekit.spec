#
# spec file for package SFEconsolekit
#
# includes module(s): ConsoleKit
#
%include Solaris.inc

# build with dbus support unless --without-dbus is used
%define with_dbus %{?_without_dbus:0}%{?!_without_dbus:1}

Name:                    SFEconsolekit
Summary:                 Framework for tracking users, login sessions, and seats.
Version:                 0.2.9
Source:                  http://people.freedesktop.org/~mccann/dist/ConsoleKit-%{version}.tar.gz
Patch1:                  ConsoleKit-01-nox11check.diff
Patch2:                  ConsoleKit-02-emptystruct.diff
Patch3:                  ConsoleKit-03-paths.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-bindings-devel
Requires: SUNWgnome-libs
Requires: SUNWdbus
Requires: SUNWdbus-bindings
Requires: %name-root
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif
%if %option_with_fox
Requires: FSWxorg-clientlibs
Requires: FSWxwrtl
BuildRequires: FSWxorg-headers
%else
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxorg-clientlibs
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n ConsoleKit-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
%if %option_with_fox
# for <X11/Xlib.h>
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}                     \
            --libexecdir=%{_libexecdir}             \
            --localstatedir=%{_localstatedir}       \
            --sysconfdir=%{_sysconfdir}             \
            --enable-rbac-shutdown=solaris.system.shutdown

make
# Not sure why this is breaking the build, commenting out for now.
#make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

# Create needed log directory.
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ConsoleKit
touch $RPM_BUILD_ROOT%{_localstatedir}/log/ConsoleKit/history

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/ConsoleKit
%{_libexecdir}/ck-collect-session-info
%{_libexecdir}/ck-get-x11-server-pid
%{_libexecdir}/ck-get-x11-display-device
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1
%{_mandir}/man8

%files root
%defattr (-, root, sys)
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_sysconfdir}/ConsoleKit/run-session.d
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%dir %attr (0755, root, sys) %dir %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0755, root, root) %{_localstatedir}/log/ConsoleKit
%attr (0644, root, root) %{_localstatedir}/log/ConsoleKit/history
%{_localstatedir}/run/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%changelog
* Fri Feb 15 2008 - brian.cameron@sun.com
- Rework ConsoleKit-03-paths.diff so it makes better use of #ifdefs.
* Fri Feb 15 2008 - simon.zheng@sun.com
- Bump to 0.2.9. Add ConsoleKit-03-noheaderpaths.diff because there's not
  header paths.h on Solaris.
* Thu Feb 07 2008 - Brian.Cameron@sun.com
- Add /var/log/ConsoleKit/history file to packaging.
* Thu Jan 31 2008 - Brian.Cameron@sun.com
- Bump to 0.2.7.  Remove two upstream patches added on January 25,
  2007.
* Fri Jan 25 2008 - Brian.Cameron@sun.com
- Bump to 0.2.6.  Rework patches.  Add patch ConsoleKit-02-RBAC.diff
  to make ConsoleKit use RBAC instead of PolicyKit on Solaris.
  Patch ConsoleKit-03-fixbugs.diff fixes some bugs I found.
* Tue Sep 18 2007 - Brian.Cameron@sun.com
- Bump to 0.2.3.  Remove upstream ConsoleKit-01-head.diff
  patch and add ConsoleKit-02-fixsolaris.diff to fix some
  issues building ConsoleKit when VT is not present.
* Mon Aug 16 2007 - Brian.Cameron@sun.com
- Created.
