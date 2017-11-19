#
# spec file for package SFEliba52
#
# includes module(s): liba52
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include packagenamemacros.inc

%include arch64.inc
%use liba52_64 = liba52.spec
%endif

%include base.inc
%use liba52 = liba52.spec

Name:                    SFEliba52
IPS_Package_Name:	library/audio/liba52
Summary:                 %{liba52.summary}
Version:                 %{liba52.version}
URL:                     http://liba52.sourceforge.net/
License:                 GPLv2+
SUNW_Copyright:          liba52.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWlibms_devel}
Requires:      %{pnm_requires_SUNWlibms}

BuildRequires: %{pnm_buildrequires_SUNWlibtool_devel}
#Requires: %{pnm_buildrequires_SUNWlibtool}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%liba52_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%liba52.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%liba52_64.build -d %name-%version/%_arch64
%endif

%liba52.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%liba52_64.install -d %name-%version/%_arch64
%endif

%liba52.install -d %name-%version/%{base_arch}

%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
for i in a52dec extract_a52 
do
  mv $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
  ( 
    cd $RPM_BUILD_ROOT%{_bindir}
#    ln -s ../lib/isaexec $i
    cp -p /usr/lib/isaexec $i
  )
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}
%hard %{_bindir}/a52dec
%hard %{_bindir}/extract_a52
%else
%{_bindir}/a52dec
%{_bindir}/extract_a52
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/a52dec
%{_bindir}/%{_arch64}/extract_a52
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sat Jan 14 2017 - Thomas Wagner
- add/change (Build)Requires pnm_buildrequires_SUNWlibtool_devel, pnm_buildrequires_SUNWlibms_devel
* Mon Oct 10 2011 - Milan Jurik
- add IPS package name
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Wed Aug 15 2007 - dougs@truemail.co.th
- converted to build 64bit
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFEliba52
- changed to root:bin to follow other JDS pkgs.
- added dependencies
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
