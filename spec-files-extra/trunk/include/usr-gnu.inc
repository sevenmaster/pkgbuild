%include osdistro.inc

%define _basedir           /usr
%define _subdir            gnu
%define _prefix		   %{_basedir}/%{_subdir}
%define _std_bindir        %{_basedir}/bin
%define _sysconfdir	   /etc/%{_subdir}
%define _std_sysconfdir    /etc
%define _localedir	   %{_libdir}/locale
%define _localstatedir     /var/%{_subdir}
%define _std_localstatedir /var
%define _pkg_config_path   %{_libdir}/pkgconfig
%define _pkg_config_path64 %{_libdir}/%{_arch64}/pkgconfig
%define _std_datadir       %{_basedir}/share
%define _infodir           %{_std_datadir}/info
%define _std_includedir    %{_basedir}/include
%define _std_libdir        %{_basedir}/lib

#defaults for new osdistro
%define _share_locale_group_changed	1
%define _share_locale_group	bin

#SXCE, to be added is as well: S10
%if %SXCE
%define _share_locale_group_changed	0
%define _share_locale_group	other
#%{SXCE}
%endif

%changelog
* Sun Jul  8 2012 - Thomas Wagner
- add flag for deviating group-id root:bin for /usr/gnu/share/locale
  instead of root:other for /usr/share/locale
