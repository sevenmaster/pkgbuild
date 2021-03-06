#
# Initial thunar-vcs-plugin spec for Solaris 11 by Ken Mays
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1

Name:			SFEthunar-vcs-plugin
Summary:		Thunar Version Control System (SVN/GIT) plugin for Xfce
Version:		0.1.4
URL:			http://goodies.xfce.org/projects/thunar-plugins/thunar-vcs-plugin
Source0:		http://archive.xfce.org/src/thunar-plugins/thunar-vcs-plugin/0.1/thunar-vcs-plugin-%{version}.tar.bz2
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/thunar-vcs-plugin-%{version}
BuildRequires:		SUNWgnome-component-devel
Requires:		SUNWgnome-component
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		SUNWgnome-panel-devel
Requires:		SUNWgnome-panel
BuildRequires:		SFElibxfcegui4-devel
Requires:		SFElibxfcegui4
BuildRequires:		SFElibxfce4util-devel
Requires:		SFElibxfce4util
BuildRequires:		SFExfce4-panel-devel
Requires:		SFExfce4-panel
Requires:		SUNWpostrun
BuildRequires:		SUNWsvn
Requires:		SUNWsvn
BuildRequires:		SUNWgit
Requires:		SUNWgit

%prep
%setup -q -n thunar-vcs-plugin-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags -lkstat"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-locales-dir=%{_datadir}/locale \
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
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%{_libdir}
%{_datadir}

%changelog
* Wed Oct 5 2011 - Ken Mays <kmays2000@gmail.com>
- Initial version (0.1.4)
