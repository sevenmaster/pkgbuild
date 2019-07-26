
#problem with OmniOSce 151030, FIONREAD not found, even if all include files are there. Try with gcc now.

##TODO## use pnm_macros for OSDISTRO default python version
##TODO## check (Build)Requires (python, others)
##TODO## use pnm_macros for OSDISTRO python_default version


#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
#%define cc_is_gcc 1
#%include base.inc

%include osdistro.inc
%if %{omnios}
%else
%define this_spec_is_only_for_omnios 1
false
%endif

%ifarch amd64 sparcv9
%include arch64.inc
%use gamin_64 = gamin.spec
%endif

%include base.inc
%use gamin = gamin.spec

Name:		SFEgamin
IPS_Package_Name:	library/file-monitor/gamin
License:	LGPLv2
Summary:	Library providing the FAM File Alteration Monitor API
Group:          System/Libraries
Version:	%{gamin.version}
SUNW_Copyright:      %{license}.copyright
URL:		http://www.gnome.org/~veillard/gamin/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
##TODO##Requires:	SUNWgnome-base-libs
##TODO##BuildRequires:	SUNWgnome-base-libs-devel

##TODO## change to pnm_macro
BuildRequires: library/glib2
Requires:      library/glib2
##TODO## change to pnm_macro
BuildRequires: runtime/python-27
Requires:      runtime/python-27

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%gamin_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%gamin.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%gamin_64.build -d %name-%version/%_arch64
%endif

%gamin.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%gamin_64.install -d %name-%version/%_arch64
#solaris userland says: The 64 bit compilation puts the .so module into  directory, but python expects it in .libs/64
mkdir -p  %{buildroot}/%{_libdir}/python2.7/site-packages/64
mv %{buildroot}/%{_libdir}/%{_arch64}/python2.7/site-packages/_gamin.so %{buildroot}/%{_libdir}/python2.7/site-packages/64/
rm -r %{buildroot}/%{_libdir}/%{_arch64}/python*
%endif

%gamin.install -d %name-%version/%{base_arch}

mv %{buildroot}%{_libdir}/python2.7/site-packages %{buildroot}%{_libdir}/python2.7/vendor-packages

rm -f %{buildroot}%{_libdir}/python2.7/vendor-packages/*.pyc
rm -f %{buildroot}%{_libdir}/python2.7/vendor-packages/*.pyo
rm -f %{buildroot}%{_libdir}/python2.7/vendor-packages/_gamin.la

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
#%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gam_server
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/gam_server
%{_libdir}/python*/*-packages/64/_*
%endif
%{_libdir}/python*/*-packages/_*
%{_libdir}/python*/*-packages/gamin*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_docdir}
#%{_docdir}/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man*/*


%changelog
* Fri Jul 26 2019 - Thomas Wagner
- fix FIONREAD not found (root cause not identified) (OM 151030)
* Fri Nov 17 2017 - Thomas Wagner
- Initial spec for OmniOS only
