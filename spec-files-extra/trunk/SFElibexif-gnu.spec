# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libexif_64 = libexif.spec
%endif

%include base.inc
%use libexif = libexif.spec

Name:		SFElibexif
IPS_Package_Name:	library/libexif
Summary:      EXIF Tag Parsing Library (/usr/gnu)
Group:		Development/Libraries
Version:      %{libexif.version}
URL:            http://libexif.sourceforge.net/
License:	LGPL2.1
##TODO##
#SUNW_Copyright:	libexif.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#BuildRequires: SFEgcc
#Requires: SFEgccruntime

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
Requires: %name

%description
reads and writes EXIF metainformation from and to image files

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%libexif_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%libexif.prep -d %name-%version/%base_arch


%build
%ifarch amd64 sparcv9
%libexif_64.build -d %name-%version/%_arch64
%endif

%libexif.build -d %name-%version/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libexif_64.install -d %name-%version/%_arch64
%endif

%libexif.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%if %{_share_locale_group_changed}
%dir %attr (0755, root, %{_share_locale_group}) %{_datadir}/locale
%defattr (-, root, %{_share_locale_group})
%else
%dir %attr (0755, root, other) %{_datadir}/locale
%defattr (-, root, other)
%endif
%{_datadir}/locale/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Mon May 27 2013 - Thomas Wagner
- initial spec version 0.6.21
