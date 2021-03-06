#
# spec file for package SFEmpg123.spec
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

Name:           SFEmpg123
IPS_package_name: audio/mpg123
Summary:        Fast console MPEG Audio Player and decoder library
Version:        1.23.8
#Version:        1.13.4
URL:            http://www.mpg123.org/
Source:         %{sf_download}/mpg123/mpg123/%{version}/mpg123-%{version}.tar.bz2
License:        LGPL,GPL
Group:          Applications/Multimedia
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:       %{pnm_buildrequires_SUNWltdl}
Requires:       %{pnm_requires_SUNWltdl}
BuildRequires:  %{pnm_buildrequires_SUNWlibsdl_devel}
Requires:       %{pnm_requires_SUNWlibsdl}
Requires:       SUNWlibms
BuildRequires:	SUNWaudh
BuildRequires:	%{pnm_buildrequires_SUNWgnome_common_devel}
Requires:       %{name}-devel

%description
mpg123 is a real time MPEG 1.0/2.0/2.5 audio player/decoder for layers
1, 2, and 3 (MPEG 1.0 layer 3 aka MP3 most commonly tested). mpg123
includes a terminal-based player, the ability to redirect the raw sound
data to stdout, gapless playback of MP3 files, a decoder library for use
with other applications, and much more.

%package devel
Summary:        mpg123 - developer files
Group:          Development/Libraries
SUNW_BaseDir:   %{_basedir}
Requires:       %name
%include default-depend.inc

%prep
%setup -q -n mpg123-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CPP="gcc -E"
export CXX=g++
#export CFLAGS="%{optflags}"
#export CFLAGS="-i -xO4 -xc99 -D_XPG6 -D__EXTENSIONS__ -xspace -xstrconst -xarch=sse -mr -xregs=no%frameptr"
export CFLAGS="%{optflags} -xc99 -D_XPG6 -D__EXTENSIONS__ -xspace -xstrconst -mr -xregs=no%frameptr"
export LDFLAGS="%{_ldflags} -lsocket"

%if %cc_is_gcc
export CFLAGS="%{gcc_optflags} -std=c99 -D_XPG6 -D__EXTENSIONS__"

#remove libtools inserted: "-z text" or get "ld: fatal: relocations remain against allocatable but non-writable sections"
cat - > ld-remove-z_text << EOF
#!/usr/bin/bash
/usr/bin/ld \`echo \$* | sed -e 's/-z text//g'\`
EOF
chmod a+rx ld-remove-z_text
export LD_ALTEXEC=`pwd`/ld-remove-z_text
%endif

#fix http://solarisx86.yahoogroups.narkive.com/bgJNXAmR/compiling-mpg123-and-symbol-relocations
#        "src/libmpg123/tabinit_mmx.S", line 48 : Illegal mnemonic
#        "src/libmpg123/tabinit_mmx.S", line 48 : Syntax error
sed -i.bak -e 's?\t\.short?\t.value?'  src/libmpg123/tabinit_mmx.S

# Build fails with --with-optimization set to > 1
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static            \
            --enable-int-quality=yes    \
            --enable-fifo=yes		\
            --enable-network=yes	\
            --with-default-audio=oss	\
            --with-module-suffix=.so	\
            --enable-ipv6=yes 		\
            --with-optimization=3       \
            --with-cpu=sse              \

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
gmake DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/mpg123/output_*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/lib*123.so*
%{_libdir}/mpg123/output_*.so


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/lib*123.pc
%{_includedir}

%changelog
* Mon Feb 27 2017 - Thomas Wagner
- bump to 1.23.8 - try again with mpd
* Mon Jul  4 2016 - Thomas Wagner
- back to version 1.13.4, "mpd" can't use the new 1.23.4 version
* Fri Jun 10 2016 - Thomas Wagner
- fix assembler syntax error in tabinit_mmx.S line 48 : Illegal mnemonic / Syntax error
- set -xc99 -D_XPG6 -D__EXTENSIONS__ for studio compiler
* Tue May 24 2016 - Thomas Wagner
- bump to 1.23.4, add new libs and libout123.pc
* Mon May 23 2016 - Thomas Wagner
- fix compile and linking on (OIH): 
  - if cc_is_gcc set CFLAGS for gcc
  - add wrapper to remove libtool's addition -z text of (or get ld: fatal: relocations remain against allocatable but non-writable sections)
- change (Build)Requires to pnm_buildrequires_SUNWgnome_common_devel
* Sun Mar 23 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- syntax error in %include Solaris.inc (was %Include)
* Sun Jun 24 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibsdl_devel}
* Sat Jun 23 2012 - Thomas Wagner
- change (Build)Requires: to %{pnm_buildrequires_SUNWltdl}, %include packagenamemacros.inc
* Sun Apr 29 2012 - Pavel Heimlich
- fix dependency (SUNWltdl is no more in S11)
* Mon Oct 24 2011 - Alex Viskovatoff
- bump to 1.13.4; make executable functional; xarch=sse; add IPS_package_name
* Thu Sep 01 2011 - Milan Jurik
- bump to 1.13.3
* Mon Aug 25 2009 - matt@greenviolet.net
- Initial version
