#
# spec file for package SFEmoxfm
#

%include Solaris.inc
%define srcname moxfm

Name:		SFEmoxfm
IPS_Package_Name:	motif/file-manager/moxfm 
Summary:	An X Window file manager (Motif port of Xfm)
Group:		Desktop (GNOME)/File Managers
Version:	1.0.1
URL:		http://www.musikwissenschaft.uni-mainz.de/~ag/xfm/
Source:		http://www.musikwissenschaft.uni-mainz.de/~ag/xfm/%srcname-%version.tar.gz

BuildRequires:	library/motif

%prep
%setup -q -n %srcname-%version

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./MakeMakefiles
make

%install
rm -rf %buildroot

# Set installation directory
# We only do it now because a path gets hard-coded during the build
gsed -i "s|\$(LIBDIR)/moxfm|%buildroot/\$(LIBDIR)/moxfm|" Imake.options
./MakeMakefiles

make install DESTDIR=%buildroot

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/%srcname
%_libdir/X11
