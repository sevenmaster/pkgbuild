#
# spec file for package SFElibfm
#
# includes module(s): libfm
#
# https://sourceforge.net/tracker/index.php?func=detail&aid=$bugid&group_id=156956&atid=801864
#
%include Solaris.inc

Name:		SFElibfm
IPS_Package_Name:	library/lxde/libfm
Summary:	LXDE lightweight file manager library
License:	GPLv2+
SUNW_Copyright:	libfm.copyright
Version:	0.1.17
Source:		%{sf_download}/pcmanfm/libfm-%{version}.tar.gz
Patch1:		libfm-01-studio.diff
URL:		http://sourceforge.net/projects/pcmanfm/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk-doc
Requires: SFEmenu-cache
BuildRequires: SFEmenu-cache
BuildRequires:	SUNWgtk-doc

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n libfm-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

export GMSGFMT=/usr/bin/gmsgfmt
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir}	\
	--enable-gtk-doc
	
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gio
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/libfm/*
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/*
%{_datadir}/mime/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/libfm
%{_sysconfdir}/xdg/libfm/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Feb 05 2012 - Milan Jurik
- bump to 0.1.17
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Wed Jun 08 2011 - brian.cameron@oracle.com
- Bump to 0.1.15.
* Thu Sep 16 2010 - brian.cameron@oracle.com
- Add patch libfm-03-fixcompile.diff so that it builds with older compilers. 
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump.
* Mon May 25 2009 - alfred.peng@sun.com
- Update source URL and set correct GMSGFMT.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version
