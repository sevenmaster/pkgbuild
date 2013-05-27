
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEexif
Summary:             exif tool
License:             ##TODO##
##TODO## SUNW_Copyright:	     exif.copyright
Version:             0.6.21
Source:       %{sf_download}/libexif/exif-%{version}.tar.bz2
URL:            http://libexif.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFElibexif-gnu-devel
Requires:	SFElibexif-gnu


%prep
%setup -q -n exif-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} %{gnu_lib_path}"
export LDFLAGS="%_ldflags %gnu_lib_path"

export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/exif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*

#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/doc
#%{_datadir}/doc/*

%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Mon May 27 2013 - Thomas Wagner
- initial spec version 
