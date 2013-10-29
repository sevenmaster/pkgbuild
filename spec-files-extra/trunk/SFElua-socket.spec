%include Solaris.inc
%define luaver 5.1
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%define baseversion 3.0-rc1
%define upstreamname luasocket
%define _pkg_docdir %_docdir/%upstreamname

Name:           SFElua-socket
IPS_package_name: lua/lua-socket
Version:        3.0
Release:        0.4rc1
Summary:        Network support for the Lua language
Group:          Development/Libraries
License:        MIT
URL:            http://www.tecgraf.puc-rio.br/~diego/professional/luasocket/
Source0:        http://github.com/diegonehab/%{upstreamname}/archive/v%{baseversion}.tar.gz
#Patch0:		    luasocket-optflags.patch
# All changes in the upstream repo from %{baseversion} tag to the
# current master. Seems to be harmless.
#Patch1:         luasocket-no-global-vars.patch

BuildRequires:  SFElua-51
#BuildRequires:  /usr/bin/iconv
#BuildRequires: system/library/iconv/unicode
Requires:       lua-51

%package devel
Summary:    Development files for %{name}
Group:      Development/Languages
Requires: %name


%description
LuaSocket is a Lua extension library that is composed by two parts: a C core
that provides support for the TCP and UDP transport layers, and a set of Lua
modules that add support for functionality commonly needed by applications
that deal with the Internet.

Among the support modules, the most commonly used implement the SMTP, HTTP
and FTP. In addition there are modules for MIME, URL handling and LTN12.

%description devel
Header files and libraries for building an extension library for the
Lua using %{name}


%prep
%setup -q -n %{upstreamname}-%{baseversion}
#%patch0 -p1 -b .optflags
#%patch1 -p1 -b .noglobal

%build
#make %{?_smp_mflags} OPTFLAGS="%{optflags} -fPIC" linux
make LUAINC_linux=/usr/include/lua-5.1 OPTFLAGS="%optflags" linux
/usr/bin/iconv -f ISO8859-1 -t UTF8 LICENSE >LICENSE.UTF8
mv -f LICENSE.UTF8 LICENSE


%install
rm -rf %buildroot
make install-unix OPTFLAGS="%{optflags}" INSTALL_TOP=$RPM_BUILD_ROOT \
    INSTALL_TOP_CDIR=$RPM_BUILD_ROOT%{lualibdir} \
    INSTALL_TOP_LDIR=$RPM_BUILD_ROOT%{luapkgdir}

# install development files
install -d $RPM_BUILD_ROOT%{_includedir}/%{upstreamname}
install -p src/*.h $RPM_BUILD_ROOT%{_includedir}/%{upstreamname}


%clean
rm -rf %buildroot


%files
%defattr(-,root,bin)
%doc doc/*
%doc README LICENSE
%{lualibdir}/*
%{luapkgdir}/*

%files devel
%defattr(-,root,bin)
%{_includedir}/%{upstreamname}


%changelog
* Sun Oct 20 2013 Alex Viskovatoff
- Import Fedora spec
* Mon Sep 09 2013 Matěj Cepl <mcepl@redhat.com> - 3.0-0.4rc1
- Add -devel package.
