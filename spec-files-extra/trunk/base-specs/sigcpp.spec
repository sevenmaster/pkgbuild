
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#

%define major_minor      2.3

Name:                    libsigc++
License:                 LGPL
Group:                   System/Libraries
Version:                 2.3.1
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Library that implements typesafe callback system for standard C++
URL:                     http://libsigc.sourceforge.net
Source:                  http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%major_minor/%{name}-%{version}.tar.xz
#Patch1:                  sigcpp-01-build-fix.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
#don't unpack please
%setup -q -c -T -n libsigc++-%version
xz -dc %SOURCE0 | ( cd ..; tar xf - )


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CXXFLAGS="%cxx_optflags"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"


perl -pi -e 's/(\s*#define SIGC_TYPEDEF_REDEFINE_ALLOWED.*)/\/\/$1/' \
    sigc++/macros/signal.h.m4

./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir} \
				    --bindir=%{_bindir} \
				    --libdir=%{_libdir} \
				    --libexecdir=%{_libexecdir} \
                                    --includedir=%{_includedir} \
                                    --mandir=%{_mandir} \
                                    --disable-static

gmake -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

pushd $RPM_BUILD_ROOT%{_datadir}/doc
mv libsigc++-2.0 libsigc++-%{major_minor}
popd

rm $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Nov  3 2013 - Thomas Wagner
- %use usr-g++.inc
- add BuildRequires: %{pnm_buildrequires_SFExz_gnu}, %include packagenamemacros.inc
- use manual xz unpacking for older pkgbuild versions
- use %{gnu_lib_path}
- make it 32/64-bit
* Wed Oct 30 2013 - Alex Viskovatoff
- Bump to 2.3.1
* Fri Aug  5 2011 - Alex Viskovatoff
- Bump to 2.2.10
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.2.2.
* Fri Feb 29 2008 - elaine.xiong@sun.com
- Bump to 2.2.1 that resolves build failure of 2.0 with CC.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.0.
* Fri Feb 22 2008 - elaine.xiong@sun.com
- Include tests binaries into dev package.
* Tue Feb 12 2008 - ghee.teo@sun.com
- Clean up %files section
* Fri Feb 01 2008 - elaine.xiong@sun.com
- create. split from SFEsigcpp.spec
