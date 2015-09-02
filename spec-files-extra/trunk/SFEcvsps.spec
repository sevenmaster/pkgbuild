#
# spec file for package SFEcvsps
#

# This really should be supplied by the system, since "git cvsimport"  uses it.

%include Solaris.inc
%define srcname cvsps

Name:		SFEcvsps
IPS_Package_Name:	developer/versioning/cvsps
Group:		Development/Source Code Management
Summary:	CVSps - Patchsets for CVS
URL:		http://www.cobite.com/cvsps/
License:	GPLv2
SUNW_Copyright:	GPLv2.copyright
Version:	2.1
Source:		http://www.cobite.com/%srcname/%srcname-%version.tar.gz
%include default-depend.inc

%description
CVSps is a program for generating 'patchset' information from a CVS
repository.  A patchset in this case is defined as a set of changes made
to a collection of files, and all committed at the same time (using a
single 'cvs commit' command).  This information is valuable to seeing the
big picture of the evolution of a cvs project.  While cvs tracks revision
information, it is often difficult to see what changes were committed
'atomically' to the repository.

%prep
%setup -q -n %srcname-%version
# not worth writing a patch
gsed -i 's/-lz/-lz -lsocket -lnsl/' Makefile

%build

export CFLAGS="%optflags"
make

%install
rm -rf %buildroot
make install prefix=%buildroot%_prefix

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%_mandir

%changelog
* Tue Sep  1 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
