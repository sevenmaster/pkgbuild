#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name	fltk

Name:		SFEfltk2
IPS_Package_Name:	library/desktop/fltk
Summary:	A C++ user interface toolkit
Version:	2.0.x-alpha-r9204
IPS_component_version: 2.0.0.0.9204
Source:		ftp://ftp.easysw.com/pub/%{src_name}/snapshots/%{src_name}-%{version}.tar.bz2
URL:		http://www.fltk.org/
License:	FLTK and LGPLv2
SUNW_Copyright:	fltk2.copyright
Group:		Desktop (GNOME)/Libraries
Patch1:		fltk2-01-scandir.diff
Patch2:		fltk2-02-sunstudio.diff
Patch3:		fltk2-03-test.diff
Patch7:		fltk2-07-soname.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWxwplt
Requires:	SUNWxwplt
BuildRequires:	SUNWxorg-mesa
Requires:	SUNWxorg-mesa

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%prep
%setup -q -n fltk-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch7 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIB="-L/usr/SFW/lib -R/usr/SFW/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"
EXTRALIB="-lXrender -lfontconfig"

export CFLAGS="%optflags -I/usr/X11/include -I/usr/gnu/include"
export LDFLAGS="%{_ldflags} $X11LIB $GNULIB $EXTRALIB"


./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --enable-shared \
            --enable-cairo \
            --enable-x11multithread

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.*a

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/man/cat*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/fluid2
%{_libdir}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/fltk2-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3

%changelog
* Tue Feb 07 2012 - Milan Jurik
- bump to r9204
* Sun Sep 25 2011 - Milan Jurik
- fix Sun Studio build
* Wed Aug 24 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 8800
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jun 11 2011 - Alex Viskovatoff
- bump to 8411
* Fri Apr 16 2011 - Alex Viskovatoff
- bump to 7722
* Sat Jun 12 2010 - Milan Jurik
- bump to 7513
* Tue Oct 22 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 6403
* Sat Jan 11 2008 - moinak.ghosh@sun.com
- Bump version, fix download URL
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial spec
