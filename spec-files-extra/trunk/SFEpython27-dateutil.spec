#
# spec file for package SFEpython27-dateutil
#
# includes module(s): dateutil
#
%include Solaris.inc

Name:                    SFEpython27-dateutil
IPS_Package_Name:	library/python-2/dateutil-27
Summary:                 dateutil - Provides powerful extensions to the standard datetime module
URL:                     http://labix.org/python-dateutil
Version:                 1.5
Source:                  http://labix.org/download/python-dateutil/python-dateutil-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

# Python27 isn't in packagenamemacros
# Requires: %{pnm_requires_SUNWPython27}
Requires:                runtime/python-27

%include default-depend.inc

%define python_version  2.7

%prep
%setup -q -n python-dateutil-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Mon 12 Jan 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec, based on SFEpython26-dateutil
