#
# spec file for package SFEnedit
#

%include Solaris.inc
%define srcname nedit

Name:		SFEnedit
IPS_Package_Name:	motif/editor/nedit 
Summary:	A fast, compact Motif/X11 plain text editor
Group:		Development/Editors
Version:	5.6
URL:		http://sourceforge.net/projects/nedit/
Source:		%sf_download/nedit/%srcname-%{version}a-src.tar.gz

BuildRequires:	library/motif

%prep
%setup -q -n %srcname-%version

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make solarisx86

%install
rm -rf %buildroot
mkdir -p %buildroot%_bindir
cp source/nc source/nedit %buildroot%_bindir
mkdir -p %buildroot%_mandir/man1
cd doc
cp nc.man %buildroot/%_mandir/man1/nc.1
cp nedit.man %buildroot/%_mandir/man1/nedit.1

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir
%dir %attr (0755, root, sys) %_datadir
%_mandir
