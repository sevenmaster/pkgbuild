#
# spec file for package SFElibass
#

# NOTE (herzen): Building with the assembler does not work at present,
# producing link errors, so this is presently disabled by passing --disable-asm
# to configure.  This is quite possibly related to the assembler code expecting
# HAVE_ALIGNED_STACK to be defined.  Building with the assembler also fails
# earlier on if "-f elf" is not passed to it.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname libass

Name:		SFElibass
IPS_Package_Name:	library/video/libass
Summary:	Portable renderer for the ASS/SSA (Substation Alpha) subtitle format
Group:		System/Multimedia Libraries
URL:		https://github.com/libass/libass
Version:	0.13.1
License:	ISC
SUNW_Copyright:	libass.copyright
SUNW_BaseDir:	%_basedir
Source:		http://github.com/%srcname/%srcname/releases/download/%version/%srcname-%version.tar.gz

%include default-depend.inc
#currently off BuildRequires:	SFEyasm >= 1.3.0

BuildRequires:	SFElibfribidi-devel
Requires:	SFElibfribidi
BuildRequires:	SFEharfbuzz-gpp-devel
Requires:	SFEharfbuzz-gpp
BuildRequires:	SFEfontconfig-gpp
Requires:	SFEfontconfig-gpp
BuildRequires:	SFEgraphite2-gpp
Requires:	SFEgraphite2-gpp
BuildRequires:	SFEgcc
Requires:	SFEgccruntime

# Copied from Wikipedia
%description
SubStation Alpha (or Sub Station Alpha), abbreviated SSA, is a subtitle file
format created by CS Low (also known as Kotus) that allows for more advanced
subtitles than the conventional SRT and similar formats. This format can be
rendered with VSFilter in conjunction with a DirectShow-aware video player
(on Microsoft Windows), or MPlayer with the SSA/ASS library.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="%optflags"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:$PKG_CONFIG_PATH
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
#export ASFLAGS="-f elf -DHAVE_ALIGNED_STACK=1"
export ASFLAGS="-f elf"
# This is so our fontconfig gets found
export PATH=/usr/g++/bin:$PATH

sed -i -e 's,#! */bin/sh,#! /usr/bin/bash,' configure 

#./configure --prefix=%_prefix
# Disable use of assembler to avoid text relocation link errors. Needs ASFLAGS="-f elf -DHAVE_ALIGNED_STACK=1" as well
./configure --prefix=%_prefix --disable-asm
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%_libdir/%srcname.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%srcname.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/ass


%changelog
* Sun Oct 30 2016 - Thomas Wagner
- correct Requires to read SFEharfbuzz-gpp
* Fri Feb 26 2016 - Thomas Wagner
#- enable again assembler, use yasm 1.3.0 instead 1.2.0 (updated SFEyasm.spec to 1.3.0 - undefined symbol HAVE_ALIGNED_STACK)
- merge different spec files sitting around
- to keep information in one non-volatile place: add forgotten %changelog entries below:
- use *.gz source
- add dependencies
* Sun Jan 31 2016 - Alex Viskovatoff
- update to 0.13.1; disable use of assembler
* Mon Sep  9 2013 - Thomas Wagner
- use bash in configure (endless loop sleep 1)
* Sat Feb 09 2013 - Milan Jurik
- bump do 0.10.1
* Thu Jun 21 2012 - Logan Bruns <logan@gedanken.org>
- added missing requires for SFElibfribidi
* Sun Dec 11 2011 - Milan Jurik
- bump to 0.10.0
* Tue Aug 30 2011 - Alex Viskovatoff
- bump to 0.9.13; use gz tarball so spec builds with unpatched pkgtool
* Fri Jul 29 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Sat Jul 16 2011 - Alex Viskovatoff
- Initial spec
