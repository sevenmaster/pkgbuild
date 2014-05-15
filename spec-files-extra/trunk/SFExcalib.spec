#
# spec file for package SFElibxcalib
#
# includes module(s): libxcalib
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                    SFElibxcalib
IPS_Package_Name:	 x11/xcalib
Group:                   Libraries/Multimedia
Version:                 0.8
Source:                  http://downloads.sourceforge.net/xcalib/xcalib-source-%{version}.tar.gz
Summary:                 xcalib - load icc color profiles for X windows
URL:                     http://xcalib.sourceforge.net/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}


%include default-depend.inc

%description
load the monitor calibration data to get propper color display.
fetch the files from your windows system where you did the
calibration, files are usually stored under:
  systemdrive:\windows\system32\spool\drivers
The file extension is names *.icc or *.icm

load one of the the example color profiles like this:
xcalib /usr/share/doc/xcalib/gamma_2_2.icc

put xcalib into your startup scripts to get the corrections
active when logging in to your desktop.

%prep
%setup -q -n xcalib-%version

gsed -i -e 's/^CFLAGS/#CFLAGS/' \
        -e 's?/usr/local/bin/?%{_bindir}/?' \
        -e '/chmod.*bin\/xcalib/ s?chmod 0644?chmod 0755?' \
    Makefile 

%build
export CC=gcc
export CFLAGS="%{optflags} -Du_int16_t=uint16_t"
export LDFLAGS="%{_ldflags}"

make xcalib

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin/
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/xcalib
cp -p *.icc  $RPM_BUILD_ROOT/%{_datadir}/doc/xcalib/
cp -p *.icm  $RPM_BUILD_ROOT/%{_datadir}/doc/xcalib/
cp -p *.rc  $RPM_BUILD_ROOT/%{_datadir}/doc/xcalib/
cp -p README*  $RPM_BUILD_ROOT/%{_datadir}/doc/xcalib/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu May 15 2014 - Thomas Wagner
- initial spec
