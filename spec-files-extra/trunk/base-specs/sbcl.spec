#
# spec file for package: sbcl
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

Name:		sbcl
Version:	%src_version
Source0:	%sf_download/sourceforge/sbcl/%name-%version-source.tar.bz2

%prep
%setup -q

# texi2dvi does not work with sh
cd doc/manual
gsed -i 's/texi2dvi /bash texi2dvi /' Makefile

%build
#export SBCL_ARCH=%sbclarch

sh make.sh --prefix=%_prefix --xc-host="%_builddir/SFE%name-%version/%bindist/src/runtime/sbcl --core %_builddir/SFE%name-%version/%bindist/output/sbcl.core --disable-debugger --no-sysinit --no-userinit"

cd doc/manual
make

%install
INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} sh install.sh

%clean
rm -rf $RPM_BUILD_ROOT
