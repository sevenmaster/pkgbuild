%include Solaris.inc
%define _pkg_docdir %_docdir/lua52
%define lua_maj_min 5.2
%define lua_revision 4

Name:           SFElua
IPS_package_name: sfe/runtime/lua
Version:        %lua_maj_min.%lua_revision
Summary:        Powerful light-weight programming language (compat version)
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%version.tar.gz
Source1:	lua.pc
# Use patches taken from OpenIndiana Userland
Patch0:		lua-01-Makefile.patch
Patch1:		lua-03-headers.patch
Patch2:		lua-04-src_Makefile.patch
BuildRequires:  readline ncurses

%description
This package contains a compatibility version of the lua-5.2 binaries.

%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires: %name

%description devel
This package contains development files for compat-lua-libs.

%prep
%setup -q -n lua-%version
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
make

%install
rm -rf %buildroot
ROOT=%buildroot make install

cd %buildroot/usr
# Rename some files to avoid conflicts with system lua
cd bin
chmod u+w lua*
# ld(1) looks in RPATH before it looks in the default paths,
# so the executable will not link with the system library
%define rpath "dyn:runpath /usr/lib/lua/%lua_maj_min"
/usr/bin/elfedit -e %rpath lua
/usr/bin/elfedit -e %rpath luac
mv lua lua%lua_maj_min
mv luac luac%lua_maj_min
cd ../share
pushd man/man1
mv lua.1 lua%lua_maj_min.1
mv luac.1 luac%lua_maj_min.1
popd
mv doc/lua doc/lua52
mkdir -p lua/%lua_maj_min
cd ../lib
mkdir -p lua/%lua_maj_min
mv liblua.so lua/%lua_maj_min
mkdir pkgconfig
cp %SOURCE1 pkgconfig/lua52.pc
cd ../include
mkdir lua%lua_maj_min
mv l*.h* lua%lua_maj_min

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%{_bindir}/lua%lua_maj_min
%{_bindir}/luac%lua_maj_min
%{_mandir}/man1/lua*%lua_maj_min.1*
%dir %attr (0755, root, other) %_docdir
%_pkg_docdir
%_libdir/lua/%lua_maj_min/liblua.so
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%lua_maj_min

%files devel
%defattr (-, root, bin)
%{_includedir}/lua%lua_maj_min/
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/lua52.pc

%changelog
* Tue Dec 22 2015 - Alex Viskovatoff <herzen@imap.cc>
- Supply lua 5.2, since S11.3 delivers lua 5.1, and remove version number
  from package name
* Tue Oct 29 2013 - Alex Viskovatoff <herzen@imap.cc>
- Import Fedora spec compat-lua.spec
* Sat Aug  3 2013 Hans de Goede <hdegoede@redhat.com> - 5.1.4-5
- New Fedora package with full lua-5.1 for use with applications not yet
  ported to 5.2
- Release fields start at 5 to be newer the compat-lua-libs from the
  non-compat lua package
