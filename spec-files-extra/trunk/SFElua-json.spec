%include Solaris.inc
%define luaver 5.2
%define luapkgdir %{_datadir}/lua/%{luaver}
%define commit 7a86bc22066858afeb23845a191a6ab680b46233
%define shortcommit %(c=%{commit}; echo ${c:0:7})
%define upstreamname luajson
%define _pkg_docdir %_docdir/%upstreamname

Name:           SFElua-json
IPS_package_name: library/lua/json
Version:        1.3.2
Summary:        JSON Parser/Constructor for Lua
Group:          Development/Libraries
License:        MIT
URL:            http://luaforge.net/projects/luajson/
Source0:        http://github.com/harningt/luajson/archive/%{commit}/luajson-%{version}-%{shortcommit}.tar.gz
Patch0:		luajson-lua-5.2.patch
BuildRoot:      %_tmppath/%name-%version-root
BuildRequires:  runtime/lua, library/lua/lpeg
# for checks
#BuildRequires:  SFElua-filesystem, SFElua-lunit
Requires:       lua
BuildArch:      noarch

%description
LuaJSON is a customizable JSON decoder/encoder, using LPEG for parsing.

%prep
%setup -q -n luajson-%{commit}
%patch0 -p1 -b .lua-52

%build

%install
rm -rf %buildroot
mkdir -p %buildroot/%{luapkgdir}
cp -pr lua/* %buildroot/%{luapkgdir}

#%check
#make check-regression
# three tests that used to fail here now pass because of how numbers work in lua 5.2
# make check-unit | tee testlog.txt
# grep -q "0 failed, 0 errors" testlog.txt


%clean
rm -rf %buildroot


%files
%defattr(-,root,bin)
%doc LICENSE docs/LuaJSON.txt docs/ReleaseNotes-1.0.txt
%{luapkgdir}/*

%changelog
* Wed Dec  4 2013 - Alex Viskovatoff
- Use Lua 5.2
* Tue Oct 22 2013 - Alex Viskovatoff
- Import Fedora spec
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
