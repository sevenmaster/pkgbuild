#
# spec file for package SFEpython27-jinja
#
# includes module(s): jinja
#
%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.7
%define src_name Jinja2

Name:		SFEpython27-jinja
IPS_Package_Name:	library/python-2/jinja-27
Version:	2.7.3
Summary:	A simple pythonic template language written in Python
License:	BSD
Group:		Development/Languages/Python
URL:		http://jinja.pocoo.org/
Source:		http://pypi.python.org/packages/source/J/%{src_name}/%{src_name}-%{version}.tar.gz
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
- Initial spec 2.7.3
