#
# spec file for package SFEasedit
#

%include Solaris.inc
%define srcname asedit

Name:		SFEasedit
IPS_Package_Name:	motif/editor/asedit 
Summary:	An X Window text editor
Group:		Development/Editors
Version:	1.3.2
URL:		ftp://ftp.x.org/contrib/editors/asedit-1.3.2.README
Source:		ftp://ftp.x.org/contrib/editors/%srcname-%version.tar.Z

BuildRequires:	library/motif

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
xmkmf
gsed -i 's/ -lPW//' Makefile
make -j$CPUS

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/asedit
%_libdir/X11
