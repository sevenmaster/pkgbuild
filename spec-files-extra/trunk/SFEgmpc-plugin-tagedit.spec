%include Solaris.inc
%define pluginname tagedit
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
IPS_package_name:	audio/mpd/gmpc/%{pluginname}
Summary:                gmpc-%{pluginname} - Editor for songtags
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgcc
Requires: SFEgccruntime

BuildRequires: SFEgmpc-devel
Requires: SFEgmpc
BuildRequires: SFEtaglib-devel
Requires: SFEtaglib
#probably only build-time requirement, but older pkgtool probably can't enforce that
BuildRequires: SFEgob
Requires: SFEgob

%description
http://gmpc.wikia.com/wiki/GMPC_PLUGIN_TAGEDIT
The tagedit plugin for GMPC adds a editor panel for editing song tags. With the plugin enabled, you are able to queue one or more songs to the Tag editor from the playlist or song browser. You may then enter the Tag editor panel and modify the tags of the queued songs one by one or by groups. The changes are recorded when you hit the Save button. If you made a mistake while editing tags, you may discard the changes you made to one song or a group of songs. 

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


%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
#%dir %attr (0755, root, other) %{_datadir}/gmpc
#%dir %attr (0755, root, other) %{_datadir}/gmpc/plugins
#%{_datadir}/gmpc/plugins/*

%changelog
* Fri Apr  4 2014 - Thomas Wagner
- add IPS_Package_Name
* Fri Jun  1 2012 - Thomas Wagner
- change to (Build)Requires: SFEgob (SFEgob2 is messed up)
* Tue May 15 2012 - Thomas Wagner
- add missing (Build)Requires: SFEgob2
* Wed Apr 25 2012 - Thomas Wagner
- fix %files
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- initial spec version to 0.20.0
