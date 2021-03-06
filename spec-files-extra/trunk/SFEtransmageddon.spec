#
# spec file for package SFEtransmageddon
#
# includes module(s): transmageddon
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEtransmageddon
IPS_Package_Name:	gnome/media/transmageddon
Summary:	Video transcoder using GStreamer
Group:		Applications/Sound and Video
License:	LGPLv2.1+
Version:	0.20
URL:		http://www.linuxrising.org/
Source:		http://www.linuxrising.org/files/transmageddon-%{version}.tar.bz2
SUNW_Copyright: transmageddon.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:	%{pnm_requires_python_default}
##TODO## re-visit dependencies (runtime)
BuildRequires:	%{pnm_buildrequires_SUNWgnome_common_devel}
BuildRequires:	%{pnm_buildrequires_perl_xml_parser}
%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n transmageddon-%{version}

%build
./configure --prefix=%{_prefix}

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{buildroot}%{_datadir}/locale
%endif

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/transmageddon.desktop
%dir %attr (-, root, other) %{_datadir}/gstreamer-0.10
%{_datadir}/gstreamer-0.10/*
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/transmageddon.svg
%{_datadir}/transmageddon

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Oct 23 2015 - Thomas Wagner
- merge with pjama's changes
* Sat May 22 2015 - pjama
- pnm changes
- ## TODO ## update from 0.20 to 0.25
-	Changes presets
* Fri Sep  2 2011 - Thomas Wagner
- make BuildRequires SUNWperl-xml-parser
- make Requires: %{pnm_buildrequires_python_default}
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Wed Jun 15 2011 - Alex Viskovatoff
- update download link
* Sun Feb 06 2011 - Milan Jurik
- initial spec
