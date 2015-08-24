#
# spec file for package SFErcs
#
# includes module: rcs
#

%include Solaris.inc
%define srcname rcs

Name:	        SFErcs
IPS_Package_Name:	developer/versioning/rcs
Summary:	GNU Revision Control System
URL:		http://www.gnu.org/software/rcs/
Vendor:		GNU Project
Version:        5.9.4
License:	GPLv3
Group:		Development/Source Code Management
SUNW_Copyright:	GPLv3.copyright
Source:		ftp://ftp.gnu.org/gnu/rcs/%srcname-%version.tar.xz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc


%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix

make -j$CPUS

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

rm %buildroot%_infodir/dir

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%_bindir/*
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, bin) %_mandir
%dir %attr (0755, root, bin) %_mandir/man1
%_mandir/man1/*.1
%dir %attr (0755, root, bin) %_mandir/man5
%_mandir/man5/rcsfile.5
%dir %attr (0755, root, bin) %_datadir/info
%_datadir/info/%srcname.info


%changelog
* Sat Aug 22 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 5.9.4; install rcs.info
* Mon Dec 05 2011 - Milan Jurik
- bump to 5.8
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
