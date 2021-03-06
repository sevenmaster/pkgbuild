#
# spec file for package SFEgmpc
#
# use gcc to compile


%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc
%define srcname gmpc

# This package no longer exists
#%define SFEgtkmm   %(/usr/bin/pkginfo -q SFEgtkmm && echo 1 || echo 0)
%define SFEgtkmm 0

Name:                    SFEgmpc
IPS_package_name:	 audio/mpd/gmpc
Summary:                 Gnome Music Player Daemon client
URL:                     http://gmpclient.org/
Version:                 11.8.16
License:                 GPLv2
SUNW_Copyright:          GPLv2.copyright
Source:                  http://download.sarine.nl/Programs/%srcname/%{version}/%srcname-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:		 SFEgob
#			Solaris 11.2 system vala is too old to build this
BuildRequires:		 SFEvala
BuildRequires:		 %{pnm_buildrequires_library_perl_5_xml_parser}
Requires:		 %{pnm_requires_library_perl_5_xml_parser}
BuildRequires:		 SFElibmpd-devel
#test#BuildRequires:           SFEavahi-devel
Requires:		SFElibmpd
Requires:		SUNWzlib

%if %SFEgtkmm
BuildRequires:		SFEgtkmm-devel
Requires:		SFEgtkmm
%else
BuildRequires:		SUNWgtkmm-devel
Requires:		SUNWgtkmm
%endif

#test#Requires:		       SFEavahi
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export LDFLAGS="%_ldflags %{gnu_lib_path} -lX11 -lxnet -lz"
export CFLAGS="%{optflags} -I/usr/gnu/include %{gnu_lib_path}"

export CC=gcc
export CXX=g++
%if %option_with_gnu_iconv
export CFLAGS="${CFLAGS} -lintl"
%endif

CC=$CC CXX=$CXX CFLAGS="$CFLAGS" XGETTEXT=/bin/gxgettext MSGFMT=/bin/gmsgfmt \
./configure --prefix=%{_prefix} \

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automatically place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%if %{build_l10n}
%else
rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%doc README ChangeLog COPYING NEWS AUTHORS TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gmpc
%{_datadir}/gmpc/*
%dir %attr (0755, root, other) %_datadir/gnome
%dir %_datadir/gnome/help
%dir %_datadir/gnome/help/gmpc
%_datadir/gnome/help/gmpc/C
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%_mandir
%defattr(-, root, other)
%dir %_datadir/icons
%_datadir/icons/Humanity
%_datadir/icons/hicolor

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Sat Jan  6 2018 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_library_perl_5_xml_parser}
* Sat Aug 29 2015 - Alex Viskovatoff <herzen@imap.cc>
- update to 11.8.16; remove runtime dependency on vala
* Tue Apr 24 2012 - Thomas Wagner
- merge with workspace changes
- change BuildRequires to %{pnm_buildrequires_developer_vala}
* Mon Aug 19 2011 - Alex Viskovatoff
- Conform to the SFE practice of letting the environment choose the gcc
* Thu Aug 11 2011 - Alex Viskovatoff
- Fix directory attributes
* Tue Aug  2 2011 - Thomas Wagner
- (Build)Requires SUNWperl-xml-parser instead new IPS name
* Wed Jun 27 2011 - Thomas Wagner
- changed to BuildRequires: SFEvala
- %files fix root:other for icons
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue Apr 12 2011 - Alex Viskovatoff
- Add missing build dependencies
* Wed Oct  6 2010 - Alex Viskovatoff
- Bump to version 0.20.0; use gmake
- Fix icon and man packaging
- Add Requires SUNWlibz; add -lz to LDFLAGS
* Sun Dec 27 2009 - Thomas Wagner
- remove SFEcurl|SUNWcurl - no longer used by gmpc
* Mon Dec 22 2008 - Thomas Wagner
- add nice and clean conditional (Build-)Requires: %if %SUNWgtkmm ... %else ... SFEgtkmm(-devel)
- create %{_docdir} in case old pkgbuild does not
* Sat Dec 20 2008 - Thomas Wagner
- adjust download URL
- add nice and clean conditional (Build-)Requires: %if %SUNWcurl ... %else ... SFEcurl(-devel)
- add LDFLAGS for network libs
- reduce files in %doc, add permissions to %{_docdir}
* Thu Jan 03 2008 - Thomas Wagner
- enabled building in parallel
* Sun Dec 02 2007 - Thomas Wagner
- bump to 0.15.5.0, add version_sub (currently at "0")
- remove --disable-sm (Session Manager)
- switch to new location of SFEcurl --with-curl=/usr/gnu
* Wed Nov 28 2007 - Thomas Wagner
- remove (Build-)Requires: SFEavahi(-devel) - needs more love (change to SUNW... bonjour/avahi/zeroconf)
- change removal of "/locale" if !build_l10n to be rm -rf (diry not longer empty)
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
- pause avahi/zeroconf on client side (will be re-enabled later)
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
