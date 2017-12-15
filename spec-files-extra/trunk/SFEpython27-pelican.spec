#
# spec file for package SFEpython27-pelican
#
# includes module(s): pelican
#
%include Solaris.inc
%include packagenamemacros.inc

%define python_version  2.7
%define src_name pelican

Name:		SFEpython27-pelican
IPS_Package_Name:	library/python-2/pelican-27
Version:	3.5.0
Summary:	A static site generator written in Python
License:	AGPL
Group:		Development/Languages/Python
URL:		http://blog.getpelican.com/
Source:		http://github.com/getpelican/pelican/archive/%{version}.tar.gz?%{src_name}-%{version}.tar.gz

SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Python27 isn't in packagenamemacros
# Requires: %{pnm_requires_SUNWPython27}
Requires: runtime/python-27
Requires: library/python-2/markdown
Requires: library/python-2/markupsafe-27
Requires: library/python-2/pytz-27
Requires: library/python/six-27
Requires: SFEpython27-blinker
Requires: SFEpython27-dateutil
Requires: SFEpython27-docutils
Requires: SFEpython27-feedgenerator
Requires: SFEpython27-jinja2
Requires: SFEpython27-unidecode

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
%{_bindir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Tue Dec  5 2017 - Thomas Wagner
- make Download file unique to this package name
- rename (Build)Requires from SFEpython27-jinja to SFEpython27-jinja2
* Tue Jan 13 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add pytz dependency
* Tue Jan 13 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add additional Requires:
* Mon Jan 12 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 3.5.0
