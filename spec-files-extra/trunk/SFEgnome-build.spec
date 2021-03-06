#
# spec file for package SFEgnome-build
#
# includes module(s): gnome-build
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use gbuild = gnome-build.spec

Name:               SFEgnome-build
Summary:            gnome-build - GNOME Build Framework
Version:            %{gbuild.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SFEgdl
Requires:           SFEperl-gettext
Requires:           SUNWgnome-base-libs
Requires:           SUNWgnome-libs
Requires:           SUNWgnome-vfs
Requires:           SUNWlxml
Requires:           SUNWperl584core
BuildRequires:      SFEgdl-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}
BuildRequires:      SFEgdl-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gbuild.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%gbuild.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gbuild.install -d %name-%version

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
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
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gnome-build-*/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-build/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
#%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/gtk-doc
#%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Use %{gbuild.version} for Version
* Mon Mar 03 2008 - nonsea@users.sourceforge.net
- Add SFEperl-gettext to Requires for upgrading.
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
