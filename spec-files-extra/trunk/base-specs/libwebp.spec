#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:	libwebp
Version:	0.2.1
Source:		http://webp.googlecode.com/files/%{name}-%{version}.tar.gz

%prep
%setup -q

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
	--libdir=%{_libdir}     \
	--mandir=%{_mandir}     \
	--docdir=%_docdir       \
	--disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libwebp*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Feb 24 2013 - Logan Bruns <logan@gedanken.org>
- updated to 0.2.1
* Sun Aug 05 2012 - Milan Jurik
- bump to 0.1.99
* Wed Dec 28 2011 - Milan Jurik
- initial spec
