# spec file for package libspectre
#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         libspectre
License:      GPLv2
Group:        System/Libraries
Version:      0.2.7
Release:      1 
Distribution: Java Desktop System
Vendor:       freedesktop.org
Summary:      Simple PostScript API wrapping Ghostscript libgs.
Source:       http://libspectre.freedesktop.org/releases/%{name}-%{version}.tar.gz
# date:2009-08-30 type:feature owner:dkenny 
Patch1:       libspectre-01-uninstalled.pc.diff
URL:          http://libspectre.freedesktop.org/
Docdir:       %{_docdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define cairo_version 0.5.0
%define gtk2_version 2.4.0

Requires:      cairo >= %{cairo_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      SUNWghostscriptu

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires:  SUNWghostscriptu

%prep
%setup -q
%patch1 -p1

%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# SFE's libtool gets confused if the S11 libtool is installed
export PATH=/opt/dtbld/bin:/usr/bin:/usr/gnu/bin:/usr/sbin
libtoolize --force

aclocal $ACLOCAL_FLAGS -I . 
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --datadir=%{_datadir}       \
	    --sysconfdir=%{_sysconfdir} \
	    --mandir=%{_mandir}	        \
        %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_libdir}/*.so.*

%changelog
* Tue Jun 22 2010 - ghee.teo@oracle.com
- Removed libspectre-02-printf_x.diff which is upstreamed.
...

* Sun Aug 30 2009 - darren.kenny@sun.com
- Initial spec file for libspectre
