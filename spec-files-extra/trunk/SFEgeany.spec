#
# spec file for package SFEgeany
#
# includes module(s): geany
#

%include Solaris.inc

%define src_url     http://download.geany.org
%define src_name    geany

Name:		SFEgeany
IPS_Package_Name:	developer/geany
Summary:	A small and lightweight integrated developer environment
Version:	1.22
License:	GPLv2+
SUNW_Copyright:	geany.copyright
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		geany-01-export.diff
URL:		http://www.geany.org/
Group:		Development/Integrated Development Environments
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	library/perl-5/xml-parser

%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%package doc
Summary:	%{summary} - documentation, man pages
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p1

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

make -j$CPUS

%install
cp geany.desktop.in geany.desktop
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/geany
%{_libdir}/geany/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/geany
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%{_datadir}/applications/*
%{_datadir}/geany/*
%{_datadir}/icons/hicolor/*/apps/*

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%files doc
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/geany
%{_docdir}/geany/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/geany
%{_includedir}/geany/*

%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 1.22
* Sat Dec 31 2011 - Milan Jurik
- bump to 0.21
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue Jan 25 2011 - Milan Jurik
- bump to 0.20
* Wed Jan 05 2011 - Milan Jurik
- bump to 0.19.2
* Wed Nov 17 2010 - Milan Jurik
- bump to 0.19.1
* Mon Mar 16 2009 - andras.barna@gmail.com
- Bumped to 0.16
* Sun May 28 2008 - Ananth Shrinivas <ananth@sun.com>
- Complete revamp of the spec file
- Cleaned up all file and directory attributes
- Bump to geany 0.14
* 2008.Mar.17 - <shivakumar dot gn at gmail dot com>
- Bumped to V0.13
- Compile with gcc since that works out of the box
* 2007.Aug.08 - <shivakumar dot gn at gmail dot com>
- Use of %package & %files for sub-package creation
  (base pkg, doc pkg, l10n pkg)
- Introduction of custom compile/link flags
- Make uses multiple CPU systems for parallelism
* 2007.Aug.08 - <shivakumar dot gn at gmail dot com>
- Use of include files for common definitions
* 2007.Aug.07 - <shivakumar dot gn at gmail dot com>
- Initial spec. Example for a badly designed but working spec
