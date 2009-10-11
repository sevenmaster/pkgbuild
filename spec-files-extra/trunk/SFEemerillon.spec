#
# spec file for package SFEemerillon
#
# includes module(s): emerillon
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
Name:                    SFEemerillon
License:                 GPL v3
Group:                   Libraries/Multimedia
Version:                 0.1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Map Viewer
# date:2009-02-13 owner:yippi type:bug bugzilla:24058
Patch1:                  emerillon-01-Wl.diff
URL:                     http://www.freedesktop.org/wiki/Software/GeoClue
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWgtk2
Requires:                SUNWdbus-glib
Requires:                SUNWgnome-config
Requires:                SFElibchamplain
Requires:                SFEgeoclue
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgnome-config-devel
Requires:                SFElibchamplain-devel
BuildRequires:           SFEgeoclue-devel

%package root
Summary:		 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
mkdir -p emerillon-%version
cd emerillon-%version
rm -fR emerillon
git-clone git://git.gnome.org/emerillon
cd emerillon
%patch1 -p1

%build
cd emerillon-%version
cd emerillon
./autogen.sh \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
cd emerillon-%version
cd emerillon
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin)%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/emerillon
%dir %attr (0755, root, bin) %{_libdir}/emerillon/plugins
%dir %attr (0755, root, bin) %{_libdir}/emerillon/plugins/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/emerillon

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/emerillon.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
