
%include Solaris.inc

%define _use_internal_dependency_generator 0

%define version_zlib %( LC_ALL=C pkg info library/zlib | grep Version | awk -F':' '{print $2}' )

Name:                SFEzlib-pkgconfig
IPS_Package_Name:   library/zlib/pkgconfig/zlib.pc
Version:             %{version_zlib}
Summary:             Add missing zlib.pc for pkg-config

SUNW_BaseDir:        %{_prefix}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

BuildRequires: library/zlib
Requires:      library/zlib

%description
Special package to add zlib.pc, the information file for
pkg-config which tells the automatic configuration process
for compiling software where the library zlib is found
and which compiler includes and linker informations are
needed.

Note: This packages determines the zlib version at compile
time of the package. If the OS has an updates zlib library,
then the content of this packge with zlib.pc is most likely
in the need to be updated too.

%prep
%setup -T -c -n %name-%version


%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{_arch64}/pkgconfig

#32-bit
cat - > $RPM_BUILD_ROOT/usr/lib/pkgconfig/zlib.pc << --EOF--
prefix=/usr
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
sharedlibdir=\${libdir}
includedir=\${prefix}/include

Name: zlib
Description: zlib compression library
Version: %{version}

Requires:
Libs: -L\${libdir} -L\${sharedlibdir} -lz
Cflags: -I\${includedir}
--EOF--

#64-bit
cat - > $RPM_BUILD_ROOT/usr/lib/%{_arch64}/pkgconfig/zlib.pc << --EOF2--
prefix=/usr
exec_prefix=\${prefix}
libdir=/usr/lib/%{_arch64}/
sharedlibdir=\${libdir}
includedir=\${prefix}/include

Name: zlib
Description: zlib compression library
Version: %{version}

Requires:
Libs: -L\${libdir} -L\${sharedlibdir} -lz
Cflags: -I\${includedir}
--EOF2--

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Thu Aug 20 2015 - Thomas Wagner
- Initial spec - add missing files "zlib.pc" for platforms which have zlib but are missing zlib.pc for pkg-config

