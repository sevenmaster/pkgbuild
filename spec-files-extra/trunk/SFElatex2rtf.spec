#
# spec file for package SFElatex2rtf
#

%include Solaris.inc
%define srcname latex2rtf
%define _pkg_docdir %_docdir/%srcname

Name:		SFElatex2rtf
IPS_Package_Name:	text/%srcname
Summary:	LaTeX to RTF converter
Group:		Applications/Office
Version:	2.3.10
URL:		http://latex2rtf.sourceforge.net/
Source:		%sf_download/%srcname/%srcname-%version.tar.gz

%include default-depend.inc
BuildRequires:	text/texinfo
BuildRequires:	SFEtexlive

%prep
%setup -q -n %srcname-%version
gsed -i -e 's|/usr/local$|/usr|' \
     -e 's|^SUPPORTDIR=/share/latex2rtf|SUPPORTDIR=/share/doc/latex2rtf|' \
     -e 's/^all : checkdir /all : /' Makefile
# Solaris' texi2dvi is broken: doesn't work with sh
gsed -i -e 's/texi2dvi /bash texi2dvi /' doc/Makefile

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
gmake

%install
rm -rf %buildroot
mkdir -p %buildroot%_pkg_docdir
# This is OK: the "final" destination path was used for the compilation phase
# We use a different value for DESTDIR for this phase
export DESTDIR=%buildroot%_prefix
gmake install
gmake install-info
rm %buildroot%_pkg_docdir/%srcname.txt
rm %buildroot%_infodir/dir

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir
%dir %attr (0755, root, sys) %_datadir
%_mandir
%_infodir
%defattr (-, root, other)
%_docdir
%_datadir/%srcname

%changelog
* Tue Feb 23 2016 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
