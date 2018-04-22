# 
# spec file for package SFElibvdpau
# 
%include Solaris.inc
%include packagenamemacros.inc

Name:                SFElibvdpau
IPS_Package_Name:	 library/video/libvdpau
Summary:             Nvidia VDPAU library
Version:             1.1.1
Source:				 https://people.freedesktop.org/~aplattner/vdpau/libvdpau-%{version}.tar.bz2
URL:                 https://www.freedesktop.org/wiki/Software/VDPAU/
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
Group:		      	 System/Multimedia Libraries
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:			 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc

%prep
%setup -q -n libvdpau-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"

./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libvdpau*
%{_libdir}/vdpau*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%attr (-, root, bin) %{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_prefix}/share
%dir %attr (0755, root, other) %{_prefix}/share/doc
%attr (-, bin, bin) %{_prefix}/share/doc/*

%files root
%defattr(-,root,sys)
%config %{_sysconfdir}/*

%changelog
* Sun Apr 22 2018 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial version 1.1.1
