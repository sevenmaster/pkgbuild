#
# spec file for package SFEnettle-gnu
#
# includes module(s): nettle
#
%include Solaris.inc


##%define cc_is_gcc 1
##%include base.inc

%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use nettle64 = nettle.spec
%endif

%include base.inc


%define	src_name nettle
%use nettle = nettle.spec

Name:                SFEnettle-gnu
IPS_Package_Name:    library/gnu/nettle
Summary:             Nettle is a cryptographic library (/usr/gnu)
Version:             %{nettle.version}
SUNW_BaseDir:        %{_prefix}
%define _infodir %{_datadir}/info
##TODO##License:	LGPL
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%nettle64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%nettle.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%nettle64.build -d %name-%version/%_arch64
%endif

%nettle.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%nettle64.install -d %name-%version/%_arch64
%endif

%nettle.install -d %name-%version/%{base_arch}

##TODO## one osdistro has /usr/gnu/share/info/nettle.info the other doesn't. Get rid of the file for now.
#move $RPM_BUILD_ROOT/usr/share/info to in /usr/gnu/share/info
#[ -d $RPM_BUILD_ROOT/usr/share ] && mv $RPM_BUILD_ROOT/usr/share $RPM_BUILD_ROOT/%{_datadir}
#avoid %files stumbling over inexistent directory
#[ -d $RPM_BUILD_ROOT/%{_datadir} ] || mkdir -p  $RPM_BUILD_ROOT/%{_datadir}
#[ -d  ${RPM_BUILD_ROOT}%{_datadir}/info ] && rm -r ${RPM_BUILD_ROOT}%{_datadir}/info
[ -d  ${RPM_BUILD_ROOT}%{_std_datadir} ] && rm -r ${RPM_BUILD_ROOT}%{_std_datadir}

find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \; || true

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif


%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/aclocal
#%{_datadir}/aclocal/*


%changelog
* Fri Aug  9 2019 - Thomas Wagner
- remove mini-gmp (collides with gmp)
* Thu Aug  8 2019 - Thomas Wagner
- bump to 3.5.1, patches from OI and pkgsrv
* Fri Jul 26 2019 - Thomas Wagner
- bump to 3.4.1
- for gnutls --enable-public-key
* Thu Jul 24 2019 - Thomas Wagner
- bump to 3.5.1
* Sat Okt 10 2015 - Thomas Wagner
- bump to 3.1.1 for new gnutls 3.4.4
* Tue Aug  4 2015 - Thomas Wagner
- fix %files and remove share/info 
* Mon Jun 15 2015 - Thomas Wagner
- downgrade to 2.7.1 (to suit gnutls)
- fix _arch64 build
- fix %files, remove file info/dir
* Thu Jun 11 2015 - Thomas Wagner
- initial spec
- make it 32/64-bit
