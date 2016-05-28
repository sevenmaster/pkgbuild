#
# spec file for package SFEquassel
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname		quassel
%define _pkg_docdir	%_docdir/%srcname


Name:			SFEquassel
IPS_package_name:	desktop/irc/quassel
Group:			Applications/Internet
Summary:		Graphical IRC client based on a client-server model
Version:		0.12.4
URL:			http://quassel-irc.org/
License:		GPLv2
SUNW_Copyright:		GPLv2.copyright
Source:			http://quassel-irc.org/pub/%srcname-%version.tar.bz2
SUNW_BaseDir:		%_basedir
%include		default-depend.inc

BuildRequires:		SFEcmake
BuildRequires:		SFEqt-gpp

%description
Quassel is a program to connect to an IRC network. It has the unique ability to
split the graphical component (quasselclient) from the part that handles the IRC
connection (quasselcore). This means that you can have a remote core permanently
connected to one or more IRC networks and attach a client from wherever you are
without moving around any information or settings. However, Quassel can easily
behave like any other client by combining them into one binary which is referred
to as "Quassel Mono".

%prep
%setup -q -n %srcname-%version


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

# gcc 4.6 produces "unrecognized command line option '-std=c++11'" error
export CC=gcc
export CXX=g++
export PATH=/usr/g++/bin:$PATH
export CFLAGS="%gcc_optflags"
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"
export QMAKESPEC=solaris-g++

mkdir -p builds/unix
cd builds/unix

cmake -DWANT_CORE=ON -DWANT_MONO=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=%_prefix -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DQT=/usr/g++ -DWITH_OPENSSL=ON -DSTATIC=OFF ../..

make -j$CPUS


%install
rm -rf %buildroot

cd builds/unix
make install DESTDIR=%buildroot

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%doc AUTHORS ChangeLog README
%_bindir/quasselclient
%_bindir/quasselcore
%dir %attr (-, root, sys) %_datadir
%defattr (-, root, other)
%_datadir/applications/quasselclient.desktop
%_datadir/icons
%_datadir/pixmaps/%srcname.png
%_datadir/%srcname


%changelog
* Fri May 27 2016 - Alex Viskovatoff <herzen@imap.cc>
- bump to 0.12.4
* Sun Nov  7 2015 - Thomas Wagner
- compile works, quasselcore + quasselclient both okay when compiled with SFEgcc.spec (rev 6024), so use this on S11 and other osdistro
* Thu Aug 27 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 0.12.2; build with system gcc (SFEgcc can't compile this)
- use SFEcmake (Solaris 11.2's cmake is too ald)
* Tue Jan 14 2014 - Alex Viskovatoff <herzen@imapmail.org>
- bump to 0.9.2
* Fri Nov  1 2013 - Alex Viskovatoff <herzen@imapmail.org>
- initial spec
