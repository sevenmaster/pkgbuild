##NOTE## the project is named on github "jinja". But as Solaris has the module and names it "junja2", we do as well.

#
# spec file for package SFEpython27-jinja2
#
# includes module(s): jinja2
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0
##TODO## could get a renamed-to-package ( library/python-2/jinja-27 -->> library/python/jinja2-27 )

%define src_name        jinja
%define githubowner1    pallets
%define githubproject1  %{src_name}


Name:                    SFEpython27-jinja2
IPS_Package_Name:	 library/python/jinja2-27
Summary:                 The Jinja2 template engine
URL:                     http://jinja.pocoo.org/
Version:                 2.10
Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{version}.tar.gz?%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

BuildRequires:           library/python/markupsafe
Requires:                library/python/markupsafe

%define python_version  2.7


%package -n SFEpython-jinja2
IPS_Package_Name:	 library/python/jinja2
Summary:                 %{summary}
Requires:	         SFEpython27-jinja2

%description
jinja
The Jinja2 template engine http://jinja.pocoo.org/

%prep
%setup -q -n jinja-%version

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
- reworked, spec file version 2.7.3 -> 2.10
- NOTE: IPS package name changed from library/python-2/jinja-27 to library/python/jinja2-27
- add renamed-to package from library/python-2/jinja-27 to library/python/jinja2-27
* Mon Jan 12 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 2.7.3
