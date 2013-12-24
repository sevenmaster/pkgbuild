#
# spec file for package faac
#
# includes module(s): faac
#

Summary:	Reference encoder and encoding library for MPEG2/4 AAC
Name:		SFEfaac
Version:	1.28
License:	LGPLv2+
Group:		Applications/Multimedia
URL:		http://www.audiocoding.com/
Source:		%{sf_download}/faac/faac-src/faac-%{version}.tar.gz
Patch1:		faac-01-mp4v2.diff
Patch2:		faac-02-wall.diff
Patch3:		faac-03-stdc.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n faac-%{version}
#%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags} -lm"

#perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure `find . -type f -exec /usr/gnu/bin/grep -q "^#\!.*/bin/sh" {} \; -print`

%if %{cc_is_gcc}
#configure: postdeps_CXX='-lCstd -lCrun'
#aclocal.m4: _LT_AC_TAGVAR(postdeps,$1)='-lCstd -lCrun'
gsed -i.bak -e '/_LT_AC_TAGVAR(postdeps,$1)=.-lCstd -lCrun./ s?.-lCstd -lCrun.??' aclocal.m4
#frontend/Makefile:LDADD = $(top_builddir)/libfaac/libfaac.la $(top_srcdir)/common/mp4v2/libmp4v2.a -lm -lCrun
#frontend/Makefile.am  <- change this file, will make up a new Makefile
gsed -i.bak -e '/^LDADD.*Crun/ s?-lCrun?-lstdc++?' frontend/Makefile.am
%endif 

./configure --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-static \
    --enable-drm \
    --with-mp4v2

make -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Dec 23 2013 - Thomas Wagner
- export AR=/usr/bin/ar (or get C++ Symbol errors on S12) (SFEfaac.spec)
- export LD=`which ld-wrapper` (SFEfaac.spec)
- remove -Wall and -lstdc++ if built with Studio compiler (SFEfaac.spec)
* Sun Aug 11 2013 - Thomas Wagner
- fix linking to C++ libs %if %{cc_is_gcc}  ( s/-lCrun/-lstdc++/ )
- %if %{cc_is_gcc} change Name, IPS_Package_Name to SFEfaac-gpp, audio/g++/faac
- %if %{cc_is_gcc} add (Build)Requires: SFEgcc(runtime)
* Sat Aug 10 2013 - Thomas Wagner
- set CC in calling spec file
* Fri Jun 28 2013 - Thomas Wagner
- use gcc because previous libs in the stack already use g++
* Wed Jan 30 2013 - Thomas Wagner
- fix build by removing sh bootstrap, change shell in scripts to bash
* Thu Aug 16 2012 - Milan Jurik
- build with internal mp4v2
* Mon Oct 17 2011 - Milan Jurik
- revert previous change to unbreak build
* Sat Aug 13 2011 - Thomas Wagner
- fix build by:
- use /usr/bin/libtoolize and not new SFE version from /usr/gnu/bin/
- use CC/CXX /usr/gnu/bin/gcc g++
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jun 18 2010 - Milan Jurik
- Initial version
