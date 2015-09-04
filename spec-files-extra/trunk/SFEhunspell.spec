#
# spec file for package SFEhunspell
#

####				USING WITH EMACS			    ####
#
# NOTE: To use Hunspell under Emacs, at least Emacs 23 is required.
# NOTE: For languages other than English, ispell often fails, complaining
# of "misalignment".
#
# It is necessary to redefine ispell's dictionary definitions, which are
# intended for aspell.  For example, place this in your .emacs file:
#
# (setq ispell-dictionary-base-alist
#   '((nil ; default
#      "[A-Za-z]" "[^A-Za-z]" "[']" t ("-d" "en_US") nil utf-8)
#     ("english" ; US English
#      "[A-Za-z]" "[^A-Za-z]" "[']" t ("-d" "en_US") nil utf-8)
#     ("german"  ; FRG German
#      "[A-Za-zäöüßA-ZÄÖÜ]" "[^A-Za-zäöüßA-ZÄÖÜ]" "[']" t ("-d" "de_DE") nil utf-8)
#     ("french"
#      "[A-Za-zÀÂÆÇÈÉÊËÎÏÔÙÛÜàâçèéêëîïôùûü]" "[^a-zÀÂÆÇÈÉÊËÎÏÔÙÛÜàâçèéêëîïôùûü]"
#      "[']" t ("-d" "fr_FR") nil utf-8)
#     ("russian"
#      "[А-Яа-яёЁ]" "[^А-Яа-яёЁ]" "[']" t ("-d" "ru_RU") nil utf-8)
# ))
#
# (eval-after-load "ispell"
#   '(setq ispell-dictionary "english"
# 	 ispell-extra-args '("-a")
# 	 ispell-silently-savep t))
#
# (setq-default ispell-program-name "hunspell")


%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname hunspell
%define _pkg_docdir %_docdir/%srcname

Name:		SFEhunspell
IPS_Package_Name:	library/spell-checking/hunspell
Summary:	Spell checker
Group:		Applications/Accessories
URL:		http://hunspell.sourceforge.net
Vendor:		László Németh
Version:	1.3.3
License:	MPLv1.1 or GPLv2+ or LGPLv2.1+
SUNW_Copyright:	hunspell.copyright
Source:		http://downloads.sourceforge.net/%srcname/%srcname-%version.tar.gz
Patch1:		hunspell-01-dict-path.diff

%include default-depend.inc

BuildRequires:	library/ncurses
Requires:	ncurses
BuildRequires:	library/readline
Requires:	readline
Requires:	library/myspell/dictionary/en

%package devel
Summary:	%summary - development files
%include default-depend.inc
Requires:	%name


%prep
%setup -q -n %srcname-%version
%patch1 -p0

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -I/usr/include/ncurses"
export LIBS="-lsocket -lpthread"
export LDFLAGS="%_ldflags %gnu_lib_path"
sed -i 's/-lcurses/-lncurses/g' configure
./configure --prefix=%_prefix --enable-threads=posix --disable-static --with-ui --with-readline

make -j$CPUS


%install
rm -rf %buildroot

gmake install DESTDIR=%buildroot

iconv -f iso-8859-1 -t utf-8 ChangeLog.O > ChangeLog.O.new
mv ChangeLog.O.new ChangeLog.O

rm -f %buildroot%_libdir/lib*a

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%doc ABOUT-NLS AUTHORS AUTHORS.myspell BUGS ChangeLog ChangeLog.O README README.myspell THANKS TODO
%_bindir/*
%_libdir/*.so*
%dir %attr (-, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%srcname.pc
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/doc
%dir %attr (-, root, other) %_datadir/locale
%attr (-, root, other) %_datadir/locale/*
%_mandir

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/*


%changelog
* Thu Sep  3 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 1.3.3; build with gcc (does not build with Studio)
* Wed Nov  7 2013 - Alex Viskovatoff
- add documentation
* Wed Oct 30 2013 - Alex Viskovatoff
- add hack to prevent picking up of /lib/libcurses.so.1
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sat Jul 23 2011 - Alex Viskovatoff
- Use SUNWncurses instead of SFEncursesw
* Fri Jun 10 2011 - Alex Viskovatoff <herzen@imap.cc>
- do not create separate IPS devel package
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- bump to 1.3.2
* Wed Mar 23 2011 - Alex Viskovatoff
- bump to 1.3.1
* Fri Feb  4 2011 - Alex Viskovatoff
- update to 1.2.14
* Wed Nov 10 2010 - Alex Viskovatoff
- add another missing build dep; do not package static lib
- add patch to make Hunspell find dictionaries without depending on DICPATH
* Mon Nov 08 2010 - Milan Jurik
- add missing build dep
* Thu Oct 14 2010 - Alex Viskovatoff
- Initial spec
