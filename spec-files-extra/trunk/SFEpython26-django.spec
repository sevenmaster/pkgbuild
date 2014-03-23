#
# spec file for package SFEpython26-django
#
# includes module(s): Django
#
%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.6
%define django_major_version 1.6

Name:		SFEpython26-django
IPS_Package_Name:	web/python/django
Version:	1.6.2
Summary:	A high-level Python Web framework that enables Rapid Development
License:	BSD
Group:		Development/Languages/Python
URL:		http://www.djangoproject.com/
Source:		http://www.djangoproject.com/m/releases/%{django_major_version}/Django-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_python_default}
Requires: %{pnm_requires_python_default}

%prep
%setup -q -n Django-%version

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p %{buildroot}%{_libdir}/python%{python_version}/vendor-packages
mv %{buildroot}%{_libdir}/python%{python_version}/site-packages/* \
   %{buildroot}%{_libdir}/python%{python_version}/vendor-packages/
rmdir %{buildroot}%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Sun Sep 01 2013 - Milan Jurik
- bump to 1.5.2
* Sun Aug 19 2012 - Milan Jurik
- bump to 1.4.1
* Fri Sep 30 2011 - Milan Jurik
- bump to 1.3.1
* Fri Mar 25 2011 - Milan Jurik
- bump to 1.3
* Tue Mar 01 2011 - Milan Jurik
- bump to 1.2.5
* Mon Feb 07 2011 - Milan Jurik
- move to python 2.6, bump to 1.2.4
* Sat Sep  3 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
