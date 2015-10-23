#
# spec file for package SFEgiflib
#
# includes module(s): giflib
#
%include Solaris.inc
%include packagenamemacros.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use giflib64 = giflib.spec
%endif

%include base.inc
%use giflib = giflib.spec

Name:		SFEgiflib
IPS_Package_Name:	image/library/giflib 
Summary:	%{giflib.summary}
Version:	%{giflib.version}
License:	MIT
SUNW_Copyright:	giflib.copyright
URL:		http://giflib.sourceforge.net/
Group:		System/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %{oihipster}
# internal pkg generator pkgdepend broken becuase it finds two versions of perl on OIHipster then gets syntax wrong and barfs ie
#pkgbuild:   dependency discovered: depend fmri=pkg:/runtime/perl-510@5.10.0-2014.0.1.0 fmri=pkg:/runtime/perl-516@5.16.3-2014.0.1.1 type=require-any
# Define requirements manually
%define _use_internal_dependency_generator 0
Requires:        x11/library/libice
Requires:        x11/library/libsm
Requires:        x11/library/libx11
Requires:        %{pnm_buildrequires_perl_default}
%endif

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%giflib64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%giflib.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%giflib64.build -d %name-%version/%_arch64
%endif

%giflib.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%giflib64.install -d %name-%version/%_arch64
%endif

%giflib.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gif*
%{_bindir}/*gif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/gif*
%{_bindir}/%{_arch64}/*gif
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri May 22 2015 - pjama
- work around pkgdepend/hipster combo bug when including dependancy packages
* Sun Oct 16 2011 - Milan Jurik
- add IPS package name
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Mon May 17 2010 - Milan Jurik
- bump to 4.1.6
* Thu Sep  6 2007 - dougs@truemail.co.th
- Initial version
