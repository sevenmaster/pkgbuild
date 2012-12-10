#
# spec file for package SFEsocat
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:		SFEsocat
IPS_Package_Name:	socat
Summary:	A multipurpose relay (SOcket CAT)
Group:		Applications/Internet
URL:		http://www.dest-unreach.org/socat
Version:	1.7.2.1
Source:		http://www.dest-unreach.org/socat/download/socat-%{version}.tar.bz2
##TODO## replace with other patch filname (rotate)
##TODO## replace with other patch filname (rotate)
Patch1:		socat-01-escape-nested-double-quotes.diff
Patch2:		socat-02-xioread.c-temp-fix-missing-ll.diff
Patch3:		socat-03-xio-socket.c-ctime_r_sizeof.diff
License:	GPL2
SUNW_Copyright:		 %{license}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SFEgcc
Requires: SFEgccruntime

%prep
%setup -q -n socat-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

export CC=gcc
export CXX=g++
#export CFLAGS="%optflags -I%{gnu_inc} %{gnu_lib_path}"
export CFLAGS="%optflags -D_XPG4_2 -D__EXTENSIONS__ -DPACKET_OUTGOING=0 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
#export CXXFLAGS="%cxx_optflags -I%{gnu_inc} %{gnu_lib_path}"
export CXXFLAGS="%cxx_optflags"
#export LDFLAGS="%_ldflags %gnu_lib_path"
export LDFLAGS="%_ldflags"

sed -i -e 's,#! */bin/sh,#! /usr/bin/bash,' configure 

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}


gmake

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc BUGREPORTS DEVELOPMENT COPYING.OpenSSL SECURITY FILES PORTING README.FIPS FAQ EXAMPLES README COPYING CHANGES VERSION
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Mon Dec 10 2011 - Thomas Wagner
- initial spec
