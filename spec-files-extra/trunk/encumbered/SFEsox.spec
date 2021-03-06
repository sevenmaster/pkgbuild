#
# spec file for package SFEsox
#
# includes module(s): sox
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name sox
%define src_ver 14.4.1
%define src_url %sf_download/project/%src_name/%src_name/%src_ver


%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)


Name:                    SFEsox
Summary:                 The swiss army knife of sound processing programs
URL:                     http://sox.sourceforge.net/
Version:                 %{src_ver}
Source:                  %{src_url}/%{src_name}-%{src_ver}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SFElibsndfile
BuildRequires:    SFElibsndfile-devel
Requires:    SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires:    SUNWltdl
Requires:    SFEffmpeg
BuildRequires:    SFEffmpeg-devel
BuildRequires:    SUNWflac-devel
BuildRequires:    SFElibmad-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires: %name

%prep
rm -rf sox-%version
%setup -q -n sox-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --libexecdir=%{_libexecdir} \
            --enable-shared	\
            --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/sox


%clean
rm -rf $RPM_BUILD_ROOT

%files

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libsox*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/sox.pc

%changelog
* Fri Mar 29 2013 - Thomas Wagner
- update to 14.4.1
* Sun Jul 17 2011 - Alex Viskovatoff
- update source URL
* Fri Aug 21 2009 - Milan Jurik
- update to 14.3.0
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Mon Jun 30 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec
