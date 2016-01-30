#
# spec file for package SFEtexlive
#

# This spec produces two packages, text/texlive and text/texlive/texmf.
# We do not have either require the other.  texmf is huge, and is not needed by
# the binaries in texlive to build or run – only to be useful.  texlive in
# contrast is a build dependency of other SFE packages.  Distributions usually
# split texmf up into smaller packages; we just omit a few files at this point.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include osdistro.inc

%define texlive_ver	20150523
%define texlive_src_ver 20150521
%define texlive_year	2015

Name:		SFEtexlive
IPS_Package_Name:	text/texlive
Version:	%texlive_year
Summary:	Binaries for the TeX formatting system
URL:		http://tug.org/texlive

Group:		System/Text Tools
License:	GPLv2 and More
URL:		http://tug.org/texlive/

Source:         ftp://tug.org/historic/systems/texlive/%texlive_year/texlive-%texlive_src_ver-source.tar.xz
Source1:	ftp://tug.org/texlive/tlnet/install-tl-unx.tar.gz
Source2:	ftp://tug.org/historic/systems/texlive/%texlive_year/texlive-%texlive_ver-texmf.tar.xz
Source3:	texmf-exclude.list
Source4:	texmf.cnf
SUNW_BaseDir:	%_basedir

BuildRequires:	SUNWflexlex
BuildRequires:	library/ncurses
BuildRequires:	library/zlib
BuildRequires:	image/library/libpng
BuildRequires:  library/gd
Buildrequires:  system/library/freetype-2
%if %oihipster
BuildRequires:  developer/icu
%else
BuildRequires:	library/motif
BuildRequires:	SFEcairo-gpp
BuildRequires:	SFEicu-gpp
%endif


%description
TeXLive is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
printable file as output. Usually, TeX is used in conjunction with
a higher level formatting package like LaTeX or PlainTeX, since TeX by
itself is not very user-friendly.

Install texlive if you want to use the TeX text formatting system. Consider
to install texlive-latex (a higher level formatting package which provides
an easier-to-use interface for TeX).

%package -n %name-texmf
IPS_Package_Name:	 text/texlive/texmf
Summary:	Data files for the TeX formatting system
Requires:	%name

%prep
%setup -q -n texlive-%texlive_src_ver-source
mkdir build


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
%if %oihipster
export LDFLAGS="%_ldflags"
%else
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export CPPFLAGS="-I/usr/g++/unicode"
export PATH=/usr/g++/bin:$PATH
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
%endif

cd build

# luajit build produces "relocations remain against allocatable but non-writable
# sections" error
# xdvi does not build on OI
# S11.3 and OpenIndiana deliver psutils

../configure \
	--disable-native-texlive-build \
	--build=i386-solaris \
	--host=i386-solaris \
	--prefix=%_prefix \
	--enable-shared \
	--disable-static \
%if %oihipster
	--disable-xdvik \
%else
	--with-xdvi-x-toolkit=motif \
%endif
	--with-x \
	--with-system-ncurses \
	--with-system-zlib \
	--with-system-libpng \
	--with-system-gd \
	--with-gd-includes=/usr/include/gd2 \
	--with-system-freetype2 \
	--with-freetype2-include=/usr/include/freetype2 \
	--with-system-icu \
	--with-system-cairo \
	--with-system-pixman \
	--with-system-gmp \
	--with-gmp-includes=/usr/include/gmp \
	--disable-multiplatform \
	--disable-luajittex \
	--disable-psutils

make -j$CPUS


%install
rm -rf %buildroot

cd build
make install-strip DESTDIR=%buildroot
cd %buildroot%_prefix
rm lib/*.la
rm share/info/dir

# To avoid complexity and a maintenance concern, let the texlive-texmf package
# deliver the files in share/texmf-dist
cd share
rm -r texmf-dist/*

# Deliver tlpkg/TeXLive, which contains perl scripts
tar xzf %SOURCE1 --wildcards --strip-components=1 '*/TeXLive/*'

# Prepare texmf-dist

tar xJf %SOURCE2 --strip-components=1 --exclude-from=%SOURCE3

# Let Kpathsea know where our texlive trees are located, following the conventions
# used for distributions, by supplying our own texmf.cnf
cd texmf-dist/web2c
cp %SOURCE4 .

# Prevent updmap-sys from complaining when it can't find some fonts
# that weren't installed due to gtar --exclude above
ggrep -v -e 'greek' -e 'hebrew' -e 'icelandic' -e '7x-urwvn' -e 'mongolian' \
      -e 'upl' -e 'dutch' updmap.cfg > updmap.new
mv updmap.new updmap.cfg


%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir
%_libdir/lib*.so*
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*.pc
%_libdir/kpathsea
%_includedir
%dir %attr (-, root, sys) %_datadir
%_infodir
%_mandir
%_datadir/tlpkg
%dir %attr (-, root, other) %_datadir/texmf-dist

%files -n %name-texmf
%defattr (-,root,other)
%dir %attr (-, root, sys) %_datadir
%_datadir/texmf-dist


%changelog
* Wed Dec 16 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 20150521; employ directory scheme used by distributions, taking
  texmf.cnf (which defines paths) unaltered from Arch Linux
- build xdvik against Motif
- merge SFEtexlive-texmf.spec into this spec
* Thu Mar 15 2012 - Logan Bruns <logan@gedanken.org>
- update to 20110705 
- TODO: post steps are not being run on OI/S11. so you have to update
  texmf/web2c/texmf.cnf and run them manually at the moment. that
  should be fixed.
* April 2010 - Gilles Dauphin
- hardcode the path of freetype2
# because freetype2 is in /usr/include , hard code the path
* 17 Aug 2009 - Gilles Dauphin
- check with texmf files.
* Aug 2009 - Gilles Dauphin
- Initial setup, I look at Fedora and Pkgsrc
