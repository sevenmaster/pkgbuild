#
# spec file for package SFEpython27-importlib
#
# includes module(s): importlib
#
%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.7
%define src_name importlib
%define src_ver 1.0.3

Name:		SFEpython27-importlib
IPS_Package_Name:	library/python-2/importlib-27
Version:	1.0.3
Summary:	importlib - wrapper for importlib.import_module
##TODO## verify this, it is probably a backport from Python3
License:	Python3
Group:		Development/Languages/Python
URL:		https://pypi.python.org/pypi/importlib
Source:		http://pypi.python.org/packages/source/i/%{src_name}/%{src_name}-%{src_ver}.tar.gz
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{src_ver}-build
%include default-depend.inc

# Python27 isn't in packagenamemacros
# Requires: %{pnm_requires_SUNWPython27}
Requires: runtime/python-27

%description
New in version 2.7.

This module is a minor subset of what is available in the more full-featured package of the same name from Python 3.1 that provides a complete implementation of import. What is here has been provided to help ease in transitioning from 2.7 to 3.1.

importlib.import_module(name, package=None)

Import a module. The name argument specifies what module to import in absolute or relative terms (e.g. either pkg.mod or ..mod). If the name is specified in relative terms, then the package argument must be specified to the package which is to act as the anchor for resolving the package name (e.g. import_module('..mod', 'pkg.subpkg') will import pkg.mod). The specified module will be inserted into sys.modules and returned.


%prep
%setup -q -n %{src_name}-%{src_ver}

%build
python2.7 setup.py build

%install
rm -rf %{buildroot}
python2.7 setup.py install --root=%{buildroot} --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p %{buildroot}%{_libdir}/python%{python_version}/vendor-packages
mv %{buildroot}%{_libdir}/python%{python_version}/site-packages/* \
   %{buildroot}%{_libdir}/python%{python_version}/vendor-packages/
rmdir %{buildroot}%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Mon Aug 10 2015 - Thomas Wagner
- Initial spec 1.0.3
