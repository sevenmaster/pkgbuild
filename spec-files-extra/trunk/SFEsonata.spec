#
# spec file for package: sonata
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc
%include packagenamemacros.inc

%define python_version 2.6

Name:		SFEsonata
IPS_package_name: audio/mpd/sonata
Version:	1.6.2.1
Summary:	An elegant music client for MPD
Group:		Applications/Sound and Video
License:	GPLv3
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://sonata.berlios.de/
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: sonata.copyright

Source0:	http://download.berlios.de/sonata/sonata-%{version}.tar.bz2
Patch0:		sonata-01-xfade.diff

%include default-depend.inc
BuildRequires:	%{pnm_buildrequires_SUNWgnu_gettext_devel}
BuildRequires:	%{pnm_buildrequires_SUNWgnome_common_devel}
BuildRequires:	SUNWxwinc
BuildRequires:	%{pnm_buildrequires_python_default}
#BuildRequires:  SUNWgnome-python26-libs
#BuildRequires:  SUNWgnome-python26-extras
#BuildRequires:  SUNWdbus-python26
BuildRequires:	SFEpython26-mpd
Requires:	%{pnm_requires_python_default}
#Requires:	SUNWgnome-python26-libs
#Requires:	SUNWgnome-python26-extras
#Requires:	SUNWdbus-python26
Requires:	SFEpython26-mpd

Meta(info.maintainer):          James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):            Scott Horowitz <stonecrest@gmail.com>
Meta(info.upstream_url):        http://sonata.berlios.de/
Meta(info.classification):	org.opensolaris.category.2008:Applications/Sound and Video

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%description
An elegant GTK+ client for the Music Player Daemon (MPD).

%prep
%setup -q -n sonata-%version
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
CFLAGS="-Immkeys" python%{python_version} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
if [ -d $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages ] ; then
	mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
	mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
		$RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
	rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
fi

mkdir $RPM_BUILD_ROOT%{_docdir}
mv $RPM_BUILD_ROOT%{_datadir}/sonata $RPM_BUILD_ROOT%{_docdir}

# el_GR breaks installation on Solaris 11
rm -rf $RPM_BUILD_ROOT/%_datadir/locale/el_GR

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}/sonata
%{_libdir}/python%{python_version}/vendor-packages/sonata
%{_libdir}/python%{python_version}/vendor-packages/Sonata-%{version}-py%{python_version}.egg-info
%{_libdir}/python%{python_version}/vendor-packages/mmkeys.so
%attr(0755,root,sys) %dir %{_datadir}
%attr(0755,root,other) %dir %{_datadir}/applications
%{_datadir}/applications/sonata.desktop
%{_mandir}/man1/sonata.1
%attr(0755,root,other) %dir %{_docdir}
%{_docdir}/sonata
%attr(0755,root,other) %dir %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr(-,root,other) %{_datadir}/locale
%endif


%changelog
* Wed Feb 12 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add sonata-01-xfade.diff (patch for compatibility with mpd >=0.18)
- include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_SUNWgnu_gettext_devel}
- change (Build)Requires to %{pnm_buildrequires_SUNWgnome_common_devel}
- change (Build)Requires to %{pnm_buildrequires_python_default}
- comment out other Python dependencies until packagenamemacros are ready to handle them
* Thu Jun 30 2011 - Alex Viskovatoff
- Package locale files separately
* Tue Dec 01 2009 - jlee@thestaticvoid.com
- Initial version
