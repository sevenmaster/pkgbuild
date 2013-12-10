%include Solaris.inc
%define srcname quvi
%define _pkg_docdir %_docdir/%srcname

Name:           SFEquvi
IPS_package_name: video/quvi
Version:        0.9.5
Summary:        Command line tool for parsing video download links
Group:          Applications/Internet
License:        LGPLv2+
URL:            http://quvi.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%srcname/%srcname-%version.tar.xz
Patch0:		quvi-01-termios.patch
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%srcname-build

BuildRequires: SFElibquvi-devel
BuildRequires: curl
BuildRequires: glib2
BuildRequires: SFEjson-glib-devel
BuildRequires: libxml2

%description
quvi is a command line tool for parsing video download links.
It supports Youtube and other similar video websites.


%prep
%setup -q -n %srcname-%version
%patch0 -p1


%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=/usr
make

%install
make install DESTDIR=%buildroot


%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%doc ChangeLog COPYING README 
%_bindir/%srcname
%_mandir/man1/%srcname*.1
%_mandir/man5/%{srcname}rc.5

%changelog
* Wed Dec  4 2013 - Alex Viskovatoff
- Bump to 0.9.5
* Tue Oct 22 2013 - Alex Viskovatoff
- Import Fedora spec
* Fri Aug 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.3.1-1
- Update to 0.9.3.1
