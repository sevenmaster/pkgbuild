#
# spec file for package SFEmcomix
#
# includes module: mcomixa
#

# NOTE: The ruby plugin does not work when compiled against runtime/ruby-18
# from the solaris repository.

# NOTE: It is not clear if spell checking works.  WeeChat is aware of aspell,
# at least.

# Note: Update and use the patch below to use Enchant instead of aspell:
# http://savannah.nongnu.org/patch/?6858

%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEmcomix
IPS_Package_Name:	 image/viewer/mcomix
Summary:	GTK+ comic book viewer
URL:		http://sourceforge.net/p/mcomix/wiki/Home/
Vendor:		oddegamra, oxaric
Version:	1.00
License:	GPLv3+
Source:		http://hivelocity.dl.sourceforge.net/project/mcomix/MComix-%{version}/mcomix-%{version}.zip
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_python_default}
BuildRequires: %{pnm_buildrequires_SUNWpython26_setuptools_devel}
Requires: %{pnm_requires_python_default}
# pygtk2 needs a packagenamemacros entry
# Requires: library/python-2/pygtk2-26
Requires: %{pnm_requires_SUNWpython26_imaging}

%description
MComix is an user-friendly, customizable image viewer. It is specifically designed to handle comic books, but also serves as a generic viewer. It reads images in ZIP, RAR, 7Zip, LHA or tar/gz/bz2 archives as well as plain image files. It is written in Python using GTK+ through the PyGTK bindings, and runs on both Linux and Windows.

MComix is a fork of the Comix project, and aims to add bug fixes and stability improvements after Comix development came to a halt in late 2009.
 
%prep
%setup -q -n mcomix-%{version}

%build

python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_bindir/mcomix
%_libdir/python2.6/site-packages/mcomix-%{version}-py2.6.egg-info
%dir %_libdir/python2.6/site-packages/mcomix
%_libdir/python2.6/site-packages/mcomix/*
%dir %attr (-, root, sys) %_datadir
%_mandir/man1/mcomix.1.gz
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/mcomix.desktop
%dir %attr (-, root, root) %_datadir/mime
%dir %attr (-, root, root) %_datadir/mime/packages
%_datadir/mime/packages/mcomix.xml
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%attr (-, root, other) %_datadir/icons/hicolor/16x16/apps/mcomix.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/mimetypes
%attr (-, root, other) %_datadir/icons/hicolor/16x16/mimetypes/*
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%attr (-, root, other) %_datadir/icons/hicolor/22x22/apps/mcomix.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/mimetypes
%attr (-, root, other) %_datadir/icons/hicolor/22x22/mimetypes/*
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24/apps
%attr (-, root, other) %_datadir/icons/hicolor/24x24/apps/mcomix.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24/mimetypes
%attr (-, root, other) %_datadir/icons/hicolor/24x24/mimetypes/*
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%attr (-, root, other) %_datadir/icons/hicolor/32x32/apps/mcomix.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/mimetypes
%attr (-, root, other) %_datadir/icons/hicolor/32x32/mimetypes/*
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%attr (-, root, other) %_datadir/icons/hicolor/48x48/apps/mcomix.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/mimetypes
%attr (-, root, other) %_datadir/icons/hicolor/48x48/mimetypes/*

%changelog
* Thu May 01 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- %include packagenamemacros.inc
- Change (Build)Requires to %{pnm_buildrequires_*}
* Sat Aug 03 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial package version 1.00
