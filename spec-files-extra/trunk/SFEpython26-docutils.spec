#
# spec file for package SFEpython26-docutils
#
# includes module(s): docutils
#
%include Solaris.inc
%include packagenamemacros.inc

Name:			SFEpython26-docutils
IPS_Package_Name:	library/python-2/python-docutils-26
Summary:		Process plaintext documentation into formats such as HTML, LaTeX, and man pages
URL:			http://docutils.sourceforge.net/
Version:		0.11
Source:			%sf_download/project/docutils/docutils/%version/docutils-%version.tar.gz
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build
Requires:		%{pnm_requires_python_default}

%include default-depend.inc

%define python_version  2.6

%prep
%setup -q -n docutils-%version

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
%_bindir
%dir %attr (0755, root, bin) %_libdir
%_libdir/python%python_version/vendor-packages

%changelog
* Sun Mar 23 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- %include packagenamemacros.inc
- change Requires to %{pnm_requires_python_default}
* 10 Oct 2013 - Alex Viskovatoff
- Initial spec, based on SFEpython26-dateutil.spec
