#
# spec file for package SFEpoppler-data-gpp
#
# includes module(s): poppler-data
#
#

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc

%use poppler_data = poppler-data.spec

Name:                    SFEpoppler-data-gpp
IPS_Package_Name:	 library/g++/poppler-data
Summary:                 poppler-data - supports poppler, the PDF rendering library (/usr/g++)
URL:                     http://poppler.freedesktop.org
License:                 GPLv2
##TODO## and adobe and MIT license, see files: COPYING COPYING.adobe COPYING.gpl2
SUNW_Copyright:          poppler.copyright
Version:                 %{poppler_data.version}
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc


%description
poppler-data is used by poppler, the PDF rendering library based on xpdf-3.0

%prep
rm -rf %name-%version
mkdir %name-%version
%poppler_data.prep -d %name-%version

%build

%poppler_data.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%poppler_data.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc poppler-data-%version/COPYING poppler-data-%version/COPYING.adobe poppler-data-%version/COPYING.gpl2
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/poppler/*
%{_datadir}/pkgconfig/*


%changelog
* Thu Nov  5 2015 - Thomas Wagner
- initial spec
