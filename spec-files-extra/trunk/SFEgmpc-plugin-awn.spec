%include Solaris.inc
%define pluginname awn
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
IPS_package_name:	audio/mpd/gmpc/%{pluginname}
Summary:                gmpc-%{pluginname} - awn - plugin for gmpc which integrates with avant window manager
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SUNWgcc
Requires: SUNWgccruntime

BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%description
http://gmpc.wikia.com/wiki/GMPC_PLUGIN_AWN
Shows track progress and album art in the task icon of GMPC on the dock. 

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
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/gmpc-%{pluginname}/icons/*


%changelog
* Fri Apr  4 2014 - Thomas Wagner
- add IPS_Package_Name
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- initial spec version to 0.20.0
