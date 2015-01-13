#
# spec file for package SFEpython27-unidecode
#
# includes module(s): unidecode
#
%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.7
%define src_name Unidecode
%define src_ver 0.04.17

Name:		SFEpython27-unidecode
IPS_Package_Name:	library/python-2/unidecode-27
Version:	0.4.17
Summary:	ASCII transliterations of Unicode text
License:	GPLv2
Group:		Development/Languages/Python
URL:		https://pypi.python.org/pypi/Unidecode
Source:		http://pypi.python.org/packages/source/U/%{src_name}/%{src_name}-%{src_ver}.tar.gz
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{src_ver}-build
%include default-depend.inc

# Python27 isn't in packagenamemacros
# Requires: %{pnm_requires_SUNWPython27}
Requires: runtime/python-27

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
* Mon Jan 12 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 0.04.17
