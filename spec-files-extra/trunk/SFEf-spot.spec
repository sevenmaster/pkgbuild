#
# spec file for package SFEf-spot
#
# includes module(s): f-spot
#
%include Solaris.inc

Name:         SFEf-spot
Version:      0.3.5
Summary:      f-spot - personal photo management application for the GNOME Desktop
Source:       http://ftp.gnome.org/pub/GNOME/sources/f-spot/0.3/f-spot-%{version}.tar.bz2
URL:          http://f-spot.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEmono-devel
BuildRequires: SFElcms-devel
BuildRequires: SFEgtk-sharp
BuildRequires: SFEsqlite
BuildRequires: SFEsqlite-devel
Requires: SUNWgnome-base-libs
Requires: SFEmono
Requires: SFElcms
Requires: SFEgtk-sharp
Requires: SFEsqlite
Requires: SFEdbus-sharp

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd f-spot-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

cd f-spot-%{version}

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --without-gnome-screensaver \
            --disable-scrollkeeper \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd f-spot-%{version}
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/f-spot/lib*a

perl -pi -e 's/^exec (.*) mono /exec $1 \/usr\/mono\/bin\/mono /' \
    $RPM_BUILD_ROOT%{_bindir}/f-spot
perl -pi -e 's/^#!\/bin\/sh/#!\/bin\/bash/' $RPM_BUILD_ROOT%{_bindir}/f-spot

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/f-spot/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/f-spot/f-spot-[a-z]*.omf
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/f-spot
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/f-spot/C
%{_datadir}/omf/f-spot/f-spot-C.omf

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/f-spot/[a-z]*
%{_datadir}/omf/f-spot/f-spot-[a-z]*.omf
%endif

%changelog
* Sat Mar 17 2007 - laca@sun.com
- update %files for 0.3.5
* Mon Mar 05 2007 - daymobrew@users.sourceforge.net
- Bump to 0.3.5.
* Wed Oct 25 2006 - markgraf@neuro2.med.uni-magdeburg.de
- fixed dependencies
* Sun Oct 15 2006 - laca@sun.com
- add pkgconfig .pc file to %files
* Sat Oct 14 2006 - laca@sun.com
- bump to 0.2.2; delete upstream patch solaris.diff
* Wed Oct 11 2006 - laca@sun.com
- add lcms dependency
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 0.2.0
* Mon Jul 24 2006 - laca@sun.com
- create!
