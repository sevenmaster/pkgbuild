#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:		libevent2
Summary:	An event notification library for event-driven network servers.
Version:	2.0.22
Source:		%{sf_download}/levent/libevent/libevent-2.0/libevent-%{version}-stable.tar.gz
Patch1:         libevent2-01-evutil_rand.c_fix_return_arc4random_buf.diff
URL:		http://monkey.org/~provos/libevent/
Group:		System/Libraries

%prep
%setup -q -n libevent-%version-stable

%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
	--libdir=%{_libdir}	\
	--mandir=%{_mandir}	\
	--docdir=%_docdir	\
	--disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libevent*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Mar  2 2015 - Thomas Wagner
- bump to 2.0.22
- add patch1 no return value from arc4random_buf 
* Tue Dec 18 2012 - Logan Bruns <logan@gedanken.org>
- updated download url
* Sat Dec 8 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 2.0.21
* Sat Feb 11 2012 - Milan Jurik
- bump to 2.0.17
* Thu Nov 17 2011 - Milan Jurik
- multiarch support
