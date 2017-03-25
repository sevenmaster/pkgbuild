#
# spec file for package SFEpython-serial
#
# includes module(s): pyserial
#
%include Solaris.inc
%include osdistro.inc

%define  src_name   pyserial

Name:                    SFEpython27-serial
IPS_Package_Name:	 library/python/python-serial-27
Summary:                 Cryptographic library for the Python Programming Language
URL:                     https://github.com/pyserial/pyserial
Version:                 3.3
#Source:			 http://pypi.python.org/packages/source/p/pyserial/%{src_name}-%{version}.tar.gz
Source:			http://pypi.python.org/packages/8d/88/cf848688ae011085a6da5a470740dafa3a4b105f84a5f79c3b720c19279c/pyserial-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7

%prep
%setup -q -n pyserial-%version

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


${PYTHON_BINARY_OFFSET}/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/miniterm.py
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

%changelog
* Sat Mar 25 2017 - Thomas Wagner
- Initial spec file version 3.3
