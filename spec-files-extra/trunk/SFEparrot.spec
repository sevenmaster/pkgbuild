#
# spec file for package SFEparrot
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname parrot

Name:		SFE%srcname
IPS_Package_Name:	runtime/parrot
Summary:	Register-based virtual machine designed to run dynamic languages efficiently
URL:		http://www.parrot.org/
Meta(info.upstream):	Parrot Developers <parrot-dev@lists.parrot.org>
Version:	6.0.0
License:	Artistic 2.0
Group:		Development/Other Languages
SUNW_Copyright:	parrot.copyright
Source:		ftp://ftp.parrot.org/pub/%srcname/releases/supported/%version/%srcname-%version.tar.bz2
SUNW_BaseDir:	%_basedir
%include default-depend.inc

# Don't require perl-5 explicitly, since all Solaris systems have it,
# and we don't want to require a specific minor version.
#BuildRequires:	SUNWperl584core
#Requires:	SUNWperl584core

%package devel
Summary:	%summary - development files
SUNW_BaseDir:	%_basedir
%include default-depend.inc
Requires: %name

%description
Parrot is a virtual machine designed to efficiently compile and execute bytecode
for dynamic languages. Parrot currently hosts a variety of language
implementations in various stages of completion, including Tcl, Javascript,
Ruby, Lua, Scheme, PHP, Python, Perl 6, APL, and a .NET bytecode translator.


%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

perl Configure.pl --prefix=%_prefix --cc=gcc --cxx=g++ --ccflags="%picflags" --ld=/usr/bin/ld --optimize
make -j$CPUS


%install
rm -rf %buildroot

make install DESTDIR=%buildroot
cd %buildroot/%_prefix
rm lib/*.a
mv src man share

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir
%_libdir/libparrot.so
%_libdir/%srcname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname
%_mandir

%files devel
%defattr (-, root, bin)
%_includedir/%srcname/%version
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, sys) %_datadir/src
%_datadir/src/%srcname/%version
%_datadir/%srcname/%version


%changelog
* Sun Feb  2 2013 - Alex Viskovatoff
- update to 6.0.0; use gcc (building with Sun Studio does not work anymore)
* Tue Aug 30 2011 - Alex Viskovatoff
- Bump to 3.6.0
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sat Apr 23 2011 - Alex Viskovatoff
- Bump to 3.3.0
* Fri Mar 11 2011 - Alex Viskovatoff
- Initial spec
