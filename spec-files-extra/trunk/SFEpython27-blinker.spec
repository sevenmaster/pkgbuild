#
# spec file for package SFEpython27-blinker
#
# includes module(s): blinker
#
%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.7
%define src_name blinker

Name:		SFEpython27-blinker
IPS_Package_Name:	library/python-2/blinker-27
Version:	1.3
Summary:	Fast, simple object-to-object and broadcast signaling for Python
License:	Blinker
Group:		Development/Languages/Python
URL:		http://pythonhosted.org/blinker/
Source:		http://pypi.python.org/packages/source/b/blinker/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{src_name}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Python27 isn't in packagenamemacros
# Requires: %{pnm_requires_SUNWPython27}
Requires: runtime/python-27

%prep
%setup -q -n %{src_name}-%{version}

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
* Mon Jan 12 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 1.3
