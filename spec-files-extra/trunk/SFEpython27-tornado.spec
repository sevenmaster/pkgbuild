##TODO## tornado: look into https://github.com/tornadoweb/tornado/blob/master/.travis.yml
# requires on python2.x: mock monotonic
####and so on
install:
    - if [[ $TRAVIS_PYTHON_VERSION == 2* ]]; then travis_retry pip install mock monotonic; fi
    - if [[ $TRAVIS_PYTHON_VERSION == 'pypy' ]]; then travis_retry pip install mock; fi
    # TODO(bdarnell): pycares tests are currently disabled on travis due to ipv6 issues.
    #- if [[ $TRAVIS_PYTHON_VERSION != 'pypy'* ]]; then travis_retry pip install pycares; fi
    - if [[ $TRAVIS_PYTHON_VERSION != 'pypy'* ]]; then travis_retry pip install pycurl; fi
    # Twisted runs on 2.x and 3.3+, but is flaky on pypy.
    - if [[ $TRAVIS_PYTHON_VERSION != 'pypy'* ]]; then travis_retry pip install Twisted; fi
    - if [[ $TRAVIS_PYTHON_VERSION == '2.7' || $TRAVIS_PYTHON_VERSION == '3.6' ]]; then travis_retry pip install sphinx sphinx_rtd_theme; fi
    # On travis the extension should always be built
    - if [[ $TRAVIS_PYTHON_VERSION != 'pypy'* ]]; then export TORNADO_EXTENSION=1; fi
    - travis_retry python setup.py install
    - travis_retry pip install codecov virtualenv
    # Create a separate no-dependencies virtualenv to make sure all imports
    # of optional-dependencies are guarded.
    - virtualenv ./nodeps
    - ./nodeps/bin/python -VV
    - ./nodeps/bin/python setup.py install
    - curl-config --version; pip freeze


##TODO## copy experimental/make_perl_cpan_settings.pl and make a generator for python modules - any volunteers please?
## :4,$ s/@@PACKAGENAME@@/_place_name_here_/gc
## :5,$ s/@@VERSION@@/_1.2.3.4_/gc
## /##FILLIN##

#
# spec file for package SFEpython27-tornado
#
# includes module(s): tornado
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#below:
##TODO##                   record open tasks or invesitgations here


%define src_name        tornado
%define githubowner1    tornadoweb
%define githubproject1  %{src_name}


Name:                    SFEpython27-tornado
IPS_Package_Name:	 library/python/tornado-27
Summary:                 Tornado is a Python web framework and asynchronous networking library.
URL:                     http://www.tornadoweb.org/
Version:                 4.5.2
#https://github.com/tornadoweb/tornado/archive/v4.5.2.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-tornado
IPS_Package_Name:	 library/python/tornado
Summary:                 %{summary}
Requires:	         SFEpython27-tornado

%description
Tornado is a Python web framework and asynchronous networking library.

%prep
#%setup -q -n tornado-release_v%version
%setup -q -n tornado-%version

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
* Tue Jan  2 2018 - Thomas Wagner
- Initial spec file version 4.5.2
