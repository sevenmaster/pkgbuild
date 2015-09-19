#
# spec file for package SFEncmpcpp
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname ncmpcpp

Name:		SFEncmpcpp
IPS_package_name: audio/mpd/ncmpcpp
Summary:	Text-mode Music Player Daemon client
License:	GPLv2
SUNW_Copyright:	ncmpcpp.copyright
URL:		http://ncmpcpp.rybczak.net
Meta(info.upstream):	Andrzej Rybczak <electricityispower.gmail.com>
Version:	0.5.10
License:	GPLv2
Source:		http://ncmpcpp.rybczak.net/stable/%srcname-%version.tar.bz2

%include default-depend.inc
BuildRequires:	library/ncurses
Requires:	library/ncurses
BuildRequires:	SFElibmpdclient-devel
Requires:	SFElibmpdclient

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/include/ncurses"
export CXXFLAGS="%cxx_optflags -L/usr/gnu/lib -R/usr/gnu/lib:/usr/g++/lib"
export LIBS=-lsocket
export LDFLAGS="%_ldflags"
# Make taglib-config get found
export PATH=$PATH:/usr/g++/bin
./configure --prefix=%_prefix

gmake -j$CPUS

%install
rm -rf %buildroot

gmake install DESTDIR=%buildroot

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%_mandir
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname


%changelog
* Sat Sep 19 2015 - Alex Viskovatoff <herzen@imap.cc>
- link to taglib; clean up
* Sat Jan 25 2013 - Alex Viskovatoff
- do not hardcode path of gcc; follow new naming convention for mpd clients
* Fri Sep 13 2013 - Alex Viskovatoff
- Update to 0.5.10
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Mon Jul 18 2011 - Alex Viskovatoff
- Add -fpermissive flag to allow compilation with gcc 4.6
* Sun May 22 2011 - N.B.Prashanth <nbprash.mit@gmail.com>
- Add missing dependencies
- Bump to 0.5.7
* Tue Feb 01 2011 - Alex Viskovatoff
- Add missing dependencies
* Sun Jan 30 2011 - Alex Viskovatoff
- Update to 0.5.6
* Thu Oct 21 2010 - Alex Viskovatoff
- Initial spec
