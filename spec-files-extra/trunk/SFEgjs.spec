
# spec file for package SFEgjs
#
# includes module(s): gjs
#
# Note that there are some issues that you need to address to avoid build
# issues when building this module:
#
# 1) The link fails due to some errors about symbols in the Firefox JavaScript
#    include files not being defined.  These include files are found in the
#    /usr/include/firefox/js directory.  The gjs module does not actually use
#    these symbols.  Simply comment them out in the Firefox header files and
#    gjs will compile.  I am working to get this fixed upstream in the Firefox
#    header files.
#

%include Solaris.inc
Name:                    SFEgjs
Summary:                 GNOME JavaScript bindings
Version:                 0.4
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gjs/0.4/gjs-%{version}.tar.bz2
Patch1:                  gjs-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWfirefox-devel
BuildRequires:           SUNWgobject-introspection-devel
Requires:                SUNWfirefox
Requires:                SUNWgobject-introspection
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%setup -q -n gjs-%version
%patch1 -p1

%build
export LDFLAGS="-L/usr/lib/firefox"
export LD=cc
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/gjs-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gjs-1.0/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Sat Aug 29 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.4.
* Mon Aug 03 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Update to build with 0.3 tarball release.
* Tue Jul 07 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Add patch gjs-01-solaris.diff.
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
