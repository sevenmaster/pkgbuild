%include Solaris.inc
%define pluginname magnatune
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - browse and preview albums from www.magnatune.com and fetch cover art - plugin for gmpc
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgcc
Requires: SFEgccruntime

BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%description
http://gmpc.wikia.com/wiki/Magnatune

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
%dir %attr (0755, root, other) %{_datadir}/gmpc
%dir %attr (0755, root, other) %{_datadir}/gmpc/plugins
%{_datadir}/gmpc/plugins/*

%changelog
* Wed Apr 25 2012 - Thomas Wagner
- fix %files
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- bump to 0.20.0
* Sat Feb 21 2009 - Thomas Wagner
- add (Build-)Requires: SFEgmpc(-devel) (moved from base-specs/gmpc-plugin.spec)
- removed %doc from %files (usually no docs contained in plugins)
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
