#
# spec file for package SFEpython27-cffi
#
# includes module(s): cffi
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

##TODO## investigate download link, has problems when dl source with pkgtool.

%define src_name        cffi
#%define githubowner1    ##FILLIN##
#%define githubproject1  %{src_name}


Name:                    SFEpython27-cffi
IPS_Package_Name:	 library/python/cffi-27
Summary:                 Foreign Function Interface for Python calling C code.
URL:                     http://cffi.readthedocs.org
Version:                 1.11.2
##TODO## with version bump, update the URL too!
Source:                  https://pypi.python.org/packages/c9/70/89b68b6600d479034276fed316e14b9107d50a62f5627da37fafe083fde3/cffi-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-cffi
IPS_Package_Name:	 library/python/cffi
Summary:                 %{summary}
Requires:	         SFEpython27-cffi

%description
cffi
Foreign Function Interface for Python calling C code. 

%prep
#%setup -q -n cffi-release_v%version
%setup -q -n cffi-%version

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
- Initial spec file version 1.11.2
