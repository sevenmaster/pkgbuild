#
# spec file for package SFExftp
#

%include Solaris.inc
%define srcname llnlxftp

Name:		SFExftp
IPS_Package_Name:	motif/ftp/xftp 
Summary:	An X Window FTP Client
Group:		Applications/System Utilities
Version:	2.1
URL:		https://computing.llnl.gov/resources/xdir/xftp.html
Source:		http://computing.llnl.gov/resources/xdir/%srcname%version.tar.Z

BuildRequires:	library/motif

%prep
%setup -q -n %srcname%version

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
%_bindir/xftp
%_libdir/X11/app-defaults/XFtp
