#
# spec file for package lame
#
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=290&atid=100290&aid=
#

Name:                    SFElame
Summary:                 lame  - Ain't an MP3 Encoder
Version:                 3.99.5
Source:                  %{sf_download}/lame/lame-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%prep
%setup -q -n lame-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc

export CFLAGS="%optflags -I%gnu_inc"
export MSGFMT="/usr/bin/msgfmt"
export LD_OPTIONS="%gnu_lib_path"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --with-fileio=sndfile	\
            --enable-shared		\
	    --disable-static

make -j$CPUS

#root@s11175:/localhomes/sfe# elfdump -d /usr/bin/i86/lame /usr/bin/amd64/lame | grep RPATH
#     [11]  RPATH           0x1265     /usr/gnu/lib:/localhomes/sfe/packages/BUILD/SFElame-3.99.5/i386/lame-3.99.5/libmp3lame/.libs:/usr/gcc/4.6/lib:/usr/gcc/lib
#     [11]  RPATH           0x11b0    /usr/gnu/lib/amd64:/localhomes/sfe/packages/BUILD/SFElame-3.99.5/amd64/lame-3.99.5/libmp3lame/.libs:/usr/lib/amd64:/usr/gcc/4.6/lib/amd64:/usr/gcc/lib/amd64

#RUNPATHURXVT=$( /usr/bin/elfedit -re 'dyn:' $RPM_BUILD_ROOT/%{_bindir}/urxvt | grep RUNPATH | sed -e s'?.* /?/?' -e 's,/usr/lib:,,' -e 's,/usr/lib/[A-z0-9]*:,,' )
#/usr/bin/elfedit -e 'dyn:runpath '$RUNPATHURXVT'' $RPM_BUILD_ROOT/%{_bindir}/urxvt
#/usr/bin/elfedit -e 'dyn:runpath '$RUNPATHURXVT'' $RPM_BUILD_ROOT/%{_bindir}/urxvtd

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Mar 26 2016 - Thomas Wagner
- make note abote: remove needless RPATH from binaries
* Tue Okt  1 2013 - Thomas Wagner
- use CC=gcc
* Fri Jun 22 2012 - Milan Jurik
- bump to 3.99.5
* Mon Oct 10 2011 - Milan Jurik
- remove GCC dependency
* Wed Mar 24 2010 - Milan Jurik
- update for 3.98.4
* Tue Oct 06 2009 - Milan Jurik
- LDFLAGS for gcc are not valid, removed
- xmmintrin.h hack removed, configure script detects it correctly now
* Tue Sep 15 2009 - Thomas Wagner
- add switch %use_gcc4 and CC/CXX compiler setting to be default gcc3 or explicitly gcc4
- comment out LDFLAGS since I see compile/link error arch=sse2 unkown switch
* Sat Mar 14 2009 - Milan Jurik
- upgrade to 3.98.2
* Thu Oct 23 2008 - dick@nagual.nl
- Add --with-fileio=sndfile for better file reckognize (i.e. au files)
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Add aclocal to fix build error
- Remove commentted patch1 and patch2
* Fri Aug 15 2008 - andras.barna@gmail.com
- new version
- add a hack to disable MMX things which causes compilation failure, FIXME
- disable patch1, patch2 not needed
* Sun Apr 22 2007 - dougs@truemail.co.th
- Forced automake to automake-1.9
* Tue Mar 20 2007 - dougs@truemail.co.th
- Changed to be a base spec
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElame
- change to root:bin to follow other JDS pkgs.
- go back to 02l version of toolame because the beta tarball download site
  is gone.
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
