#
# spec file for package libquicktime
#
# includes module(s): libquicktime
#

%define src_ver 1.2.4
%define src_name libquicktime
%define src_url http://downloads.sourceforge.net/%{src_name}

Name:		libquicktime
Summary:	Quicktime library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libquicktime-01-gccflags.diff
Patch2:		libquicktime-1.2.4-ffmpeg-2.0.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags"
export AVCODEC_CFLAGS="%optflags"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export CFLAGS="$CFLAGS -m64"
        export CXXFLAGS="$CXXFLAGS -m64"
        export LDFLAGS="-Wl,-64 -L%{_libdir} -L/usr/X11/lib/%{_arch64} -R%{_libdir}:/usr/X11/lib/%{_arch64} $LDFLAGS"
else
        export LDFLAGS="-L%{_libdir} -L/usr/X11/lib -R%{_libdir}:/usr/X11/lib $LDFLAGS"
fi

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --without-visibility	\
            --enable-shared		\
	    --disable-static

cp /usr/bin/libtool libtool

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/libquicktime/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Nov 19 2017 - Thomas Wagner
- recover missing patch libquicktime-1.2.4-ffmpeg-2.0.patch
- Sun Dec 11 2016 - Thomas Wagner
- use correct pnm_macro for SUNWogg-vorbis
* Wed May 6 2014 - pjama
- ruthlessly steal patch from slackware to mod ffmpeg plugin files to suit ffmpeg v2
* Fri Jun 22 2012 - Milan Jurik
- bump to 1.2.4
* Sun Nov 20 2011 - Milan Jurik
- bump to 1.2.3
* Tue Jan 25 2011 - Milan Jurik
- update to 1.2.2
* Sun Apr 18 2010 - Milan Jurik
- update to 1.1.5
- additional build dependencies
* Tue Sep 08 2009 - Milan Jurik
- update to 1.1.3
* Fri Feb 22 2008 - trisk@acm.jhu.edu
- Bump to 1.0.2, drop patch1, patch2
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Add a patch to fix a compile failure with Sun Studio 11
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
