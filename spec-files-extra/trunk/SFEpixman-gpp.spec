#
# spec file for package SFEpixman-gpp
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%use pixman_64 = pixman.spec
%endif

%include base.inc
%define gtk_doc_option --disable-gtk-doc
%use pixman = pixman.spec

Name:                    SFEpixman-gpp
License:		 LGPL v2
IPS_package_name:        library/graphics/g++/pixman
Group:			 Desktop (GNOME)/Libraries
Summary:                 Pixel manipulation library for X and Cairo
Version:                 %pixman.version
SUNW_BaseDir:            %_basedir

%include default-depend.inc
BuildRequires:		SFEglib2-gpp-devel
Requires:		SFEglib2-gpp

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%pixman_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%pixman.prep -d %name-%version/%{base_arch}

%build

export CC=gcc
export CXX=g++

%ifarch amd64 sparcv9
export LDFLAGS="-L/usr/g++/lib/amd64 -R/usr/g++/lib/amd64"
export PKG_CONFIG_PATH="%_pkg_config_path64"
%pixman_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="%_pkg_config_path"
%pixman.build -d %name-%version/%{base_arch}

%install
rm -rf %buildroot

%ifarch amd64 sparcv9
%pixman_64.install -d %name-%version/%_arch64
%endif

%pixman.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %_libdir
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %_includedir
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%_arch64
%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
%_libdir/%_arch64/pkgconfig/*
%endif

%changelog
* Mon Dec 28 2015 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
