Version:        1.0.11
Summary:        Library for decoding and encoding video in the Dirac format

Group:          Applications/Multimedia
License:        LGPL/MIT/MPL
URL:            http://diracvideo.org/
#Source:         http://diracvideo.org/download/schroedinger/schroedinger-%{version}.tar.gz
Source:         http://diracvideo.org/download/schroedinger/schroedinger-%{version}.tar.gz
Patch1:		schroedinger-01-return.diff
Patch2:		schroedinger-02-testsuite.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n schroedinger-%{version}
perl -i.orig -lpe 'if ($. == 1){s/^.*$/#!\/bin\/bash/}' configure
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"

#find SFEorc orc-0.4.pc
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
#                              orc
  export PKG_CONFIG_PATH="/usr/gnu/lib/%{_arch64}/pkgconfig"
  export LDFLAGS="${LDFLAGS} -m64"
else
#                              orc
  export PKG_CONFIG_PATH="/usr/gnu/lib/pkgconfig"
echo
fi


./configure --prefix=%{_prefix}                 \
            --libdir=%{_libdir}                 \
            --datadir=%{_datadir}               \
            --mandir=%{_mandir}                 \
            --enable-gtk-doc                    \
            --enable-shared                     \
            --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov 23 2016 - Thomas Wagner
- set PKG_CONFIG_PATH=/usr/gnu/lib/<%{arch64}|>pkgconfig to find relocated SFEorc
- add "-m64" to LDFLAGS if building 64-bit
* Sun Nov 29 2015 - Thomas Wagner
- remove export PKG_CONFIG_PATH as it doesn't work for 64 bit, try default setting from nclude/*inc files
* Tue Jan 24 2012 - Milan Jurik
- bump to 1.0.11
* Mon Oct 17 2011 - Milan Jurik
- bump to 1.0.10
* Tue Jul 13 2010 - Thomas Wagner
- change shell of configure to be real bash
* Apr 2010 - Gilles Dauphin
- find pkg-config for ORC if in /opt/SFE
* Fri Apr 09 2010 - Milan Jurik
- initial import to SFE
* Wed May 7 2008 Christian Schaller <christian.schaller@collabora.co.uk>
- Added Schrovirtframe.h

* Fri Feb 22 2008 David Schleef <ds@schleef.org>
- Update for 1.0

* Fri Feb 1 2008 Christian F.K. Schaller <christian.schaller@collabora.co.uk>
- add schromotionest.h
- remove schropredict.h

* Tue Jan 22 2008 Christian F.K. Schaller <christian.schaller@collabora.co.uk>
- Update for latest changes

* Thu Apr 05 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- Further updates.

* Thu Apr 27 2006 Christian F.K. Schaller <christian@fluendo.com>
- Updates for carid -> schroedinger change
