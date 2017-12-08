
#needs automatic uninstall once SRU is being installed:
#kommandant tom ~/spec-files-extra pkg list -af library/python/ipaddress     
#NAME (PUBLISHER)                                  VERSION                    IFO
#library/python/ipaddress                          1.0.16-0.175.3.20.0.1.0    ---
#library/python/ipaddress                          1.0.16-0.175.3.14.0.2.0    i--

#ELSE it would stumble into library/python/ipaddress  1.0.16-5.12.0.0.0.122.0    i--
#                           library/python/ipaddress  1.0.16-5.12.0.0.0.115.0    ---
#                           library/python/ipaddress  1.0.14-5.12.0.0.0.105.1    ---
#                           library/python/ipaddress  1.0.14-5.12.0.0.0.95.0     ---






#
# spec file for package SFEpython27-ipaddress
#
# includes module(s): ipaddress
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#below:
##TODO## add more OS if they deliver starting with entire@version to deliver a suitable ipaddress module for python27


%define  src_name   ipaddress

Name:                    SFEpython27-ipaddress
IPS_Package_Name:	 library/python/ipaddress-27
Summary:                 Python 3.3's ipaddress for older Python versions - uninstall this module yourself once the OS update has its own ipaddress module for python-27
URL:                     https://github.com/phihag/ipaddress
#https://github.com/phihag/ipaddress/archive/v1.0.18.tar.gz
#please, DO NOT update version without thinking on consequences for all all SFE supported target OS versions
Version:                 1.0.16
Source:		         http://github.com/phihag/ipaddress/archive/v%{version}.tar.gz?%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-ipaddress
IPS_Package_Name:	 library/python/ipaddress
Summary:                 Python 3.3's ipaddress for older Python versions - uninstall this module yourself once the OS update has its own ipaddress module for python-27
Requires:	         SFEpython27-ipaddress


%if %{solaris11}%{solaris12}
#prepare a automatic uninstall package like this:
#package is built *now* but carries a dependency on a package the osdistro shows when our package needs to be uninstalled
%package -n %{name}-noinst-1
Summary:                Python 3.3's ipaddress for older Python versions - uninstall this module yourself once the OS update has its own ipaddress module for python-27
IPS_Package_Name:	/library/python/ipaddress
%if %{solaris11}
%define ips_branch_renamed_package 0.175.3.14.0.2.0
%define renamed_from_oldname      library/python/ipaddress
%define renamed_to_newnameversion library/python/ipaddress = %{version}-%{ips_branch_renamed_package}
IPS_legacy: false
Meta(pkg.renamed): true
PkgBuild_Make_Empty_Package: true

Renamed_To: %{renamed_to_newnameversion}
IPS_Vendor_Version: %{ips_branch_renamed_package}
Meta(variant.opensolaris.zone): global, nonglobal

%endif
%if %{solaris12}
%define ips_branch_renamed_package 5.12.0.0.0.95.0
%define renamed_from_oldname      library/python/ipaddress
%define renamed_to_newnameversion library/python/ipaddress = %{version}-%{ips_branch_renamed_package}
IPS_legacy: false
Meta(pkg.renamed): true
PkgBuild_Make_Empty_Package: true
Renamed_To: %{renamed_to_newnameversion}
IPS_Vendor_Version: %{ips_branch_renamed_package}
Meta(variant.opensolaris.zone): global, nonglobal
%endif
##TODO## add more OSDistro

#%define renamed_from_oldname      library/desktop/gnu/cairo
#%define renamed_to_newnameversion library/desktop/g++/cairo = *
#%include pkg-renamed-package.inc



%package -n %{name}-noinst-2
#pause IPS_Package_Name:	 library/python/ipaddress-27
IPS_Package_Name:	/library/python/ipaddress-27
%if %{solaris11}
%define ips_branch_renamed_package 0.175.3.14.0.2.0
#0.5.11,5.11
%define ips_os_component_os_buildversion 0.%{ips_build_version},%{ips_build_version}
%define renamed_from_oldname      library/python/ipaddress-27
%define renamed_to_newnameversion library/python/ipaddress-27 = %{version}-%{ips_branch_renamed_package}
IPS_legacy: false
Meta(pkg.renamed): true
PkgBuild_Make_Empty_Package: true
Renamed_To: %{renamed_to_newnameversion}
IPS_Vendor_Version: %{ips_branch_renamed_package}
Meta(variant.opensolaris.zone): global, nonglobal
%endif
%if %{solaris12}
%define ips_branch_renamed_package 5.12.0.0.0.95.0
#5.12,5.12
%define ips_os_component_os_buildversion %{ips_build_version},%{ips_build_version}
%define renamed_from_oldname      library/python/ipaddress-27
%define renamed_to_newnameversion library/python/ipaddress-27 = %{version}-%{ips_branch_renamed_package}
IPS_legacy: false
Meta(pkg.renamed): true
PkgBuild_Make_Empty_Package: true
Renamed_To: %{renamed_to_newnameversion}
IPS_Vendor_Version: %{ips_branch_renamed_package}
Meta(variant.opensolaris.zone): global, nonglobal
%endif
##TODO## add more OSDistro



#list all the old published package name wich need to go away with upgrade to our new package name/location
#special case here, as we want the renamed part only be effective on S12 build 87 and up, we need to put a dependency on that release/name@5.12,5.12-5.12.0.0.0.87
#release/name can be "optional" as it is normally present and then it needs to have at least this revision
%actions -n %{name}-noinst-1
depend fmri=entire@%{ips_os_component_os_buildversion}-%{ips_branch_renamed_package} type=optional
depend fmri=consolidation/osnet/osnet-incorporation@%{ips_os_component_os_buildversion}-%{ips_branch_renamed_package} type=optional

%actions -n %{name}-noinst-2
depend fmri=entire@%{ips_os_component_os_buildversion}-%{ips_branch_renamed_package} type=optional
depend fmri=consolidation/osnet/osnet-incorporation@%{ips_os_component_os_buildversion}-%{ips_branch_renamed_package} type=optional

%endif #%{solaris11}%{solaris12}


%description
Python module "ipaddess" (backported from Python 3.3)

NOTE: once the OSdistro has its own module ipaddress (e.g. S11 11.3 SRU 14), then this module uninstalls automatically in favor of the ODDISTRO provided module.
These OS Releases have ipaddress themselves:

library/python/ipaddress  1.0.16-0.175.3.14.0.2.0 and later


%prep
%setup -q -n ipaddress-%version

%if %{omnios}
gsed -e '/std=c99/ s/^/#/' < setup.py
%endif

%build
%if %( expr %{solaris11} '=' 1 '|' %{solaris12} '=' 1 )
export CC=cc
%else
export CC=gcc
%endif

%if %( /usr/bin/python%{python_version}-config --cflags  | grep -- -m64 >/dev/null && echo 1 || echo 0 )
BITS=64
export CFLAGS="-m64 -I%{gnu_inc}"
export LDFLAGS="-L%gnu_lib/%{_arch64} -R%gnu_lib/%{_arch64}"
export PYTHON_BINARY_OFFSET="/usr/bin/%{_arch64}"
%else
BITS=32
export CFLAGS="-I%{gnu_inc}"
export LDFLAGS="-L%gnu_lib -R%gnu_lib"
export PYTHON_BINARY_OFFSET="/usr/bin"
%endif
echo "compiling for ${BITS}-bit python!"


${PYTHON_BINARY_OFFSET}/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/dummybinary
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

#%files -n %{name}-noinst-1
#empty! get out of the way of the noinst-1 and noinst-2 packages!

#%files -n %{name}-noinst-2
#empty! get out of the way of the noinst-1 and noinst-2 packages!


%changelog
* Fri Dec  8 2017 - Thomas Wagner
- make automatic uninstall @ specific OSDISTRO version only for solaris11 solaris12 (S11 S12)
* Sun Oct  8 2017 - Thomas Wagner
- Initial spec file version 1.0.16 (to keep it upgradable by the OS)
