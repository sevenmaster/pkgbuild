#
# spec file for package SFEgnome-shell
#
# includes module(s): gnome-shell
#
# Note, to build GNOME Shell, you need to build the GNOME 3 modules from
# spec-files.  To access.
#
# svn co svn+ssh://anon@svn.opensolaris.org/svn/jds/spec-files/trunk

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEgnome-shell
Summary:                 GNOME Shell
Version:                 3.4.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-shell/3.4/gnome-shell-%{version}.tar.xz
# This patch is not well written, and could use work.
#
Patch1:                  gnome-shell-01-compile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           runtime/python-26
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgtk3-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWlibrsvg-devel
BuildRequires:           SUNWclutter-devel
BuildRequires:           SUNWgobject-introspection-devel
BuildRequires:           SFEgjs-devel
BuildRequires:           SFEcaribou-devel
BuildRequires:           SFElibtelepathy-devel
BuildRequires:           SFEtelepathy-logger-devel
Requires:                SUNWdbus-glib
Requires:                SUNWgtk3
Requires:                SUNWgnome-media
Requires:                SUNWlibrsvg
Requires:                SUNWclutter
Requires:                SUNWgobject-introspection
BuildRequires:           SFEcaribou
Requires:                SFEgjs
Requires:                SFEmutter
Requires:                SFElibtelepathy
Requires:                SFEtelepathy-logger
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gnome-shell-%version
%patch1 -p1

%build

# This is needed for the gobject-introspection compile to find libdrm.
export LD_LIBRARY_PATH="/usr/lib/xorg:/usr/lib/firefox"

export PYTHON=/usr/bin/python%{pythonver}
aclocal-1.11 $ACLOCAL_FLAGS -I ./m4
automake-1.11 -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --mandir=%{_mandir} \
   --sysconfdir=%{_sysconfdir} \
   --without-ca-certificates
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache icon-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-shell
%{_libdir}/gnome-shell-hotplug-sniffer
%{_libdir}/gnome-shell-perf-helper
%{_libdir}/mozilla
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/dbus-1
%{_datadir}/GConf
%{_datadir}/glib-2.0
%{_datadir}/gnome-shell
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu May 10 2012 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 3.4.1.
* Fri Oct 21 2011 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 3.2.1.
* Wed Jul 06 2011 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 3.1.3.
* Fri Oct 22 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 2.91.0.
* Wed Jun 23 2010 - Lin Ma <lin.ma@sun.com>
- Ugly build patch for gnome-shell --perf crash.
* Tue Jun 01 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 2.31.2.
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.29.1.
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.29.0.
* Thu Nov 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- No longer install the shell.desktop file since this is not an appropriate
  way to launch GNOME Shell.  Instead users should run "gnome-shell --replace"
  after starting their session.
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.28.0.
* Wed Sep 16 2009 - Halton Huo <halton.huo@sun.com>
- Bump to 2.27.3.
* Sat Sep 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.27.2.
* Wed Aug 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove missing-dash.diff and missing-svg.diff patches since they are now
  upstream.
* Wed Aug 05 2009 - Halton Huo  <halton.huo@sun.com>
- Remove upstreamed patch lookingglass.diff
- Add patch missing-dash.diff to fix bugzilla #590813
- Add patch missing-svg.diff to fix bugzilla #590814
* Mon Aug 03 2009 - Brian Cameron  <brian.cameron@sun.com>
- Add gnome-shell-03-lookingglass.diff so this javascript file gets installed.
  Otherwise gnome-shell won't start up.
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove patch gnome-shell-02-overlay.diff which no longer applies.
* Tue Apr 28 2009 - Brian Cameron  <brian.cameron@sun.com>
- Install dekstop file for GNOME Shell.
* Sat Apr 06 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
