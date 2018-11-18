#
# spec file for package SFElibpng
#
# includes module(s): libpng
#

%include Solaris.inc
%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libpng_64 = libpng.spec
%endif

%include base.inc
%use libpng = libpng.spec


Name:                    SFElibpng16-gnu
IPS_Package_Name:	 image/library/gnu/libpng16
Summary:    	         %{libpng.summary} (/usr/gnu)
Version:                 %{libpng.version}
URL:			 %{libpng.url}
Source:         ftp://ftp-osl.osuosl.org/pub/libpng/src/libpng16/libpng-%{version}.tar.gz
##TODO## SUNW_Copyright: libpng-utils.copyright
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

#%define cc_is_gcc 0

%description 
libpng - reference library for use in applications that create and manipulate PNG (Portable Network Graphics) raster image files
Note: results from /usr/gnu/bin/libpng-config does not distinguish 32/64-bit. Use /usr/gnu/bin/i86/libpng-config, /usr/gnu/bin/64/libpng-config, /usr/gnu/bin/sparcv7/libpng-config or /usr/gnu/bin/64/libpng-config

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
Requires:       %{name}
%endif

%prep
rm -rf %{name}-%{version}
%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%libpng_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_isa
%libpng.prep -d %{name}-%{version}/%base_isa


%build
%ifarch amd64 sparcv9
%libpng_64.build -d %{name}-%{version}/%_arch64
%endif

%libpng.build -d %{name}-%{version}/%{base_isa}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libpng_64.install -d %{name}-%{version}/%_arch64
%endif

%libpng.install -d %{name}-%{version}/%{base_isa}

mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
cp -d %{buildroot}/%{_bindir}/pngfix %{buildroot}/%{_bindir}/%{base_isa}/
cp -d %{buildroot}/%{_bindir}/png-fix-itxt %{buildroot}/%{_bindir}/%{base_isa}/
cp -d %{buildroot}/%{_bindir}/libpng16-config %{buildroot}/%{_bindir}/%{base_isa}/
for binary in pngfix png-fix-itxt
  do
  #move real i386/sparc 32 bit binaries to %{_bindir}/%{base_isa}
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  #sorry, this is a hack. we have no isaexec in /usr/gnu/lib
  ln -s -f /usr/lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary
#symbolic links remain in place, they are copied instead

find ${RPM_BUILD_ROOT} -type f -name "*.a" -exec rm -f {} ';' -o -type f -name "*.la" -exec rm -f {} ';' -o -type l -name "*.a" -exec rm -f {} ';'  -o -type l -name "*.la" -exec rm -f {} ';'


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, bin)
%ifarch amd64 sparcv9
%{_bindir}/%{base_isa}/*
%{_bindir}/%{_arch64}/*
%hard %{_bindir}/png-fix-itxt
%hard %{_bindir}/pngfix
%{_bindir}/libpng-config
%{_bindir}/libpng16-config
#those are symlinks to the binaries above
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%dir %attr(0755, root, bin) %{_mandir}/man5
%{_mandir}/man*/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
#%dir %attr (0755, root, other) %{_datadir}/doc
#%{_datadir}/doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif



%changelog
* Sat Nov 17 2018 - Thomas Wagner
- reworked spec and made 32/64-bit
- renamed to SFElibpng16-gnu, IPS_Package_Name: image/library/gnu/libpng16
- bump to 1.6.34
* Mon Jun 25 2018 - Thomas Wagner
- fix metadata in spec file to enable propper pkgtool --autodeps
* Sun Jan 28 2018 - Thomas Wagner
- bumped to 1.6.34
* Tue Sep  5 2017 - Thomas Wagner
- bumped to 1.6.32
* Tue May 1 2012 - Logan Bruns <logan@gedanken.org>
- moved to /usr/gnu.
* Sun Apr 29 2012 - Logan Bruns <logan@gedanken.org>
- split out -devel package so runtime libs can be installed without conflicts
- bumped to 1.5.10
- fixed some permissions
* Sun Feb 26 2012 - Logan Bruns <logan@gedanken.org>
- Brought back and bumped to 1.4.9. This fixes security CVE-2011-3026 and with a rebuilt imagemagick support for PNG which is broken with the OI bundled libpng.
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
