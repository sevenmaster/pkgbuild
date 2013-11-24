%include Solaris.inc
%define srcname libquvi-scripts
%define _pkg_docdir %_docdir/%srcname

Name:           SFElibquvi-scripts
IPS_package_name: video/libquvi-scripts
Version:        0.9.20131012
Summary:        Embedded lua scripts that libquvi uses for parsing the media details
License:        AGPLv3+
URL:            http://quvi.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/quvi/0.9/%srcname/%srcname-%version.tar.xz
BuildArch:      noarch
BuildRequires:	SFElua-socket, SFElua-json, SFElua-expat
Requires:       lua-socket
Requires:       lua-json
Requires:	lua-expat

%description
libquvi-scripts contains the embedded lua scripts that libquvi
uses for parsing the media details. Some additional utility
scripts are also included.

%prep
%setup -q -n %srcname-%version

%build
export CC=gcc
./configure --prefix=/usr --with-nsfw

%install
# Noarch fix.
make install DESTDIR=%buildroot pkgconfigdir=%_datadir/pkgconfig/

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%doc AUTHORS ChangeLog COPYING NEWS README
%_datadir/%srcname
%_datadir/pkgconfig/%srcname*.pc
%_mandir/man7/%srcname.7*
%_mandir/man7/quvi-modules*.7*

%changelog
* Wed Oct 30 2013 Alex Viskovatoff
- Import Fedora spec
* Thu Sep 26 2013 Christopher Meng <rpm@cicku.me> - 0.9.20130903-1
- New version.
- Add missing lua dep(BZ#1012165).
