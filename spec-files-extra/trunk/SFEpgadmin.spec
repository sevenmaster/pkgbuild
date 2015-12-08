#
# spec file for package SFEpgadmin
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname pgadmin3

Name:		SFEpgadmin
IPS_Package_Name:	database/postgres/pgadmin3
Summary:	pgAdmin administration and development GUI for PostgreSQL
Group:		System/Databases
URL:		http://www.pgadmin.org
Version:	1.20.0
Source:		http://ftp.postgresql.org/pub/%srcname/release/v%version/src/%srcname-%version.tar.gz
License:	PostgreSQL
SUNW_Copyright: %srcname.copyright

%include	default-depend.inc
BuildRequires:	SFEpostgres-94-devel
BuildRequires:	SFEwxwidgets-gpp-devel

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl -R/usr/postgres/9.4/lib"
export PATH=/usr/g++/bin:$PATH

./configure --with-wx=/usr/g++ --prefix=%_prefix
make -j$CPUS

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (0755, root, sys) %_datadir
%defattr (-, root, other)
%_datadir/%srcname

%changelog
* Tue Dec  8 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
