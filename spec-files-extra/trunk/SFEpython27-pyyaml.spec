#
# spec file for package SFEpython27-pyyaml
#
# includes module(s): pyyaml
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#below:
##TODO##                   record open tasks or invesitgations here


%define src_name        pyyaml


Name:                    SFEpython27-pyyaml
IPS_Package_Name:	 library/python/pyyaml-27
Summary:                 YAML parser and emitter for Python
URL:                     https://github.com/eliben/pyyaml
Version:                 3.12
Source:                  http://pyyaml.org/download/pyyaml/PyYAML-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-pyyaml
IPS_Package_Name:	 library/python/pyyaml
Summary:                 %{summary}
Requires:	         SFEpython27-pyyaml

%description
pyyaml
YAML parser and emitter for Python

YAML is a data serialization format designed for human readability and interaction with scripting languages. PyYAML is a YAML parser and emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle support, capable extension API, and sensible error messages. PyYAML supports standard YAML tags and provides Python-specific tags that allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex configuration files to object serialization and persistance.

%prep
#%setup -q -n pyyaml-release_v%version
#%setup -q -n pyyaml-%version
%setup -q -n PyYAML-%version

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
- Initial spec file version 3.12
