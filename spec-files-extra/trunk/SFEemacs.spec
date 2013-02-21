#
# spec file for package SFEemacs
#
# includes module(s): GNU emacs
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

# Avoid conflict with editor/gnu-emacs
%include usr-gnu.inc
%define _infodir %_datadir/info

%include packagenamemacros.inc

Name:                    SFEemacs
IPS_Package_Name:	 sfe/editor/gnu-emacs
Summary:                 GNU Emacs - an operating system in a text editor
Version:                 24.2.1
License:                 GPLv3+
SUNW_Copyright:          emacs.copyright
%define emacs_version    24.2
%define src_version      24.2
Source:                  http://ftp.gnu.org/pub/gnu/emacs/emacs-%emacs_version.tar.bz2
#Patch1:                  emacs-01-sound.diff
URL:                     http://www.gnu.org/software/emacs/emacs.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%define _with_gtk 1

BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk2
BuildRequires: SFEalsa-lib-devel
BuildRequires: SUNWtexi
Requires: SUNWTiff
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWlibms
Requires: SUNWzlib
Requires: %pnm_requires_perl_default
Requires: SUNWtexi
Requires: SUNWdbus
Requires: SFEalsa-lib
Requires: SFEalsa-plugins
Requires: %{name}-root
%if %{?_with_gtk:1}%{?!_with_gtk}
%define toolkit gtk
Requires: SUNWgtk2
Requires: SUNWglib2
Requires: SUNWcairo
%else
%define toolkit motif
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxwice
%endif
BuildRequires: SFEgiflib-devel
Requires: SFEgiflib
BuildRequires: SFElibmagick-gpp-devel
Requires: SFElibmagick-gpp

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n emacs-%src_version
#%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CFLAGS="$CFLAGS -O6"
export CXX=g++
export LDFLAGS="$LDFLAGS -L/usr/gnu/lib -R/usr/gnu/lib -lncurses -R/usr/g++/lib"

export PERL=/usr/perl5/bin/perl

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/gnu/lib/pkgconfig:/usr/lib/pkgconfig

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
            --localstatedir=%{_localstatedir}   \
            --with-gif=yes \
            --with-x-toolkit=%toolkit \
            --with-xft

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
        infodir=$RPM_BUILD_ROOT%{_infodir} \
        localstatedir=$RPM_BUILD_ROOT%{_localstatedir}

rm -f $RPM_BUILD_ROOT%{_bindir}/ctags
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/emacs
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/emacs.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps/
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/emacs/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%attr (0755, root, bin) %{_infodir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/games
%dir %attr (0755, root, sys) %{_localstatedir}/games/emacs
%{_localstatedir}/games/emacs/*

%changelog
* Wed Feb 20 2013 - Logan Bruns <logan@gedanken.org>
- minor tweaks and cleanups.
* Fri Feb  8 2013 - Logan Bruns <logan@gedanken.org>
- updated to 24.2
- added IPS name
* Sun Apr 01 2012 - Pavel Heimlich
- bump to 23.3b, workaround for Studio 12.3
* Sun Oct  2 2011 - Alex Viskovatoff
- Work around usr-gnu.inc not placing info dir in /usr/gnu
* Mon Sep 12 2011 - Alex Viskovatoff
- bump to version 23.3a
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Mon Jun 27 2011 - Alex Viskovatoff
- Install in /usr/gnu so as not to conflict with system gnu-emacs
* Sun Apr 12 2011 - Alex Viskovatoff
- Add missing build dependencies
* Thu Mar 17 2011 - Alex Viskovatoff
- Bump to 23.3; reenable sound support
* Wed Sep 15 2010 - knut.hatlen@oracle.com
- Add missing dependencies.
* Mon Jul 19 2010 - markwright@internode.on.net
- Bump to 23.2
* Tue Aug 04 2009 - jedy.wang@sun.com
- Bump to 23.1
* Thu Oct 2 2008 - markwright@internode.on.net
- Bump to 22.3
* Wed Oct 17 2007 - laca@sun.com
- change /var/games owner to root:bin to match Maelstrom
* Tue Oct 16 2007 - laca@sun.com
- enable building with gtk if the --with-gtk build option is used (default
  remains motif)
- disable sound support (alsa breaks the build currently)
* Wed Jul 24 2007 - markwright@internode.on.net
- Bump to 22.1, change CPP="cc -E -Xs", add --with-gcc=no --with-x-toolkit=motif, add %{_localstatedir}/games/emacs.
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEemacs
- add missing deps
* Wed Oct 12 2005 - laca@sun.com
- create
