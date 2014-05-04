#
# spec file for package SFEldns.spec
#
# includes module(s): ldns
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use ldns_64 = ldns.spec
%endif

%include base.inc
%use ldns = ldns.spec

Name:		SFEldns
IPS_Package_Name:	library/ldns
URL:		%{ldns.url}
Summary:	%{ldns.summary}
Version:	%{ldns.version}
Group:		%{ldns.group}
License:	%{ldns.license}
SUNW_Copyright:	ldns.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries

%description
The goal of ldns is to simplify DNS programming, it supports recent RFCs like the DNSSEC documents, and allows developers to easily create software conforming to current RFCs, and experimental software for current Internet Drafts.

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
%ldns_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%ldns.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%ldns_64.build -d %name-%version/%_arch64
%endif

%ldns.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%ldns_64.install -d %name-%version/%_arch64
%endif

%ldns.install -d %name-%version/%{base_arch}

mkdir -p %{buildroot}%{_bindir}/%{base_isa}
mv %{buildroot}%{_bindir}/drill %{buildroot}%{_bindir}/%{base_isa}
cd %{buildroot}%{_bindir} && ln -s ../../usr/lib/isaexec drill

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%if %can_isaexec
%{_bindir}/%{base_isa}/drill
%hard %{_bindir}/drill
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/drill
%endif
%endif
%{_libdir}/libldns.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libldns.so*
%endif


%files devel
%defattr (-, root, bin)
%{_bindir}/ldns-config
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/ldns-config
%endif
%{_includedir}/ldns
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Sun May 04 2014 - Milan Jurik
- bump to 1.6.17, add multiarch support
* Mon Sep 09 2013 - Milan Jurik
- bump to 1.6.16
* Sun Jul 29 2012 - Milan Jurik
- bump to 1.6.13
* Tue May 15 2012 - Milan Jurik
- bump to 1.6.12
* Fri Nov 25 2011 - Milan Jurik
- bump to 1.6.11
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jun 30 2011 - Milan Juril
- bump to 1.6.10
* Fri Mar 25 2011 - Milan Jurik
- bump to 1.6.9
* Mon Jan 24 2011 - Milan Jurik
- bump to 1.6.8
* Mon Nov 08 2010 - Milan Jurik
- bump to 1.6.7
- disable GOST because of old OpenSSL
* Thu Sep 23 2010 - Milan Jurik
- bump to 1.6.6
* Wed Jun 09 2010 - Milan Jurik
- Initial version
