%include Solaris.inc
%define luaver 5.1
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%define _pkg_docdir %_docdir/lua-lpeg

Name:           SFElua-lpeg
IPS_package_name: lua-51/lua-lpeg
Version:        0.12
Summary:        Parsing Expression Grammars for Lua
Group:          Development/Libraries
License:        MIT
URL:            http://www.inf.puc-rio.br/~roberto/lpeg/
Source0:        http://www.inf.puc-rio.br/~roberto/lpeg/lpeg-%{version}.tar.gz
BuildRoot:      %_tmppath/%name-%version-root

BuildRequires:  SFElua-51
Requires:       lua-51

%description
LPeg is a new pattern-matching library for Lua, based on Parsing Expression
Grammars (PEGs).

%prep
%setup -q -n lpeg-%{version}
sed -i -e "s|/usr/bin/env lua5.1|%{_bindir}/lua|" test.lua
# strict module not part of our Lua 5.1.4
sed -i -e 's|require"strict"|-- require"strict"|' test.lua
chmod -x test.lua

%build
#make %{?_smp_mflags} COPT="%{optflags}"
make LUADIR=/usr/include/lua-5.1 COPT="%gcc_optflags"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{lualibdir}
mkdir -p %{buildroot}%{luapkgdir}
install -p lpeg.so %{buildroot}%{lualibdir}/lpeg.so.%{version}
ln -s lpeg.so.%{version} %{buildroot}%{lualibdir}/lpeg.so
install -p -m 0644 re.lua %{buildroot}%{luapkgdir}


#%check
#lua test.lua


%clean
rm -rf %buildroot


%files
%defattr(-,root,bin)
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%{lualibdir}/*
%{luapkgdir}/*


%changelog
* Tue Oct 22 2013 - Alex Viskovatoff
- Import Fedora spec
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
