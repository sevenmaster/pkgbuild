#
# spec file for package SFEpango-gpp
#

# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-g++.inc
%define _pkg_docdir %_docdir/pango
%define cc_is_gcc 1

#%ifarch amd64 sparcv9
%if 0
%include arch64.inc
%define _sysconfdir /etc/%{_arch64}
%use pango_64 = pango.spec
%endif

%include base.inc
%define _sysconfdir %_prefix/etc
%define gtk_doc_option --disable-gtk-doc

%use pango = pango.spec

Name:                    SFEpango-gpp
IPS_package_name:        library/desktop/g++/pango
#Meta(info.classification): %{classification_prefix}:Desktop (GNOME)/Libraries
Group:			 Desktop (GNOME)/Libraries
Summary:                 GNOME core text and font handling libraries
Version:                 %{pango.version}
License:                 %{pango.license}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright

%include default-depend.inc
BuildRequires: consolidation/X/X-incorporation
BuildRequires: data/sgml-common
BuildRequires: developer/gnu-binutils
BuildRequires: file/gnu-findutils
BuildRequires: SFEglib2-gpp-devel
BuildRequires: SFEcairo-gpp-devel
BuildRequires: SFEgobject-introspection-gpp-devel
BuildRequires: system/library/math
BuildRequires: text/gawk
BuildRequires: text/gnu-grep
BuildRequires: text/gnu-sed
BuildRequires: x11/library/libxft
BuildRequires: x11/server/xorg
BuildRequires: SFEfontconfig-gpp

%if 0
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
%endif

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

#%ifarch amd64 sparcv9
%if 0
mkdir %name-%version/%_arch64

%pango_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%pango.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
#gzcat %SOURCE0 | tar xf -

%build

export CC=gcc
export CXX=g++

#%ifarch amd64 sparcv9
%if 0
export LDFLAGS="%_ldflags -L/usr/g++/lib/amd64 -R/usr/g++/lib/amd64"
export PKG_CONFIG_PATH="%_pkg_config_path64"
%pango_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="%_pkg_config_path"
%pango.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
%if 0
%pango_64.install -d %name-%version/%_arch64
%endif

%pango.install -d %name-%version/%{base_arch}

# rm -rf $RPM_BUILD_ROOT%{_mandir}
# cd %{_builddir}/%name-%version/sun-manpages
# make install DESTDIR=$RPM_BUILD_ROOT

# on linux, these config files are created in %post
# that would be more complicated on Solaris, especially
# during jumpstart or live upgrade, so it's better to do
# it during the build
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
mkdir -p %buildroot%_sysconfdir/pango
$RPM_BUILD_ROOT%{_bindir}/pango-querymodules \
    $RPM_BUILD_ROOT%{_libdir}/pango/*/modules/*.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%_sysconfdir/pango/pango.modules
rm %buildroot%_libdir/pango/1.8.0/modules/*.la

#%ifarch amd64 sparcv9
%if 0
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}/%{_arch64}

$RPM_BUILD_ROOT%{_bindir}/%{_arch64}/pango-querymodules \
    $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/pango/*/modules/*.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/pango/pango.modules

rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/pango-view
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc -d  %{base_arch} pango-%{pango.version}/README
%doc -d  %{base_arch} pango-%{pango.version}/AUTHORS
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-0
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-2
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-4
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-6
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-8
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-10
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-12
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-14
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-16
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-18
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-20
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%_datadir/gtk-doc
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pango-querymodules
%{_bindir}/pango-view
%_mandir/man1/pango-view.1
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/pango/*/*/*.so
%{_libdir}/girepository-1.0/*
#%ifarch amd64 sparcv9
%if 0
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/pango-querymodules
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/pango/*/*/*.so
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/girepository-1.0
%{_libdir}/%{_arch64}/girepository-1.0/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0/*.gir
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/pango-querymodules.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
#%ifarch amd64 sparcv9
%if 0
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%endif

#%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%config %ips_tag(original_name=SUNWpango:%{@}) %{_sysconfdir}/pango
#%ifarch amd64 sparcv9
%if 0
%config %ips_tag(original_name=SUNWpango:%{@}) %{_sysconfdir}/%{_arch64}/pango
%endif

%changelog
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Import spec from Solaris desktop repository
* Thu May 03 2012 - brian.cameron@oracle.com
- Fix Requires/BuildRequires.
* Tue Jun 08 2010 - Michal.Pryc@Oracle.Com
- Updated BuildRequires to fit SourceJuicer.
* Mon Mar  5 2010 - christian.kelly@sun.com
- Deliver Pango-1.0.gir, gtk needs it.
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)

