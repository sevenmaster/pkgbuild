%include Solaris.inc
%define luaver 5.2
%define lualibdir %_libdir/lua/%luaver
%define luapkgdir %_datadir/lua/%luaver

Name:           SFElua-expat
IPS_package_name: library/lua/expat
Version:        1.2.0
Summary:        SAX XML parser based on the Expat library
Group:          Development/Libraries
License:        MIT
URL:            http://www.keplerproject.org/luaexpat/
Source0:        http://matthewwild.co.uk/projects/luaexpat/luaexpat-%{version}.tar.gz
# http://code.matthewwild.co.uk/lua-expat/rev/e981a82571cf
Patch0:		lua-expat-lua-5.2.patch
# http://code.matthewwild.co.uk/lua-expat/rev/b2a77ebe7aed
Patch1:		lua-expat-lua-5.2-test-fix.patch

BuildRequires:  runtime/lua
BuildRequires:  expat
Requires:       lua

%description
LuaExpat is a SAX XML parser based on the Expat library.

%prep
%setup -q -n luaexpat-%{version}
%patch0 -p1 -b .lua-52
%patch1 -p1 -b .testfix


%build
make PREFIX=%_prefix LUA_LIBDIR=%lualibdir LUA_DIR=%luapkgdir LUA_INC=%_includedir/lua-%luaver EXPAT_INC=%_includedir CC=cc CFLAGS="%optflags -KPIC -I%_includedir/lua-%luaver"  LUA_VERSION_NUM=502
/usr/bin/iconv -f ISO8859-1 -t UTF8 README >README.UTF8
mv -f README.UTF8 README


%install
rm -rf %buildroot
make install PREFIX=%_prefix LUA_LIBDIR=%buildroot%lualibdir LUA_DIR=%buildroot%luapkgdir LUA_VERSION_NUM=502


%check
pushd src
ln -s lxp.so.* lxp.so
popd
lua -e 'package.cpath="./src/?.so;"..package.cpath; dofile("tests/test.lua");'
lua -e 'package.cpath="./src/?.so;" .. package.cpath; package.path="./src/?.lua;" .. package.path; dofile("tests/test-lom.lua");'

%clean
rm -rf %buildroot


%files
%defattr(-,root,bin)
%doc README doc/us/*
%{lualibdir}/*
%{luapkgdir}/*


%changelog
* Wed Dec  4 2013 - Alex Viskovatoff
- Use Lua 5.2
* Wed Oct 30 2013 - Alex Viskovatoff
- Import Fedora spec
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 1.2.0-5
- fix for lua 5.2
