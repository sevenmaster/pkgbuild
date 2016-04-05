#
# spec file for package terminator
#
# Copyright (c) 2010, 2013, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# %define owner kevmca
#

%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#%define OSR 9644:0.9

Name:           SFEterminator
IPS_package_name: sfe/terminal/terminator
Meta(info.classification): %{classification_prefix}:Applications/System Utilities
License:        GPLv2
Version:        0.98
Summary:        Multiple GNOME terminals in one window
Source:         http://launchpad.net/terminator/trunk/%{version}/+download/terminator-%{version}.tar.gz
# date:2009-02-19 owner:mattman type:branding
Patch1:         terminator-01-manpages.diff
URL:            http://www.tenshu.net/terminator/
SUNW_Basedir:   %{_basedir}
SUNW_Copyright: %{license}.copyright
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
##%include desktop-incorporation.inc
##TODO## re-visit (Build)Requires and make sure to catch the right ones
BuildRequires: %{pnm_buildrequires_python_default}
Requires: %{pnm_requires_python_default}
##TODO## on python_default update, might need better fix for marjorminor number in pkg name
BuildRequires: %{pnm_buildrequires_library_python_setuptools_26}
BuildRequires: %{pnm_buildrequires_SUNWgnome_python26_libs_devel}
Requires: %{pnm_buildrequires_service_gnome_desktop_cache}
Requires: %{pnm_requires_library_gnome_gnome_libs}

%description
This is a project to produce an efficient way of filling a
large area of screen space with terminals. This is done by
splitting the window into a resizeable grid of terminals. As
such, you can  produce a very flexible arrangements of terminals
for different tasks.

%package l10n
Summary: %{summary} - l10n files

%prep
%setup -q -c -n terminator-%{version}
cd terminator-%{version}
%patch1 -p1
rm po/ru_RU.po

perl -pi -e 's:^#! *.*/python.*:#!/usr/bin/python%{python_major_minor_version}:'  `ggrep -r -l "^#\!.*/bin/python"`


%build
export PYTHON="/usr/bin/python%{python_version}"
cd terminator-%{version}
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd terminator-%{version}
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#%restart_fmri icon-cache desktop-mime-cache

#%postun
#%restart_fmri icon-cache desktop-mime-cache

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, other) %{_datadir}/icons
%attr(-, root, other) %{_datadir}/icons/*
#https://people.freedesktop.org/~hughsient/appdata/ display info on program in software shops
%dir %attr(0755, root, other) %{_datadir}/appdata
%{_datadir}/appdata/*
%dir %attr(0755, root, other) %{_docdir}
%{_docdir}/terminator/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*


%files l10n
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%attr(-, root, other) %{_datadir}/locale/*

%changelog
* Tue Apr  5 2016 - Thomas Wagner
- import from solaris-desktop repository (removal pending)
- bump to 0.98
- change (Build)Requires to pnm_macro, include packagenamemacros.inc
- remove patch1, replace patch2 with perl regex
- change IPS name to sfe/terminal/terminator to escape incorporation dictatorship
* Thu Jul 11 2013 - wasif.khan@oracle.com
- Added TPNO and modified copyright
* Fri Feb 10 2012 - padraig.obriain@oracle.com
- Update Requires and BuildRequires to be IPS package names.
* Wed Oct 27 2010 - brian.cameron@oracle.com
- Bump to 0.95.
* Tue May 25 2010 - brian.cameron@oracle.com
- Bump to 0.93.
* Tue May 04 2010 - harry.fu@sun.com
- Bypass ru_RU translations at the moment.
* Thu Apr 15 2010 - brian.cameron@sun.com
- Bump to 0.92.
* Wed Jan 27 2010 - brian.cameron@sun.com
- Bump to 0.14.
* Mon Dec 07 2009 - yuntong.jin@sun.com
- use python2.6 in script explicitly.
* Mon Nov 09 2009 - ke.wang@sun.com
- Change dependency from SUNWPython to SUNWPython26.
* Fri Oct 02 2009 - brian.cameron@sun.com
- Now build with Python 2.6.  Terminator no longer works with Python 2.4.
  See CR #6885253.
* Wed Aug 12 2009 - christian.kelly@sun.com
- Bump to 0.13.
- Remove terminator-02-interpreters.diff, upstream.
* Fri May 29 2009 - kevin.mcareavey@sun.com
- Add patch to fix python path.
* Wed Apr 22 2009 - kevin.mcareavey@sun.com
- Bump to 0.12.
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun.
* Thu Feb 19 2009 - matt.keenan@sun.com
- Add manpages patch for Attributes and ARC case comments.
* Thu Sep 11 2008 - kevin.mcareavey@sun.com
- Add %doc to %files for copyright.
* Fri Aug 8 2008 - kevin.mcareavey@sun.com
- Updated Summary and %description.
* Tue Aug 5 2008 - kevin.mcareavey@sun.com
- Initial version.

#old changelog from previous SFE version
%changelog
* Wed Aug 06 2008 - (andras.barna@gmail.com)
- version bump
* Tue Jul 01 2008 - (andras.barna@gmail.com)
- Permission fixes
* Fri Jun 27 2008 - (andras.barna@gmail.com)
- Initial spec


