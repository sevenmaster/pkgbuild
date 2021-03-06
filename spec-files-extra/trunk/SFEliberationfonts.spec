# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include packagenamemacros.inc

Name:                SFEliberationfonts
License:             GPL+exception
Summary:             OpenSource TrueType fonts from RedHat
Version:             0.2
URL:                 https://www.redhat.com/promo/fonts/
#Source:              http://www.redhat.com/f/fonts/liberation-fonts-ttf-3.tar.gz
Source:              http://www.redhat.com/f/fonts/liberation-fonts.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:  %{pnm_buildrequires_SUNWTk_devel}
Requires:       %{pnm_requires_SUNWTk}


%prep
%setup -q -n liberation-fonts-%version

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/openwin/lib/X11/fonts/TrueType
cp * ${RPM_BUILD_ROOT}%{_prefix}/openwin/lib/X11/fonts/TrueType

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/fc-cache

%postun
/usr/bin/fc-cache

%files
%defattr (-, root, bin)
%{_prefix}/*

%changelog
* Tue Mar 22 2016 - Thomas Wagner
- change (Build)Requires to  %{pnm_buildrequires_SUNWTk_devel}
* Mon Apr 14 2008 - shivakumar.gn@gmail.com
- The source location of the tarball has changed
* Sun Feb 03 2008 - moinak.ghosh@sun.com
- Initial spec.
