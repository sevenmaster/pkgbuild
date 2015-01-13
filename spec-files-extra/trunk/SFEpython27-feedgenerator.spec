#
# spec file for package SFEpython27-feedgenerator
#
# includes module(s): feedgenerator
#
%include Solaris.inc
%include packagenamemacros.inc

%define src_name feedgenerator

Name:			SFEpython27-feedgenerator
IPS_Package_Name:	library/python-2/feedgenerator-27
Summary:		Standalone version of django.utils.feedgenerator
License:		BSD
URL:			https://pypi.python.org/pypi/feedgenerator
Version:		1.7
Source:			http://pypi.python.org/packages/source/f/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build
Requires:		runtime/python-27

%include default-depend.inc

# Python27 isn't in packagenamemacros
# Requires: %{pnm_requires_SUNWPython27}
%define python_version  2.7

%prep
%setup -q -n feedgenerator-%version

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
%dir %attr (0755, root, bin) %_libdir
%_libdir/python%python_version/vendor-packages

%changelog
* Tue Jan 13 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 1.7
