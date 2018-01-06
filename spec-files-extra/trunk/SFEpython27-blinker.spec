#
# spec file for package SFEpython27-blinker
#
# includes module(s): blinker
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

%define src_name        blinker
%define githubowner1    jek
%define githubproject1  %{src_name}


Name:                    SFEpython27-blinker
IPS_Package_Name:	 library/python/blinker-27
Summary:	         Fast, simple object-to-object and broadcast signaling for Python object
URL:		         http://pythonhosted.org/blinker/
Version:                 1.4
#https://github.com/jek/blinker/archive/rel-1.4.tar.gz
Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/rel-%{version}.tar.gz?%{src_name}-%{version}.tar.gz
License:                 MIT
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-blinker
IPS_Package_Name:	 library/python/blinker
Summary:                 %{summary}
Requires:	         SFEpython27-blinker

%description
Blinker provides fast & simple object-to-object and broadcast signaling for Python objects.


%prep
%setup -q -n %{src_name}-rel-%{version}

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
* Fri Jan  5 2018 - Thomas Wagner
- reworked spec, bump to version 1.4
* Mon Jan 12 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 1.3
