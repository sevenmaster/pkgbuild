#
# spec file for package gst-plugins-ugly
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:           gst-plugins-ugly
License:        GPL
Version:        0.10.19
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Group:          Libraries/Multimedia
Summary:        GStreamer Streaming-media framework plug-ins - restricted redistribution.
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on
Prereq:         /sbin/ldconfig

%define 	majorminor	0.10

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%prep
%setup -n gst-plugins-ugly-%{version} -q

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
CONFIG_SHELL=/bin/bash \
bash ./configure \
  --prefix=%{_prefix}	\
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  %{gtk_doc_option}     \
%if %with_amrnb
%else
  --disable-amrnb \
%endif
%if %with_amrwb
%else
  --disable-amrwb \
%endif
  --disable-sidplay     \
  --enable-external     \
  --enable-orc

# FIXME: hack: stop the build from looping
touch po/stamp-it

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make 
else
  make
fi

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ]
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean out files that should not be part of the rpm.
# This is the recommended way of dealing with it for RH8
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/gstreamer-*/*.so
%{_sysconfdir}/gconf/schemas/gstreamer-*.schemas
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%post 
%{_bindir}/gst-register > /dev/null 2> /dev/null
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gstreamer-0.10.schemas"
for S in $SCHEMAS; do
 gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%package devel
Summary: 	GStreamer Plugin Library Headers.
Group: 		Development/Libraries
Requires: 	gstreamer-plugins-devel >= 0.10.0
Requires:       %{name} = %{version}

%description devel
GStreamer support libraries header files.

%files devel
%defattr(-, root, root)
%{_datadir}/gtk-doc

%changelog
* Sat Sep 28 2013 - Milan Jurik
- bump to 0.10.19
* Thu Sep 01 2011 - Milan Jurik
- bump to 0.10.18
- enable x264 support again because gst-ffmpeg x264 support is unstable
* Thu Apr 28 2011 - Alex Viskovatoff
- disable x264, since it breaks build (x264 decoder support is provided by ffmpeg)
* Sun Feb 06 2011 - Milan Jurik
- bump to 0.10.17, remove support for old gstreamer
* Thu Jun 10 2010 - Albert Lee <trisk@opensolaris.org>g
- Bump to 0.10.15, use 0.10.13 for older GStreamer
* Sun Dec 20 2009 - Milan Jurik
- upgrade to 0.10.13
* Wed Sep 02 2009 - Albert Lee <trisk@forkgnu.org>
- Add %gtk_doc_option
- Disable twolame
* Sun Jun 28 2009 - Milan Jurik
- upgrade to 0.10.12
- build cleanup, libtool shave disable (problematic shell script)
- amrnb as optional
- cdio and lame by default
* Fri Dec 12 2008 - trisk@acm.jhu.edu
- Bump to 0.10.10
- Disable more plugins
* Thu Sep 08 2008 - halton.huo@sun.com
- Bump to 0.10.9
* Wed Jul 23 2008 - trisk@acm.jhu.edu
- Add patch2 to use dvdnav
* Tue Jul 22 2008 - trisk@acm.jhu.edu
- Bump to 0.10.8
* Thu Oct 18 2007 - trisk@acm.jhu.edu
- Licence should be GPL
* Wed Oct 17 2007 - trisk@acm.jhu.edu
- Initial spec, based on gst-plugins-good
