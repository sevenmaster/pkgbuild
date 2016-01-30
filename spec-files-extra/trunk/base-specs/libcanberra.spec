#
# spec file for package libcanberra
#
# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:                    libcanberra
License:                 LGPL v2.1
Group:                   Libraries/Multimedia
Version:                 0.28
Distribution:            Java Desktop System
Vendor:                  0pointer.de
Summary:                 Event Sound API Using XDG Sound Theming Specification
Source:                  http://0pointer.de/lennart/projects/libcanberra/libcanberra-%{version}.tar.gz
# This patch is needed until autoconf is updated to 2.63 and libtool to 2.2.
#owner:yippi date:2008-09-02 type:branding 
Patch1:                  libcanberra/01-solaris.patch
#owner:yippi date:2010-09-24 type:bug doo:16974 
Patch2:                  libcanberra/02-device.patch
#Patch3:                  libcanberra/03-gtk3.patch
URL:                     http://0pointer.de/blog/projects/sixfold-announcement.html
%include default-depend.inc

Requires:                SUNWgnome-config
BuildRequires:           SUNWgnome-config-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires: %name

%prep
%setup -q -n %{name}-%{version}
#%define _patch_options --unified
%patch1 -p1
%patch2 -p1
#%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%{_ldflags}"

autoreconf --force --install

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir} --bindir=%{_bindir} \
            --libexecdir=%{_libexecdir}      \
            --enable-gtk \
            --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Oct 29 2012 - rohini.s@oracle.com
- Bump to 0.28.
...

* Fri Jul 24 2009 - ke.wang@sun.com
- Split from SUNWlibcanberra.spec to add 64-bit support

