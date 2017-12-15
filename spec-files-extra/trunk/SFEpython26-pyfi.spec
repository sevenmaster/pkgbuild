#
# spec file for package SFEpython26-pyfi
#
# automatic packagename by platform default python version
#
# includes module(s): Django
#
%include Solaris.inc
%include packagenamemacros.inc

#https://pypi.python.org/packages/source/P/PyFi/PyFi-0.1.6.tar.gz#md5=522cbfdbf689d4e7cf9bcffbc424522f
#https://github.com/project-fifo/pyfi/archive/0.1.18.tar.gz
# https://pypi.python.org/packages/source/P/PyFi/PyFi-0.1.19.tar.gz 
#%define src_url         http://pypi.python.org/packages/source/P/PyFi
%define src_url         http://pypi.python.org/packages/source/P/PyFi
%define src_name_uc     SetupTools
%define src_name        PyFi
%define src_version	0.7.1
%define src_version_major_minor	0.7.1
%define packagename SFEpython%{python_version_package_string}-pyfi

Name:		%{packagename}
##TODO## check IPS package naming conventions for SFE
IPS_Package_Name:	web/python/%{src_name}
Version:	%{src_version}
Summary:	Project FiFo API implementation and console client.
License:	CDDL
Group:		Development/Languages/Python
#watch out for latest version on possibly different link:
URL:		https://pypi.python.org/pypi/pyfi
Source:		%{src_url}/%{src_name}-%{src_version_major_minor}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	%{pnm_buildrequires_python_default}
Requires:	%{pnm_requires_python_default}
#python26 has already BuildRequires:	SFEpython26-setuptools
#python26 has already Requires:	SFEpython26-setuptools
BuildRequires:	SFEpython26-configparser
Requires:	SFEpython26-configparser
BuildRequires:	SFEpython26-argparse
Requires:	SFEpython26-argparse

%description
fifo: This is a python implementation of (most) of the Project FiFo API along with a console client to access it.

%prep
%setup -q -n %{src_name}-%{src_version_major_minor}


%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=%{buildroot} --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p %{buildroot}%{_libdir}/python%{python_version}/vendor-packages
mv %{buildroot}%{_libdir}/python%{python_version}/site-packages/* \
   %{buildroot}%{_libdir}/python%{python_version}/vendor-packages/
rmdir %{buildroot}%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Wed Dec  7 2017 - Thomas Wagner
- fix (Build)Requires
* Sun Jan  3 2016 - Thomas Wagner
- bump to 0.7.1
* Sat Jun 14 2014 - Thomas Wagner
- bump to 0.1.24
* Mon May 12 2014 - Thomas Wagner
- bump to 0.1.20
* Tue Feb 18 2014 - Thomas Wagner
- bump to 0.1.17
* Thu Apr 25 2013 - Thomas Wagner
- initial spec
