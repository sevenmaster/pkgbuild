#
# spec file for package SFElibzen
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define download_loc	http://mediaarea.net/download/source/
%define srcname		libzen
%define _pkg_docdir	%_docdir/%srcname
%define libzen_version	0.4.32

Name:           SFElibzen
IPS_package_name: system/library/libzen
Version:        %{libzen_version}
Summary:        C++ utility library
License:        Zlib
Group:          System Environment/Libraries
URL:            http://sourceforge.net/projects/zenlib
Packager:       MediaArea.net SARL <info@mediaarea.net>
Source:		%download_loc%srcname/%version/%{srcname}_%version.tar.bz2

BuildRequires:  doxygen
%include	default-depend.inc

%description
ZenLib is a C++ utility library. It includes classes for handling strings,
configuration, bit streams, threading, translation, and cross-platform
operating system functions.


%package        doc
Summary:        C++ utility library -- documentation
Group:          Development/Libraries
Requires:       %{name}

%description    doc
ZenLib is a C++ utility library. It includes classes for handling strings,
configuration, bit streams, threading, translation, and cross-platform
operating system functions.

This package contains the documentation

%package        devel
Summary:        C++ utility library -- development
Group:          Development/Libraries
Requires:    	%{name}

%description    devel
ZenLib is a C++ utility library. It includes classes for handling strings,
configuration, bit streams, threading, translation, and cross-platform
operating system functions.

This package contains the include files and mandatory libraries
for development.

%prep
%setup -q -n ZenLib
#Correct documentation encoding and permissions
sed -i 's/.$//' *.txt
chmod 644 *.txt Source/Doc/Documentation.html

chmod 644 Source/ZenLib/*.h Source/ZenLib/*.cpp \
    Source/ZenLib/Format/Html/*.h Source/ZenLib/Format/Html/*.cpp \
    Source/ZenLib/Format/Http/*.h Source/ZenLib/Format/Http/*.cpp

pushd Project/GNU/Library
    autoreconf -i
popd

%build
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CPPFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

#Make documentation
pushd Source/Doc/
    doxygen Doxyfile
popd
cp Source/Doc/*.html ./

pushd Project/GNU/Library
    %configure --disable-static --enable-shared

    make clean
    make
popd

%install
rm -rf %buildroot

pushd Project/GNU/Library
    make install DESTDIR=%{buildroot}
popd

#Install headers and ZenLib-config
install -dm 755 %{buildroot}%{_includedir}/ZenLib
install -m 644 Source/ZenLib/*.h \
    %{buildroot}%{_includedir}/ZenLib
for i in HTTP_Client Format/Html Format/Http; do
    install -dm 755 %{buildroot}%{_includedir}/ZenLib/$i
    install -m 644 Source/ZenLib/$i/*.h \
        %{buildroot}%{_includedir}/ZenLib/$i
done

sed -i -e 's|Version: |Version: %{version}|g' \
    Project/GNU/Library/%{srcname}.pc
install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -m 644 Project/GNU/Library/%{srcname}.pc \
    %{buildroot}%{_libdir}/pkgconfig
rm %buildroot%_libdir/%srcname.la

%post -n %{name}0 -p /sbin/ldconfig

%postun -n %{name}0 -p /sbin/ldconfig

%clean
rm -rf %buildroot

%files
%defattr(-,root,bin,-)
%doc History.txt License.txt ReadMe.txt
%{_libdir}/%{srcname}.so.*

%files doc
%defattr(-,root,bin,-)
%doc Documentation.html
%doc Doc

%files devel
%defattr(-,root,bin,-)
%{_bindir}/%{srcname}-config
%{_includedir}/ZenLib
%{_libdir}/%{srcname}.so
%dir %attr (-, root, other) %_libdir/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Feb 10 2014 - Alex Viskovatoff
- import spec into SFE
* Tue Jan 01 2009 MediaArea.net SARL <info@mediaarea.net> - 0.4.29-0
- See History.txt for more info and real dates
- Previous packages made by Toni Graffy <toni@links2linux.de>
- Fedora style made by Vasiliy N. Glazov <vascom2@gmail.com>
