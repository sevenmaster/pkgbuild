#
# spec file for package SFEnmap
#
# includes module(s): nmap
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

Name:         SFEnmap
Summary:      Network Mapper
License:      GPL
Version:      7.12
Group:        System/GUI/GNOME
Source:       http://download.insecure.org/nmap/dist/nmap-%{version}.tar.bz2
#Patch1:       nmap-01-__FUNCTION__.diff
#Patch2:       nmap-02-Makefile.diff
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://insecure.org/nmap/index.html

%include default-depend.inc

BuildRequires: 	         %{pnm_buildrequires_python_default}
Requires: 	         %{pnm_requires_python_default}

%description
Nmap ("Network Mapper") is a free open source utility for network exploration or security auditing.

%prep
%setup -q -n nmap-%version
#%patch1 -p1
#%patch2 -p1


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir}

make -j$CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/nmap
%{_datadir}/nmap/*
%dir %attr (0755, root, bin) %{_datadir}/zenmap
%{_datadir}/zenmap/*
%dir %attr (0755, root, bin) %{_datadir}/ncat
%{_datadir}/ncat/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/*/*


%changelog
* Sun Apr 24 2016 - Thomas Wagner
- bump to 7.12
- fix %files
* Sat Mar 19 2016 - Thomas Wagner
- bump to 7.10
* Thu Jan 11 2007 - dermot.mccluskey@sun.com
- Initial version
