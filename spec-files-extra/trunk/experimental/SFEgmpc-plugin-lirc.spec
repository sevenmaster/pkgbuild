%include Solaris.inc
%define pluginname lirc
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - lirc - plugin for gmpc
# Version e.g. 0.15.5.0, note: gmpcplugin.gmpcmainversion is 0.15.5
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgmpc-devel
Requires: SFEgmpc
BuildRequires: *lirc*
Requires: *lirc*

%prep
%gmpcplugin.prep
 
%build
%gmpcplugin.build
 
%install
%gmpcplugin.install

%clean
%gmpcplugin.clean

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/gmpc/plugins/*.so
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gmpc-%{pluginname}/icons/*


%changelog
* Tue Apr 24 2012 - Thomas Wagner
- initial spec
- needs lirc to work, so place it in experimental
