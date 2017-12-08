#
# spec file for package SFEpython27-pyasn1
#
# includes module(s): pyasn1
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0


%define src_name        pyasn1
%define githubowner1    etingof
%define githubproject1  %{src_name}


Name:                    SFEpython27-pyasn1
IPS_Package_Name:	 library/python/pyasn1-27
Summary:                 ASN.1 types and codecs
URL:                     https://github.com/eliben/pyasn1
Version:                 0.4.2
#Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{version}.tar.gz?%{src_name}-%{version}.tar.gz
Source:                  http://codeload.github.com/%{githubowner1}/%{githubproject1}/tar.gz/v0.4.2?pyasn1-0.4.2.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-pyasn1
IPS_Package_Name:	 library/python/pyasn1
Summary:                 %{summary}
Requires:	         SFEpython27-pyasn1

%description
pyasn1
Pure-Python implementation of ASN.1 types and DER/BER/CER codecs (X.208)

%prep
#%setup -q -n pyasn1-release_v%version
%setup -q -n pyasn1-%version

#%if %{omnios}
#gsed -e '/std=c99/ s/^/#/' < setup.py
#%endif

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
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/dummybinary
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}


%changelog
* Thu  7 Dec 2017 - Thomas Wagner
- Initial spec file version 0.4.2
