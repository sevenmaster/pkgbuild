#
# spec file for package SFEfreeciv.spec
#
# includes module(s): freeciv
#
# bugdb: http://bugs.freeciv.org/Ticket/Display.html?id=
#
%include Solaris.inc

Name:		SFEfreeciv
IPS_Package_Name:	games/freeciv
Summary:	freeciv - a multiplayer strategy game
URL:		http://freeciv.wikia.com/
Version:	2.4.0
Group:		Amusements/Games
Source:		%{sf_download}/freeciv/freeciv-%{version}.tar.bz2
# date:2008-12-23 type:bug owner:halton bugid:40661
Patch4:		freeciv-04-nothing.diff
Patch5:		freeciv-05-return.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
Requires:	SFEsdl-mixer
Requires:	SFEggz-gtk
BuildRequires:	SFEsdl-mixer-devel
BuildRequires:	SFEggz-gtk-devel
BuildRequires:	SUNWgnome-common-devel

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc
Requires: SUNWpostrun-root

%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
Requires:       %{name}

%prep
%setup -q -n freeciv-%version
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/freeciv
%{_libdir}/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/ggz.modules
%{_sysconfdir}/freeciv

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Mon Oct 28 2013 - Milan Jurik
- bump to 2.4.0
* Sat Oct 22 2011 - Milan Jurik
- bump to 2.3.0
* Wed Mar 30 2011 - Milan Jurik
- bump to 2.2.5
* Wed Jan 05 2010 - Milan Jurik
- bump to 2.2.4
* Thu Sep 23 2010 - Milan Jurik
- bump to 2.2.3
* Thu Jan 15 2009 - halton.huo@sun.com
- Bump to 2.1.8
- Remove unused patch signedchar.diff
- Add pkg -root
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Apr 21 2006 - dougs@truemail.co.th
- Added SFEsdl-mixer and enabled sound
- A slight tidy up of spec file
* Sun Apr 21 2006 - dougs@truemail.co.th
- Bumped to 2.1.0-beta4
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
