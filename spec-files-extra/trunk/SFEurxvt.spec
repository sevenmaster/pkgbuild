#
# spec file for package SFEurxvt
#

%define src_version 9.18
%define version 9.18

#include perl
%define with_perl 1

##TODO## needs rework for IPS: %{version} is not truly numeric: 9.06 .. needs workaround for IPS
#TODO# urxvt does not set terminal-size. have to use: stty rows 50; stty columns 132; export LINES=50 COLUMNS=132
##DONE## #TODO# cleanup environment setting CFLAGS/CXXFLAGS/LDFLAGS...
#TODO# solve build errors with --enable-perl 
#TODO# something like infocmp -C rxvt-unicode >> /etc/termcap as postinstall script (safely) - "screen" needs this
#TODO# put nice descrition of features into %description
#TODO# really need fix the terminfo entries, "tic" issues warnings....
#TODO# check libafterimage - if usefull, add

#   tested with: SFEgcc (older version gcc 4.0.0) and /usr/sfw/bin/gcc
#
#   NOT working with: sunstudio 12,  SFEgcc 4.2 (incl. gnu ld)
#       if you do not specify the CC/CXX before running pkgtool (see above) you might get 
#       gnu 4.x.x or sunstudio compilers...
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc


Name:                    SFEurxvt
IPS_Package_Name:        terminal/urxvt
Group:                   Applications/System Utilities
Summary:                 urxvt - X Terminal Client (+multiscreen Server) with unicode support, derived from rxvt
URL:                     http://software.schmorp.de
Version:                 %{version}
Source:                  http://dist.schmorp.de/rxvt-unicode/Attic/rxvt-unicode-%{src_version}.tar.bz2
Patch10:		 urxvt-10-terminfo_enacs.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{src_version}-build


%include default-depend.inc

#old gcc is enough BuildRequires: SFEgcc
#old gcc is enough Requires:      SFEgccruntime
#let the IPS dependency resolve do it for us
##TODO## need automatic setting of build/runtime dependeny on gcc runtime
#BuildRequires: SUNWgcc
#Requires:      SUNWgccruntime


%description
Note: Remember to set your LC_CYTPE *before* running rxvt, see file
%{_docdir}README.FAQ

urxvt is a Multiscreenserver and Client for Terminal emulation. Supports Unicode
charsets and has tons of nice features. With "compiz" you can enable traparent 
backgrounds (unmodified or shaded background inside the Terminal window)

To add the terminal controls to /etc/termcap run this command after package install:
grep "^rxvt-unicode" /etc/termcap || \
 TERMINFO=/usr/share/lib/terminfo infocmp -C rxvt-unicode >> /etc/termcap 

Infos about perl extentions as helpers in urxvt:
e.g. http://www.jukie.net/bart/blog/urxvt-url-yank


%prep
%setup -q -n rxvt-unicode-%{src_version}
%patch10 -p1
#%patch11 -p1

perl -w -pi.bak_bash -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure

gsed -i.bak_XOPEN_SOURCE -e '/define _XOPEN_SOURCE 500.*confdefs.h/ s?^?#?' configure


%build
export CC=gcc
export CXX=g++
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags -L/usr/X11/lib -R/usr/X11/lib -lX11 -lXext -lXrender"
export CXXFLAGS="%cxx_optflags"

export TIC=/usr/bin/tic

./configure \
            --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
 	    --enable-shared \
 	    --disable-static \
            --enable-transparency \
            --enable-24bits \
            --enable-xft  \
%if %with_perl
--enable-perl \
%else
--disable-perl \
%endif
            --enable-xgetdefault \
            --enable-mousewheel \
            --disable-menubar \
            --enable-ttygid \
            --enable-half-shadow \
            --enable-smart-resize \
            --enable-256-color \
            --enable-24bit \
            --enable-unicode3\
            --enable-combining\
            --enable-xft       \
            --enable-font-styles\
            --enable-afterimage\
            --enable-transparency  \
            --enable-fading    \
            --enable-tinting    \
            --enable-rxvt-scroll\
            --enable-next-scroll \
            --enable-xterm-scroll \
            --enable-plain-scroll \
            --enable-xim           \
            --enable-xpm-background \
            --enable-fallback \
            --enable-resources \
            --with-save-lines=2000 \
            --enable-linespace \
            --enable-iso14755    \
            --enable-frills       \
            --enable-keepscrolling \
            --enable-selectionscrolling \
            --enable-mousewheel  \
            --enable-slipwheeling \
            --enable-smart-resize\
            --enable-text-blink   \
            --enable-pointer-blank \
            --enable-utmp \
            --enable-wtmp  \
            --enable-lastlog\
            --with-codesets=all
         


make

%install
rm -rf $RPM_BUILD_ROOT

##TODO## do older systems have /usr/share/terminfo at all?
#else: just set with /lib/ on any os release
THISOSTERMINFO="$RPM_BUILD_ROOT/%{_datadir}/terminfo/"
[ -d %{_datadir}/lib/terminfo ] && THISOSTERMINFO="%{_datadir}/lib/terminfo/"

mkdir -p "$RPM_BUILD_ROOT/$THISOSTERMINFO"
#need TERMINFO tewaked only at make install time to influence "tic"'s target directory
export TERMINFO="$RPM_BUILD_ROOT/$THISOSTERMINFO"
make install DESTDIR=$RPM_BUILD_ROOT

#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT


#TODO# postinstall with TERMINFO=/usr/share/lib/terminfo infocmp -C rxvt-unicode >> /etc/termcap if !grep "^rxvt-unicode" /etc/termcap
#TODO# postinstall display note to user to really read the README.FAQ with tons of usefull hints


%files
%defattr(-, root, bin)
%doc README.FAQ README.configure Changes COPYING INSTALL MANIFEST
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%if %with_perl
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(-, root, sys) %{_datadir}/[l|t]*
%{_datadir}/[l|t]*/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*



%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}/locale
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Fru Oct 18 2013 - Thomas Wagner
- remove _XOPEN_SOURCE 500 from configure
* Thu Oct 17 2013 - Thomas Wagner
- bump to 9.18
- replace Patch12 with perl call in %prep, Patch16 (now in the source)
- set gcc compiler free: CC=gcc CXX=g++, remove (Build)Requires and let IPS dependency resolver do for now
- use TIC=/usr/bin/tic, export TERMINFO set to our $DESTDIR, then make install, remove patch11
- add IPS_Package_Name, Group
* Thu Aug 16 2012 - Thomas Wagner
- enable perl helper
* Sat Mar 31 2012 - Pavel Heimlich
- fix download location
* Thu Jun 09 2011 - Thomas Wagner
- bump to 9.11
- add Patch16 (already in svn code) to fix initial window not initialized with rows/columns
- (Build)Requires SUNWgcc<|runtime>  is sufficient
- fix location of terminfo directory, fix files for terminfo
* Sat Jun 19 2010 - Thomas Wagner
- bump to 9.07
- make version number IPS compatible (9.07 -> 9.7)
* Fri Feb 06 2009 - Thomas Wagner
- set compiler to gcc in any case
- (Build)Requires: SFEgcc(runtime)
- removed SunStudio left overs
- bump to 9.06
- rework patch10 for 9.06
- add patch12 bash for configure
- ##TODO## needs version textstring reworked for OS2008.xx/IPS
- create %{_docdir} in case old pkgbuild doesn't
- %doc adjusted files to be included - pkgbuild starting with 1.3.2 honours %doc and all files must be listed exactly
* Sat Mar 15 2008 Thomas Wagner
- reworked patch 10
- added patch 11 remove "tic" vom doc/Makfile 
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 0.92
* Fri Nov 23 2007  - Thomas Wagner
- refined, first version of terminfo/termcap
- open issues see TODO - any ideas?
* Sat Jul 14 2007  - Thomas Wagner
- Initial spec
