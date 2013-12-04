%include Solaris.inc
%define srcname libquvi
%define _pkg_docdir %_docdir/%srcname

Name:           SFElibquvi
IPS_package_name: library/video/libquvi
Version:        0.9.4
Summary:        A cross-platform library for parsing flash media streams
License:        AGPLv3+
URL:            http://quvi.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/quvi/0.9/%srcname/%srcname-%version.tar.xz
#Patch1:		libquvi-01-luaL-register.patch  # for Lua 5.2
BuildRequires:  runtime/lua SFElua-socket
BuildRequires:  glib2
BuildRequires:  curl libgcrypt libproxy SFElibquvi-scripts
BuildRequires:  doxygen
#BuildRequires:  pkgconfig
BuildRequires:	gettext
Requires:       SFElibquvi-scripts

%description
Libquvi is a cross-platform library, with a C API, for parsing flash media
stream URLs.

%package        devel
Summary:        Development files for %{name}
Requires:       %name

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %srcname-%version
#%patch1 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lresolv -lsocket -lnsl"
./configure --prefix=/usr --enable-static=no
make
make doc

%install
rm -rf %buildroot
make install DESTDIR=%buildroot
find %buildroot -name '*.la' -delete

# Building with gcc produces this errror:
# "ERROR:quvi.c:102:test_version: stderr of child process (23784) failed to match: v?.?*"

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%doc AUTHORS ChangeLog COPYING README 
%{_libdir}/%{srcname}-0.9-%version.so
%{_mandir}/man3/%{srcname}.3*

%files devel
%defattr (-, root, bin)
%{_includedir}/quvi-0.9
%{_libdir}/%{srcname}-0.9.so
%dir %attr (-, root, other) %_libdir/pkgconfig
%{_libdir}/pkgconfig/%{srcname}-0.9.pc
%{_mandir}/man7/quvi-object.7*

%changelog
* Wed Dec  4 2013 - Alex Viskovatoff
- Bump to 0.9.4
* Sun Oct 13 2013 Alex Viskovatoff
- Import Fedora spec
* Mon Aug 26 2013 Christopher Meng <rpm@cicku.me> - 0.9.2-1
- New version.
- SPEC Cleanup.
- License changed to AGPL.
