#
# spec file for package SFEpython26-importlib
#
# includes module(s): python-importlib
#
# Note: Required for compilation of LibreOffice and is included in Python 2.7 but we're using 2.6 on some distros so need to install backported importlib

## TODO ##
# pnms
# fix Source
#	INFO: Finding sources
#	ERROR: SFEpython-importlib: Source file importlib-1.0.3.tar.bz2 not found

%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.6
%define src_name importlib
%define src_ver 1.0.3
#%define src_ver 1.0.4 # exists somewhere as a zip file

Name:			SFEpython26-importlib
IPS_Package_Name:	library/python-2/importlib-26
Summary:		Backport of importlib.import_module() from Python 2.7
URL:			https://pypi.python.org/pypi/importlib/
Version:		%{src_ver}
License:		LGPL
Source:			https://pypi.python.org/packages/source/i/importlib/importlib-%{version}.tar.bz2
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:		runtime/python-26
Requires:		runtime/python-26

%description
Backport of importlib.import_module() from Python 2.7

This package contains the code from importlib as found in Python 2.7. It is provided so that people who wish to use importlib.import_module() with a version of Python prior to 2.7 or in 3.0 have the function readily available. The code in no way deviates from what can be found in the Python 2.7 standard library.

%prep
%setup -q -n importlib-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=%{buildroot}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Thu Sep 29 2016 - pjama
- a few cosmetic changes to match python27-importlib
* Wed Jul 01 2015 - pjama
- initial spec
