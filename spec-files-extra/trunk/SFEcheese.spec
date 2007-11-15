#
# spec file for package SFEcheese
#
# includes module(s): cheese
#
%include Solaris.inc

Name:                    SFEcheese
Summary:                 Cheese - GNOME application for taking pictures and videos from a webcam
Version:                 0.2.3
#Source:                  http://live.gnome.org/Cheese/Releases?action=AttachFile&do=get&target=cheese-%{version}.tar.gz
Source:                  http://trisk.acm.jhu.edu/cheese-%{version}.tar.gz
Patch1:                  cheese-01-nongnu.diff
Patch2:                  cheese-02-sunpro.diff
Patch3:                  cheese-03-flags.diff
Patch4:                  cheese-04-threads.diff
%if %option_with_gnu_iconv
Patch5:                  cheese-05-gnu-iconv.diff
$endif
URL:                     http://live.gnome.org/Cheese
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWevolution-data-server-devel
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-media
Requires: SUNWgnome-vfs
Requires: SUNWdbus
Requires: SUNWevolution-data-server
%if %option_with_fox
Requires: FSWxorg-clientlibs
Requires: FSWxwrtl
BuildRequires: FSWxorg-headers
%else
Requires: SUNWxwrtl
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n cheese-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%if %option_with_gnu_iconv
%patch5 -p1
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -mt `pkg-config --cflags gtk+-2.0` `pkg-config --cflags libglade-2.0` `pkg-config --cflags dbus-1` `pkg-config --cflags gnome-vfs-2.0` `pkg-config --cflags libgnomeui-2.0` `pkg-config --cflags gstreamer-0.10` `pkg-config --cflags libebook-1.2`"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export LDFLAGS="%{_ldflags} -lc -mt -lpthread `pkg-config --libs gtk+-2.0` `pkg-config --libs libglade-2.0` `pkg-config --libs dbus-1` `pkg-config --libs gnome-vfs-2.0` `pkg-config --libs libgnomeui-2.0` `pkg-config --libs gstreamer-0.10` -lgstinterfaces-0.10 `pkg-config --libs libebook-1.2` -lXxf86vm"

CFLAGS="$CFLAGS" ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} 

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/cheese
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/cheese
%{_datadir}/cheese/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Add support for Indiana build via CFLAGS change and 05-gnu-iconv patch.

* Thu Aug 30 2007 - trisk@acm.jhu.edu
- Initial spec
