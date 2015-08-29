#
# spec file for package SFEmkvtoolnix
#

# Don't try to get GUIs to build.
%define enable_gui 0

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname mkvtoolnix
%define _pkg_docdir %_docdir/%srcname

Name:		SFEmkvtoolnix
IPS_Package_Name:	media/mkvtoolnix
Summary:	Tools for the Matroska video container
Group:		Applications/Sound and Video
URL:		http://www.bunkus.org/videotools/mkvtoolnix
Meta(info.upstream):	Moritz Bunkus <moritz@bunkus.org>
Version:	8.3.0
License:	GPLv2
SUNW_Copyright:	mkvtoolnix.copyright
Source:		http://www.bunkus.org/videotools/%srcname/sources/%srcname-%version.tar.xz
Patch7:	mkvtoolnix-07-hevc-variable-types.patch

SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires: runtime/ruby-21
BuildRequires: SFElibmatroska-gpp-devel
BuildRequires: SFEboost-gpp-devel
BuildRequires: SUNWlexpt
BuildRequires: library/zlib
BuildRequires: library/lzo
BuildRequires: SUNWogg-vorbis
BuildRequires: SUNWflac
%if %enable_gui
BuildRequires: SFEwxwidgets-gpp-devel
%endif
BuildRequires: text/gnu-gettext
# configure can't find libmagick because it's in /usr/gnu;
# adding its path to CXXFLAGS keeps other things from being found
# so: TODO: make configure find libmagick (in file/file)
#BuildRequires: file/file

%description
MKVToolNix is a set of tools to create, alter and inspect Matroska files under
Linux, other Unices and Windows. They do for Matroska what the OGMtools do for
the OGM format and then some.

MKVToolNix consists of the tools mkvmerge, mkvinfo, mkvextract, and mkvpropedit.

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version
%patch7 -p0


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

# gcc 4.6 is too old to build this.  It builds with 4.8.2.
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export USER_CXXFLAGS="%cxx_optflags -fpermissive -D_POSIX_PTHREAD_SEMANTICS -D_GLIBCXX_USE_C99_MATH_TR1"
export USER_LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export ZLIB_CFLAGS="-I/usr/include"
export ZLIB_LIBS=-lz
%if %enable_gui
export PATH=/usr/g++/bin:$PATH
%endif

CXXFLAGS=$USER_CXXFLAGS LDFLAGS=$USER_LDFLAGS ./configure --prefix=%_prefix \
--with-extra-includes=/usr/g++/include --with-boost-libdir=/usr/g++/lib \
%if %enable_gui
--with-wx-config=/usr/g++/bin/wx-config
%else
--disable-gui
%endif

./drake -j$CPUS


%install
rm -rf %buildroot

./drake install DESTDIR=%buildroot

%if %build_l10n
%else
rm -rf %buildroot%_datadir/locale
rm -rf %buildroot%_docdir/%srcname/guide/zh_CN
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (-, root, other) %_docdir
%doc ChangeLog README.md AUTHORS
%_bindir
%dir %attr (-, root, sys) %_datadir
%_mandir

%if %enable_gui
%_docdir/%srcname/guide
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/mkvinfo.desktop
%_datadir/applications/mkvmergeGUI.desktop
%dir %attr (-, root, root) %_datadir/mime
%dir %attr (-, root, root) %_datadir/mime/packages
%_datadir/mime/packages/%srcname.xml
%defattr (-, root, other)
%_datadir/icons
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (-, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Fri Aug 28 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 8.3.0; disable GUIs; build with system gcc (SFEgcc is too old)
* Sun Feb  9 2014 - Alex Viskovatoff <herzen@imap.cc>
- require libmatroska: that and libebml can be external libraries again
* Sun Feb  2 2014 - Alex Viskovatoff <herzen@imap.cc>
- update to 6.7.0, adding one patch (build fails with gcc 4.7 without it)
  (bug report: https://trac.bunkus.org/ticket/977 )
* Sun Aug 05 2012 - Milan Jurik
- bump to 5.7.0
* Fri Oct 14 2011 - Alex Viskovatoff <herzen@imap.cc>
- Bump to 5.0.1
* Tue Aug  9 2011 - Alex Viskovatoff <herzen@imap.cc>
- Add missing (build) dependency
* Sat Jul 23 2011 - Alex Viskovatoff <herzen@imap.cc>
- Bump to 4.9.1; add SUNW_Copyright
* Mon Jul 18 2011 - Alex Viskovatoff <herzen@imap.cc>
- Modify CXXXFLAGS to enable building with gcc 4.6
* Thu Jun 23 2011 - Alex Viskovatoff <herzen@imap.cc>
- Build with g++
- Update to 4.8.0; build GUI
* Tue Apr 12 2011 - Alex Viskovatoff <herzen@imap.cc>
- Add patch to make build on oi_147
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- Bump to 4.6.0
* Sat Feb  5 2011 - Alex Viskovatoff
- Update to 4.5.0, adding one patch and removing one no longer needed
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4 because SS 12u1 does indeed understand it
* Sun Nov 21 2010 - Alex Viskovatoff
- Update to 4.4.0, with two patches no longer required
- Accommodate to stdcxx libs and headers residing in /usr/stdcxx
- Do not use -library=stdcxx4, which Sun Studio 12u1 does not understand
* Thu Oct 21 2010 - Alex Viskovatoff
- Add patch kindly provided by Moritz Bunkus to fix runtime bug (number 567)
- Move out of experimental
* Sun Oct 10 2010 - Alex Viskovatoff
- Initial spec
