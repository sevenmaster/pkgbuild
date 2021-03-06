#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.10

Name:                SFEkdeaddons3
Summary:             Additional plugins and scripts for some KDE applications.
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdeaddons-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
BuildRequires: SFEkdegames3-devel
Requires: SUNWlibsdl
BuildRequires: SUNWlibsdl-devel

%prep
%setup -q -n kdeaddons-%version

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -fPIC -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/gnu/include/sasl:/usr/sfw/include:/usr/include/pcre" \
           --with-ssl-dir=/usr/sfw


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/applnk
%dir %attr (0755, root, other) %{_datadir}/applnk/.hidden
%{_datadir}/applnk/.hidden/*
%dir %attr (0755, root, other) %{_datadir}/mimelnk
%{_datadir}/mimelnk/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*

%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Tue Nov 27 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 3.5.10
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Fixed typo in configure options.
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Initial spec.
