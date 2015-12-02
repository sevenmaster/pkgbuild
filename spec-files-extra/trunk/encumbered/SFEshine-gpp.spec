#
# spec file for package SFEshine-gpp
#
# includes module(s): shine
#
%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc

Name:		SFEshine-gpp
IPS_Package_Name:	library/audio/g++/shine 
Summary:	shine - fast fixed-point mp3 encoding (/usr/g++)
Group:		System/Multimedia Libraries
URL:		https://github.com/toots/shine
License:	LGPLv2
SUNW_copyright:	%{license}.copyright
Version:	3.1.0
Source:         http://github.com/toots/shine/releases/download/%{version}/shine-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%description
savonet/shine is a blazing fast mp3 encoding library implemented in fixed-point arithmetic. The library can thus be used to performe super fast mp3 encoding on architectures without a FPU, such as armel, etc.. It is also, however, also super fast on architectures with a FPU!

%prep
%setup -q -n shine-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')  

export CC=gcc
export CXX=g++

export CFLAGS="%{optflags}"
export CXXLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/shineenc
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Weg Dec  2 2015 - Thomas Wagner
- initial spec version 3.1.0
