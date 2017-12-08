#
# spec file for package SFEpython27-pycparser
#
# includes module(s): pycparser
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0


%define  src_name   pycparser

Name:                    SFEpython27-pycparser
IPS_Package_Name:	 library/python/pycparser-27
Summary:                 parser for the C language
URL:                     https://github.com/eliben/pycparser
Version:                 2.18
#Source:		         http://github.com/eliben/pycparser/archive/%{version}.tar.gz?%{src_name}-%{version}.tar.gz
Source:			 http://github.com/eliben/pycparser/archive/release_v%{version}.tar.gz?%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-pycparser
IPS_Package_Name:	 library/python/pycparser
Summary:                 parser for the C language
Requires:	         SFEpython27-pycparser

%description
pycparser is a parser for the C language, written in pure Python. It is a module designed to be easily integrated into applications that need to parse C source code.

%prep
#pycparser-release_v2.18
%setup -q -n pycparser-release_v%version

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
* Wed Dec  6 2017 - Thomas Wagner
- add generic IPS_Package_Name library/python/pycparser
* Tue Dec  5 2017 - Thomas Wagner
- Initial spec file version 2.18
