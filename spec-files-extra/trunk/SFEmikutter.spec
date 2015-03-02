#
# spec file for package SFEmikutter
#
%include Solaris.inc

%define src_name	mikutter

Name:                   SFEmikutter
IPS_package_name:		communication/twitter/mikutter
Summary:                A moest twitter client
Version:                3.2.2
Source:                 http://mikutter.hachune.net/bin/%{src_name}.%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEruby
BuildRequires: SFEruby-gnome2
Requires: SFEruby
Requires: SFEruby-gnome2
Requires: SFEruby-moneta
Requires: SFEruby-nokogiri

%prep
%setup -q -n %{src_name}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{src_name}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp -r * $RPM_BUILD_ROOT/%{_datadir}/%{src_name}

cat <<'EOF' > "$RPM_BUILD_ROOT/%{_bindir}/mikutter"
#!/bin/sh
ruby /usr/share/mikutter/mikutter.rb $@
EOF

cat <<'EOF' > "$RPM_BUILD_ROOT/%{_datadir}/applications/%{src_name}.desktop"
[Desktop Entry]
Name=mikutter
Name[ja]=mikutter
Comment=Twitter Client
Comment[ja]=Twitterクライアント
Exec=mikutter
Icon=/usr/share/mikutter/core/skin/data/icon.png
Terminal=false
Type=Application
Categories=Network;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %{_bindir}
%attr (0755, root, bin) %{_bindir}/mikutter
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, sys) %{_datadir}/%{src_name}
%{_datadir}/%{src_name}/*

%changelog
* Thu Feb 26 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- BUmp to 3.2.2
* Mon Oct 13 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Bump to 3.0.6
* Thu Jul 17 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Bump to 3.0.3
* Tue Apr 29 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial version 0.2.2.1537
