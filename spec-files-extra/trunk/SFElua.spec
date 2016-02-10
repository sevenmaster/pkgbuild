%include Solaris.inc
%define _pkg_docdir %_docdir/lua-51

Name:           SFElua-51
IPS_package_name: runtime/lua-51
Version:        5.1.4
Summary:        Powerful light-weight programming language (compat version)
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:         lua-5.1.4-00-autotoolize.patch
Patch1:         lua-5.1.4-01-lunatic.patch
Patch2:         lua-5.1.4-02-idsize.patch
Patch3:         lua-5.1.4-03-2.patch
Patch4:         lua-5.1.4-04-pc-compat.patch
BuildRequires:  readline ncurses libtool

%description
This package contains a compatibility version of the lua-5.1 binaries.

%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires: %name

%description devel
This package contains development files for compat-lua-libs.


%prep
%setup -q -n lua-%version
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p0
%patch4 -p1
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing
# Avoid make doing auto-reconf itself, killing our rpath removel in the process
autoreconf -i -f


%build
%configure --with-readline
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i 's/ -Wall//' src/Makefile
# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
#make %{?_smp_mflags} LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"
make LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"
# also remove readline from lua.pc
sed -i 's/-lreadline -lncurses //g' etc/lua.pc


%install
rm -rf %buildroot
make install DESTDIR=%buildroot
rm %buildroot%{_libdir}/liblua.{a,la}
mkdir -p %buildroot%{_libdir}/lua/5.1
mkdir -p %buildroot%{_datadir}/lua/5.1
# Rename some files to avoid conflicts with 5.2
mv %buildroot%{_bindir}/lua %buildroot%{_bindir}/lua-5.1
mv %buildroot%{_bindir}/luac %buildroot%{_bindir}/luac-5.1
mv %buildroot%{_mandir}/man1/lua.1 \
  %buildroot%{_mandir}/man1/lua-5.1.1
mv %buildroot%{_mandir}/man1/luac.1 \
  %buildroot%{_mandir}/man1/luac-5.1.1
mkdir -p %buildroot%{_includedir}/lua-5.1
mv %buildroot%{_includedir}/l*h* %buildroot%{_includedir}/lua-5.1
rm %buildroot%{_libdir}/liblua.so
mv %buildroot%{_libdir}/pkgconfig/lua.pc \
  %buildroot%{_libdir}/pkgconfig/lua-5.1.pc


%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%{_bindir}/lua-5.1
%{_bindir}/luac-5.1
%{_mandir}/man1/lua*5.1.1*
%doc COPYRIGHT HISTORY README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_libdir}/liblua-5.1.so
%dir %{_libdir}/lua
%dir %{_libdir}/lua/5.1
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.1

%files devel
%defattr (-, root, bin)
%{_includedir}/lua-5.1/
%dir %attr (0755, root, other) %_libdir/pkgconfig
%{_libdir}/pkgconfig/lua-5.1.pc


%changelog
* Tue Oct 29 2013 - Alex Viskovatoff <herzen@imapmail.org>
- Import Fedora spec compat-lua.spec
* Sat Aug  3 2013 Hans de Goede <hdegoede@redhat.com> - 5.1.4-5
- New Fedora package with full lua-5.1 for use with applications not yet
  ported to 5.2
- Release fields start at 5 to be newer the compat-lua-libs from the
  non-compat lua package
