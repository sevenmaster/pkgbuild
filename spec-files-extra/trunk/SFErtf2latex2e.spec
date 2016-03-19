#
# spec file for package SFErtf2latex2e
#

%include Solaris.inc
%define srcname rtf2latex2e
%define dash_version 2-2-2

Name:		SFErtf2latex2e
IPS_Package_Name:	text/%srcname
Summary:	Rich Text Format to LaTeX converter
Group:		Applications/Office
Version:	2.2.2
URL:		http://sourceforge.net/projects/rtf2latex2e
Source:		%sf_download/%srcname/files/%srcname-%dash_version.tar.gz

%prep
%setup -q -n %srcname-%dash_version
gsed -i -e 's/gcc/cc/' -e 's|/usr/local$|/usr|' Makefile

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
gmake

%install
rm -rf %buildroot
export DESTDIR=%buildroot
gmake install

%check
gmake test

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir
%dir %attr (0755, root, sys) %_datadir
%_mandir
%defattr (-, root, other)
%_datadir/%srcname

%changelog
* Fri Mar 18 2016 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
