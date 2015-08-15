#
# spec file for package SFEmeld
#
# includes module(s): meld
#
%include Solaris.inc
%include usr-gnu.inc

Name:                    SFEmeld-gnu
IPS_Package_Name:	developer/gnu/meld
Summary:                 Meld Diff and Merge Tool (/usr/gnu)
Version:                 1.8.6
%define major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:                  http://ftp.gnome.org/pub/GNOME/sources/meld/%{major_minor_version}/meld-%{version}.tar.xz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWbison
BuildRequires: SUNWPython
Requires: SUNWgnome-libs
%if %SXCE
BuildRequires: SUNWgnome-python-libs-devel
Requires: SUNWgnome-python-libs
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
#don't unpack please
%setup -q -c -T -n meld-%version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)
for po in po/*.po; do
  dos2unix -ascii $po $po
done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export PYTHON="/usr/bin/python"
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

make prefix=%{_prefix} -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make prefix=%{_prefix} install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

# Delete unneeded scrollkeeper files.
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

# Delete info file with no direct use: meld.appdata.xml
rm -rf $RPM_BUILD_ROOT%{_datadir}/appdata/

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update' 
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun 
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0 
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update' 
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/omf/meld/meld-C.omf
#%dir %attr (0755, root, other) %{_datadir}/application-registry
#%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/meld
%{_datadir}/meld/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
#%{_datadir}/pixmaps/*
%dir %attr (0755, root, root) %{_datadir}/mime
%{_datadir}/mime/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
#%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
#%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
#%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrast/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrast/scalable/apps/
%{_datadir}/icons/HighContrast/scalable/apps/*

       # /usr/gnu/share/appdata
       # /usr/gnu/share/appdata/meld.appdata.xml


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Aug  3 2014 - Thomas Wagner
- Bump to 1.8.6
- relocate with %include usr-gnu.inc
- rename to SFEmeld-gnu / add IPS_Package_Name developer/gnu/meld
* Sun Oct 2 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.5.2
* Thu Jun 14 2007 - damien.carbery@sun.com
- Bump to 1.1.5.1.
* Tue Nov 28 2006 - glynn.foster@sun.com
- Initial version
