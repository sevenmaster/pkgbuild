#
# spec file for package: tmux
#
# Copyright 2010 Guido Berhoerster.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%include base.inc

%define srcname tmux
%define _pkg_docdir %_docdir/%srcname

Name:           SFEtmux-gnu
IPS_Package_Name:	terminal/gnu/tmux
Summary:        Terminal multiplexer (/usr/gnu)
#Summary:        Terminal multiplexer (/usr/gnu) - GIT Version
#remember to increment the 4th digit with every git commit snapshot to help upgrading git checked out tmux
#git IPS_Component_Version: 1.9.0.2
#git %define git_snapshot	df6488a47088ec8bcddc6a1cfa85fec1a462c789
#git Version:        1.9a.git.df6488
Version:        2.3
License:        ISC ; BSD3c ; BSD 2-Clause
Url:            http://tmux.github.io/
#git Source:		http://sourceforge.net/code-snapshots/git/t/tm/tmux/tmux-code.git/tmux-tmux-code-%{git_snapshot}.zip
Source:		http://github.com/tmux/tmux/releases/download/%{version}/tmux-%{version}.tar.gz
Group:          Applications/System Utilities
Distribution:   OpenIndiana
Vendor:         OpenIndiana Community
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:	tmux.copyright
SUNW_Basedir:   %{_basedir}
%include default-depend.inc

##TODO## needs a pnm macro!
%if %{oihipster}
Requires:       library/libevent2
BuildRequires:  library/libevent2
%else
Requires:       SFElibevent2
BuildRequires:  SFElibevent2
%endif

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):            Nicholas Marriott <nicm@users.sf.net>
Meta(info.maintainer):          Guido Berhoerster <gber@openindiana.org>
Meta(info.repository_url):      http://tmux.cvs.sourceforge.net/viewvc/tmux/tmux/

%description
tmux is a terminal multiplexer: it enables a number of terminals (or windows),
each running a separate program, to be created, accessed, and controlled from a
single screen. tmux may be detached from a screen and continue running in the
background, then later reattached. tmux is intended to be a modern,
BSD-licensed alternative to programs such as GNU screen.

tmux uses a client-server model. The server holds multiple sessions and each
window is a independent entity which may be freely linked to multiple sessions,
moved between sessions and otherwise manipulated. Each session may be attached
to (display and accept keyboard input from) multiple clients.

%prep
#%setup -q -n %{srcname}-%{srcname}-code-%{git_snapshot}
%setup -q -n %{srcname}-%{version}
#tmux-tmux-code-df6488a47088ec8bcddc6a1cfa85fec1a462c789
#cd %{srcname}-%{srcname}-code-%{git_snapshot}

#%patch6 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %{cc_is_gcc}
CC=gcc
CXX=g++
%endif

export CFLAGS="%optflags -I/usr/gnu/include -D_XPG6"
%if %{cc_is_gcc}
%else
#studio
export CFLAGS="$CFLAGS -xc99"
%endif 

# try avoiding core dumps by linking to 0@0.so.1
#export LDFLAGS="/usr/lib/0@0.so.1 %_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags"
export LIBNCURSES_CFLAGS="-I/usr/include/ncurses"
export LIBNCURSES_LIBS="-lncurses"

export LIBEVENT_CFLAGS="-I/usr/gnu/include"
export LIBEVENT_LIBS="-R/usr/gnu/lib -L/usr/gnu/lib -levent"

#find our SFElibevent2
####export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig

[ -x autogen.sh ] && bash autogen.sh
./configure
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 %{buildroot}%{_bindir}
install -m 0755 tmux %{buildroot}%{_bindir}/tmux
install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 0644 tmux.1 %{buildroot}%{_mandir}/man1/tmux.1
mkdir %buildroot%_docdir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%_bindir/tmux
%dir %attr (-, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%doc CHANGES FAQ TODO
%doc %_mandir/man1/tmux.1


%changelog
* Wed Oct 26 2016 - Thomas Wagner
- tried avoiding terminal-resize being ignored (S11.3). Shorten LDFLAGS (remove 0@0, hope it doesn't core dump now)
- point to our libevent from /usr/gnu/ (note: not fully tested on hipster where we use osdistro libevent)
- remove again patch6
* Sun Oct  9 2016 - Thomas Wagner
- re-introduce Patch6 tmux-06-client.c-client-resize-needs-to-trigger-window-resize.diff
* Fri Oct  7 2016 - Thomas Wagner
- bump to 2.3
- use gcc, remove compile fix for vis.h
- set LIBNCURSES_CFLAGS LIBNCURSES_LIBS for ncurses
* Tue Jul 12 2016 - Thomas Wagner
- bump to 2.2
* Sun Jan 17 2016 - Thomas Wagner
- conditional (Build)Requires on SFElibevent2 or library/libevent2 (OIH) duplicate packages!
  workaround until pnm_macro for for libevent2 package is available
* Fri Jan 15 2016 - Thomas Wagner
- bump to 2.1
- upgrade to settings -D_XPG6 -xc99
- keep the commented git checkout instructions in case we need them again
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Mon Aug 10 2015 - Thomas Wagner
- bump to 2.0
- new URL, new SOURCE (pause git checkout)
* Sun Jan 18 2015 - Thomas Wagner
- move to get snapshot instead regular downlod (try if mark/copy_to_clipbord stops writing core dumps)
- bump to df6488a47088ec8bcddc6a1cfa85fec1a462c789 (git snapshot df6488)
- obsolete patch5
- rework patch6
* Sat Dec 20 2014 - Thomas Wagner
- bump to 1.9a, add IPS_Component_Version 1.9.0.1
- remove patch1, remove/replace patch2 and patch3 by new patch6 (adopted from Solaris Userland), 
- add patch5 errno.h
- %include usr-gnu.inc (conflicting with Solaris 11 tmux package)
* Tue Dec 18 2012 - Logan Bruns <logan@gedanken.org>
- updated to 1.7, added ips name and updated patches
* Mon Oct 31 2011 - Alex Viskovatoff
- Add patch fixing window name updates in statusbar for debug OS builds
* Sun Oct  2 2011 - Alex Viskovatoff
- Adapt to SFElibevent2 being moved to /usr/gnu; update to 1.5
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Sun Apr 10 2011 - Alex Viskovatoff
- Use SFElibevent2
* Mon Mar 14 2011 - Alex Viskovatoff
- Import spec from http://hg.openindiana.org/spec-files-oi-extra/
  installing in /usr and bumping to 1.4
* Wed Oct  6 2010 - gber@openindiana.org
- Initial version.
