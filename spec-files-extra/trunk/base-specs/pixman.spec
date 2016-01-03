#
# spec file for package pixman
#

Name:         pixman
License:      LGPL v2
Group:        System/Libraries
Version:      0.32.8
Release:      1
Distribution: Java Desktop System
Vendor:	      Gnome Community
Summary:      Pixel manipulation library for X and Cairo
Source:       http://cairographics.org/releases/pixman-%version.tar.gz
URL:          http://www.pixman.org/

%package devel
Summary:      Pixman Developer Libraries
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}

%prep
%setup -q

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`

libtoolize -f
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

export CFLAGS="%{optflags}"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
export LIBS="-lgmodule-2.0"
./configure \
            --prefix=%{_prefix}         \
            --sysconfdir=%{_sysconfdir}	\
            --libdir=%{_libdir}         \
            --bindir=%{_bindir}         \
	    --disable-gtk \
	    %{gtk_doc_option}
make -j $CPUS

%install
#export RPM_BUILD_ROOT=%_tmppath/SFEpixman-gpp-%version-build
make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%_libdir/*.*a

%changelog
* Mon Dec 28 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
