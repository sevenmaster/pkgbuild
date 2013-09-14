#
# spec file for package SFEweechat
#
# includes module: weechat
#

# NOTE: The ruby plugin does not work when compiled against runtime/ruby-18
# from the solaris repository.

# NOTE: It is not clear if spell checking works.  WeeChat is aware of aspell,
# at least.

# Note: Update and use the patch below to use Enchant instead of aspell:
# http://savannah.nongnu.org/patch/?6858

%include Solaris.inc
%include packagenamemacros.inc
%define srcname weechat

Name:		SFE%srcname
IPS_Package_Name:	 communication/irc/weechat
Summary:	Lightweight console IRC client
URL:		http://www.weechat.org/
Vendor:		Sebastien Helleu <flashcode@flashtux.org>
Version:	0.4.1
License:	GPLv3+
Source:		http://www.weechat.org/files/src/%srcname-%version.tar.bz2
Patch5:		weechat-05-remove-xopen-source-override.diff
Patch6:		weechat-06-add-string-h-include.diff
SUNW_Copyright:	weechat.copyright
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SUNWgsed
BuildRequires:	SFEcmake
BuildRequires:	SFElibiconv
BuildRequires:	SFEruby
#BuildRequires:	runtime/lua
BuildRequires:  SUNWlua
Requires:	SFElibiconv
Requires:	SFEruby
#Requires:	runtime/lua
Requires:	SUNWlua

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif

%description
WeeChat (Wee Enhanced Environment for Chat) is a fast and light cross-platform
chat environment. It can be entirely controlled with the keyboard, has a
plugin-based architecture and is customizable and extensible with scripts in
several scripting languages.
 
Authors:
--------
Sebastien Helleu <flashcode@flashtux.org>


%prep
%setup -q -n %srcname-%version
%patch5 -p1
%patch6 -p1

mkdir build

#our xgettext doesn't support these switches
gsed -i.bak 's/--package-name=.WeeChat. --package-version=\${VERSION}//' po/CMakeLists.txt


%build

export CC=gcc
export LIBS="-L/usr/gnu/lib -lncurses -L/usr/lib -L/usr/ruby/1.8/lib"
export CPPFLAGS="-I/usr/include/ncurses -I/usr/include"

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

sed 's| -Wall -W -Werror-implicit-function-declaration||' CMakeLists.txt > foo
mv foo CMakeLists.txt
cd build

cmake -DPREFIX=/usr \
	-DCMAKE_C_FLAGS="%gcc_optflags -std=c99 -D_XOPEN_SOURCE=600 -D__EXTENSIONS__ -I/usr/include/ncurses -I/usr/gnu/include" \
	-DCMAKE_EXE_LINKER_FLAGS="%_ldflags -liconv -lnsl -lsocket -lxnet -lruby -llua -L/usr/gnu/lib -R/usr/gnu/lib" \
	-DRUBY_LIBRARY="/usr/lib/libruby.so.1" \
	-DRUBY_EXECUTABLE="/usr/bin/ruby" \
	-DRUBY_INCLUDE_DIRS="/usr/include/ruby-1.9.1" \
	-DCMAKE_ARGS="-DENABLE_RUBY=yes -DENABLE_LUA=yes" ..

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
cd build
gmake install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_bindir}
%{_bindir}/weechat-curses
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/%{srcname}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/%{srcname}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (-, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%{srcname}.pc
%defattr (-, root, other)
%{_datadir}/icons/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Sep 14 2013 - Thomas Wagner
- integrate Ian's work
- change to (Build)Requires SUNWlua
- re-numbering patches / add as patch5, patch6
- set CC=gcc
- fix group for icons dir
##TODO## libruby.so needs to be specified accoding to the recorded dependency
* Tue Jun 11 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Bump to 0.4.1
- Replace patches with new set for 0.4.x
- Fix ruby plugin (now depends on SFEruby)
* Mon Jun 30 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.3.8
* Sun Oct 30 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.3.6
- Patched TIOCGWINSZ and Aspell issue (use Enchant)
* Wed Aug 24 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.3.5
* Wed Jul 27 2011 - Alex Viskovatoff
- SFEaspell doesn't build, so don't try to link against it
* Mon Jul 25 2011 - N.B.Prashanth
- add SUNW_Copyright
* Sun Mar 13 2011 - Alex Viskovatoff
- Initial spec

