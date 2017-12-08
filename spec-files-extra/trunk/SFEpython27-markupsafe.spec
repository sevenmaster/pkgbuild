#
# spec file for package SFEpython27-markupsafe
#
# includes module(s): markupsafe
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

##TODO## investigate download link, has problems when dl source with pkgtool.

%define src_name        markupsafe
%define githubowner1    pallets
%define githubproject1  %{src_name}


Name:                    SFEpython27-markupsafe
IPS_Package_Name:	 library/python/markupsafe-27
Summary:                 Implements a XML/HTML/XHTML Markup safe string for Python
URL:                     http://markupsafe.readthedocs.org
Version:                 1.0
Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{version}.tar.gz?%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-markupsafe
IPS_Package_Name:	 library/python/markupsafe
Summary:                 %{summary}
Requires:	         SFEpython27-markupsafe

%description
markupsafe
Implements a XML/HTML/XHTML Markup safe string for Python.
Implements a unicode subclass that supports HTML strings.

%prep
#%setup -q -n markupsafe-release_v%version
%setup -q -n markupsafe-%version

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

#special to this module:
%if %( expr %{solaris11} '=' 1 '|' %{solaris12} '=' 1 )
export CC=cc
%else
export CC=gcc
%endif

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
- Initial spec file version 1.0
