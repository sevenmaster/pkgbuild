#
# spec file for package SFEpython27-unidecode
#
# includes module(s): unidecode
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#below:
##TODO##                   record open tasks or invesitgations here


%define src_name        unidecode
%define githubowner1    avian2
%define githubproject1  %{src_name}


Name:                    SFEpython27-unidecode
IPS_Package_Name:	 library/python/unidecode-27
Summary:                 ASCII transliterations of Unicode text
URL:		         https://pypi.python.org/pypi/Unidecode
Version:                 1.0.22
#https://github.com/avian2/unidecode/archive/unidecode-1.0.22.tar.gz
#Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{version}.tar.gz?%{src_name}-%{version}.tar.gz
Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-unidecode
IPS_Package_Name:	 library/python/unidecode
Summary:                 %{summary}
Requires:	         SFEpython27-unidecode

%description
It often happens that you have text data in Unicode, but you need to represent it in ASCII.
For example when integrating with legacy code that doesn't support Unicode, or for ease of
entry of non-Roman names on a US keyboard, or when constructing ASCII machine identifiers
from human-readable Unicode strings that should still be somewhat intelligible (a popular
example of this is when making an URL slug from an article title).



%prep
%setup -q -n %{src_name}-%{src_name}-%{version}

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
export LDFLAGS="-L%{gnu_lib}/%{_arch64} -R%{gnu_lib}/%{_arch64}"
export PYTHON_BINARY_OFFSET="/usr/bin/%{_arch64}"
%else
BITS=32
export CFLAGS="-I%{gnu_inc}"
export LDFLAGS="-L%{gnu_lib} -R%{gnu_lib}"
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
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}


%changelog
* Fri Jan  5 2018 - Thomas Wagner
- reworked, bump to 1.0.22
* Mon Jan 12 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 0.04.17
