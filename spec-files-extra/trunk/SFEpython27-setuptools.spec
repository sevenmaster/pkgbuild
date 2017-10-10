#
# spec file for package SFEpython27-setuptools
#
# includes module(s): setuptools
#
%include Solaris.inc
%include osdistro.inc

%define  src_name   setuptools

Name:                    SFEpython27-setuptools
IPS_Package_Name:	 sfe/library/python/setuptools-27
Summary:	         Python setuptools (site-packages)
URL:		         https://pypi.python.org/pypi/setuptools
Version:                 36.5.0
#https://github.com/pypa/setuptools/archive/v36.5.0.tar.gz
Source:		         http://github.com/pypa/setuptools/archive/v%{version}.tar.gz?%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

BuildRequires:		SFEpython27-setuptools
Requires:		SFEpython27-setuptools

%define python_version  2.7

%description

Attention: This package updates the system delivered old version of python setuptools.
Calling script is renamed to easy_install-2.7-sfe and easy_install-sfe


%prep
%setup -q -n setuptools-%version

#we can't package a file with "spaces", one solution would be pkgmogrify but
#the other solution is, renameing it (here in the source, then in %install below)
#ggrep -r "launcher manifest" -->>
#easy_install.py:    manifest = pkg_resources.resource_string(__name__, 'launcher manifest.xml')
gsed -i -e 's?launcher manifest.xml?launcher_manifest.xml?' \
    setuptools/command/easy_install.py



%if %{omnios}
gsed -e '/std=c99/ s/^/#/' < setup.py
%endif

%build
%if %( expr %{solaris11} '=' 1 '|' %{solaris12} '=' 1 )
export CC=cc
%else
export CC=gcc
%endif

%if %( /usr/bin/python%{python_version}-config --cflags  | grep -- -m64 >/dev/null && echo 1 || echo 0 )
BITS=64
export CFLAGS="-m64 -I%{gnu_inc}"
export LDFLAGS="-L%gnu_lib/%{_arch64} -R%gnu_lib/%{_arch64}"
export PYTHON_BINARY_OFFSET="/usr/bin/%{_arch64}"
%else
BITS=32
export CFLAGS="-I%{gnu_inc}"
export LDFLAGS="-L%gnu_lib -R%gnu_lib"
export PYTHON_BINARY_OFFSET="/usr/bin"
%endif
echo "compiling for ${BITS}-bit python!"


${PYTHON_BINARY_OFFSET}/python%{python_version} bootstrap.py

${PYTHON_BINARY_OFFSET}/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

#stay in site-packages as OS has own setuptools delivered # move to vendor-packages
#stay in site-packages as OS has own setuptools delivered mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
#stay in site-packages as OS has own setuptools delivered mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
#stay in site-packages as OS has own setuptools delivered $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
#stay in site-packages as OS has own setuptools delivered rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

#need to move out of the way of system delivered setuptools
mv $RPM_BUILD_ROOT/%{_bindir}/easy_install-2.7 $RPM_BUILD_ROOT/%{_bindir}/easy_install-2.7-sfe
mv $RPM_BUILD_ROOT/%{_bindir}/easy_install $RPM_BUILD_ROOT/%{_bindir}/easy_install-sfe

#PKG/IPS does not take spaces in file names. A) escape or B) change the filename and patch the code
#now we try B)
#if we don't, pkgbuild would just end failing with just a "No Error."
#note: before setup.py we gsed easy_install.py to use the new filename
mv  $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/setuptools/command/"launcher manifest.xml" \
    $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/setuptools/command/"launcher_manifest.xml"

mv  $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/setuptools/"script (dev).tmpl" \
    $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/setuptools/"script_(dev).tmpl"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

%changelog
* Sat Mar 25 2017 - Thomas Wagner
- Initial spec file version 36.5.0
- don't use spaces in filenames, as pkgbuild/IPS can't take them without workarounds
