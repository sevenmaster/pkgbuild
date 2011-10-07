#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc


Name:			SFExfce4-mpc-plugin
Summary:		Plugin for controling mpd deamon from the Xfce panel
Version:		0.3.6
URL:			http://www.xfce.org/
Source0:		http://archive.xfce.org/src/panel-plugins/xfce4-mpc-plugin/0.3/xfce4-mpc-plugin-%{version}.tar.bz2		
#Patch1:			xfce4-mpc-plugin-01-libnsl.diff
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/mpc-plugin-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
Requires:		SUNWpcre
BuildRequires:		SFElibxfcegui4-devel
Requires:		SFElibxfcegui4
BuildRequires:		SFExfce4-panel-devel
Requires:		SFExfce4-panel
Requires:		SUNWpostrun
%prep
%setup -q -n xfce4-mpc-plugin-%{version}
#%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -lsocket -lnsl"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-gtk-doc \
            --disable-static
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/xfce4
%{_datadir}/xfce4*
%defattr(0755,root,other)
%{_datadir}/locale*

%changelog
* Fri Oct 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.3.6
* Mon Apr 11 2007 - sobotkap@students.zcu.cz
- Initial Version
