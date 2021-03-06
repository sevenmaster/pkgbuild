#
# spec file for package SFElibgsm
#
# includes module(s): libgsm
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libgsm_64 = libgsm.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%use libgsm_sse2 = libgsm.spec
%endif

%include base.inc
%use libgsm = libgsm.spec

Name:		SFElibgsm
IPS_Package_Name:	library/audio/libgsm
Summary:	%{libgsm.summary}
Version:	%{libgsm.version}
License:	%{libgsm.license}
SUNW_Copyright:	libgsm.copyright
URL:		https://launchpad.net/libgsm
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This is a free and public implementation of GSM audio encoding and
decoding. The gsm library is used in many free software projects
including 'rplay', but has never been packaged as a stand-alone shared
library. GSM encoding has specific uses in transmission of packetized
audio over the Internet.

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
%libgsm_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%libgsm_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%{base_arch}
%libgsm.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%libgsm_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%libgsm_sse2.build -d %name-%version/%sse2_arch
%endif

%libgsm.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libgsm_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%libgsm_sse2.install -d %name-%version/%sse2_arch
%endif

%libgsm.install -d %name-%version/%{base_arch}

%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/toast  $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
mv $RPM_BUILD_ROOT%{_bindir}/tcat  $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
mv $RPM_BUILD_ROOT%{_bindir}/untoast  $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec toast
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec tcat
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec untoast
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%if %can_isaexec
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}
%endif
%{_bindir}/%{base_isa}
%hard %{_bindir}/toast
%hard %{_bindir}/tcat
%hard %{_bindir}/untoast
%else
%{_bindir}
%endif
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%if %arch_sse2
%{_libdir}/%{sse2_arch}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man3

%changelog
* Mon Dec 12 2016 - Thomas Wagner
- LDFLAGS -m64 is moved out into include/arch64.inc
* Thu Aug 13 2015 - Thomas Wagner
- remove PICFLAG="-KPIC" for gcc, needs testing with studio compiler (OIH)
* Sun Oct 23 2011 - Milan Jurik
- fix multiarch
* Mon Oct 10 2011 - Milan Jurik
- add IPS package name
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Nov 28 2010 - Milan Jurik
- add pentium_pro+mmx lib
* Tue Sep 08 2009 - Milan Jurik
- update to 1.0.13
- multiarch support
* Tue Dec 02 2008 - Giles Dauphin
- Fix to mandir ownership by Giles Dauphin (again sorry)
* Fri May 23 2008 - michal.bielicki@voiceworks.pl
- Fix to mandir ownership by Giles Dauphin
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Changed a failing install -d to mkdir -p
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
