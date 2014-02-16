# 
# 
# 
%include Solaris.inc
%include base.inc
%include packagenamemacros.inc

Name:                SFEttytter
IPS_Package_Name:	communication/twitter/ttytter
License:             FFSL
Summary:             A multi-functional, command-line twitter client
Version:             2.1.0
Source:				 http://www.floodgap.com/software/ttytter/dist2/%{version}0.txt
URL:                 http://www.floodgap.com/software/ttytter/
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{license}.copyright
Group:		     Applications/Internet
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		 %{pnm_buildrequires_perl_default}
Requires:			 %{pnm_requires_perl_default}

%description
A multi-functional, command-line twitter client

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
install -c -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/ttytter

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Feb 16 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec version 2.1.0
