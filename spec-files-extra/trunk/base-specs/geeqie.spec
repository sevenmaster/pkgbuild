#
# spec file for package geeqie 
#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#Owner: jouby
#

Summary: Graphics file browser utility.
Name: geeqie 
Version: 1.1 
Release: 0
License: GPL
Group: Applications/Multimedia
Source:  http://surfnet.dl.sourceforge.net/sourceforge/geeqie/geeqie-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

URL: http://geeqie.sourceforge.net

Requires: gtk2 >= 2.4.0

%description
Geeqie is a browser for graphics files.Forked from Gqview project.
Offering single click viewing of your graphics files.
Includes thumbnail view, zoom and filtering features.
And external editor support.

%prep
%setup -q -n geeqie-%version
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} --datadir=%{_datadir} 
make -j$CPUS 

cd doc
make html
cd ..
mkdir html
#cp doc/html/*.html doc/*.txt html/.
cp doc/html/*.html html/

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)


%changelog
* Sun Nov 18 2012 - Thomas Wagner
- fix %install for html doc
- remove owner
- add BuildRequires: SUNWdoxygen
- add IPS_Package_Name, add Group
- bump to 1.1
* Mon Aug 24 2009 - yuntong.jin@sun.com
- Initial build.
