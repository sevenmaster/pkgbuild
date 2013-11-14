

%define _use_internal_dependency_generator 0


#
# spec file for package SFEurxvt
#

%define src_version 9.18
%define version 9.18

#include perl
%define with_perl 1

#TODO# urxvt does not set terminal-size. have to use: stty rows 50; stty columns 132; export LINES=50 COLUMNS=132
##DONE## #TODO# cleanup environment setting CFLAGS/CXXFLAGS/LDFLAGS...
#TODO# something like infocmp -C rxvt-unicode >> /etc/termcap as postinstall script (safely) - "screen" needs this
#TODO# really need fix the terminfo entries, "tic" issues warnings....
#TODO# check libafterimage - if usefull, add

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include pkgbuild-features.inc

#description of this download method:
#https://fedorahosted.org/fpc/attachment/ticket/233/slask
#urxvtclip
%define githubowner2  fixje
%define githubproject2 dotfiles
#for github commits see link on the right with the shortened commitid on the Webpage
#  -> https://github.com/fixje/dotfiles/commit/5bd056fd147f87f85549104112b63170b1afda1c
%define commit2 5bd056fd147f87f85549104112b63170b1afda1c
#e.g. 5bd056f
%define shortcommit2 %(c=%{commit2}; echo ${c:0:7})

#mark-yank-urls
%define githubowner3   bartman
#%define githubowner3   dezgeg
%define githubproject3 urxvt-scripts
#for github commits see link on the right with the shortened commitid on the Webpage
# bartman -> https://github.com/bartman/urxvt-scripts/commit/1dc9f95f4e974d990ebdc0fed02e994e1eb7c2db
# problem: Missing sqlite tables: dezgeg  -> https://github.com/dezgeg/urxvt-scripts/commit/1bc76306b40d8fcfd6a61c75eb94b25c19da00f8
#%define commit3 1bc76306b40d8fcfd6a61c75eb94b25c19da00f8
%define commit3 1dc9f95f4e974d990ebdc0fed02e994e1eb7c2db
#e.g. 1bc7630
%define shortcommit3 %(c=%{commit3}; echo ${c:0:7})

#clipboard
%define githubowner4   muennich
%define githubproject4 urxvt-perls
#for github commits see link on the right with the shortened commitid on the Webpage
# muennich -> https://github.com/muennich/urxvt-perls/commit/adacf7920de47ce5b66b98679f1aec9b261836ee
%define commit4 adacf7920de47ce5b66b98679f1aec9b261836ee
#e.g. adacf79
%define shortcommit4 %(c=%{commit4}; echo ${c:0:7})

Name:                    SFEurxvt
IPS_Package_Name:        terminal/urxvt
Group:                   Applications/System Utilities
Summary:                 urxvt - X Terminal Client (+multiscreen Server) with unicode support, derived from rxvt
URL:                     http://software.schmorp.de
Version:                 %{version}
Source:                  http://dist.schmorp.de/rxvt-unicode/Attic/rxvt-unicode-%{src_version}.tar.bz2
Source2:                 http://github.com/%{githubowner2}/%{githubproject2}/archive/%{shortcommit2}/%{githubproject2}-%{commit2}.tar.gz
Source3:                 http://github.com/%{githubowner3}/%{githubproject3}/archive/%{shortcommit3}/%{githubproject3}-%{commit3}.tar.gz
Source4:                 http://github.com/%{githubowner4}/%{githubproject4}/archive/%{shortcommit4}/%{githubproject4}-%{commit4}.tar.gz
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

Requires: SFExclip
Requires: SFEperl-clipboard


#START automatic renamed package  (remember %actions)
# create automatic package with old name and "renamed=true" in it
%include pkg-renamed.inc

#STRONG NOTE:
#remember to set in this spec file the %action which
#adds the depend rule in a way that the new package 
#depends on the old package in a slightly updated branch
#version and has the flag "renamed=true" in it

%package %{name}-1-noinst
#if oldname is same as the "Name:"-tag in this spec file:
#example_ab# %define renamed_from_oldname      %{name}
#example_ab# %define renamed_from_oldname      SFEstoneoldpkgname
#
#example_a#  %define renamed_to_newnameversion category/newpackagename = *
#or
#example_b#  %define renamed_to_newnameversion category/newpackagename >= 1.1.1
#
#do not omit version equation!
%define renamed_from_oldname      %{name}
%define renamed_to_newnameversion terminal/urxvt = *
%include pkg-renamed-package.inc



#example# %package %{name}-2-noinst
#example# #add more and different old names here (increment the counter at the end)
#example# %define renamed_from_oldname      SFEstoneoldpkgname
#example# %define renamed_to_newnameversion terminal/urxvt >= 1.23
#example# %include pkg-renamed-package.inc

#END automatic renamed package

%description
Note: Remember to set your LC_CYTPE *before* running rxvt, see file
file://%{_docdir}/README.FAQ

urxvt is a Multiscreenserver and Client for Terminal emulation. Supports Unicode
charsets and has tons of nice features. With "compiz" you can enable traparent 
backgrounds (unmodified or shaded background inside the Terminal window)

make your setup with urxvt better:
----------------------------------
To add the terminal controls to /etc/termcap run this command after package install:
grep "^rxvt-unicode" /etc/termcap || \
 TERMINFO=/usr/share/lib/terminfo infocmp -C rxvt-unicode >> /etc/termcap 


added extra perl extension scripts: mark-url-yank, mark-and-yank, urxvtclip, clipboard, url-select
-----------------------------------

mark-url-yank, mark-and-yank ( bundled extension - needs your $HOME/.Xdefaults be setup)
----------------------------
Infos this perl extention: (mind the code forks/branches)
e.g. http://www.jukie.net/bart/blog/urxvt-url-yank


urxvtclip ( bundled extension - needs your $HOME/.Xdefaults be setup)
---------
https://github.com/fixje/dotfiles/tree/master/scripts
(read the ../Xdefaults file on github to get the keyboard shortcuts below)
clipboard features for urxvt. <C-v> to copy and <C-S-v> to paste.
(requires package xclip)
location: /usr/lib/urxvt/perl/urxvtclip
Xdefaults needs this at minimum:
URxvt.keysym.Shift-Control-V: perl:clipboard:paste
! add "," separated more modules e.g. thismodule,urxvtclip,othermodule
URxvt.perl-ext-common: urxvtclip

clipboard, url-select ( bundled extension - needs your $HOME/.Xdefaults be setup)
---------
https://github.com/muennich/urxvt-perls/blob/master/README.md



%prep
%setup -q -n rxvt-unicode-%{src_version}
%patch10 -p1
#%patch11 -p1

perl -w -pi.bak_bash -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure

gsed -i.bak_XOPEN_SOURCE -e '/define _XOPEN_SOURCE 500.*confdefs.h/ s?^?#?' configure

#oh well. some tar versions complain about a pax flag "g", so use gnu one
gzcat %{SOURCE2} | gtar xf -
gzcat %{SOURCE3} | gtar xf -
gzcat %{SOURCE4} | gtar xf -

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

test -d $RPM_BUILD_ROOT%{_docdir}/%{name} || mkdir $RPM_BUILD_ROOT%{_docdir}/%{name}

#extension urxvtclip
SOURCE2DIR=$( basename %{SOURCE2} | sed -e 's?\.tar\.gz??' )
SOURCE2DIRSHORT=$( echo $SOURCE2DIR | sed -e "s/%{commit2}/%{shortcommit2}/" )
cp $SOURCE2DIR/scripts/urxvtclip $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
cp -pr $SOURCE2DIR/ $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE2DIRSHORT/
[ -f $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE2DIRSHORT/.gitignore ] && rm $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE2DIRSHORT/.gitignore

#extension mark-and-yank mark-yank-urls
SOURCE3DIR=$( basename %{SOURCE3} | sed -e 's?\.tar\.gz??' )
SOURCE3DIRSHORT=$( echo $SOURCE3DIR | sed -e "s/%{commit3}/%{shortcommit3}/" )
cp $SOURCE3DIR/mark-and-yank $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
cp $SOURCE3DIR/mark-yank-urls $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
cp -pr $SOURCE3DIR/ $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE3DIRSHORT/
[ -f $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE3DIRSHORT/.gitignore ] && rm $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE3DIRSHORT/.gitignore

#extension clipboard
SOURCE4DIR=$( basename %{SOURCE4} | sed -e 's?\.tar\.gz??' )
SOURCE4DIRSHORT=$( echo $SOURCE4DIR | sed -e "s/%{commit4}/%{shortcommit4}/" )
#cp $SOURCE4DIR/clipboard $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
#cp $SOURCE4DIR/keyboard-select $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
#cp $SOURCE4DIR/url-select $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
cp $SOURCE4DIR/[a-z]* $RPM_BUILD_ROOT%{_libdir}/urxvt/perl/
cp -pr $SOURCE4DIR/ $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE4DIRSHORT/
[ -f $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE4DIRSHORT/.gitignore ] && rm $RPM_BUILD_ROOT%{_docdir}/%{name}/$SOURCE4DIRSHORT/.gitignore

%clean
rm -rf $RPM_BUILD_ROOT


#TODO# postinstall with TERMINFO=/usr/share/lib/terminfo infocmp -C rxvt-unicode >> /etc/termcap if !grep "^rxvt-unicode" /etc/termcap
#TODO# postinstall display note to user to really read the README.FAQ with tons of usefull hints

# automatic uninstall oldpkg on upgrade or on install newpkg

#list *all* old package names here which could be installed on
#user's systems
#stay in sync with section above controlling the "renamed" packages
#SFEurxvt@9.18-5.11,0.0.175.0.0.0.2.1 (note: last digit is incremented calculated
#on the branch version printed by pkg info release/name
%actions
depend fmri=SFEurxvt@%{ips_version_release_renamedbranch} type=optional
#depend fmri=SFEotheroldnamesgohere@%{ips_version_release_renamedbranch} type=optional


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
#match the extra perl extensions
%{_docdir}/%{name}/*-[0-9a-f]*/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*



%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}/locale
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Thu Nov 14 2013 - Thomas Wagner
- improve renamed package (oldpkg now with incremented IPS_Vendor_version aka branch)
- re-sort include logic to get %package working (would be a no-op if hidden inside an %include or %use)
* Tue Nov  5 2013 - Thomas Wagner
- add perl exensions mark-url-yank, mark-and-yank, urxvtclip
- add pkg-renamed.inc, define old package names and some examples
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
