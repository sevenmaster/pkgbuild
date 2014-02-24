#
# spec file for package SFEpython-imaging-header
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

%define python_version 2.6

Name:		SFEpython26-imaging-header
IPS_Package_Name:	library/python-2/python-imaging-26/header
Summary:	Headers for the Python Imaging Library
Version:	1.1.7
URL:		http://www.pythonware.com/products/pil/
Source:		http://effbot.org/downloads/Imaging-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	%{pnm_buildrequires_python_default}
Requires:		%{pnm_requires_python_default}

%include default-depend.inc

%description
The Python Imaging Library (PIL) adds image processing capabilities to your Python interpreter. This library provides extensive file format support, an efficient internal representation, and powerful image processing capabilities.

%prep
%setup -q -n Imaging-%{version}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/python%{python_version}
install -c -m 0644 $RPM_BUILD_DIR/Imaging-%{version}/libImaging/ImPlatform.h $RPM_BUILD_ROOT%{_includedir}/python%{python_version}/
install -c -m 0644 $RPM_BUILD_DIR/Imaging-%{version}/libImaging/Imaging.h $RPM_BUILD_ROOT%{_includedir}/python%{python_version}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}/python%{python_version}/*

%changelog
* Mon Feb 24 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec version 1.1.7
