#
# spec file for package SFEquassel
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname		quassel
%define _pkg_docdir	%_docdir/%srcname


Name:			SFEquassel
IPS_package_name:	desktop/irc/%srcname
Group:			Applications/Internet
Summary:		Graphical IRC client based on a client-server model
Version:		0.9.1
URL:			http://quassel-irc.org/
License:		GPLv2
SUNW_Copyright:		GPLv2.copyright
Source:			http://quassel-irc.org/pub/%srcname-%version.tar.bz2
SUNW_BaseDir:		%_basedir
%include		default-depend.inc

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

cd %buildroot/%_datadir
mv apps/quassel .
rmdir apps


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
* Fri Nov  1 2013 - Alex Viskovatoff <herzen@imapmail.org>
- initial spec
