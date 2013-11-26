#
# spec file for package SFElibid3tag-gnu
#
# includes module(s): libid3tag
#

%include Solaris.inc
%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libid3tag_64 = libid3tag.spec
%endif

%include base.inc
%use libid3tag = libid3tag.spec

Name:		SFElibid3tag-gnu
IPS_Package_Name:	library/audio/g++/libid3tag
Summary:	%{libid3tag.summary} (/usr/gnu)
Group:		System/Multimedia Libraries
Version:	%{libid3tag.version}
License:	GPLv2
SUNW_Copyright:	libid3tag.copyright
URL:		http://www.underbit.com/products/mad/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWzlib

%description
ID3 tag manipulation library a wide range of multimedia formats


%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

##TODO## check this: Requires: SUNWgnome-libs

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libid3tag_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libid3tag.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libid3tag_64.build -d %name-%version/%_arch64
%endif

%libid3tag.build -d %name-%version/%{base_arch}


%install
##TODO## check this export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%ifarch amd64 sparcv9
%libid3tag_64.install -d %name-%version/%_arch64
%endif

%libid3tag.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/id3tag.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/id3tag.pc
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Mar 27 2013 - Thomas Wagner
- again merge from SFElibid3tag.spec (adds 32/64-bit)
- location /usr/gnu
* Sat Jul 14 2007 - dougs@truemail.co.th
- Converted from SFElibid3tag
