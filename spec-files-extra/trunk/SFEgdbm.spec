#
# spec file for package SFEgdbm
#
# includes module(s): gdbm
#

##NOTE## only works on osdistro which misses the gdbm package. For example on OmniOS.

%include Solaris.inc
%define cc_is_gcc 1

%include packagenamemacros.inc
#%if %( expr %{omnios} '|' %{openindiana} '|' %{oihipster} '|' %{solaris12} '&' %{osbuild} '>=' 63 '|' %{solaris11} '&' %{osdistro_entire_padded_number4}.0 '>=' 0000017500030000000000120001.0 )
%if %( test %{pnm_buildrequires_SUNWgnu_dbm} != SFEgdbm && echo 1 )
%include usr-gnu.inc
%endif
%include base.inc


Name:         SFEgdbm
%if %( test %{pnm_buildrequires_SUNWgnu_dbm} != SFEgdbm && echo 1 )
Summary:      GNU Database Routines (/usr/gnu)
IPS_Package_Name: library/database/gnu/gdbm
#noting to do
%else
##only build if osdistro has no gdbm
Summary:      GNU Database Routines
IPS_Package_Name: library/database/gdbm
%endif
Group:        libraries/database
Version:      1.11
License:      GPL
Group:        Development/Libraries/C and C++
Release:      1
BuildRoot:    %{_tmppath}/gdbm-%{version}-build
Source0:      http://ftp.gnu.org/gnu/gdbm/gdbm-%{version}.tar.gz
URL:          http://directory.fsf.org/gdbm.html
#Patch1:       gdbm-01-fixmake.diff
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%description
GNU database routines

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n gdbm-%version
#%patch1 -p1

%build

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

#glib-gettextize -f
#libtoolize --force
#aclocal
#autoconf
CFLAGS="$CFLAGS $RPM_OPT_FLAGS"         \
        ./configure                     \
                --prefix=%{_prefix}     \
                --infodir=%{_datadir}/info \
                --mandir=%{_mandir}     \
                --libdir=%{_libdir}     \
                --disable-static

%install
rm -rf $RPM_BUILD_ROOT
gmake DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*


%changelog
* Mon Aug  3 2015 - Thomas Wagner
- relocate with usr-gnu.inc if osdisto's gdbm is the default S12, S11 >= 116, OI
* Mon Jun 29 2015 - Thomas Wagner
- prevent building on S12, S11 >= 116, OI
* Sat Jan 17 2015 - Thomas Wagner
- compile with gcc, fix %files, remove patch1 gdbm-01-fixmake.diff
* Mon Dec 23 2014 - Thomas Wagner
- bump to 1.11
- add IPS_Package_Name
- unarchive for OmniOS, use distro's gdbm until that versions aren't suffient any more
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgdbm
- delete -share subpkg
- update file attributes
* Fri May 05 2006 - damien.carbery@sun.com
- Remove unnecessary intltoolize call.
* Wed Mar 08 2006 - brian.cameron@sun.com
- Created.
