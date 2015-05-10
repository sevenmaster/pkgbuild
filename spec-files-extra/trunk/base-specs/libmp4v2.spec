#
# spec file for package libmp4v2
#
# includes module(s): libmp4v2
#

%define src_ver		2.0.0
%define src_name	mp4v2
%define src_url		http://mp4v2.googlecode.com/files

Name:                    libmp4v2
Summary:                 Library providing an API to create and modify mp4 files as defined by ISO-IEC:14496-1:2001 MPEG-4 Systems
Version:                 %{src_ver}
Source:                  %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		libmp4v2-01-sunpro.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags" 

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    export LDFLAGS="$LDFLAGS -m64"
fi

%if %( expr %{omnios} '>=' 1 '|' %{openindiana} '>=' 1 )
#no aclocal/* please
#avoid running autotools (make would do that from GNUMakefile)
[ -L autoaux/missing ] || mv autoaux/missing autoaux/missing_away
[ -f autoaux/missing ] || echo /usr/bin/true > autoaux/missing
%else
libtoolize --force
aclocal
automake -a -c -f
autoconf
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun May 15 2015 - Thomas Wagner
- disable script autoaux/missing on omnios and openindiana
* Wed Mar  4 2015 - Thomas Wagner
- %include osdistro.inc, exclude aclocal on %{omnios}
* Sun Aug 19 2012 - Milan Jurik
- use GCC
* Sun Jul 29 2012 - Milan Jurik
- bump to 2.0.0
* Sun Oct 16 2011 - Milan Jurik
- fix sun studio build
* Fri Jun 18 2010 - Milan Jurik
- fix 64-bit build
* Fri Aug 21 2009 - Milan Jurik
- Initial base spec file
