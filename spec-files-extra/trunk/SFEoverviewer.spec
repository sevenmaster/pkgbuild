#
# spec file for package SFEoverviewer
#

%include Solaris.inc
%include packagenamemacros.inc

%define python_version 2.7
%define src_name overviewer

Name:		SFEoverviewer
IPS_Package_Name:	games/minecraft/overviewer
Summary:	The Minecraft Overviewer
Version:	0.12.198
Group:		Amusements/Games
License:	GPLv3
URL:		http://overviewer.org/
#Source:		https://github.com/overviewer/Minecraft-Overviewer/archive/v%{version}.tar.gz
Source:		http://overviewer.org/builds/src/3/%{src_name}-%{version}.tar.gz
Source:		http://overviewer.org/builds/src/41/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	%{pnm_buildrequires_python_default}
BuildRequires:	SFEpython27-imaging-header
Requires:		%{pnm_requires_python_default}

%include default-depend.inc

%description
Render high-resolution images of a Minecraft map with a Google Maps-powered interface

%prep
%setup -q -n Minecraft-Overviewer-%{version}

# Remove gcc-specific compiler flags hardcoded into setup.py
gsed -i 's/-Wno-unused-variable//g' setup.py
gsed -i 's/-Wno-unused-function//g' setup.py
gsed -i 's/-Wdeclaration-after-statement//g' setup.py
gsed -i 's/-Werror=declaration-after-statement//g' setup.py

%build

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root $RPM_BUILD_ROOT

# move to vendor-packages
if [ -d $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages ] ; then
    mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
    mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
        $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
    rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
fi

mv $RPM_BUILD_ROOT%{_bindir}/overviewer.py $RPM_BUILD_ROOT%{_bindir}/overviewer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}/*
%{_libdir}/python%{python_version}/vendor-packages/Minecraft_Overviewer-%{version}-py%{python_version}.egg-info
%dir %{_libdir}/python%{python_version}/vendor-packages/overviewer_core
%{_libdir}/python%{python_version}/vendor-packages/overviewer_core/*
%attr(0755,root,sys) %dir %{_datadir}
%attr(0755,root,other) %dir %{_docdir}
%attr(0755,root,other) %dir %{_docdir}/minecraft-overviewer
%{_docdir}/minecraft-overviewer/*

%changelog
* Thu Jun 22 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- Bump to 0.12.198
* Tue Nov 08 2016 - Ian Johnson <ianj@tsundoku.ne.jp>
- Bump to 0.12.137
- Change default python to 2.7
* Mon Feb 24 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec version 0.11.0
