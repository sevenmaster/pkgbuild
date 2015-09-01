#
# spec file for package SFEmpdscribble
#
# includes module: mpdscribble
#

%include Solaris.inc
%define srcname mpdscribble

Name:		SFEmpdscribble
IPS_package_name: audio/mpd/mpdscribble
Summary:	MPD client which submits information about tracks being played to Last.fm
URL:		http://mpd.wikia.com/wiki/Client:Mpdscribble
Meta(info.upstream):	Max Kellermann <max@duempel.org>
License:	GPLv2
SUNW_Copyright:	mpdscribble.copyright
Version:	0.22
Source:		http://www.musicpd.org/download/%srcname/%version/%srcname-%version.tar.bz2
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFElibmpdclient-devel
Requires:	SFElibmpdclient

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name


%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix --sysconfdir=%_sysconfdir

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%_bindir/%srcname
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%srcname
%dir %attr (0755, root, bin) %_mandir
%dir %attr (0755, root, bin) %_mandir/man1
%{_mandir}/man1/%srcname.1


%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%attr (-, root, root) %_sysconfdir/%srcname.conf


%changelog
* Tue Sep 01 2015 - Alex Viskovatoff <herzen@imap.cc>
- update source url
* Tue Oct 25 2011 - Alex Viskovatoff
- Bump to 0.22
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
