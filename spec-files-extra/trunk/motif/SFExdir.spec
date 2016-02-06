#
# spec file for package SFExdir
#

%include Solaris.inc
%define srcname llnlxdir

Name:		SFExdir
IPS_Package_Name:	motif/ftp/xdir
Summary:	An Advanced Graphical FTP Client
Group:		Applications/System Utilities
Version:	2.1.2
URL:		https://computing.llnl.gov/resources/xdir/xdir.html
Source:		http://computing.llnl.gov/resources/xdir/%srcname%2_1_2.tar.Z

BuildRequires:	library/motif

%prep
%setup -q -n %{srcname}2_1_2

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
cd sources
xmkmf
make -j$CPUS

%install
rm -rf %buildroot
cd sources
make install DESTDIR=%buildroot

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%_bindir/xdir
%_libdir/X11/app-defaults/XDir
