#
# spec file for package SFElibdvdcss
#
# includes module(s): libdvdcss
#
%include Solaris.inc

Name:		SFElibdvdcss
IPS_Package_Name:	library/video/libdvdcss 
Summary:	A simple library designed for accessing DVDs like a block device without having to bother about decryption
Group:		System/Multimedia Libraries
URL:		http://www.videolan.org/developers/libdvdcss.html
License:	GPLv2
SUNW_copyright:	libdvdcss.copyright
Version:	1.4.0
Source:		http://download.videolan.org/pub/libdvdcss/%{version}/libdvdcss-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n libdvdcss-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Dec  9 2016 - Thomas Wagner
- add to %files %{_docdir}/*
* Sat Apr  2 2016 - Thomas Wagner
- bump to 1.4.0
* Sun Nov 20 2011 - Milan Jurik
- bump to 1.2.11
* Mon Oct 10 2011 - Milan Jurik
- add IPS package name
* Sat Jun 13 2009 - Milan Jurik
- upgrade to 1.2.10
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdvdcss
- changed to root:bin to follow other JDS pkgs.
* Wed Feb 15 2004 - glynn.foster@sun.com
- Initial version
